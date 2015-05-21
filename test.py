#!/usr/bin/env python2
# -*- coding: utf-8 -*-

### New Python Template File
### H27 Mar 16

import os, sys
import time
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI

GPIO.setup("P9_12",GPIO.OUT)
GPIO.output("P9_12",GPIO.HIGH)
print("GPIO >> HIGH")

spi_in = SPI(0, 0)
spi_out = SPI(0, 1)

spi_out.msh = 500000

while True:
    
    GPIO.output("P9_12",GPIO.LOW)
    print("GPIO >> LOW")
    spi_out.writebytes([0b00001111])
    print("write >> num")
    print spi_in.readbytes(1)
    GPIO.output("P9_12",GPIO.HIGH)
    print("GPIO >> HIGH")
    time.sleep(1)

GPIO.cleanup()


