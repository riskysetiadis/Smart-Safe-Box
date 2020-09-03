import RPi.GPIO as GPIO
import time

pin_use = 13 # Pin yang digunakan untuk buzzer (dapat diubah)

def setup_pin():
	GPIO.setmode(GPIO.BCM) # Perintah untuk setup mode pin raspberry
	GPIO.setup(pin_use, GPIO.OUT) # Perintah untuk set status pin menjadi mode output
	#print("[INFO] SETUP BUZZER...")

def testing_pin():
	operasikan_pin(True) # Perintah untuk menyalakan pin
	time.sleep(1.0) # Perintah untuk memberikan delay
	operasikan_pin(False) # Perintah untuk mematikan pin
	time.sleep(1.0)
	print("[INFO] TESTING BUZZER...")

def operasikan_pin(status):
	print("[INFO] BUZZER DIOPERASIKAN...", status)
	if status == False:
		GPIO.cleanup()
	else:
		setup_pin()        
		GPIO.output(pin_use, status) # Perintah untuk mengubah status dari pin

def nyalakan_pin():
	setup_pin()
	GPIO.output(pin_use, True) # Perintah untuk mengubah status dari pin
	time.sleep(1.0)
	GPIO.cleanup()
	

if __name__ == '__main__':
	try:

		setup_pin()

		while True:
			nyalakan_pin()

	except KeyboardInterrupt:

		GPIO.cleanup() # Perintah untuk mereset pin raspberry
		print("[INFO] WIPE PIN...")
