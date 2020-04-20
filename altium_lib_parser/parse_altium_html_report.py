#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 12:08:24 2020

@author: Eve

Another ugly regexp parser, to export pin number by components from Altium lib
HTML reports.
And yes I thought about using BeautifulSoup and I did not, regexp were
easier in this case.

"""
import os
import re
import csv
import io

directory = "/media/psf/Home/STM32CubeIDE/HTML"
base_filename = "DEVIALET_IC2_{}.html"
output_filename = "pin_numbers.csv"
components = list()
pins = list()
idx = 1

while True:
    file = base_filename.format(idx)
    filename = os.path.join(directory, file)
    idx += 1
    if not os.path.exists(filename):
        print("Last file at index {}".format(idx-1))
        break
    
    with open(filename, "r") as myfile:
        html = ""
        for line in io.open(filename, encoding="ISO-8859-1", newline="\r\n"):
            html = html + line
    
    reg_name = re.compile("""<b>\s+Library Reference\s+</b>\s+</font>\s+""" +\
                       """</td>\s+<td valign="top">\s+<h2>\s+""" +\
                       """<font face="Arial" size="2">\s+([\S ]+)\s+</font>""", re.MULTILINE)
    
    
    reg_num = re.compile("""Number of Pins\s+</b>\s+</font>\s+""" +\
                       """</td>\s+<td valign="top">\s+<font face="Arial" size="2">\s+""" +\
                       """(\d+)""", re.MULTILINE)
    
    component_name = reg_name.findall(html)
    if len(component_name) < 1:
        print("No component found at idx {}".format(idx))
        continue
    else:
        component_name = component_name[0]
    component_pin_num = reg_num.findall(html)
    if len(component_pin_num) < 1:
        print("No pin number found for component {}".format(component_name))
        component_pin_num = 0
    else:
        component_pin_num = component_pin_num[0]
    components.append(component_name)
    pins.append(int(component_pin_num))
    
output_file = output_filename
mylist = zip(components, pins)
with open(output_file, 'w') as myfile:
    mycsv = csv.writer(myfile)
    mycsv.writerows(mylist)