#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 17:34:25 2018

@author: eve
"""

import os, sys

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_DIR)

FW_DIR = os.path.realpath(os.path.join(CURRENT_DIR, "../fw/emmc-usineos.img"))
from core import execute_flash_command, is_tito, is_manolo

def flash_device(ip):
    '''
    Flashes usineos FW on device
    '''
    if not os.path.exists(FW_DIR):
        return("Firmware file could not be found in {}".format(FW_DIR))
    if not (is_tito(ip) or is_manolo(ip)):
        return("Device is not a Tito or a Manolo, aborting flash")
    stdout, stderr = execute_flash_command(ip, FW_DIR, "/dev/mmcblk0")
    ret = "{} {}".format(stdout, stderr)
    return(ret)
    
if __name__ == "__main__":
    import core
    devices = core.find_ip()
    for ip in devices:
        a = flash_device(ip)

        

