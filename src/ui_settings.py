# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_settings.ui'
#
# Created: Fri Apr 01 16:36:11 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MetatoolsSettingsDialog(object):
    def setupUi(self, MetatoolsSettingsDialog):
        MetatoolsSettingsDialog.setObjectName(_fromUtf8("MetatoolsSettingsDialog"))
        MetatoolsSettingsDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(MetatoolsSettingsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(MetatoolsSettingsDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.generalTab = QtGui.QWidget()
        self.generalTab.setObjectName(_fromUtf8("generalTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.generalTab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.generalTab)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.leFilterFileName = QtGui.QLineEdit(self.groupBox)
        self.leFilterFileName.setObjectName(_fromUtf8("leFilterFileName"))
        self.horizontalLayout.addWidget(self.leFilterFileName)
        self.btnSelectFilter = QtGui.QPushButton(self.groupBox)
        self.btnSelectFilter.setObjectName(_fromUtf8("btnSelectFilter"))
        self.horizontalLayout.addWidget(self.btnSelectFilter)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.tabWidget.addTab(self.generalTab, _fromUtf8(""))
        self.isoTab = QtGui.QWidget()
        self.isoTab.setObjectName(_fromUtf8("isoTab"))
        self.formLayout = QtGui.QFormLayout(self.isoTab)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.defaultProfileLabel = QtGui.QLabel(self.isoTab)
        self.defaultProfileLabel.setObjectName(_fromUtf8("defaultProfileLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.defaultProfileLabel)
        self.defaultProfileComboBox = QtGui.QComboBox(self.isoTab)
        self.defaultProfileComboBox.setObjectName(_fromUtf8("defaultProfileComboBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.defaultProfileComboBox)
        self.tabWidget.addTab(self.isoTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(MetatoolsSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MetatoolsSettingsDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MetatoolsSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MetatoolsSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MetatoolsSettingsDialog)

    def retranslateUi(self, MetatoolsSettingsDialog):
        MetatoolsSettingsDialog.setWindowTitle(QtGui.QApplication.translate("MetatoolsSettingsDialog", "Metatools settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MetatoolsSettingsDialog", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MetatoolsSettingsDialog", "Filter file", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectFilter.setText(QtGui.QApplication.translate("MetatoolsSettingsDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), QtGui.QApplication.translate("MetatoolsSettingsDialog", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultProfileLabel.setText(QtGui.QApplication.translate("MetatoolsSettingsDialog", "Default profile", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.isoTab), QtGui.QApplication.translate("MetatoolsSettingsDialog", "ISO 19115", None, QtGui.QApplication.UnicodeUTF8))

