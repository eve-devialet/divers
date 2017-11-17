# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 14:37:23 2017

@author: eveaporee

Pretty plots for CEM measurements (CSV file format)
"""

import os
import numpy as np
import matplotlib.pyplot as plt


#def madmax(vector):
if 1:
    vector = np.arange(0, 10)
    mat = np.array([vector[0:-3], vector[1:-2], vector[2:-1], vector[3:]])
    np.max(mat)

plt.clf()
if 1:
    filelist = os.listdir("./")
    csvfilelist = list()
    for idx, filename in enumerate(filelist):
        if filename[-4:] == ".csv" :
            print(filename)
            csvfilelist.append(filename)
            
    print(csvfilelist)
    
    
    for myfile in csvfilelist:
        with open(myfile, "r") as myofile:
            ch = myofile.read()
            ch = ch.replace(",", ".")
            with open(myfile + "temp", "w") as mytfile:
                mytfile.write(ch)
        
        my_data = np.genfromtxt(myfile + "temp", delimiter=';')
        
        vector = my_data[:, 0]

        
        plt.semilogx(my_data[:, 0], my_data[:, 1], label=myfile)
        
    plt.legend()
    plt.xlim(150000,30000000)
    plt.ylim(0,100)
    plt.xticks([150e3,500e3,1e6,2e6,5e6,10e6,30e6],
               ["150k", "500k", "1M", "2M", "5M","10M","30M"])
    plt.xlabel("Freq(Hz)")
    plt.ylabel("Peak(dBuV)")
    plt.title("Emission conduite")
    plt.grid()
    newfilelist = os.listdir("./")
    for filename in newfilelist:
        if filename.find(".csvtemp") > -1:
            os.remove(filename)
            
