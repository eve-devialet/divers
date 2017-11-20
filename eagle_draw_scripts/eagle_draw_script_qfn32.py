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
    size = np.array([0.4064, 0.2032])
    if not vertical:
        txt = ""
    elif vertical:
        txt = "R90"
        size = np.array([0.2032, 0.4064])
    if name != "":
        myname = "'%s'"%name
    else:
        myname = ""
    myplace = place + size/2. # Because it is centered
    cmd = "SMD 0.4064 0.2032 -40 %s %s (%3f %3f);\n"%(myname, txt, 
           myplace[0], myplace[1])
    return(cmd)
cmd = return_cmd(0.4, [0, 0], [2, 3])


linewidth = 0.4

cmd = cmd + "CHANGE LAYER 1;\n"


# Small pads 0.4064 x 0.2032

size_vpad = np.array([0.2032, 0.4064])
size_hpad = np.array([0.4064, 0.2032])
spacing = 0.4 - size_vpad[0]
topbottom = 3.8
leftright = 3.8

# Left and right
for j, x in enumerate([-leftright / 2 - size_vpad[1] / 2, 
                       leftright / 2 - size_vpad[1] / 2]):
    for i in range(0, 4):
        if j == 0:
            idx = 4 - i
        elif j == 1:
            idx = 21 + i
        place = np.array([x, spacing * (0.5 + i) + i * size_vpad[0]])
        mycmd = mycmd + return_smd(place, 
                                   name="%d"%idx,
                                   vertical=False)
    for i in range(0, 4):
        if j == 0:
            idx = 5 + i
        elif j == 1:
            idx = 20 - i
        place = np.array([x, -spacing * (i + 0.5) - size_vpad[0] * (i+1)])
        mycmd = mycmd + return_smd(place, 
                                   name="%d"%idx,
                                   vertical=False)



# SMD pads
# Top and bottom
size_hpad = np.array([0.8128, 0.4064])
topbottom = 3.8
for j, y in enumerate([-topbottom / 2 - size_vpad[1] / 2, 
                       topbottom / 2 - size_vpad[1] / 2]):
    for i in range(0, 4):
        if j == 0:
            idx = 13 + i
        elif j == 1:
            idx = 28 - i
        place = np.array([spacing * (0.5 + i) + i * size_vpad[0], y])
        mycmd = mycmd + return_smd(place, 
                                   name="%d"%idx)
    for i in range(0, 4):
        if j == 0:
            idx = 12 - i
        elif j == 1:
            idx = 29 + i
        place = np.array([-spacing * (i + 0.5) - size_vpad[0] * (i+1), y])
        mycmd = mycmd + return_smd(place, 
                                   name="%d"%idx)
        
with open("myscript.scr", "w") as myfile:
    myfile.write(mycmd)
    
