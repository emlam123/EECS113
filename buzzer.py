import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
buzzer = 27 # pin 13
GPIO.setup(buzzer, GPIO.OUT)

def buzz():
    t_end = time.time() + 5
    while time.time() < t_end:
        GPIO.output(buzzer, GPIO.HIGH)
        sleep(.001)
        GPIO.output(buzzer, GPIO.LOW)
        sleep(.001)

