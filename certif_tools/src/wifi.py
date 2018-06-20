#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 18:19:49 2018

@author: eve
"""

import re
import time
import os, sys

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_DIR)
from core import config, execute_command, sPopen, execute_scp

def end_test(*args):
    print(args)
    sys.exit()

def debug(*args):
    print(args)

def wifi_connection(ip):
    '''
    Tries to connect to the Wifi network
    Works but only with static IP
    Returns ssid and IPv6 of remote Wifi network
    '''
    wlan_iface = config["dut_wifi_iface"]
    ssid = config["wifi_ssid"]
    password = config["wifi_pass"]
    pos = hash(ip)%256
    static_ip = "192.168.1.{}".format(pos)
    pos = hash(ip)%(0xffff)
    static_ipv6 = "fe80::7ec4:efff:feff:{:04x}/64".format(pos)

    # First detect if we are already connected to wifi or not
    connected = False
    comm, err = execute_command(ip, "/usr/sbin/iw dev {} link".format(wlan_iface))
    returned = str(comm)
    verif_regex = re.compile("""SSID: ([^\\\\]+)""")
    valid = verif_regex.findall(returned)
    if len(valid) < 1:
        connected = False
    elif valid[0] != ssid:
        return("Connected to wrong SSID, should pose problem")
    else:
        connected = True

    if not connected:
        # Start up interface
        cmd_wifi = """/sbin/ifconfig {} up""".format(wlan_iface)
        stdout, stderr = execute_command(ip, cmd_wifi)
        returned = "{} {}".format(stdout, stderr)
        # Scan list of available Wifi networks
        cmd_wifi = """/usr/sbin/iw dev {} scan""".format(wlan_iface) # | grep "SSID.{}" -c
        stdout, stderr = execute_command(ip, cmd_wifi)
        returned = "{} {}".format(stdout, stderr)
        returned = str(returned)

        fail_regex = re.compile("failed", re.IGNORECASE)
        is_fail = fail_regex.findall(returned)
        if len(is_fail) > 0:
            return("Wifi scan failed: {}".format(returned))

        split_regex = re.compile("\nBSS ")
        found_nets = split_regex.split(returned)
        wifi_regex = re.compile("""([^\(^\s]+)\(on \S+\).*signal:\s+(\S+)\s+.*SSID:\s([^\n\t]*)""", re.DOTALL)

        for net in found_nets:
            res = wifi_regex.findall(net)[0]
            if res[2].find(ssid) > -1:
                debug("Found SSID {}".format(res[2]))

        cmd_pass = """wpa_passphrase "{}" "{}" """.format(ssid, password)
        pc = sPopen(cmd_pass)
        ans = pc.communicate()[0]
        wpaconf = str(ans)
        if pc.returncode != 0:
            return("wpa_passphrase failed with error: {}".format(wpaconf))
        with open("wpa.conf", "w") as myconf:
            myconf.writelines(wpaconf)

        # Send wpa.conf to DUT
        execute_scp(ip, "wpa.conf", '/tmp')

        # Setting static IP
        cmdlist = list()
        cmdlist.append("/sbin/ifconfig {} down".format(wlan_iface))
        cmdlist.append("/sbin/ifconfig {} {}".format(wlan_iface, static_ip))
        cmdlist.append("/sbin/ifconfig {} up".format(wlan_iface))
        cmd_connect = """/usr/sbin/wpa_supplicant -Dnl80211 -i{} -B -c/tmp/wpa.conf""".format(wlan_iface)
        cmdlist.append(cmd_connect)

        for cmd in cmdlist:
            stdout, stderr = execute_command(ip, cmd)
            returned = "{} {}".format(stdout, stderr)
            debug(returned)

        stdout, stderr = execute_command(ip, "/usr/sbin/iw dev {} link".format(wlan_iface))
        returned = "{} {}".format(stdout, stderr)
    # Waiting for connection for at maximum timeout seconds
    timeout = 80
    invalid = 1
    loops = 0
    verif_regex = re.compile("""Not connected""")
    while invalid:
        loops += 1
        if loops > timeout:
            return("Timeout to connect to Wifi network expired")
        stdout, stderr = execute_command(ip,
                                        "/usr/sbin/iw dev {} link".format(wlan_iface))
        returned = "{} {}".format(stdout, stderr)
        valid = verif_regex.findall(returned)
        if len(valid) > 0:
            debug("Not connected to any WiFi network, waiting...")
            invalid = 1
            time.sleep(1)
        else:
            invalid = 0

    # Verifying SSID
    verif_regex = re.compile("""SSID: ([^\\\\]+)""")
    valid = verif_regex.findall(returned)
    if len(valid) < 1:
        return("Not connected to any WiFi network")
    elif valid[0] != ssid:
        return("Connected to Wifi but SSID {} not right".format(valid))

    # Waiting for IPV6 assignment
    invalid = 1
    loops = 0
    ip_regex = re.compile("""inet6 addr: ([^/]*)/(\d*) Scope:""")

    while invalid:
        loops += 1
        if loops > timeout:
            return("Timeout to get global IPv6 for Wifi network expired")
        stdout, stderr = execute_command(ip,
                                        "/sbin/ifconfig {}".format(wlan_iface))
        returned = "{} {}".format(stdout, stderr)
        valid = ip_regex.findall(returned)
        if len(valid) < 1:
            debug("Not connected to any WiFi network, IPv6 issue, waiting...")
            invalid = 1
            time.sleep(1)
        else:
            invalid = 0
            ipv6 = valid[0]

    # Changing IPV6
    # Find bad ipv6 wifi address
    ip_regex = re.compile("""inet6 addr: ([^/]*)/(\d*) Scope:""")
    stdout, stderr = execute_command(ip, """/sbin/ifconfig {}""".format(wlan_iface))
    returned = "{} {}".format(stdout, stderr)
    ip_found = ip_regex.findall(returned)
    print(ip_found)
    if len(ip_found) > 0:
        wlan_ipv6 = "{}/{}".format(ip_found[0][0], ip_found[0][1])
    else:
        print("FAILED with ret: {} and ipfound {}".format(returned, ip_found))
        return()
    cmdlist = list()
    cmdlist.append("/sbin/ifconfig {} add {}".format(wlan_iface, static_ipv6))
    cmdlist.append("/sbin/ifconfig {} del {}".format(wlan_iface, wlan_ipv6))
    for cmd in cmdlist:
        stdout, stderr = execute_command(ip, cmd)
        returned = "{} {}".format(stdout, stderr)
        debug(returned)
    # End changing IPV6

    return("Connected to Wifi with SSID {} and ipv6 {}".format(ssid, static_ipv6))