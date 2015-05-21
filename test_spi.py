#!/usr/bin/env	python
# -*-	coding: utf-8 -*-
import time
from Adafruit_BBIO.SPI import SPI

spi_in = SPI(0, 0)
spi_out = SPI(0, 1)


while True:
	try:
		print spi_in.readbytes(1)
		time.sleep(0.03)

	except KeyboardInterrupt:
		Break

