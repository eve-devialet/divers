# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 14:37:23 2017

@author: eveaporee

Pretty plots for CEM measurements (CSV file format)
"""

import os
import numpy as np
import matplotlib.pyplot as plt


def max_glissant(vector, n_avg=4):
    '''
    Maximum glissant
    vector : input data
    n_avg : number of samples to average from
    '''
    result_vect = np.zeros(np.shape(vector))

    # Beginning: take n first samples as is
    result_vect[0:n_avg-1] = vector[0:n_avg-1]

    for i in np.arange(n_avg, np.size(vector)+1):
        result_vect[i-1] = np.max(vector[i-n_avg:i])
    return(result_vect)

plt.clf()

filelist = os.listdir("./")
csvfilelist = list()
for idx, filename in enumerate(filelist):
    if filename[-4:] == ".csv":
        csvfilelist.append(filename)

for myfile in csvfilelist:
    with open(myfile, "r") as myofile:
        ch = myofile.read()
        ch = ch.replace(",", ".")
        with open(myfile + "temp", "w") as mytfile:
            mytfile.write(ch)

    my_data = np.genfromtxt(myfile + "temp", delimiter=';')

    freq_axis = my_data[:, 0]
    data = my_data[:, 1]
    # Uncomment if you want to take maximum value over n samples
    # data = max_glissant(data, n_avg=6)

    plt.semilogx(freq_axis, data, label=myfile[0:-4])

plt.legend()
plt.xlim(150000, 30000000)
plt.ylim(0, 100)
plt.xticks([150e3, 500e3, 1e6, 2e6, 5e6, 10e6, 30e6],
           ["150k", "500k", "1M", "2M", "5M", "10M", "30M"])
plt.xlabel("Freq(Hz)")
plt.ylabel("Peak(dBuV)")
plt.title("Emission conduite")
plt.grid()
newfilelist = os.listdir("./")
for filename in newfilelist:
    if filename.find(".csvtemp") > -1:
        os.remove(filename)
