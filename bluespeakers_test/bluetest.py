# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import subprocess
import time
import audio_common
import os, shutil
import csv

#Measurement parameters
macs = ["04:52:C7:F9:43:38", "00:12:6F:B6:8D:BC", "88:C6:26:8C:0B:B1"]
devices = ["Bose", "Beoplay",  "Megaboom"]
record_time = 5
sleep_time = 15


def message(device, mac_device, msg):
    now = time.time() - start_time
    with open("result.txt", "a") as myres:
        myres.write("{:.0f}s, device {} ({}): {}\n".format(now, device, 
                    mac_device, msg))

def write_values(val_list):
    val_list_c = [time.time() - start_time] + val_list
    with open("levels.csv", "a") as myres:
        csvw = csv.writer(myres)
        csvw.writerow(val_list_c)

def disconnect(device, mac_device):
    if int(ret) < 1:
        stop_time = time.time() - start_time
        with open("result.txt", "a") as myres:
            print("{} disconnected !".format(device))
            myres.write("Stop time for {} ({}):\n".format(device, 
                            mac_device))
            myres.write("{:.0f} seconds\n".format(stop_time))
            myres.write("{:.0f}h {:.0f}m {:.0f}s\n".format(stop_time/3600, 
                        stop_time%3600, stop_time%60))
            myres.write("\n\n")    

def runcmd(cmd):
    sp = subprocess.Popen(cmd, shell=True, 
                           stdout=subprocess.PIPE)
      
    ret = sp.communicate()[0]
    if sp.returncode != 0:
        print(sp.returncode)
        print("Command {} failed with error code {}".format(cmd, sp.returncode))
        message("", "", "Command {} failed with error code {}".format(cmd, sp.returncode))
    return(ret)

start_time = time.time()
with open("result.txt", "a") as myres:
     myres.write("***\nStart time: {}\n".format(time.ctime(start_time)))
cmd_bt = "timeout -k 2 1 /usr/bin/hcitool con | grep -c {}"
cmd_rec = "timeout -k {} {} arecord -d {} -c 1 -r 8000 -f S16_LE {}"
wavfilename_spec = "sounds/{}{}.wav"
idx = 0

#Cleaning sound files
if os.path.exists("sounds"):
    shutil.rmtree("sounds")
if not os.path.exists("sounds"):
    os.mkdir("sounds")


write_values(devices)
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
            write_values(devices)
    
    values = []
    for device, mac_device in zip(devices, macs):
        wavfilename = wavfilename_spec.format(device, idx)
        ret = runcmd(cmd_rec.format(record_time + 5, record_time + 2, record_time, wavfilename))
        # TODO test if this fails ?
        try:
            is_ok, value = audio_common.compute_signal(wavfilename, threshold=0.05, nb_chan=1, log="")
            values.append(value)
            if not is_ok:
                message(device, mac_device, "Signal not found: value {:.2f} inferior to threshold".format(value))
        except:
            print("Failed audio computing")
    write_values(values)
    time.sleep(sleep_time)