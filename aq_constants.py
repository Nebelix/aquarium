##################################
####### Constants/Settings #######
##################################
aq_debug=0          #debug flag for direct console output in python
aq_version=2.1      #release version of aquarium.py
########### Hardware ###########
usage_DHT11=0       #use blue DHT11 sensor
usage_DS1820=1      #use steel water temp sensor
usage_display=1     #I2C serial 20x4 2004 LCD Module
########### Seasons ###########
m_summer_start=7    #July(7) = begin of summer or drought
m_winter_start=1    #January(1) = begin of winter or rains
########### Lighting time ###########
z_dawn_end=0        #End of dawn
z_dusk_start=0      #Start of dusk
########### Temperatures (Celsius) ###########
t_summer = 29
t_winter = 27
t_noct_fall = 1.5   #nightly reduce of temperature
t_hysteresis = 0.3  #temperature difference between starting and stopping heating
minmaxresettime=3   #clock time at which min/max temps are reset, 3 = from 03:00 to 03:01 AM min/max temp is set to actual value
########### Network ###########
usage_ccheck=1      #set 1 if platform has usually a network/internet connection
ccheck_host='https://github.com/'
ccheck_timeout=1    #report no network connection after this time [seconds]
########### Timer ###########
s_cycletime=1       #Set time for 1 script cycle in seconds
cyclegain_slow=10   #number of standard cycles to execute between 2 slow cycles