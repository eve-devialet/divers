#!/usr/bin/python3
"""
Created on Tue Jun 12 17:27:46 2018

@author: devialet
"""
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

from src.core import *

if __name__ == "__main__":
    devices = find_ip()
    for ip in devices:
        if is_manolo(ip):
            print("This is a Manolo")
            start_audio(ip, analog=True)