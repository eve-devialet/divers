#!/usr/bin/env python

"""
This script sends the UBoot files through UART.
Usage :
python script_xmodem.py DIRECTORY TTY
"""

import serial
import io
from xmodem import XMODEM
from time import sleep
import logging
from os import path
import sys

logging.basicConfig()

fwpath = "."
serialport = "/dev/ttyUSB0"

try:
    fwpath = path.abspath(sys.argv[1])
except:
    logging.warn("No path for firmwares was given, using ./")
    fwpath = "."
try:
    serialport = path.abspath(sys.argv[2])
except:
    logging.warn("No serial port was given, using /dev/ttyUSB0")
    serialport = "/dev/ttyUSB0"
    
if not path.exists(fwpath):
    logging.warn("Invalid path %s"%fwpath)
    fwpath = "."
files = ["bin.boot1", "bin.uboot", "bin.m0patch", "bin.ssb"]
for cfile in files:
    if not path.isfile(path.join(fwpath, cfile)):
        raise IOError("Missing file %s in path %s"%(cfile, fwpath))

s = serial.Serial(port=serialport, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)

# Change line_buffering to \r
s_io = io.TextIOWrapper(io.BufferedRWPair(s, s, 1),
                               newline = '\r',
                               line_buffering = True)

# Define XMODEM putc / getc
def getc(size, timeout=1):
    return s.read(size)
def putc(data, timeout=1):
    s.write(data)
modem = XMODEM(getc, putc)

step = 0
while(1):
	x = s_io.readline()
	print("{}".format(repr(x)))

	if(x.find("UART for Xmodem-1k file transfer") > -1 or x.find("Send data using the Xmodem-1k protocol now ...") > -1):

		if(step == 0):
			print("Sending Boot 1...")
			stream = open(path.join(fwpath,'bin.boot1'), 'rb')
			status = modem.send(stream, retry=8)
			print("End of Sending Boot1")
			step = step + 1
		elif(step == 1):
			print("Sending U-Boot...")
			stream = open(path.join(fwpath,'bin.uboot'), 'rb')
			status = modem.send(stream, retry=8)
			print("End of Sending")
			step = step + 1
		elif(step == 2):
			print("Sending M0Patch...")
			stream = open(path.join(fwpath,'bin.m0patch'), 'rb')
			status = modem.send(stream, retry=8)
			print("End of Sending")
			step = step + 1
		elif(step == 3):
			print("Sending SSB...")
			stream = open(path.join(fwpath,'bin.ssb'), 'rb')
			status = modem.send(stream, retry=8)
			print("End of Sending")
			step = step + 1
s.close()

