import numpy            #handling vectors, used for detecting the actual season
import Adafruit_DHT     #DHT11 temperature sensor
from time import *      #handling all time related stuff
import RPi.GPIO as GPIO #access GPIO pins (control diodes and more)
import lcddriver        #20x4 LCD

########### Constants + Settings ###########
from aq_constants import *

########### initialize sensors ###########
DHT11sensor = Adafruit_DHT.DHT11
DHTdatapin = 4
humidity = 999 # in case not measured

########### initialize variables ###########
mintemp=100
maxtemp=0
errors=0

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
    lcd.lcd_display_string("  run aquarium"+aq_version, 1)
    fkochars = [
            # heart
            [0x00,0x00,0x1B,0x1F,0x1F,0x0E,0x04,0x00],
            # face
            [0x00,0x00,0x0A,0x00,0x11,0x0E,0x00,0x00]
             ]

########### Assign months to seasons ###########
if (m_winter_start-1 == 0):      #Autumn is always the 1 month before winter
    m_autumn=12
else:
    m_autumn=m_winter_start-1
    
if (m_summer_start-1 == 0):      #Spring is always the 1 month before summer
    m_spring=12
else:
    m_spring=m_summer_start-1
m_summer=numpy.arange(m_summer_start, m_autumn)
m_winter=numpy.arange(m_winter_start, m_spring)
t_springautumn=(t_summer+t_winter)/2

########### custom functions ###########
class fko:
    def clock(h,m,s):
        if h < 10 :      #need to print 0 manually to have all characters always in same place
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
        GPIO.output(18,GPIO.LOW)           #LED off
        if usage_display == 1 :
            lcd.lcd_display_string(" ", 1) #erase heart
        sleep(sleeptime*0.5)
        GPIO.output(18,GPIO.HIGH)          #LED on
        if usage_display == 1 :
            lcd.lcd_write(0x80)
        if usage_display == 1 :
            lcd.lcd_write_char(0)          #print heart; printing at end means it will still longer than 50% of runtime because sensor is checked after this
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