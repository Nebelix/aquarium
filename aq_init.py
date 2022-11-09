import numpy            #Vektorenhandling Jahreszeitenerkennung
import Adafruit_DHT     #DHT11 Sensor
from time import *      #Durchlaufzeit messen
import RPi.GPIO as GPIO #LED
import lcddriver        #Display

########### Konstanten + Einstellungen ###########
from aq_constants import *

########### initialize sensors ###########
DHT11sensor = Adafruit_DHT.DHT11
DHTdatapin = 4
humidity = 999 # in case not measured

########### Variablen initialisieren ###########
oldtime = 0
new_s_cycletime = s_cycletime
buffer_cycletime=numpy.zeros(buffer_size)
counter_buffer = 0
avg_cycletime = s_cycletime*1000
mintemp=100
maxtemp=0
errors=0
numpy.place(buffer_cycletime, buffer_cycletime==0, [s_cycletime*1000])

########### initialize GPIO for LED ###########
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

########### initialize GPIO for relay ###########
GPIO.setup(23,GPIO.OUT)

########### initialize LC Display ###########
if usage_display == 1 :
    lcd = lcddriver.lcd()
    lcd.lcd_clear()
    lcd.lcd_display_string("  run aquarium.py", 1)
    fkochars = [
            # heart
            [0x00,0x00,0x1B,0x1F,0x1F,0x0E,0x04,0x00],
            # face
            [0x00,0x00,0x0A,0x00,0x11,0x0E,0x00,0x00]
             ]

########### Monate und Jahreszeiten verknüpfen ###########
if (m_winter_start-1 == 0):      #Herbst ist immer der Monat vor Winter
    m_herbst=12
else:
    m_herbst=m_winter_start-1
    
if (m_sommer_start-1 == 0):      #Frühling ist immer der Monat vor Sommer
    m_spring=12
else:
    m_spring=m_sommer_start-1
m_sommer=numpy.arange(m_sommer_start, m_herbst)
m_winter=numpy.arange(m_winter_start, m_spring)
t_springherbst=(t_sommer+t_winter)/2

########### Funktionen ###########
class fko:
    def clock(h,m,s):
        if h < 10 :
            tenhour="0"
        else:
            tenhour=""
        if m < 10 :
            tenmin="0"
        else:
            tenmin=""
        if s < 10 :
            tensec="0"
        else:
            tensec=""
        lcd.lcd_display_string(tenhour+str(h)+":"+tenmin+str(m)+":"+tensec+str(s), 4)
    def heartbeat(sleeptime):
        #switchtimefactor: 0.1=10% of cycle time diode is off
        GPIO.output(18,GPIO.LOW) #LED off
        if usage_display == 1 :
            lcd.lcd_display_string(" ", 1) # erase heart
        sleep(sleeptime*0.5)
        GPIO.output(18,GPIO.HIGH) #LED on
        if usage_display == 1 :
            lcd.lcd_write(0x80)
        if usage_display == 1 :
            lcd.lcd_write_char(0) # print heart
        sleep(sleeptime*0.5)
    def sectime(h,m,pos):
        if h < 10 :
            tenhour="0"
        else:
            tenhour=""
        if m < 10 :
            tenmin="0"
        else:
            tenmin=""
        if usage_display == 1 :
            lcd.lcd_display_string(tenhour+str(h)+":"+tenmin+str(m),4,pos)