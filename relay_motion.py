import RPi.GPIO as GPIO
import time
import I2C_LCD_driver
from time import sleep
#GPIO pins defined
RelayPin = 17
PIRPin = 26
w_time = 0 

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RelayPin, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(PIRPin, GPIO.IN)

    print('Initializing PIR')
    
    time.sleep(10)

        
def sprinkler(mylcd,mutex):
    #mylcd = I2C_LCD_driver.lcd()
    #global w_time
    detect = GPIO.input(PIRPin)
    if (detect == 1):
        print('Relay close: Sprinkler Off')
        mutex.acquire()
        mylcd.lcd_clear()
        #time.sleep(1)
        mylcd.lcd_display_string("Irrigation off", 1)
        mylcd.lcd_display_string("                ",2)
        mutex.release()
        #time.sleep(5)
        print('Motion detected')
        #w_time += 1
        GPIO.output(RelayPin, GPIO.LOW)
			    
    elif (detect == 0):
        print('Relay open: Sprinkler On')
        print('No motion')
        
        GPIO.output(RelayPin, GPIO.HIGH)
        time.sleep(1)

def destroy():
    GPIO.output(RelayPin, GPIO.LOW)
    GPIO.cleanup()
	
def relay(start_time,water_time,mylcd,mutex):
    global w_time
    w_time = start_time
    try:
        while(((time.time()-w_time)/60) < water_time):
                sprinkler(mylcd,mutex)
                 
        GPIO.output(RelayPin, GPIO.LOW)

    except KeyboardInterrupt:
        destroy()
