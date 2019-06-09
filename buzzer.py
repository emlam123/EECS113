from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(13) # GPIO27

def buzz():
    buzzer.on()
    sleep(1)
    buzzer.off()
