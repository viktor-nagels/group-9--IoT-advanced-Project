from picamera import PiCamera
from time import sleep
import requests
import RPi.GPIO as GPIO
import time
import spidev
import cgitb
import mysql.connector
import RPi.GPIO as GPIO

cgitb.enable()

ultrasonic1 = 17
ultrasonic2 = 4
button = 20
step1 = 18
step2 = 23
step3 = 24
step4 = 25
pinstep = 18,23,24,25
LED_PIN_R2 = 26
LED_PIN_G2 = 12
LED_PIN_R1 = 27
LED_PIN_G1 = 22
LED_PIN_R3 = 13
LED_PIN_G3 = 16
LED_PIN_R4 = 5
LED_PIN_G4 = 6
LED_PIN_R5 = 20
light_intensety = 970
light_intensety1 = 970

GPIO.setmode(GPIO.BCM)
GPIO.setup((ultrasonic2), GPIO.IN)
GPIO.setup((ultrasonic1,step1,step2,step3,step4,LED_PIN_G1,LED_PIN_G2,LED_PIN_G3,LED_PIN_G4,LED_PIN_R1,LED_PIN_R2,LED_PIN_R3,LED_PIN_R4,LED_PIN_R5), GPIO.OUT)
#GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.output((LED_PIN_G1, LED_PIN_G2, LED_PIN_G3, LED_PIN_G4, LED_PIN_R1, LED_PIN_R2, LED_PIN_R3, LED_PIN_R4, LED_PIN_R5), 1)

spi = spidev.SpiDev()  # create spi object
spi.open(0, 0)  # open spi port 0, device CS0 pin 24
spi.max_speed_hz = (1000000)

def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    r = spi.xfer2([1, (8+adcnum) << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

def updateDB(Status, ID):
    mydb = mysql.connector.connect(
    host="localhost",
    user="pi",
    password="raspberry",
    database="ParkingDB"
    )

    mycursor = mydb.cursor()

    sql = "UPDATE ParkingLot SET bezet = %s WHERE ID = %s"
    val = (Status, ID)

    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record(s) affected")

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
    camera = PiCamera() 
    camera.rotation = -90
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/images/photo.jpg')  
    camera.stop_preview()
    #camera.off()
    camera.close()

def numberplate():
    regions = ['mx', 'be'] # Change to your country
    with open('/home/pi/images/photo.jpg', 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': 'Token 315a9c42be797329049bf2cc52a5cb41ab960e15'})
    json_results = (response.json())  
    if (response.json()['results'] == []):
        numberplate = "FALSE"
    else:
        numberplate = (json_results['results'][0]['plate'])
        print((json_results['results'][0]['plate']))
        
    return numberplate

def stepmotor():
    for n in range(0, 130):
            stepdrive(step1,step2,step3,step4)
    time.sleep(10)   #TODO moet nog veranderd worden naar als de auto weg is
    
    for n in range(0, 130):
            stepdrive(step4,step3,step2,step1)

def ultrasonic():
    GPIO.output(ultrasonic1,1)
    time.sleep(0.00001)
    GPIO.output(ultrasonic1,0)
    
    while(GPIO.input(ultrasonic2)==0):
        pass
    signaalhigh = time.time()

    while(GPIO.input(ultrasonic2)==1):
        pass

    signaallow = time.time()
    timepassed = signaallow - signaalhigh
    distance = timepassed * 17000
    return distance

while True:
    buttonState = GPIO.input(button)
    distance = ultrasonic()
    print(distance)

    if distance <= 30 :    #in centimeter
        photo()
        numberplate()
        plate = numberplate()
        print(plate)
        if plate != "FALSE":
            print("Car can access parking") 
        
            stepmotor()
        else:
            GPIO.output(LED_PIN_R5, 0)
            print("There was no numberplate found")
            time.sleep(2)
            GPIO.output(LED_PIN_R5, 1)
        
    else:
        print('GEEN auto aan de bareel')
        time.sleep(0.5)
    


    lightsensor1 = readadc(1)
    lightsensor2 = readadc(0)
    lightsensor3 = readadc(2)
    lightsensor4 = readadc(3)
    lightsensor5 = readadc(4)
    print(lightsensor1, lightsensor2, lightsensor3, lightsensor4, lightsensor5)

        #? Code for exiting the parking 
    if lightsensor5 > light_intensety1:
        photo()
        numberplate()
        plate = numberplate()
        print(plate)
        if plate == "FALSE":
            print("Car can exit parking")
            print("There was no numberplate found")
            
        
            stepmotor()
        else:
            print("there was a numberplate found")
            GPIO.output(LED_PIN_R5, 0)
            time.sleep(2)
            GPIO.output(LED_PIN_R5, 1)

        #!Parking lot 1
    if lightsensor1 > light_intensety:
        GPIO.output(LED_PIN_R1, 0)
        GPIO.output(LED_PIN_G1, 1)
        updateDB(1,1)
    else:
        GPIO.output(LED_PIN_R1, 1)
        GPIO.output(LED_PIN_G1, 0)
        updateDB(0,1)
    #!Parking lot 2
    if lightsensor2 > light_intensety:
        GPIO.output(LED_PIN_R2, 0)
        GPIO.output(LED_PIN_G2, 1)
        updateDB(1,4)
    else:
        GPIO.output(LED_PIN_R2, 1)
        GPIO.output(LED_PIN_G2, 0)
        updateDB(0,4)
    #!Parking lot 3
    if lightsensor3 > light_intensety:
        GPIO.output(LED_PIN_R3, 0)
        GPIO.output(LED_PIN_G3, 1)
        updateDB(1,3)
    else:
        GPIO.output(LED_PIN_R3, 1)
        GPIO.output(LED_PIN_G3, 0)
        updateDB(0,3)

    #!Parking lot 4
    if lightsensor4 > light_intensety:
        GPIO.output(LED_PIN_R4, 0)
        GPIO.output(LED_PIN_G4, 1)
        updateDB(1,2)
    else:
        GPIO.output(LED_PIN_R4, 1)
        GPIO.output(LED_PIN_G4, 0)
        updateDB(0,2)   
    time.sleep(1)

    if ((lightsensor1 < 950) and (lightsensor2 < 950) and (lightsensor3 < 950) and (lightsensor4 < 950)):
        GPIO.output(LED_PIN_R5, 0)
    else:
        GPIO.output(LED_PIN_R5, 1)

