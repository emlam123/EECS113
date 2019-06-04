import RPi.GPIO as GPIO
import time

RelayPin = 17
PIRPin = 26
def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RelayPin, GPIO.OUT, initial = GPIO.LOW)
	GPIO.setup(PIRPin, GPIO.IN)
	GPIO.setup()
def main():
	while True:
		detect = GPIO.input(PIRPin)
		if detect == 1:
			print('Relay close: Sprinkler Off')
			print('Motion detected')
			GPIO.output(RelayPin, GPIO.LOW)
			start_t = time.time()
		if detect == 1 && time.time() - start_t > 10:
			print('Timer > 10')
			detect = 0
			
		elif detect == 0:
			print('Relay open: Sprinkler On')
			print('No motion')
			GPIO.output(RelayPin, GPIO.HIGH)
			time.sleep(1)

def destroy():
	GPIO.output(RelayPin, GPIO.LOW)
	GPIO.cleanup()
	
if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy()
