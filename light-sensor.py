#!/usr/bin/env python
import time
import spidev
import cgitb
cgitb.enable()

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
    
        
