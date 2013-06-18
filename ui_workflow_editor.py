# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_workflow_editor.ui'
#
# Created: Wed Mar 30 16:36:35 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_WorkflowEditorDialog(object):
    def setupUi(self, WorkflowEditorDialog):
        WorkflowEditorDialog.setObjectName(_fromUtf8("WorkflowEditorDialog"))
        WorkflowEditorDialog.resize(352, 370)
        self.verticalLayout = QtGui.QVBoxLayout(WorkflowEditorDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cmbWorkflow = QtGui.QComboBox(WorkflowEditorDialog)
        self.cmbWorkflow.setObjectName(_fromUtf8("cmbWorkflow"))
        self.verticalLayout.addWidget(self.cmbWorkflow)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnNew = QtGui.QPushButton(WorkflowEditorDialog)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.horizontalLayout.addWidget(self.btnNew)
        self.btnRemove = QtGui.QPushButton(WorkflowEditorDialog)
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.horizontalLayout.addWidget(self.btnRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(WorkflowEditorDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.leName = QtGui.QLineEdit(self.groupBox)
        self.leName.setObjectName(_fromUtf8("leName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.leName)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.textDescription = QtGui.QTextEdit(self.groupBox)
        self.textDescription.setObjectName(_fromUtf8("textDescription"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.textDescription)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(WorkflowEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(WorkflowEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), WorkflowEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), WorkflowEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(WorkflowEditorDialog)

    def retranslateUi(self, WorkflowEditorDialog):
        WorkflowEditorDialog.setWindowTitle(QtGui.QApplication.translate("WorkflowEditorDialog", "Manage workflows", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNew.setText(QtGui.QApplication.translate("WorkflowEditorDialog", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRemove.setText(QtGui.QApplication.translate("WorkflowEditorDialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("WorkflowEditorDialog", "Workflow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("WorkflowEditorDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("WorkflowEditorDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))

