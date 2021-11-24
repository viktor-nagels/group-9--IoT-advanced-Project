from picamera import PiCamera
from time import sleep
import requests
from pprint import pprint
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.IN)



def stepdrive(pin1,pin2,pin3,pin4):  
    pinnumbers = pin1,pin2,pin3,pin4
    GPIO.setup(pinnumbers, GPIO.OUT)
    GPIO.output(pinnumbers, 0)
    GPIO.output(pin1, 1)
    GPIO.output(pin2, 1)
    GPIO.output(pin3, 0)
    GPIO.output(pin4, 0)
    time.sleep(0.01)
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 1)
    GPIO.output(pin3, 1)
    GPIO.output(pin4, 0)
    time.sleep(0.01)
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 0)
    GPIO.output(pin3, 1)
    GPIO.output(pin4, 1)
    time.sleep(0.01)
    GPIO.output(pin1, 1)
    GPIO.output(pin2, 0)
    GPIO.output(pin3, 0)
    GPIO.output(pin4, 1)
    time.sleep(0.01)


def photo():
    camera = PiCamera() # TODO deze rotatie kan nog aangepast worden A.D.H.V. hoe de camera geposisioneert staat
    camera.rotation = 180
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/images/photo.jpg')  # TODO make location for the pictures
    camera.stop_preview()

def numberplate():
    regions = ['mx', 'be'] # Change to your country
    with open('/home/pi/images/photo.jpg', 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': 'Token 315a9c42be797329049bf2cc52a5cb41ab960e15'})
    json_results = (response.json())
    numberplate = (json_results['results'][0]['plate'])
    return numberplate


