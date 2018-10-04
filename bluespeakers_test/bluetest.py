# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import subprocess
import time
import audio_common
import os

#Measurement parameters
macs = ["04:52:C7:F9:43:38", "00:12:6F:B6:8D:BC", "88:C6:26:8C:0B:B1"]
devices = ["Bose", "Beoplay",  "Megaboom"]
record_time = 5
sleep_time = 15

def runcmd(cmd):
    ret = subprocess.Popen(cmd, shell=True, 
                           stdout=subprocess.PIPE).communicate()[0]
    return(ret)

def message(device, mac_device, msg):
    now = time.time() - start_time
    with open("result.txt", "a") as myres:
        myres.write("{:.0f}s, device {} ({}): {}\n".format(now, device, 
                    mac_device, msg))

def disconnect(device, mac_device):
    if int(ret) < 1:
        stop_time = time.time() - start_time
        with open("result.txt", "a") as myres:
            print("{} disconnected !".format(device))
            myres.write("Stop time for {} ({}):\n".format(device, 
                            mac_device))
            myres.write("{:.0f} seconds\n".format(stop_time))
            myres.write("{:.0f}h {:.0f}m {:.0f}s\n".format(stop_time/3600, 
                        stop_time/60, stop_time))
            myres.write("\n\n")    


start_time = time.time()
with open("result.txt", "a") as myres:
     myres.write("***\nStart time: {}\n".format(time.ctime(start_time)))
cmd_bt = "/usr/bin/hcitool con | grep -c {}"
cmd_rec = "arecord -d {} -c 1 -r 8000 -f S16_LE {}"
wavfile_spec = "sounds/{}{}.wav"
idx = 0
resultfile = "result.txt"

#Cleaning sound files
try:
    os.rmdir("./sounds")
    os.mkdir("sounds")
except:
    pass

while 1:
    idx += 1
    if len(devices) < 1:
        break
    for device, mac_device in zip(devices, macs):
        ret = runcmd(cmd_bt.format(mac_device))
        if int(ret) < 1:
            disconnect(device, mac_device)                
            devices.remove(device)
            macs.remove(mac_device)
    
    for device, mac_device in zip(devices, macs):
        wavfile = wavfile_spec.format(device, idx)
        ret = runcmd(cmd_rec.format(record_time, wavfile))
        # TODO test if this fails ?
        is_ok, value = audio_common.compute_signal(wavfile, threshold=0.05, nb_chan=1, log="")
        if not is_ok:
            message(device, mac_device, "Signal not found: value {:.2f} inferior to threshold".format(value))
    time.sleep(sleep_time)