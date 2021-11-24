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
    lightsensor = readadc(0)  # read channel 0

    print "lichgehalte:", lightsensor
    time.sleep(0.2)
