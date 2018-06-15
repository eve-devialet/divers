#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 15:48:38 2018

@author: eve
"""

import subprocess
import os
import re
import json
import sys

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# Load parameters from JSON
with open(os.path.join(CURRENT_DIR, "../config.json"), "r") as infile:
    config = json.load(infile)
key_file = config["RsaFile"]
iface = config["LocalInterface"]


def sPopen(command):
    '''
    Execute subprocess but do not wait for return
    '''
    p = subprocess.Popen(command, shell=True, stdin=None,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         preexec_fn=os.setsid)
    return(p)

def dnwPopen(command):
    '''
    Execute subprocess but do not wait for return
    '''
    p = subprocess.Popen(command, shell=True, stdin=None, stdout=None,
                         stderr=None)
    return(p)

def execute_command(ipv6, cmd):
    '''
    Execute a command on a device
    '''
    cmd = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i {key} root@{ipv6}%{iface} {cmd}".format(key=key_file, ipv6=ipv6, iface=iface, cmd=cmd)
    ret = sPopen(cmd)
    print(cmd)
    out = ret.stdout.readlines()
    err = ret.stderr.readlines()
    print(err)
    return(out, err)

def execute_scp(ipv6, file, target_path):
    '''
    Execute a command on a device
    '''
    cmd = "scp -6 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i {key} {file} root@\[{ipv6}%{iface}\]:{target_path}".format(key=key_file, ipv6=ipv6, iface=iface, file=file, target_path=target_path)
    ret = sPopen(cmd)
    print(cmd)
    out = ret.stdout.readlines()
    err = ret.stderr.readlines()
    print(err)
    return(out, err)

def execute_command_no_ret(ipv6, cmd):
    cmd = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i {key} root@{ipv6}%{iface} {cmd} &".format(key=key_file, ipv6=ipv6, iface=iface, cmd=cmd)
    dnwPopen(cmd)

def stop_plc(ipv6):
    '''
    Stops plc
    '''
    execute_command(ipv6, "/root/plc_stop.sh")

def find_ip():
    '''
    Find Titolo IPs
    '''
    cmd = "ping6 -c 5 -I {} ff02::1 | grep 7ec4".format(iface)

    ret = sPopen(cmd)
    ret = ret.stdout.readlines()
    rex = re.compile("(fe80:[0-9a-f:]*)")
    if len(ret) == 0:
        print("No Devialet devices found")
    devices = list()
    for r in ret:
        print(r)
        ip = rex.findall(str(r))
        if len(ip) > 0:
            ip = ip[0]
            if ip[-1] == ":":
                ip = ip[0:-1]
            print(ip)
            devices.append(ip)
    devset = set(devices)
    return(devset)

def is_manolo(ipv6):
    cmd = "/bin/cat /sys/bus/platform/devices/hw_id/hw-id/family"
    ret, __ = execute_command(ipv6, cmd)
    if len(ret) < 1:
        print("No HW family, let us say Tito")
        return(False)
    ret = str(ret)
    print(ret)
    if ret.find("Manolo") > -1:
        manolo = True
    else:
        manolo = False
    return(manolo)


def start_audio(ipv6, analog=True):
    '''
    Starts manolo audio
    '''
    execute_command(ipv6, "/usr/bin/killall gst-launch-1.0")
    print("Starting audio")
    if analog:
        execute_command_no_ret(ipv6, "/root/analog.sh")
    else:
        execute_command_no_ret(ipv6, "/root/digital.sh")
    #print("Audio started")

def start_hdmi_audio(ipv6):
    '''
    Starts manolo audio
    '''
    execute_command(ipv6, "/usr/bin/killall gst-launch-1.0")
    print("Starting audio")
    execute_command_no_ret(ipv6, "/root/hdmi_audio.sh")

def start_tito_spdif(ipv6):
    '''
    Starts Tito spdif audio
    '''
    execute_command(ipv6, "/usr/bin/killall gst-launch-1.0")
    print("Starting audio")
    execute_command_no_ret(ipv6, "/root/tito_digital.sh")

def start_plc(ipv6):
    '''
    Starts PLC
    '''
    stdout, __ = execute_command(ipv6, "/root/plc.sh")
    print(stdout)

def flash_plc(ipv6):
    '''
    Flash PLC
    '''
    stdout, __ = execute_command(ipv6, "/root/PLC_install/plc_flash.sh")
    print(stdout)
    
def unflash_plc(ipv6):
    '''
    Unflash PLC
    '''
    stdout, __ = execute_command(ipv6, "/usr/bin/plcinit -i plc0 -E")
    print(stdout)
    
def info_plc(ipv6):
    stdout, __ = execute_command(ipv6, "plcinit -i plc0 -r")
    print(stdout)
    return(stdout)

if __name__ == "__main__":
    devices = find_ip()
    for ip in devices:
        if is_manolo(ip):
            print("This is a Manolo")
        execute_scp(ip, "{}/../test.txt".format(CURRENT_DIR), "/root/")
            #start_audio(ip, analog=True)
