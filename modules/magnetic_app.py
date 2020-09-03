import RPi.GPIO as GPIO
import time

pin_use = 26 # Pin yang digunakan untuk SWITCH (dapat diubah)

def setup_pin():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin_use, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	#print("[INFO] SETUP SWITCH...")

def testing_pin():
	if baca_pin() == GPIO.HIGH:
		print("[INFO] DOOR CLOSED...")
	else:
		print("[INFO] DOOR OPEN...")


def baca_pin():
	return GPIO.input(pin_use)

def baca_status_pintu():
	return baca_pin() == GPIO.LOW

if __name__ == '__main__':
	try:

		setup_pin()

		while True:
			testing_pin()

	except KeyboardInterrupt:

		GPIO.cleanup() # Perintah untuk mereset pin raspberry
		print("[INFO] WIPE PIN...")
