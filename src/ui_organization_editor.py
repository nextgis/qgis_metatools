# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_organization_editor.ui'
#
# Created: Mon Mar 21 15:43:20 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_OrganizationEditorDialog(object):
    def setupUi(self, OrganizationEditorDialog):
        OrganizationEditorDialog.setObjectName(_fromUtf8("OrganizationEditorDialog"))
        OrganizationEditorDialog.resize(300, 350)
        self.gridLayout = QtGui.QGridLayout(OrganizationEditorDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.orgComboBox = QtGui.QComboBox(OrganizationEditorDialog)
        self.orgComboBox.setObjectName(_fromUtf8("orgComboBox"))
        self.gridLayout.addWidget(self.orgComboBox, 0, 0, 1, 2)
        self.addButton = QtGui.QPushButton(OrganizationEditorDialog)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.gridLayout.addWidget(self.addButton, 1, 0, 1, 1)
        self.removeButton = QtGui.QPushButton(OrganizationEditorDialog)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.gridLayout.addWidget(self.removeButton, 1, 1, 1, 1)
        self.orgGroupBox = QtGui.QGroupBox(OrganizationEditorDialog)
        self.orgGroupBox.setObjectName(_fromUtf8("orgGroupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.orgGroupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.nameLineEdit = QtGui.QLineEdit(self.orgGroupBox)
        self.nameLineEdit.setObjectName(_fromUtf8("nameLineEdit"))
        self.gridLayout_3.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.nameLabel = QtGui.QLabel(self.orgGroupBox)
        self.nameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.gridLayout_3.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.descTextEdit = QtGui.QTextEdit(self.orgGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descTextEdit.sizePolicy().hasHeightForWidth())
        self.descTextEdit.setSizePolicy(sizePolicy)
        self.descTextEdit.setObjectName(_fromUtf8("descTextEdit"))
        self.gridLayout_3.addWidget(self.descTextEdit, 1, 1, 1, 1)
        self.descriptionLabel = QtGui.QLabel(self.orgGroupBox)
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.gridLayout_3.addWidget(self.descriptionLabel, 1, 0, 1, 1)
        self.orgButtonBox = QtGui.QDialogButtonBox(self.orgGroupBox)
        self.orgButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.orgButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.orgButtonBox.setObjectName(_fromUtf8("orgButtonBox"))
        self.gridLayout_3.addWidget(self.orgButtonBox, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.orgGroupBox, 2, 0, 1, 2)

        self.retranslateUi(OrganizationEditorDialog)
        QtCore.QObject.connect(self.orgButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), OrganizationEditorDialog.accept)
        QtCore.QObject.connect(self.orgButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), OrganizationEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OrganizationEditorDialog)

    def retranslateUi(self, OrganizationEditorDialog):
        OrganizationEditorDialog.setWindowTitle(QtGui.QApplication.translate("OrganizationEditorDialog", "Edit institution", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("OrganizationEditorDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("OrganizationEditorDialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.orgGroupBox.setTitle(QtGui.QApplication.translate("OrganizationEditorDialog", "Institution", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("OrganizationEditorDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtGui.QApplication.translate("OrganizationEditorDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))

