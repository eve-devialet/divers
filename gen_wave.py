#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:27:53 2019

@author: Eve
"""

import wave, struct, math

def create_stereo(sampleRate=44100.0, duration=2.0, freq=200.0):
    '''
    Create stereo sound file
    '''
    # Use same frequency for left and right
    rFreq= freq
    lFreq= freq
    name = "stereo_{:.0f}Hz.wav".format(freq)
    wavef = wave.open(name, 'w')
    wavef.setnchannels(2) # stereo
    wavef.setsampwidth(2) 
    wavef.setframerate(sampleRate)
    
    for i in range(int(duration * sampleRate)):
        l = int(32767.0*math.cos(2*lFreq*math.pi*float(i)/float(sampleRate)))
        r = int(32767.0*math.cos(2*rFreq*math.pi*float(i)/float(sampleRate)))
        dat = struct.pack('<hh', l, r )
        wavef.writeframesraw(dat)
    
    wavef.writeframes(b'')
    wavef.close()

if __name__ == "__main__":
    sampleRate = 44100.0 # hertz
    duration = 4.0       # seconds
    freq = 200.0         # hertz
    create_stereo(sampleRate, duration, freq)