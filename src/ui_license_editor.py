# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_license_editor.ui'
#
# Created: Sun Mar 20 03:43:07 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LicenseEditorDialog(object):
    def setupUi(self, LicenseEditorDialog):
        LicenseEditorDialog.setObjectName("LicenseEditorDialog")
        LicenseEditorDialog.setWindowModality(QtCore.Qt.NonModal)
        LicenseEditorDialog.resize(300, 350)
        LicenseEditorDialog.setSizeGripEnabled(True)
        LicenseEditorDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(LicenseEditorDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.licenseComboBox = QtGui.QComboBox(LicenseEditorDialog)
        self.licenseComboBox.setObjectName("licenseComboBox")
        self.gridLayout.addWidget(self.licenseComboBox, 0, 0, 1, 2)
        self.addButton = QtGui.QPushButton(LicenseEditorDialog)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 1, 0, 1, 1)
        self.removeButton = QtGui.QPushButton(LicenseEditorDialog)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 1, 1, 1, 1)
        self.licenseGroupBox = QtGui.QGroupBox(LicenseEditorDialog)
        self.licenseGroupBox.setEnabled(False)
        self.licenseGroupBox.setObjectName("licenseGroupBox")
        self.gridLayout_3 = QtGui.QGridLayout(self.licenseGroupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.nameLineEdit = QtGui.QLineEdit(self.licenseGroupBox)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.gridLayout_3.addWidget(self.nameLineEdit, 1, 1, 1, 1)
        self.nameLabel = QtGui.QLabel(self.licenseGroupBox)
        self.nameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout_3.addWidget(self.nameLabel, 1, 0, 1, 1)
        self.versionLabel = QtGui.QLabel(self.licenseGroupBox)
        self.versionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.versionLabel.setObjectName("versionLabel")
        self.gridLayout_3.addWidget(self.versionLabel, 2, 0, 1, 1)
        self.versionLineEdit = QtGui.QLineEdit(self.licenseGroupBox)
        self.versionLineEdit.setObjectName("versionLineEdit")
        self.gridLayout_3.addWidget(self.versionLineEdit, 2, 1, 1, 1)
        self.descriptionLabel = QtGui.QLabel(self.licenseGroupBox)
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.gridLayout_3.addWidget(self.descriptionLabel, 3, 0, 1, 1)
        self.descTextEdit = QtGui.QTextEdit(self.licenseGroupBox)
        self.descTextEdit.setObjectName("descTextEdit")
        self.gridLayout_3.addWidget(self.descTextEdit, 3, 1, 1, 1)
        self.licenseButtonBox = QtGui.QDialogButtonBox(self.licenseGroupBox)
        self.licenseButtonBox.setEnabled(False)
        self.licenseButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.licenseButtonBox.setObjectName("licenseButtonBox")
        self.gridLayout_3.addWidget(self.licenseButtonBox, 4, 0, 1, 2)
        self.gridLayout.addWidget(self.licenseGroupBox, 2, 0, 1, 2)

        self.retranslateUi(LicenseEditorDialog)
        QtCore.QMetaObject.connectSlotsByName(LicenseEditorDialog)

    def retranslateUi(self, LicenseEditorDialog):
        LicenseEditorDialog.setWindowTitle(QtGui.QApplication.translate("LicenseEditorDialog", "Edit license", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("LicenseEditorDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("LicenseEditorDialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.licenseGroupBox.setTitle(QtGui.QApplication.translate("LicenseEditorDialog", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("LicenseEditorDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.versionLabel.setText(QtGui.QApplication.translate("LicenseEditorDialog", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtGui.QApplication.translate("LicenseEditorDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))

