# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindowUIModel.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(791, 571)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setSizeIncrement(QtCore.QSize(1, 1))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setAnimated(False)
        MainWindow.setDocumentMode(True)
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QStackedWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 791, 27))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionLoad_File = QtGui.QAction(MainWindow)
        self.actionLoad_File.setObjectName(_fromUtf8("actionLoad_File"))
        self.actionSave_Desc = QtGui.QAction(MainWindow)
        self.actionSave_Desc.setObjectName(_fromUtf8("actionSave_Desc"))
        self.actionOpen_Desc = QtGui.QAction(MainWindow)
        self.actionOpen_Desc.setObjectName(_fromUtf8("actionOpen_Desc"))
        self.actionNew_Arrayspeaker_Tab = QtGui.QAction(MainWindow)
        self.actionNew_Arrayspeaker_Tab.setObjectName(_fromUtf8("actionNew_Arrayspeaker_Tab"))
        self.actionOpen_HI_and_LO_P3D = QtGui.QAction(MainWindow)
        self.actionOpen_HI_and_LO_P3D.setObjectName(_fromUtf8("actionOpen_HI_and_LO_P3D"))
        self.actionSave_P3D_As_Csv = QtGui.QAction(MainWindow)
        self.actionSave_P3D_As_Csv.setObjectName(_fromUtf8("actionSave_P3D_As_Csv"))
        self.actionOpen_P3D = QtGui.QAction(MainWindow)
        self.actionOpen_P3D.setObjectName(_fromUtf8("actionOpen_P3D"))
        self.actionSave_File = QtGui.QAction(MainWindow)
        self.actionSave_File.setObjectName(_fromUtf8("actionSave_File"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Blaze.py", None))
        self.actionLoad_File.setText(_translate("MainWindow", "Load Data File", None))
        self.actionLoad_File.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionSave_Desc.setText(_translate("MainWindow", "Save Array Description", None))
        self.actionOpen_Desc.setText(_translate("MainWindow", "Open Array Description", None))
        self.actionNew_Arrayspeaker_Tab.setText(_translate("MainWindow", "New Arrayspeaker Tab", None))
        self.actionOpen_HI_and_LO_P3D.setText(_translate("MainWindow", "Open HI and LO P3D", None))
        self.actionOpen_HI_and_LO_P3D.setStatusTip(_translate("MainWindow", "Import 2 P3D files, one with values before 1000 Hz (low) and one after 1000 Hz (high)", None))
        self.actionSave_P3D_As_Csv.setText(_translate("MainWindow", "Save P3D As Csv", None))
        self.actionSave_P3D_As_Csv.setStatusTip(_translate("MainWindow", "Export as CSV files for GLL creation.", None))
        self.actionSave_P3D_As_Csv.setShortcut(_translate("MainWindow", "Ctrl+E", None))
        self.actionOpen_P3D.setText(_translate("MainWindow", "Open P3D", None))
        self.actionOpen_P3D.setStatusTip(_translate("MainWindow", "Imports a single P3D file in the viewer.", None))
        self.actionSave_File.setText(_translate("MainWindow", "Save Current Data", None))
        self.actionSave_File.setShortcut(_translate("MainWindow", "Ctrl+S", None))

