# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CertifUIModel.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(686, 435)
        self.verticalLayout_7 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.deviceInfo = QtGui.QPushButton(Form)
        self.deviceInfo.setObjectName(_fromUtf8("deviceInfo"))
        self.verticalLayout_5.addWidget(self.deviceInfo)
        self.plcInfo = QtGui.QPushButton(Form)
        self.plcInfo.setObjectName(_fromUtf8("plcInfo"))
        self.verticalLayout_5.addWidget(self.plcInfo)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.wifiConnect = QtGui.QPushButton(Form)
        self.wifiConnect.setObjectName(_fromUtf8("wifiConnect"))
        self.verticalLayout_4.addWidget(self.wifiConnect)
        self.plcStart = QtGui.QPushButton(Form)
        self.plcStart.setObjectName(_fromUtf8("plcStart"))
        self.verticalLayout_4.addWidget(self.plcStart)
        self.plcStop = QtGui.QPushButton(Form)
        self.plcStop.setObjectName(_fromUtf8("plcStop"))
        self.verticalLayout_4.addWidget(self.plcStop)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.plcFlash = QtGui.QPushButton(Form)
        self.plcFlash.setObjectName(_fromUtf8("plcFlash"))
        self.verticalLayout_6.addWidget(self.plcFlash)
        self.plcErase = QtGui.QPushButton(Form)
        self.plcErase.setObjectName(_fromUtf8("plcErase"))
        self.verticalLayout_6.addWidget(self.plcErase)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_2.addWidget(self.line)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.manoAnaStart = QtGui.QPushButton(Form)
        self.manoAnaStart.setObjectName(_fromUtf8("manoAnaStart"))
        self.verticalLayout_3.addWidget(self.manoAnaStart)
        self.manoDigiStart = QtGui.QPushButton(Form)
        self.manoDigiStart.setObjectName(_fromUtf8("manoDigiStart"))
        self.verticalLayout_3.addWidget(self.manoDigiStart)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.titoHdmiStart = QtGui.QPushButton(Form)
        self.titoHdmiStart.setObjectName(_fromUtf8("titoHdmiStart"))
        self.verticalLayout_2.addWidget(self.titoHdmiStart)
        self.titoSpdifStart = QtGui.QPushButton(Form)
        self.titoSpdifStart.setObjectName(_fromUtf8("titoSpdifStart"))
        self.verticalLayout_2.addWidget(self.titoSpdifStart)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.scrollArea = QtGui.QScrollArea(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 664, 201))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.answerLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.answerLabel.sizePolicy().hasHeightForWidth())
        self.answerLabel.setSizePolicy(sizePolicy)
        self.answerLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.answerLabel.setObjectName(_fromUtf8("answerLabel"))
        self.verticalLayout.addWidget(self.answerLabel)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.deviceInfo.setText(_translate("Form", "Device info", None))
        self.plcInfo.setText(_translate("Form", "PLC info", None))
        self.wifiConnect.setText(_translate("Form", "Wifi connect", None))
        self.plcStart.setText(_translate("Form", "PLC start", None))
        self.plcStop.setText(_translate("Form", "PLC stop", None))
        self.plcFlash.setText(_translate("Form", "PLC flash", None))
        self.plcErase.setText(_translate("Form", "PLC erase", None))
        self.manoAnaStart.setText(_translate("Form", "Manolo analog audio start", None))
        self.manoDigiStart.setText(_translate("Form", "Manolo digital audio start", None))
        self.titoHdmiStart.setText(_translate("Form", "Tito HDMI audio start", None))
        self.titoSpdifStart.setText(_translate("Form", "Tito spdif audio start", None))
        self.answerLabel.setText(_translate("Form", ">", None))
