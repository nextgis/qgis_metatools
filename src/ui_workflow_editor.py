# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_workflow_editor.ui'
#
# Created: Tue Mar 29 13:29:07 2011
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
        WorkflowEditorDialog.resize(300, 350)
        WorkflowEditorDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(WorkflowEditorDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.workflowComboBox = QtGui.QComboBox(WorkflowEditorDialog)
        self.workflowComboBox.setObjectName(_fromUtf8("workflowComboBox"))
        self.gridLayout.addWidget(self.workflowComboBox, 0, 0, 1, 2)
        self.addButton = QtGui.QPushButton(WorkflowEditorDialog)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.gridLayout.addWidget(self.addButton, 1, 0, 1, 1)
        self.removeButton = QtGui.QPushButton(WorkflowEditorDialog)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.gridLayout.addWidget(self.removeButton, 1, 1, 1, 1)
        self.workflowGroupBox = QtGui.QGroupBox(WorkflowEditorDialog)
        self.workflowGroupBox.setEnabled(False)
        self.workflowGroupBox.setObjectName(_fromUtf8("workflowGroupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.workflowGroupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.nameLineEdit = QtGui.QLineEdit(self.workflowGroupBox)
        self.nameLineEdit.setObjectName(_fromUtf8("nameLineEdit"))
        self.gridLayout_3.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.nameLabel = QtGui.QLabel(self.workflowGroupBox)
        self.nameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.gridLayout_3.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.descriptionLabel = QtGui.QLabel(self.workflowGroupBox)
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.gridLayout_3.addWidget(self.descriptionLabel, 1, 0, 1, 1)
        self.descTextEdit = QtGui.QTextEdit(self.workflowGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descTextEdit.sizePolicy().hasHeightForWidth())
        self.descTextEdit.setSizePolicy(sizePolicy)
        self.descTextEdit.setObjectName(_fromUtf8("descTextEdit"))
        self.gridLayout_3.addWidget(self.descTextEdit, 1, 1, 1, 1)
        self.workflowButtonBox = QtGui.QDialogButtonBox(self.workflowGroupBox)
        self.workflowButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.workflowButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.workflowButtonBox.setObjectName(_fromUtf8("workflowButtonBox"))
        self.gridLayout_3.addWidget(self.workflowButtonBox, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.workflowGroupBox, 2, 0, 1, 2)

        self.retranslateUi(WorkflowEditorDialog)
        QtCore.QObject.connect(self.workflowButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), WorkflowEditorDialog.accept)
        QtCore.QObject.connect(self.workflowButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), WorkflowEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(WorkflowEditorDialog)

    def retranslateUi(self, WorkflowEditorDialog):
        WorkflowEditorDialog.setWindowTitle(QtGui.QApplication.translate("WorkflowEditorDialog", "Edit workflow", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("WorkflowEditorDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("WorkflowEditorDialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.workflowGroupBox.setTitle(QtGui.QApplication.translate("WorkflowEditorDialog", "Workflow", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("WorkflowEditorDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtGui.QApplication.translate("WorkflowEditorDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))

