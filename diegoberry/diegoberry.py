#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:01:32 2019

@author: parallels
"""
import subprocess as sp
import logging
logger = logging.getLogger(__name__)
import time

import os,sys
lib_path = os.path.abspath(os.path.join(__file__, 'amp'))
sys.path.append(lib_path)
import tas2770 as amp

def ex_cmd(cmd):
    '''
    Execute a Linux command with Popen
    '''
    logger.debug(cmd)
    pop = sp.Popen(cmd.split(" "), stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = pop.communicate()
    if pop.returncode == 0:
        return(stdout)
    else:
        raise IOError("CMD error: {}".format(stderr))

if __name__ == '__main__':

    # Needs to have pigpiod service started :
    # sudo raspi-config -> enable "allow remote connections" for GPIO and
    # sudo systemctl enable pigpiod
    
    
    # PWM freq 100kHz
    freq = 100000
    # Duty cycle 40% gives 16.2 V
    duty = 40
    cmd = "pigs hp 12 {:d} {:d}".format(freq, int(duty*1e4)) # 500000 is 50% duty cycle
    ex_cmd(cmd)
    
    # Amp init
    device = amp.TAS2770_DEFAULT_I2C
    amp.tas2770_set_volume(device, -12)
    amp.tas2770_unmute(device)
    
if 0:
    time.sleep(1)
    # Play a multichannel sound
    soundfile = "/home/pi/TheRobots8.wav"
    cmd = "aplay {} -D hw:1,0".format(soundfile)
    ex_cmd(cmd)
