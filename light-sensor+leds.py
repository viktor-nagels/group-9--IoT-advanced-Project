#!/usr/bin/env python
import time
import spidev
import cgitb
import RPi.GPIO as GPIO
cgitb.enable()

LED_PIN_R1 = 6
LED_PIN_G1 = 5
LED_PIN_R2 = 22
LED_PIN_G2 = 27
LED_PIN_R3 = 4
LED_PIN_G3 = 18
LED_PIN_R4 = 23
LED_PIN_G4 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup((LED_PIN_G1, LED_PIN_G2, LED_PIN_G3, LED_PIN_G4, LED_PIN_R1, LED_PIN_R2, LED_PIN_R3, LED_PIN_R4), GPIO.OUT)
GPIO.output((LED_PIN_G1, LED_PIN_G2, LED_PIN_G3, LED_PIN_G4, LED_PIN_R1, LED_PIN_R2, LED_PIN_R3, LED_PIN_R4), 1)


spi = spidev.SpiDev()  # create spi object
spi.open(0, 0)  # open spi port 0, device CS0 pin 24
spi.max_speed_hz = (1000000)


# read SPI data 8 possible adc's (0 thru 7)
def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    r = spi.xfer2([1, (8+adcnum) << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout


while True:
      # read channel 0
    lightsensor1 = readadc(0)
    lightsensor2 = readadc(1)
    lightsensor3 = readadc(2)
    lightsensor4 = readadc(3)
    

    print("lichgehalte1:", lightsensor1)
    print("lichgehalte2:", lightsensor2)
    print("lichgehalte3:", lightsensor3)
    print("lichgehalte4:", lightsensor4)
    print("-----------------------------")
    time.sleep(0.7)
    
    #!Parking lot 1
    if lightsensor1 > 950:
        GPIO.output(LED_PIN_R1, 0)
        GPIO.output(LED_PIN_G1, 1)
    else:
        GPIO.output(LED_PIN_R1, 1)
        GPIO.output(LED_PIN_G1, 0)

    #!Parking lot 2
    if lightsensor2 > 950:
        GPIO.output(LED_PIN_R2, 0)
        GPIO.output(LED_PIN_G2, 1)
    else:
        GPIO.output(LED_PIN_R2, 1)
        GPIO.output(LED_PIN_G2, 0)

    #!Parking lot 3
    if lightsensor3 > 950:
        GPIO.output(LED_PIN_R3, 0)
        GPIO.output(LED_PIN_G3, 1)
    else:
        GPIO.output(LED_PIN_R3, 1)
        GPIO.output(LED_PIN_G3, 0)

    #!Parking lot 4
    if lightsensor4 > 950:
        GPIO.output(LED_PIN_R4, 0)
        GPIO.output(LED_PIN_G4, 1)
    else:
        GPIO.output(LED_PIN_R4, 1)
        GPIO.output(LED_PIN_G4, 0)
