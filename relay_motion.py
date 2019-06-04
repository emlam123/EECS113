import RPi.GPIO as GPIO
import time

#GPIO pins defined
RelayPin = 17
PIRPin = 26
<<<<<<< HEAD
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RelayPin, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(PIRPin, GPIO.IN)
    print('Initializing PIR')
    
    time.sleep(30)

        
def sprinkler():
    detect = GPIO.input(PIRPin)
    if (detect == 1):
        print('Relay close: Sprinkler Off')
        print('Motion detected')
        GPIO.output(RelayPin, GPIO.LOW)
			    
    elif (detect == 0):
        print('Relay open: Sprinkler On')
        print('No motion')
        GPIO.output(RelayPin, GPIO.HIGH)
        time.sleep(1)

def destroy():
    GPIO.output(RelayPin, GPIO.LOW)
    GPIO.cleanup()
	
def relay():
    #call setup in main
    #setup()
    try:
        sprinkler()
    except KeyboardInterrupt:
        destroy()
