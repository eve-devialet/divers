#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:12:21 2020

@author: Eve Redero
"""

import re
import io
import csv

filename = "component.lia"

### Open file and parse pins
with open(filename, "r") as myfile:
    mytext = ""
    for line in io.open("component.lia", encoding="ISO-8859-1"):
        mytext = mytext + line
 
myreg = re.compile("""\(compPin "(\S+)" \(pinName "(\S+)"\) \(partNum (\d+)\) \(symPinNum (\d+)\) \(gateEq (\d+)\) \(pinEq (\d+)\) \(pinType (\S+)\) \)""")
parsed_pin_header = ["compPin", "pinName", "partNum", "symPinNum", "gateEq", "pinEq", "pinType"]
parsed_pin_list = myreg.findall(mytext)

### Export csv
with open(filename + ".csv", 'w') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(parsed_pin_header)
    writer.writerows(parsed_pin_list)

### Remapping
remap_filename = "pin_remap.csv"
with open(remap_filename, "r") as myfile:
    reader = csv.reader(myfile, delimiter=";")
    remap = []
    for line in reader:
        remap.append(line)

remap_header = remap.pop(0)
int_cols = [remap_header.index("partNum"), remap_header.index("symPinNum")]
for line in remap:
    for idx in int_cols:
        line[idx] = int(line[idx])
remapidx = [i[0] for i in remap]
        
remap_pin_col = remap_header.index("Final_pinTC")
remap_name_col = remap_header.index("Final_pin_name")
# Replace in pin description section
copytext = mytext
for trouve in myreg.finditer(mytext):
    groups = trouve.groups()
    pin = groups[0]
    idx_pin = remapidx.index(pin)
    original = trouve.group()
    rep = re.sub(pin, remap[idx_pin][remap_pin_col], original)
    rep = re.sub(groups[1], remap[idx_pin][remap_name_col], rep)
    copytext = copytext.replace(original, rep)
    
# Replace in pinmap section
myreg_pinmap = re.compile("""\(padNum  (\d+)\) \(compPinRef "(\S+)"\)""")
res = myreg_pinmap.findall(mytext)
for trouved in myreg_pinmap.finditer(mytext):
    groups = trouved.groups()
    pin = groups[1]
    idx_pin = remapidx.index(pin)
    original = trouved.group()
    rep = re.sub(pin, remap[idx_pin][remap_pin_col], original)
    copytext = copytext.replace(original, rep)
    
# Replace in pin name section
myreg_pindesc = re.compile("""\s+\(pin \(pinNum (\d+)\).*$""" +\
                           """\s+\(pinDisplay.*$""" +\
                           """\s+\(pinDes\s+\(text\s+\(pt \S+ \S+\) "(\S+)" .*$""" +\
                           """\s+\)$""" +\
                           """\s+\(pinName\s+\(text\s+\(pt \S+ \S+\) "(\S+)"\s*""", re.MULTILINE)
for trouved in myreg_pindesc.finditer(mytext):
    groups = trouved.groups()
    pin = groups[1]
    idx_pin = remapidx.index(pin)
    original = trouved.group()
    rep = re.sub(pin, remap[idx_pin][remap_pin_col], original)
    rep = re.sub(groups[2], remap[idx_pin][remap_name_col], rep)
    copytext = copytext.replace(original, rep)

filename_out = re.sub(".lia", ".remap.lia", filename)
with open(filename_out, 'w') as myfile:
    myfile.write(copytext)
