import RPi.GPIO as GPIO
import time

PIN_USED = 25

def setup_relay():
    print("Info: relay Setup")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_USED, GPIO.OUT)

def testing_relay():
    print("Info: relay Off")
    operate_relay(True)
    time.sleep(1)
    print("Info: relay On")
    operate_relay(False)
    time.sleep(1)
    print("Info: relay Off")
    operate_relay(True)
    time.sleep(1)

def operate_relay(status):
    if status == True:
        GPIO.output(PIN_USED, GPIO.HIGH)
    else:
        GPIO.output(PIN_USED, GPIO.LOW)

def nyalakan_pin():
    setup_relay()
    GPIO.output(PIN_USED, False) # Perintah untuk mengubah status dari pin
    time.sleep(1.0)
    GPIO.cleanup()
    

if __name__ == "__main__":

    try:
        setup_relay()
        while True:
            testing_relay()
            
    except:
        GPIO.cleanup()
