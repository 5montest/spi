#!/usr/bin/env ipython3
# -*- coding: utf-8 -*-

### New Python Template File
### H27 Mar 16

import os, sys
import time

import Adafruit_BBIO.GPIO as GPIO

GPIO.setup("P9_22",GPIO.OUT)


while True:
    GPIO.output("P9_22",GPIO.LOW)
    time.sleep(0.001)
    GPIO.output("P9_22",GPIO.HIGH)
    time.sleep(0.001)

