# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/modules/TaskRunner/analysisModules/Photostim/PhotostimTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(310, 405)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 1)
        self.clampStopSpin = QtWidgets.QLabel(Form)
        self.clampStopSpin.setObjectName("clampStopSpin")
        self.gridLayout.addWidget(self.clampStopSpin, 8, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 9, 0, 1, 1)
        self.deleteBtn = QtWidgets.QPushButton(Form)
        self.deleteBtn.setObjectName("deleteBtn")
        self.gridLayout.addWidget(self.deleteBtn, 13, 0, 1, 1)
        self.clampBaseStopSpin = SpinBox(Form)
        self.clampBaseStopSpin.setMaximum(100000.0)
        self.clampBaseStopSpin.setProperty("value", 0.09)
        self.clampBaseStopSpin.setObjectName("clampBaseStopSpin")
        self.gridLayout.addWidget(self.clampBaseStopSpin, 7, 2, 1, 1)
        self.recomputeBtn = QtWidgets.QPushButton(Form)
        self.recomputeBtn.setObjectName("recomputeBtn")
        self.gridLayout.addWidget(self.recomputeBtn, 13, 2, 1, 1)
        self.spikeThresholdSpin = SpinBox(Form)
        self.spikeThresholdSpin.setProperty("value", 0.05)
        self.spikeThresholdSpin.setObjectName("spikeThresholdSpin")
        self.gridLayout.addWidget(self.spikeThresholdSpin, 9, 1, 1, 1)
        self.clampBaseStartSpin = SpinBox(Form)
        self.clampBaseStartSpin.setMaximum(100000.0)
        self.clampBaseStartSpin.setObjectName("clampBaseStartSpin")
        self.gridLayout.addWidget(self.clampBaseStartSpin, 7, 1, 1, 1)
        self.clampTestStartSpin = SpinBox(Form)
        self.clampTestStartSpin.setMaximum(100000.0)
        self.clampTestStartSpin.setProperty("value", 0.1)
        self.clampTestStartSpin.setObjectName("clampTestStartSpin")
        self.gridLayout.addWidget(self.clampTestStartSpin, 8, 1, 1, 1)
        self.clampDevCombo = InterfaceCombo(Form)
        self.clampDevCombo.setObjectName("clampDevCombo")
        self.gridLayout.addWidget(self.clampDevCombo, 4, 1, 1, 2)
        self.scannerDevCombo = InterfaceCombo(Form)
        self.scannerDevCombo.setObjectName("scannerDevCombo")
        self.gridLayout.addWidget(self.scannerDevCombo, 3, 1, 1, 2)
        self.cameraModCombo = InterfaceCombo(Form)
        self.cameraModCombo.setObjectName("cameraModCombo")
        self.gridLayout.addWidget(self.cameraModCombo, 1, 1, 1, 2)
        self.enabledCheck = QtWidgets.QCheckBox(Form)
        self.enabledCheck.setObjectName("enabledCheck")
        self.gridLayout.addWidget(self.enabledCheck, 0, 1, 1, 2)
        self.clampTestStopSpin = SpinBox(Form)
        self.clampTestStopSpin.setMaximum(100000.0)
        self.clampTestStopSpin.setProperty("value", 0.12)
        self.clampTestStopSpin.setObjectName("clampTestStopSpin")
        self.gridLayout.addWidget(self.clampTestStopSpin, 8, 2, 1, 1)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(Qt.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.colorMapper = ColorMapWidget(self.groupBox)
        self.colorMapper.setMinimumSize(Qt.QSize(0, 70))
        self.colorMapper.setObjectName("colorMapper")
        self.gridLayout_2.addWidget(self.colorMapper, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.taskList = QtWidgets.QListWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taskList.sizePolicy().hasHeightForWidth())
        self.taskList.setSizePolicy(sizePolicy)
        self.taskList.setObjectName("taskList")
        self.gridLayout_3.addWidget(self.taskList, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.splitter, 10, 0, 1, 3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.spikeThresholdAbsRadio = QtWidgets.QRadioButton(Form)
        self.spikeThresholdAbsRadio.setObjectName("spikeThresholdAbsRadio")
        self.horizontalLayout_2.addWidget(self.spikeThresholdAbsRadio)
        self.spikeThresholdRelRadio = QtWidgets.QRadioButton(Form)
        self.spikeThresholdRelRadio.setChecked(True)
        self.spikeThresholdRelRadio.setObjectName("spikeThresholdRelRadio")
        self.horizontalLayout_2.addWidget(self.spikeThresholdRelRadio)
        self.gridLayout.addLayout(self.horizontalLayout_2, 9, 2, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        Qt.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = Qt.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Camera Module:"))
        self.label_3.setText(_translate("Form", "Clamp Device:"))
        self.label_4.setText(_translate("Form", "Scanner Device:"))
        self.label_5.setText(_translate("Form", "Clamp Baseline:"))
        self.clampStopSpin.setText(_translate("Form", "Clamp Test:"))
        self.label_6.setText(_translate("Form", "Spike Threshold:"))
        self.deleteBtn.setText(_translate("Form", "Delete"))
        self.recomputeBtn.setText(_translate("Form", "Recompute"))
        self.enabledCheck.setText(_translate("Form", "Enabled"))
        self.groupBox.setTitle(_translate("Form", "Color Map"))
        self.groupBox_2.setTitle(_translate("Form", "Recordings"))
        self.spikeThresholdAbsRadio.setText(_translate("Form", "Abs."))
        self.spikeThresholdRelRadio.setText(_translate("Form", "Rel."))

from acq4.pyqtgraph.widgets.ColorMapWidget import ColorMapWidget
from acq4.pyqtgraph.widgets.SpinBox import SpinBox
from acq4.util.InterfaceCombo import InterfaceCombo
