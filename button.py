import RPi.GPIO as GPIO
import time

button = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN)

while True:
    if GPIO.input(button) == GPIO.HIGH:
        print("Button was pushed!")
        time.sleep(0.5)


