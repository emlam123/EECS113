#!/usr/bin/python
import sys
import Adafruit_DHT as fruit
import I2C_LCD_driver 
import datetime

def local_data():
    #lcd = CharLCD(cols=15,rows=2,pin_rs=37,pin_e=35,pins_data=[33,31,29,23])
    mylcd = I2C_LCD_driver.lcd()
    #we are using DHT11 so 11 is our sensor type and it's connected to GPIO pin 4
    humidity, temperature = fruit.read_retry(11,4) 
    if humidity is not None and temperature is not None:
        #display temp and humidity on lcd
        mylcd.lcd_display_string("Temp: %.1f C" %(temperature), 1)
        mylcd.lcd_display_string("Humidity: %.1f %% " %(humidity),2)
        #print ("Temp: {0:0.1f}C Humidity: {1:0.1f} %".format(temperature,humidity))
        return (temperature,humidity)
    else:
        return None


if __name__=='__main__':
    local_data()
