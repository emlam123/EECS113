from gpiozero import Buzzer
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
buzzer = 27

GPIO.setup(buzzer,GPIO.OUT)
while True:
	GPIO.output(buzzer,GPIO.HIGH)
	print("Beep")
	sleep(.001)
	GPIO.output(buzzer,GPIO.LOW)
	print("No beeep")
	sleep(0.001)
"""

buzzer = Buzzer(13) # GPIO27

def buzz():
    buzzer.on()
    sleep(1)
    buzzer.off()

buzz()
"""
