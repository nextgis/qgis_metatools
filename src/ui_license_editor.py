# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_license_editor.ui'
#
# Created: Wed Mar 30 16:35:50 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LicenseEditorDialog(object):
    def setupUi(self, LicenseEditorDialog):
        LicenseEditorDialog.setObjectName(_fromUtf8("LicenseEditorDialog"))
        LicenseEditorDialog.resize(352, 370)
        self.verticalLayout = QtGui.QVBoxLayout(LicenseEditorDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cmbLicense = QtGui.QComboBox(LicenseEditorDialog)
        self.cmbLicense.setObjectName(_fromUtf8("cmbLicense"))
        self.verticalLayout.addWidget(self.cmbLicense)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnNew = QtGui.QPushButton(LicenseEditorDialog)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.horizontalLayout.addWidget(self.btnNew)
        self.btnRemove = QtGui.QPushButton(LicenseEditorDialog)
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.horizontalLayout.addWidget(self.btnRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(LicenseEditorDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.leName = QtGui.QLineEdit(self.groupBox)
        self.leName.setObjectName(_fromUtf8("leName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.leName)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.leVersion = QtGui.QLineEdit(self.groupBox)
        self.leVersion.setObjectName(_fromUtf8("leVersion"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.leVersion)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.textDescription = QtGui.QTextEdit(self.groupBox)
        self.textDescription.setObjectName(_fromUtf8("textDescription"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.textDescription)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(LicenseEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(LicenseEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LicenseEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LicenseEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LicenseEditorDialog)

    def retranslateUi(self, LicenseEditorDialog):
        LicenseEditorDialog.setWindowTitle(QtGui.QApplication.translate("LicenseEditorDialog", "Manage licenses", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNew.setText(QtGui.QApplication.translate("LicenseEditorDialog", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRemove.setText(QtGui.QApplication.translate("LicenseEditorDialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("LicenseEditorDialog", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LicenseEditorDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LicenseEditorDialog", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("LicenseEditorDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))

