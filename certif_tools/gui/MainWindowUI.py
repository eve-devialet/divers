# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 11:03:14 2014

@author: eredero
"""

import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_DIR)
import CertifUI as cui
import MainWindowUIModel as UIModel

from PyQt4 import QtCore
from PyQt4 import QtGui
import logging

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(my_string):
        '''
        Something useful for Qt
        '''
        return my_string

logger = logging.getLogger(__name__)

class MyMainWindow(QtGui.QMainWindow, UIModel.Ui_MainWindow):
    '''
    Creates the main window starting from the
    SpeakerPlotUIModel generated by pyuic4
    '''
    def __init__(self):
        '''
        Creates the window

        poll_thread, status_thread, log_thread : The threads allowing
        to access and retrieve logs from the device.

        to_stop : A list of threads with "stop" methods to stop them.
        Allows the main windows to kill all threads, even non-standard ones.
        '''
        QtGui.QMainWindow.__init__(self)
        UIModel.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Adds the custom tab
        self.widget = cui.MyWidget(parent=self)
        self.tabWidget.addWidget(self.widget)

  
    def closeEvent(self, event):
        '''
        Stops what needs to be stopped before closing windows
        '''
        pass