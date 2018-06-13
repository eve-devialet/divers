#!/usr/bin/python3
"""
Created on Tue Jun 12 17:27:46 2018

@author: devialet
"""
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

from src.core import find_ip, is_manolo, start_hdmi_audio

if __name__ == "__main__":
    devices = find_ip()
    for ip in devices:
        if not is_manolo(ip):
            print("This is a Tito")
            start_hdmi_audio(ip)