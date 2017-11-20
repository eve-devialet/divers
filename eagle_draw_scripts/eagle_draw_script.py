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

def return_smd(place, name=""): 
    cmd = "SMD 0.8128 0.4064 -40 R90 %s (%3f %3f)"%(name, place[0], place[1])
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

# Small pads
linewidth = 0.2
# Top right
size_hpad = np.array([0.862, 0.401])
place = np.array([size0[0] / 2. + 0.171, 0.792 / 2. + 0.141])
mycmd = mycmd + return_cmd(linewidth, place, size_hpad, name="PAD12")
names.append("PAD12")

# Bottom right
place = np.array([size0[0] / 2. + 0.171, - 0.792 / 2. - 0.141 - size_hpad[1]])
mycmd = mycmd + return_cmd(linewidth, place, size_hpad, name="PAD13")
names.append("PAD13")

# Bottom left
place = np.array([-size0[0] / 2. - 0.171 - size_hpad[0], - 0.792 / 2. - 0.141 - size_hpad[1]])
mycmd = mycmd + return_cmd(linewidth, place, size_hpad, name="PAD24")
names.append("PAD24")

# Top left
place = np.array([-size0[0] / 2. - 0.171 - size_hpad[0], 0.792 / 2. + 0.141])
mycmd = mycmd + return_cmd(linewidth, place, size_hpad, name="PAD1")
names.append("PAD1")

# SMD pads
# Lateral pads
size_vpad = np.array([ 0.401, 0.862])
spacing = 0.50 - size_vpad[0] # Separated by 0.50 (see spec)

for j, y in enumerate([size0[1] / 2. + 0.327, 
                       -size0[1] / 2. - 0.327 - size_vpad[1]]):
    for i in range(0, 5):
        if j == 0:
            idx = 7 + i
        elif j == 1:
            idx = 18 - i
        place = np.array([0.102 * (i + 0.5) + size_vpad[0] * i, y])
        mycmd = mycmd + return_cmd(linewidth, place, size_vpad, 
                                   name="PAD%d"%idx)
        names.append("PAD%d"%idx)
    for i in range(0, 5):
        if j == 0:
            idx = 6 - i
        elif j == 1:
            idx = 19 + i
        place = np.array([-0.102 * (i + 0.5) - size_vpad[0] * (i+1), y])
        mycmd = mycmd + return_cmd(linewidth, place, size_vpad, 
                                   name="PAD%d"%idx)
        names.append("PAD%d"%idx)
        
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
    
