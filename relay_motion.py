import RPi.GPIO as GPIO
import time

#GPIO pins defined
RelayPin = 17
PIRPin = 26

def setup():	#pin and board setup
	GPIO.setwarnings(False)			
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RelayPin, GPIO.OUT, initial = GPIO.LOW)	#relay is closed = sprinkler off	
	GPIO.setup(PIRPin, GPIO.IN)				#motion sensor set as an input
	GPIO.setup()
def main():
	while True:
		detect = GPIO.input(PIRPin)	#motion sensor is always detecting motion
		if detect == 1:			#if motion is detected
			print('Relay close: Sprinkler Off')
			print('Motion detected')
			GPIO.output(RelayPin, GPIO.LOW)		#close the relay to turn off the sprinkler
			
		elif detect == 0:		#if no motion is detected
			print('Relay open: Sprinkler On')	
			print('No motion')
			GPIO.output(RelayPin, GPIO.HIGH)	#keep the relay open
			time.sleep(1)

def destroy():	#clean up function when everything is done
	GPIO.output(RelayPin, GPIO.LOW)
	GPIO.cleanup()
	
if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy()
