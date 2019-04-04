#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:01:32 2019

@author: parallels
"""
import subprocess as sp
import logging
logger = logging.getLogger(__name__)

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

if 0:
    # Play a multichannel sound
    soundfile = "multicanal8.wav"
    
    # R20 for Rodolphe, T20 for TI
    cmd = "aplay {} -D sysdefault:CARD=T20".format(soundfile)
    ex_cmd(cmd)
    
if 1:
    # Needs to have pigpiod service started :
    # sudo raspi-config -> enable "allow remote connections" for GPIO and
    # sudo systemctl enable pigpiod
    
    # PWM freq 100kHz
    freq = 100000
    # Duty cycle 40% gives 16.2 V
    duty = 40
    cmd = "pigs hp 12 {:d} {:d}".format(freq, int(duty*1e4)) # 500000 is 50% duty cycle
    ex_cmd(cmd)
    