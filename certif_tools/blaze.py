#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 11:04:12 2018

@author: eve
"""
import os, sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import gui.MainWindowUI as mwui

if __name__ == "__main__":
    myApp = QtGui.QApplication(sys.argv)
    win = mwui.MyMainWindow()
    win.show()
    sys.exit(myApp.exec_())
    
