# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 14:26:38 2016

@author: eveaporee
"""
import numpy as np

mycmd = "GRID MM;\n"
mycmd = mycmd + "CHANGE LAYER 1;\n" # Top
names = list()
place = [0, 0] # Where to place the object (x, y)
size = [20, 50] # Horizontal, vertical size
linewidth = 0.4 # Linewidth
# "polygon 0.4 (0 0) (0 50) (50 50) (50 0)"

def return_cmd(linewidth, place, size, name="mypoly"):
    x1 = place[0] + linewidth / 2.
    x2 = place[0] + size[0] - linewidth / 2.
    y1 = place[1] + linewidth / 2.
    y2 = place[1] + size[1] - linewidth / 2.
    cmd = "polygon %.3f (%.3f %.3f) (%.3f %.3f) (%.3f %.3f) (%.3f %.3f) (%.3f %.3f);\n"%(linewidth, 
          x1, y1, x2, y1, x2, y2, x1, y2, x1, y1)
    return(cmd)

def return_smd(place, name="", vertical=True): 
    size = np.array([0.8128, 0.4064])
    if not vertical:
        txt = ""
    elif vertical:
        txt = "R90"
        size = np.array([0.4064, 0.8128])
    if name != "":
        myname = "'%s'"%name
    else:
        myname = ""
    myplace = place + size/2. # Because it is centered
    cmd = "SMD 0.8128 0.4064 -40 %s %s (%3f %3f);\n"%(myname, txt, 
           myplace[0], myplace[1])
    return(cmd)
cmd = return_cmd(0.4, [0, 0], [2, 3])


linewidth = 0.4

cmd = cmd + "CHANGE LAYER 1;\n"

# Main pad
size0 = np.array([4.046, 2.163])
place0 = -size0 / 2. # Centering
mycmd = mycmd + return_cmd(linewidth, place0, size0, name="THERM")

# Side pads
margin = 0.2
# Right pad
size1 = np.array([1.032 + margin, 0.792])
place1 = np.array([size0[0] / 2. - margin, -size1[1]/2.]) # Y centering
mycmd = mycmd + return_cmd(linewidth, place1, size1, name="THERM")

# Left pad
place1 = np.array([-size0[0] / 2. - size1[0] + margin, -size1[1]/2.]) # Y centering
mycmd = mycmd + return_cmd(linewidth, place1, size1, name="THERM")

names.append("THERM")
mycmd = mycmd + return_smd(place, name="PAD25", vertical=False)

# Small pads
size_hpad = np.array([0.8128, 0.4064])
# Top right
place = np.array([size0[0] / 2. + 0.171, 0.792 / 2. + 0.141])
mycmd = mycmd + return_smd(place, name="PAD12", vertical=False)

# Bottom right
place = np.array([size0[0] / 2. + 0.171, - 0.792 / 2. - 0.141 - size_hpad[1]])
mycmd = mycmd + return_smd(place, name="PAD13", vertical=False)

# Bottom left
place = np.array([-size0[0] / 2. - 0.171 - size_hpad[0], - 0.792 / 2. - 0.141 - size_hpad[1]])
mycmd = mycmd + return_smd(place, name="PAD24", vertical=False)

# Top left
place = np.array([-size0[0] / 2. - 0.171 - size_hpad[0], 0.792 / 2. + 0.141])
mycmd = mycmd + return_smd(place, name="PAD1", vertical=False)

# SMD pads
# Lateral pads
size_vpad = np.array([0.4064, 0.8128])
spacing = 0.5 - size_vpad[0]

for j, y in enumerate([size0[1] / 2. + 0.327, 
                       -size0[1] / 2. - 0.327 - size_vpad[1]]):
    for i in range(0, 5):
        if j == 0:
            idx = 7 + i
        elif j == 1:
            idx = 18 - i
        place = np.array([0.102 * (i + 0.5) + size_vpad[0] * i, y])
        mycmd = mycmd + return_smd(place, 
                                   name="PAD%d"%idx)
    for i in range(0, 5):
        if j == 0:
            idx = 6 - i
        elif j == 1:
            idx = 19 + i
        place = np.array([-0.102 * (i + 0.5) - size_vpad[0] * (i+1), y])
        mycmd = mycmd + return_smd(place, 
                                   name="PAD%d"%idx)
        
# RUN cmd-draw-polygon-contours-as-wire SIGNALNAME [FILLING] [Layernumber]
for name in names:
    mycmd = mycmd + "RUN cmd-draw-polygon-contours-as-wire %s\n"%name
mycmd = mycmd + "CHANGE LAYER 39;\n" # 39 Keepout
mycmd = mycmd + "RECT (-2.825 -1.825) (2.825 1.825);\n"

#21 tPlace placer for device
mycmd = mycmd + "CHANGE LAYER 21;\n"
mycmd = mycmd + "WIRE (-2.825 -1.825) (-2.825 1.825);\n"
#mycmd = mycmd + "CHANGE LAYER 21;\n" 
mycmd = mycmd + "WIRE (-2.825 1.825) (2.825 1.825);\n"
#mycmd = mycmd + "CHANGE LAYER 21;\n" 
mycmd = mycmd + "WIRE (2.825 1.825) (2.825 -1.825);\n"
#mycmd = mycmd + "CHANGE LAYER 21;\n" 
mycmd = mycmd + "WIRE (2.825 -1.825) (-2.825 -1.825);\n"
#mycmd = mycmd + "CHANGE LAYER 21;\n"
with open("myscript.scr", "w") as myfile:
    myfile.write(mycmd)
    
