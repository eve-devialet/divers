#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:50:12 2019

@author: parallels
"""

import serial
import time
import os

class ModuleError(Exception):
    pass

def open_serial():
    '''
    Opens a serial connection
    '''
    # configure the serial connections
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    ser.isOpen()
    return(ser)

def send_command(ser, cmd):
    '''
    Send a command to serial object and retreive answer
    '''
    time.sleep(0.2)
    ser.write("{}\r\n".format(cmd))

    time.sleep(1)
    out = ''
    while ser.inWaiting() > 0:
        out += ser.read(1)
    print(out)
    return(out)

def parse_answer(out):
    if out.find("OK") > -1:
        return(True)
    elif out.find("ERROR") > -1:
        print("Error: {}".format(out))
        raise ModuleError(out)
    else:
        raise IOError("Could not parse serial answer")

def send_and_retry(ser, cmd, retry=4):
    '''
    Send and retry
    '''
    retrynum = 0
    while(retrynum < retry):
        retrynum += 1
        try:
           out = send_command(ser, cmd)
           parse_answer(out)
        except ModuleError:
            continue
        except IOError:
            continue
        return

def read_pinfile():
    pinfile = "/home/pi/Documents/divers/diegoberry/mypin.txt"
    if not os.path.isfile(pinfile):
        raise IOError("File {} not found, cannot use pin code".format(pinfile))
    with open(pinfile) as mypinfile:
        pin = mypinfile.read()
        pin = pin.rstrip()
    return(pin)

def close_serial(ser):
    '''
    Closes the serial connection
    '''
    ser.close()

if __name__ == '__main__':
    mypin = read_pinfile()

    ser = open_serial()

    cmd = "AT+CPIN?"
    out = send_command(ser, cmd)
    if out.find("SIM PIN") < -1:
        raise ModuleError(out)

    cmd = 'AT+CPIN="{}"'.format(mypin)
    out = send_and_retry(ser, cmd, 2)

    cmd = "AT+CPIN=?"
    out = send_and_retry(ser, cmd)

    # Wait for a signal
    print("Wait 20 seconds for connection")
    time.sleep(20)
    out = ''
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out.find("+PBREADY") < -1:
        raise ModuleError(out)
    print(out)

    cmd = 'AT+CGDCONT=3,"10.62.44.72","mmsbouygtel.com"'
    out = send_command(ser, cmd)

    #AT^SWWAN=<action>, <cid>[, <WWAN adapter>]'
    cmd = 'AT^SWWAN=1, 3' #, 1 or 2 (usb0 or usb1)
    out = send_and_retry(ser, cmd)

    close_serial(ser)
