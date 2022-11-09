########### Initialisieren ###########
from aq_init import *
if usage_display == 1 :
    lcd.lcd_load_custom_chars(fkochars)
########### Schleife ###########
while True:
    if aq_debug == 1 :
        print("___________")
    ########### Timer ###########
    #print(strftime("%H:%M.%S", localtime()))
    if usage_display == 1 : # show timestamp on display
        fko.clock(localtime().tm_hour,localtime().tm_min,localtime().tm_sec)
        
#     currenttime=int(time()*1000)
#     if counter_buffer > 0 :
#         cycletime=currenttime-oldtime
#         if cycletime > 2*s_cycletime*1000 :
#             cycletime=s_cycletime*1000 #Ausreisser entfernen
#         buffer_cycletime[counter_buffer-1]=cycletime
#         avg_cycletime=int(numpy.average(buffer_cycletime))
#         if aq_debug == 1 :
#             print(buffer_cycletime)
#             print("Durschschnittliche Durchlaufzeit:",avg_cycletime/1000,"s")
#     else:
#         cycletime=s_cycletime*1000
#     if aq_debug == 1 :
#         print("Durchlaufzeit:",cycletime)
#     new_s_cycletime=round(new_s_cycletime-cycletime_Igain*(avg_cycletime/1000-s_cycletime), 3)
#     if new_s_cycletime < min_s_cycletime: #avoid error in sleep function
#         new_s_cycletime = min_s_cycletime
#     if aq_debug == 1 :
#         print("neuer sleep:",new_s_cycletime)
#     oldtime=currenttime
    m_act=localtime().tm_mon     #Aktueller Monat als Zahlenwert
    if m_act == m_spring :
        season=1
        season_string="Frühling"
    elif (m_act == m_sommer).any() :
        season=2
        season_string="Sommer"
    elif m_act == m_herbst :
        season=3
        season_string="Herbst"
    elif (m_act == m_winter).any() :
        season=4
        season_string="Winter"
    else :
        print("Error_UnknownMonth")
    if aq_debug == 1 :
        print("Frühling:",m_spring,", Sommer:",m_sommer,", Herbst:",m_herbst,", Winter:",m_winter)
        print("Aktuelle Jahreszeit:",season_string)

    ########### Sensor ###########
    if usage_DHT11 == 1 :
        humidity, temperature = Adafruit_DHT.read_retry(DHT11sensor, DHTdatapin)
    elif usage_DS1820 == 1 :
        tempsensorfile = open("/sys/bus/w1/devices/28-108ec70664ff/w1_slave")
        tempsensorcontent = tempsensorfile.read()
        tempsensorfile.close()
        try:
            tempsensordata = tempsensorcontent.split("\n")[1].split(" ")[9]
        except Exception as e:
            print('Error:',str(e))
            errors=errors+1
        temperature = (float(tempsensordata[2:]))/1000
        lcd.lcd_display_string(str(errors),1,18)
    else:
        temperature = 999
    if aq_debug == 1 :
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
    if usage_display == 1 :
        lcd.lcd_display_string('T={0:0.1f}'.format(temperature) +chr(223)+"C", 3)
    
    ########### Buffer handling ###########
    if counter_buffer < buffer_size:
        counter_buffer=counter_buffer+1
    else:
        counter_buffer=1
        
    ########### Regler ###########
    if season == 1 :
        t_sp=(t_sommer+t_winter)/2
    elif season == 2 :
        t_sp=t_sommer
    elif season == 3 :
        t_sp=(t_sommer+t_winter)/2
    elif season == 4 :
        t_sp=t_winter
    else :
        print("Error_UnknownSeason")
    if aq_debug == 1 :
        print("Solltemperatur =",t_sp,"°C")
        
    ########### History ###########        
    if temperature < mintemp or localtime().tm_hour == minmaxresettime and localtime().tm_min == 0 :
        mintemp = temperature
        fko.sectime(localtime().tm_hour,localtime().tm_min,9)
    if temperature > maxtemp or localtime().tm_hour == minmaxresettime and localtime().tm_min == 0:
        maxtemp = temperature
        fko.sectime(localtime().tm_hour,localtime().tm_min,15)
    if aq_debug == 1 :
        print("Min/Max-Temperatur =",mintemp,"/",maxtemp,"°C")
    if usage_display == 1 :
        lcd.lcd_display_string('  {0:0.1f}'.format(mintemp) +'  {0:0.1f}'.format(maxtemp), 3,8)

    ########### Alife LED + sleep + displayheartbeat ###########
    fko.heartbeat(s_cycletime)
#     GPIO.output(23,GPIO.LOW) #relay off
#     GPIO.output(23,GPIO.HIGH) #relay on
