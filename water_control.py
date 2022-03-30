import RPi.GPIO as GPIO
import time

FLOW = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


GPIO.setup(FLOW, GPIO.OUT)

#This function turns the valve on and off in 5 sec. intervals. 
def water_control():
            GPIO.output(FLOW, GPIO.LOW)
            print("GPIO LOW (off), valve should be on")
            time.sleep(5)