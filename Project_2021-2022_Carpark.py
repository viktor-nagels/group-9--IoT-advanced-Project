from picamera import PiCamera
from time import sleep
import requests
from pprint import pprint
import RPi.GPIO as GPIO
import time

pinsoon1 = 20
pinsoon2 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinsoon1, GPIO.OUT)
GPIO.setup(pinsoon2, GPIO.IN)

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


while True:
    GPIO.output(20,1)
    time.sleep(0.00001)
    GPIO.output(20,0)
    
    while(GPIO.input(21)==0):
        pass
    signaalhigh = time.time()

    while(GPIO.input(21)==1):
        pass

    signaallow = time.time()
    timepassed = signaallow - signaalhigh
    distance = timepassed * 17000
  
    if distance <= 30 :    #in centimeter
        photo()
        print('AUTO aan de bareel')
        for n in range(0, 130):
                stepdrive(23,24,25,26)
        time.sleep(30)   # moet nog veranderd worden naar als de auto weg is
        
        for n in range(0, 130):
                stepdrive(26,25,24,23)
        
    else:
        GPIO.output(23, 0)
        GPIO.output(24, 0)
        GPIO.output(25, 0)
        GPIO.output(26, 0)
        print('GEEN auto aan de bareel')
        time.sleep(0.5)