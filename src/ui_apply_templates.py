# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_apply_templates.ui'
#
# Created: Wed Mar 30 16:35:31 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ApplyTemplatesDialog(object):
    def setupUi(self, ApplyTemplatesDialog):
        ApplyTemplatesDialog.setObjectName(_fromUtf8("ApplyTemplatesDialog"))
        ApplyTemplatesDialog.resize(521, 263)
        self.gridLayout = QtGui.QGridLayout(ApplyTemplatesDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.chkExternalFiles = QtGui.QCheckBox(ApplyTemplatesDialog)
        self.chkExternalFiles.setObjectName(_fromUtf8("chkExternalFiles"))
        self.horizontalLayout.addWidget(self.chkExternalFiles)
        self.btnSelectDataFiles = QtGui.QPushButton(ApplyTemplatesDialog)
        self.btnSelectDataFiles.setEnabled(False)
        self.btnSelectDataFiles.setObjectName(_fromUtf8("btnSelectDataFiles"))
        self.horizontalLayout.addWidget(self.btnSelectDataFiles)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.lstLayers = QtGui.QListWidget(ApplyTemplatesDialog)
        self.lstLayers.setObjectName(_fromUtf8("lstLayers"))
        self.gridLayout.addWidget(self.lstLayers, 1, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(ApplyTemplatesDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.cmbOrganization = QtGui.QComboBox(self.groupBox)
        self.cmbOrganization.setMinimumSize(QtCore.QSize(100, 0))
        self.cmbOrganization.setObjectName(_fromUtf8("cmbOrganization"))
        self.gridLayout_2.addWidget(self.cmbOrganization, 0, 1, 1, 1)
        self.cmbLicense = QtGui.QComboBox(self.groupBox)
        self.cmbLicense.setMinimumSize(QtCore.QSize(100, 0))
        self.cmbLicense.setObjectName(_fromUtf8("cmbLicense"))
        self.gridLayout_2.addWidget(self.cmbLicense, 1, 1, 1, 1)
        self.cmbWorkflow = QtGui.QComboBox(self.groupBox)
        self.cmbWorkflow.setMinimumSize(QtCore.QSize(100, 0))
        self.cmbWorkflow.setObjectName(_fromUtf8("cmbWorkflow"))
        self.gridLayout_2.addWidget(self.cmbWorkflow, 2, 1, 1, 1)
        self.btnManageOrgs = QtGui.QPushButton(self.groupBox)
        self.btnManageOrgs.setObjectName(_fromUtf8("btnManageOrgs"))
        self.gridLayout_2.addWidget(self.btnManageOrgs, 0, 2, 1, 1)
        self.btnManageLicenses = QtGui.QPushButton(self.groupBox)
        self.btnManageLicenses.setObjectName(_fromUtf8("btnManageLicenses"))
        self.gridLayout_2.addWidget(self.btnManageLicenses, 1, 2, 1, 1)
        self.btnManageWorkflows = QtGui.QPushButton(self.groupBox)
        self.btnManageWorkflows.setObjectName(_fromUtf8("btnManageWorkflows"))
        self.gridLayout_2.addWidget(self.btnManageWorkflows, 2, 2, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.leLogFile = QtGui.QLineEdit(self.groupBox)
        self.leLogFile.setReadOnly(True)
        self.leLogFile.setObjectName(_fromUtf8("leLogFile"))
        self.gridLayout_2.addWidget(self.leLogFile, 3, 1, 1, 1)
        self.btnSelectLogFile = QtGui.QPushButton(self.groupBox)
        self.btnSelectLogFile.setObjectName(_fromUtf8("btnSelectLogFile"))
        self.gridLayout_2.addWidget(self.btnSelectLogFile, 3, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ApplyTemplatesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(ApplyTemplatesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ApplyTemplatesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ApplyTemplatesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ApplyTemplatesDialog)

    def retranslateUi(self, ApplyTemplatesDialog):
        ApplyTemplatesDialog.setWindowTitle(QtGui.QApplication.translate("ApplyTemplatesDialog", "Apply templates", None, QtGui.QApplication.UnicodeUTF8))
        self.chkExternalFiles.setText(QtGui.QApplication.translate("ApplyTemplatesDialog", "Select files from disk", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectDataFiles.setText(QtGui.QApplication.translate("ApplyTemplatesDialog", "Select files...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ApplyTemplatesDialog", "Templates", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ApplyTemplatesDialog", "Institution", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ApplyTemplatesDialog", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ApplyTemplatesDialog", "Workflow", None, QtGui.QApplication.UnicodeUTF8))
        self.btnManageOrgs.setText(QtGui.QApplication.translate("ApplyTemplatesDialog", "Manage", None, QtGui.QApplication.UnicodeUTF8))
        self.btnManageLicenses.setText(QtGui.QApplication.translate("ApplyTemplatesDialog", "Manage", None, QtGui.QApplication.UnicodeUTF8))
        self.btnManageWorkflows.setText(QtGui.QApplication.translate("ApplyTemplatesDialog", "Manage", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ApplyTemplatesDialog", "Log file", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectLogFile.setText(QtGui.QApplication.translate("ApplyTemplatesDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))

