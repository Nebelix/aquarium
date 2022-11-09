##################################
########### Konstanten ###########
##################################
aq_debug=0
########### Hardware ###########
usage_DHT11=0 #use blue DHT11 sensor
usage_DS1820=1 #use steel water temp sensor
usage_display=1 #I2C Serielles 20x4 2004 LCD Modul
########### Jahreszeiten ###########
m_sommer_start=7 #Juli(7) = Beginn Sommer bzw. Trockenzeit
m_winter_start=1 #Januar(1) = Beginn Winter bzw. Regenzeit
########### Uhrzeiten ###########
z_dawn_end=0   #Ende der Morgendämmerung
z_dusk_start=0 #Start der Abenddämmerung
########### Temperaturen ###########
t_sommer = 29
t_winter = 27
t_nacht_diff = 1.5
hysterese = 0.3
minmaxresettime=3 # Reset-Uhrzeit, 3 = 03:00 wird 1 min lang min/max temp auf Istwerte gesetzt
########### Timer ###########
s_cycletime=1       #Soll-Durchlaufzeit in s
min_s_cycletime=0.5 #untere Grenze für sleep in s
cycletime_Igain=0.5 #Integrator-Faktor sleep
buffer_size=10
