########### Init ###########
from aq_init import *
if usage_display == 1 :
    lcd.lcd_load_custom_chars(fkochars)
########### main loop ###########
while True:
    if aq_debug == 1 :
        print("___________")
    ########### Timer ###########
    fko.clock(localtime().tm_hour,localtime().tm_min,localtime().tm_sec) #show timestamp on display
    m_act=localtime().tm_mon   #take actual month as number
    if m_act == m_spring :
        season=1
        season_string="Spring"
    elif (m_act == m_summer).any() :
        season=2
        season_string="Summer"
    elif m_act == m_autumn :
        season=3
        season_string="Autumn"
    elif (m_act == m_winter).any() :
        season=4
        season_string="Winter"
    else :
        print("Error_UnknownMonth")
    if aq_debug == 1 :
        print("Spring:",m_spring,", Summer:",m_summer,", Autumn:",m_autumn,", Winter:",m_winter)
        print("Current season:",season_string)

    ########### Temp sensor ###########
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
			if usage_display == 1 :
				lcd.lcd_display_string(str(errors),1,18)
        temperature = (float(tempsensordata[2:]))/1000        
    else:
        temperature = 999
    if aq_debug == 1 :
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
    if usage_display == 1 :
        lcd.lcd_display_string('T={0:0.1f}'.format(temperature) +chr(223)+"C", 3)
        
    ########### Temperature controller ###########
    heater_on = fko.tempcontrol(season,temperature,heater_on)
        
    ########### Temporary storage ###########
    if temperature < mintemp or localtime().tm_hour == minmaxresettime and localtime().tm_min == 0 :
        mintemp = temperature
        fko.sectime(localtime().tm_hour,localtime().tm_min,9)
		if usage_display == 1 :
			lcd.lcd_display_string('  {0:0.1f}'.format(mintemp), 3,8)
    if temperature > maxtemp or localtime().tm_hour == minmaxresettime and localtime().tm_min == 0:
        maxtemp = temperature
        fko.sectime(localtime().tm_hour,localtime().tm_min,15)
		if usage_display == 1 :
			lcd.lcd_display_string('  {0:0.1f}'.format(maxtemp), 3,14)
    if aq_debug == 1 :
        print("Min/Max temperature =",mintemp,"/",maxtemp,"°C")
    
    ########### slow loop ###########
    if cycleslow_counter >= cyclegain_slow :
        ### place slow functions below ###
        fko.connectcheck()
        ### place slow functions above ###
        cycleslow_counter=0
    else:
        cycleslow_counter=cycleslow_counter+1

    ########### Alife LED + sleep + displayheartbeat ###########
    fko.heartbeat()