#!/usr/bin/python
import sys
import Adafruit_DHT as fruit
import I2C_LCD_driver 
import datetime
import rpi_data
from time import sleep
import time

def local_data(mylcd,temperatures,humidities,mutex):
    temp_avg=0
    hum_avg=0
    count=0
    #global temperatures,humidities

    print("COLLECTING LOCAL DATA\n")
    #lcd = CharLCD(cols=15,rows=2,pin_rs=37,pin_e=35,pins_data=[33,31,29,23])
    #mylcd = I2C_LCD_driver.lcd()
    #we are using DHT11 so 11 is our sensor type and it's connected to GPIO pin 4
    current_hour = datetime.datetime.now().time().hour
    #print("IN LOCAL: %d\n" %current_hour)
    while (True):
        humidity, temperature = fruit.read_retry(11,4) 
        if humidity is not None and temperature is not None:
            #display temp and humidity on lcd
            temperature = temperature * (9/5) + 32
            mutex.acquire()
            mylcd.lcd_clear()
            #time.sleep(1)
            mylcd.lcd_display_string("Temp: %.1f F      " %(temperature), 1)
            mylcd.lcd_display_string("Humidity: %.1f %% " %(humidity),2)
            mutex.release()

            time.sleep(1)
            print ("Temp: {0:0.1f}F Humidity: {1:0.1f} %".format(temperature,humidity))
            temp_avg+=temperature
            hum_avg+=humidity
            count+=1
            temperatures[current_hour]=temp_avg
            humidities[current_hour]=hum_avg
            #return (temperature,humidity)
        #else:
            #return None
        new_hour = datetime.datetime.now().time().hour
        if (new_hour==current_hour+1):
            temp_avg=temp_avg/count
            hum_avg=hum_avg/count
            temperatures[current_hour]=temp_avg
            humidities[current_hour]=hum_avg
            print("TEMP AVG: %d\n" %temp_avg)
            print("HUM AVG:%d\n" %hum_avg)

            temp_avg=0
            hum_avg=0
            count=0
            current_hour = datetime.datetime.now().time().hour


if __name__=='__main__':
    local_data()
