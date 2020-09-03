import RPi.GPIO as GPIO
import time

pin_use = 16 # Pin yang digunakan untuk PUSH (dapat diubah)

def setup_pin():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin_use, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	#print("[INFO] SETUP PUSH...")

def testing_pin():
	if baca_pin() == GPIO.HIGH:
		print("[INFO] PUSH...")
	else:
		print("[INFO] NOT PUSH...")


def baca_pin():
	return GPIO.input(pin_use)

def baca_status_pintu():
	return baca_pin() == GPIO.HIGH

if __name__ == '__main__':
	try:

		setup_pin()

		while True:
			testing_pin()

	except KeyboardInterrupt:

		GPIO.cleanup() # Perintah untuk mereset pin raspberry
		print("[INFO] WIPE PIN...")
