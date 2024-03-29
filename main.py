import RPi.GPIO as GPIO
import time
import rpi_data
import datetime
import relay_motion    
import I2C_LCD_driver
from keypad import keypad

def main():

    ### KEYPAD INITIALIZATION ###
    kp = keypad(columnCount = 4)
    digit = None

    #global target
    global target
    target = ""
    print("Enter your zip code or press '#' for Irvine: ")
    for i in range(5):
        digit = None
        while digit == None:
            digit = kp.getKey()
        if (digit == "#"):
            break;
        print(digit)
        target = target + str(digit)
        time.sleep(0.4)

    ### END KEYPAD ###

    relay_motion.setup()
    current_hr = datetime.datetime.now().time().hour 
    print(current_hr)
    mylcd = I2C_LCD_driver.lcd()
    #current_hr = 18
    rpi_data.read_sensors(current_hr,mylcd)
    # the main function
    # obtain CIMIS humidity, temperature, and ET0
    # obtain RPI humidity, temperature, and ET0
    # derate CIMIS ET0
    # calculate water needed
    # turn on the relay for specified time

    # all the while...
    # display updated data onto LED!!

    # question: if the required water is supplied within an hour... what do???

if __name__ == '__main__':
    main()
