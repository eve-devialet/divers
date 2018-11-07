#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 10:07:35 2018

@author: eve
"""
import numpy as np

# Boost design with TPS43069

### User values
Vin_min = 6.
Vin_max = 8.4
Vout_min = 12.
Vout_max = 40.
# Average values
Vin = 3.6 * 2
Vout = 35.

#Iout_max = 14.
Iout_max = 8.
Iout = 6.

# Desired delta V for a given output delta I
DItran = 1.
DVtran = 0.6
# Acceptable ripple tension 
Vripple = 1

# Kind is the ratio of inductor peak-to-peak ripple current to the 
#average inductor current. It depends on the output capacitor ESR.
Kind = 0.7

# Mos
Qg_mos = 10e-9

# UVLO values
Vuvlo_start = 6.6
Vuvlo_stop = 6.

### Values for loop compensation
# Output capacitor ESR value
ESR = 5e-3
# Vout setting resistors (typical values)
Rsh_typ = 220e3
Rsl_typ = 10e3

# Output file
outfile = "boost_design.txt"


##############################################################################
### Switching frequency selection
# Duty cycle range
# Min Vin
D1_1 = (Vout_max - Vin_min) / Vout_max
D1_2 = (Vout_min - Vin_min) / Vout_min
# Max Vin
D2_1 = (Vout_max - Vin_max) / Vout_max
D2_2 = (Vout_min - Vin_max) / Vout_min
# Normal behaviour
D = (Vout - Vin) / Vout


Dmin = np.min([D1_1, D1_2, D2_1, D2_2])
Dmax = np.max([D1_1, D1_2, D2_1, D2_2])

ton_min = 100e-9
fsw_ontime = (Dmin / ton_min)
toff_min = 250e-9
fsw_offtime = (1-Dmax) / toff_min
fsw_min = np.max([fsw_ontime, fsw_offtime])

print("Frequency should be inferior than {} MHz".format(fsw_min / 1e6))
fsw = input("Please input frequency (MHz):")
fsw = float(fsw) * 1e6
assert(fsw <= fsw_min)
print("You chose frequency {} MHz".format(fsw / 1e6))

Rt_th = (57500. / fsw) * 1e6

print("Rt target = {} kOhms".format(Rt_th / 1e3))
Rt = input("Please input real Rt value (kOhms):")
Rt = float(Rt) * 1e3
fsw = (57500. / Rt) * 1e6
print("Real frequency: {} MHz".format(fsw * 1e-6))
assert(fsw <= fsw_min)

### Inductor selection
Iin = Iout / (1-Dmax)

print("Iin = {} A".format(Iin))

Lmin_1 = Vout_max / (Iin * Kind) * 1. / (4 * fsw)
Lmin_2 = Vin_max * Dmax / (Iin * Kind * fsw)
print("Lmin_1 = {} uH, Lmin_2 = {} uH".format(Lmin_1*1e6, Lmin_2*1e6))
Lmin = np.max([Lmin_1, Lmin_2])

print("Lmin = {} uH".format(Lmin * 1e6))

L = input("Please input inductance (uH):")
L = float(L) * 1e-6
#assert(L >= Lmin * 0.95)

Ilrms = np.sqrt( (Iout / (1-Dmax)) ** 2 + ((Vin_min * Dmax) / (np.sqrt(12) * L * fsw)) ** 2)
print("Ilrms = {} A".format(Ilrms))

Ilpeak = Iout / (1-Dmax) + (Vin_min * Dmax) / (2 * L * fsw)
print("Ilpeak = {} A".format(Ilpeak))


### Current sense resistor
Vcsmax_typ = 68e-3
Rcs_th = Vcsmax_typ / (1.2 * Ilpeak)
print("Rcs target (max) = {} mOhms".format(Rcs_th * 1e3))

Rcs = input("Please input real Rcs value (mOhms):")
Rcs = float(Rcs) * 1e-3

Prcs = Vcsmax_typ ** 2 / Rcs
print("Power admissible by Rcs: {} W".format(Prcs))

### Control loop compensation and recommended bandwidth (1/2)
frhpz = Iout / (2 * np.pi * L * Vout) * (Vin_min / Vout) ** 2

fco1 = frhpz / 4
fco2 = fsw / 5
print("fco1 < {} kHz, fco2 < {} kHz".format(fco1 * 1e-3, fco2 * 1e-3))
fbw = np.min([fco1, fco2])
print("fbw = {} kHz".format(fbw * 1e-3))

### Output capacitors selection
Cout_min1 = (DItran / (2*np.pi*fbw * DVtran))
Cout_min2 = (Dmax * Iout_max) / (fsw * Vripple)
print("Minimum output capacitor: {} or {} uF".format(Cout_min1*1e6, Cout_min2*1e6))
Cout = input("Please input real output capacitor value Cout (uF):")
Cout = float(Cout) * 1e-6

### MOSFET selection
Igd = 2 * Qg_mos * fsw
print("MOSFET required gate current Igd: {} mA".format(Igd*1e3))

### Input capacitor

### UVLO
Ruvlo_h = ((Vuvlo_start * (1.14/1.21) - Vuvlo_stop)) / (1.8e-6 * (1-(1.14/1.21)) + 3.2e-6)
Ruvlo_l = Ruvlo_h * 1.14 / (4.3 - 1.14 + Ruvlo_h * (1.8e-6 + 3.2e-6))
print("Ruvlo_h = {} kOhms, Ruvlo_v = {} kOhms".format(Ruvlo_h * 1e-3, Ruvlo_l * 1e-3))

# Verify Rsh and Rsl values
Vout_typ = 1.22 * ((Rsh_typ / Rsl_typ) + 1)
assert(Vout_typ >= Vout_min)
assert(Vout_typ <= Vout_max)

### Control loop compensation and recommended bandwidth (2/2)
adc = (3./40) * (Vin_min / 2 * Rcs * Iout)
print("ADC = {}".format(adc))
fpmod = Iout / (2 * np.pi * Vout * Cout)
fzmod = 1. / (2 * np.pi * ESR * Cout)

Gea = 1.1e-3
Rcomp = (40 * 2 * np.pi * Cout * Rcs * Vout * fbw * (Rsh_typ + Rsl_typ)) / (Rsl_typ * Vin_min * Gea)
Ccomp = 10. / (2 * np.pi * Rcomp)
Chf1 = (Cout * ESR) / Rcomp
Chf2 = 1./ (20 * np.pi * fbw * Rcomp)


with open(outfile, "a") as myfile:
    myfile.writelines(["*Input data: \n",
                       ### User values
                    "Vin_min: {} V\n".format(Vin_min),
                    "Vin_max: {} V\n".format(Vin_max),
                    "Vout_min: {} V\n".format(Vout_min),
                    "Vout_max: {} V\n".format(Vout_max),
                    "Vin: {} V\n".format(Vin),
                    "Vout: {} V\n".format(Vout),
                    "Iout_max: {} A\n".format(Iout_max),
                    "Iout: {} A\n".format(Iout),
                    "DItran: {} A\n".format(DItran),
                    "DVtran: {} V\n".format(DVtran),
                    "Vripple: {} V\n".format(Vripple),
                    "Kind: {}\n".format(Kind),
                    "Qg_mos: {}\n".format(Qg_mos),
                    "Vuvlo_start: {} V\n".format(Vuvlo_start),
                    "Vuvlo_stop: {} V\n".format(Vuvlo_stop),
                    "Rsh_typ: {} Ohms\n".format(Rsh_typ),
                    "Rsl_typ: {} Ohms\n".format(Rsl_typ),
                    "ESR: {}\n".format(ESR),
                    "\n"
                    ])

    myfile.writelines(["\n*Resulting component values:\n",
                       "fsw: {} MHz\n".format(fsw / 1e6),
                       "Rt: {} kOhms\n".format(Rt / 1e3),
                        "L: {} uH\n".format(L * 1e6),
                        "Ilrms: {} A\n".format(Ilrms),
                        "Ilpeak: {} A\n".format(Ilpeak),
                        "Rcs: {} mOhms\n".format(Rcs * 1e3),
                        "Prcs: {} W\n".format(Prcs),
                        "fbw: {} kHz\n".format(fbw * 1e-3),
                        "Cout: {} uF\n".format(Cout * 1e6),
                        "MOS Igd: {} mA\n".format(Igd * 1e-3),
                        "Ruvlo_h: {} kOhms\n".format(Ruvlo_h * 1e-3),
                        "Ruvlo_l: {} kOhms\n".format(Ruvlo_l * 1e-3),
                        "Ccomp: {} uF\n".format(Ccomp * 1e6),
                        "Rcomp: {} Ohms\n".format(Rcomp),
                        "Chf (1st option): {} pF\n".format(Chf1 * 1e12),
                        "Chf (2nd option): {} pF\n".format(Chf2 * 1e12),
                        "\n\n"])
    
### Not mandatory : power calculations
# MOSFET
if 0:
    Rdson_ls = 4.2e-3
    Rdson_hs = 4.2e-3
    Qgd = 16e-9
    Rg = 1.2
    Vgs_th = 1.1
    Vcc = 5.5
    Coss = 680e-12
    Pcondls = Dmax * Ilrms**2 * Rdson_ls
    Psw = (fsw / 2) * (Coss * Vout**2 + Vout*(Iout/(1-Dmax)) * Qgd * Rg / (Vcc - Vgs_th))
    Pcondhs = (1-Dmax) * Ilrms**2 * Rdson_hs
