#Importerer bibliotek for funksjoner fra Raspberry Pi(RPi)
import machine
#Importerer tids funksjoner
from time import sleep_ms
#Importerer informasjon om sensoren fra APDS9900 biblioteket
from uPy_APDS9900.apds9900LITE import APDS9900LITE
#Importerer Pin- og PWM-funksjoner fra RPi 
from machine import Pin,PWM
import sys

#Aktiverer og definerer sensorene
i2c_a =  machine.I2C(0,scl=machine.Pin(17), sda=machine.Pin(16))
apds9900_a=APDS9900LITE(i2c_a)      # Poweron APDS9900
i2c_b =  machine.I2C(1,scl=machine.Pin(19), sda=machine.Pin(18))
apds9900_b=APDS9900LITE(i2c_b)         # Poweron APDS9900

# Definerer hvilke pins som er inn/ut av RPi Pico ved å gi dem navn
# Motorsett 1
motor_a=Pin(27,Pin.OUT)
motor_b=Pin(26,Pin.OUT)
#Motorsett 2
motor_c=Pin(22,Pin.OUT)
motor_d=Pin(21,Pin.OUT)

# Setter verdien av motor B og D som 0 for å skape en spenningsforskjell (A og C = 1)
motor_b.value(0);
motor_d.value(0);

#Led dioder, definerer navn og pins 
led_1 = Pin(7, Pin.OUT)
led_2 = Pin(6, Pin.OUT)
led_3 = Pin(9, Pin.OUT)
led_4 = Pin(10, Pin.OUT)

#Sensoravlesning, verdien hvor Picoen vil aktivere sving
sensor_verdi = 900

#Hastighet, fremover, svinge etc
sving_hastighet = 4000
sving_hastighet_motsatt = 20000
fremover_hastighet = 13000 #Hastighet bane kjøring
#fremover_hastighet_drag = 50000 #Hastighet drag kjøring


#Defininerer de ulike kjørefunksjonene til bilen
def run_forward():
    PWM(motor_a)
    duty=fremover_hastighet
    PWM(motor_a).duty_u16(duty)
    PWM(motor_c)
    duty=fremover_hastighet
    PWM(motor_c).duty_u16(duty)
    
    #Alle dioder lyser
    led_1.value(1) #led_1 PÅ
    led_2.value(1) #led_2 PÅ
    led_3.value(1) #led_1 PÅ
    led_4.value(1) #led_2 PÅ

def stop_bilen():
    PWM(motor_a)
    duty=0
    PWM(motor_a).duty_u16(duty)
    PWM(motor_c)
    duty=0
    PWM(motor_c).duty_u16(duty)
    
    #Ingen dioder lyser
    led_1.value(0) #led_1 AV
    led_2.value(0) #led_2 AV
    led_3.value(0) #led_1 AV
    led_4.value(0) #led_2 AV
    
def left_turn():
    PWM(motor_a)
    duty=sving_hastighet_motsatt
    PWM(motor_a).duty_u16(duty)
    PWM(motor_c)
    duty=sving_hastighet
    PWM(motor_c).duty_u16(duty)
    
    #Venstre side lyser
    led_1.value(0) #led_1 AV
    led_2.value(0) #led_2 AV
    led_3.value(1) #led_1 PÅ
    led_4.value(1) #led_2 PÅ

    
def right_turn():
    PWM(motor_a)
    duty=sving_hastighet
    PWM(motor_a).duty_u16(duty)
    PWM(motor_c)
    duty=sving_hastighet_motsatt
    PWM(motor_c).duty_u16(duty)
    
    #Høyre side lyser
    led_1.value(1) #led_1 PÅ
    led_2.value(1) #led_2 PÅ
    led_3.value(0) #led_1 AV
    led_4.value(0) #led_2 AV
    


#Definerer en konstant loop hvor sensorer leser av, og forteller bilen hvilken kjøreretning den skal ta
#Loopen går så lenge noe i den er sant
while(True):
    # Aktiver proximity sensorering
    apds9900_a.prox.enableSensor()   
    apds9900_b.prox.enableSensor()   
    sleep_ms(25)                     # Vent til sensoravlesning er klar

    #Kontrollerer bilens kjøreretning basert på sensorenes verdi
    if (apds9900_a.prox.proximityLevel < sensor_verdi and apds9900_b.prox.proximityLevel < sensor_verdi): #Stopp bil
        stop_bilen()
        #sleep_s(1)
        
    elif (apds9900_a.prox.proximityLevel < sensor_verdi ): #Svinge til venstre
        left_turn()
                
    elif (apds9900_b.prox.proximityLevel < sensor_verdi):#Svinge til høyre
        right_turn()

    else:                 #Kjøre rett frem
        run_forward()
      
      
