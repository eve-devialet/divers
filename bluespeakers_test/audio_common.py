#!/usr/bin/env python3
##
##


import numpy as np
import sys

from scipy.io import wavfile as sciwavfile
#from scipy.fftpack import fft
#from scipy.signal import blackman


def find_frequency(myarray, fs=48000):
    '''
    Find array frequency
    '''
    fourier = np.fft.fft(myarray)
    frequencies = np.fft.fftfreq(len(myarray), 1./fs)
    # where 2nd arg is the inter-sample time difference
    magnitudes = abs(fourier[np.where(frequencies > 0)])  # magnitude spectrum

    peak_frequency = np.argmax(magnitudes)
    # Correction factor if duration is not 1 second:
    duration = myarray.shape[0] / fs
    peak_frequency = peak_frequency / duration
    return(peak_frequency)

def end_test(num, msg, msg2=""):
    print("{} {}".format(msg, msg2))
    sys.exit(num)
    
def debug_and_log(msg, log):
    log = "{}\n{}".format(log, msg)
    return(log)
    
def compute_fft(wav_file, nb_chan, expected, max_offset=0.05, log=""):

        # Analyse wave file
    try:
        wavefile = sciwavfile.read("{}".format(wav_file))
    except Exception as e:
        end_test(3, "Invalid wave file", e)
    framerate = wavefile[0]
    wavedata = wavefile[1]
    nchannels = wavedata.shape[1]
    # Converting int to float
    maxint = np.iinfo(wavedata.dtype).max
    wavedata = wavedata / maxint

    try:
        assert(nchannels == nb_chan)
        totlength = wavedata.shape[0]
        assert(totlength > 1000)
    except AssertionError as exc:
        log = debug_and_log("Invalid sound format, error: {}".format(exc), log)
        end_test(4, "Invalid sound format", exc)

    for i in range(nb_chan):
        if (np.mean(np.abs(wavedata[:, i])) < 0.01):
            log = debug_and_log("No signal found on channel {}".format(i+1), log)
            end_test(5, "fft error", log)
        else:
            log = debug_and_log("Signal found on channel {}".format(i+1), log)
        freq = find_frequency(wavedata[:, i], fs=framerate)
        th_freq = expected[i]
        if ((np.abs(float(th_freq - freq)) / th_freq) > 0.1):
            log = debug_and_log("Frequency does not match on channel {}: {} Hz instead of {} Hz".format(i+1, freq, th_freq), log)
            end_test(6, "fft error", log)
        else:
            log = debug_and_log("Frequency {} Hz OK on channel {}".format(freq, i+1), log)

    wavesum = np.abs(np.mean(wavedata, axis=0))
    for idx, mysum in enumerate(wavesum):
        if mysum > max_offset:
            log = debug_and_log("Wave signal has too much offset",
                     "{} on channel {}".format(mysum, idx+1), log)
            end_test(7, "fft error", log)

    return log

def compute_signal(wav_file, threshold=0.01, nb_chan=1, log=""):
        # Analyse wave file
    try:
        wavefile = sciwavfile.read("{}".format(wav_file))
    except Exception as e:
        end_test(3, "Invalid wave file", e)
    #framerate = wavefile[0]
    wavedata = wavefile[1]
    #nchannels = wavedata.shape[1]
    # Converting int to float
    maxint = np.iinfo(wavedata.dtype).max
    wavedata = wavedata / maxint

    try:
        #assert(nchannels == nb_chan)
        totlength = wavedata.shape[0]
        assert(totlength > 1000)
    except AssertionError as exc:
        log = debug_and_log("Invalid sound format, error: {}".format(exc), log)
        end_test(4, "Invalid sound format", exc)

    for i in range(nb_chan):
        val = np.mean(np.abs(wavedata[:]))
        print("Avg sound value: {}".format(val))
        if (val < threshold):
            log = debug_and_log("No signal found on channel {}".format(i+1), log)
            return(False, val)
            #end_test(5, "fft error", log)
        else:
            log = debug_and_log("Signal found on channel {}".format(i+1), log)
            return(True, val)
            


    return log
