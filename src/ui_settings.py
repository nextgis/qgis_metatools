# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_settings.ui'
#
# Created: Sun Mar 20 02:43:10 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MetatoolsSettingsDialog(object):
    def setupUi(self, MetatoolsSettingsDialog):
        MetatoolsSettingsDialog.setObjectName("MetatoolsSettingsDialog")
        MetatoolsSettingsDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(MetatoolsSettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(MetatoolsSettingsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.generalTab = QtGui.QWidget()
        self.generalTab.setObjectName("generalTab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.generalTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.autoGeneratePreviewCheckBox = QtGui.QCheckBox(self.generalTab)
        self.autoGeneratePreviewCheckBox.setObjectName("autoGeneratePreviewCheckBox")
        self.verticalLayout_2.addWidget(self.autoGeneratePreviewCheckBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.tabWidget.addTab(self.generalTab, "")
        self.isoTab = QtGui.QWidget()
        self.isoTab.setObjectName("isoTab")
        self.formLayout = QtGui.QFormLayout(self.isoTab)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.defaultProfileLabel = QtGui.QLabel(self.isoTab)
        self.defaultProfileLabel.setObjectName("defaultProfileLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.defaultProfileLabel)
        self.defaultProfileComboBox = QtGui.QComboBox(self.isoTab)
        self.defaultProfileComboBox.setObjectName("defaultProfileComboBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.defaultProfileComboBox)
        self.tabWidget.addTab(self.isoTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(MetatoolsSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MetatoolsSettingsDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), MetatoolsSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), MetatoolsSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MetatoolsSettingsDialog)

    def retranslateUi(self, MetatoolsSettingsDialog):
        MetatoolsSettingsDialog.setWindowTitle(QtGui.QApplication.translate("MetatoolsSettingsDialog", "Metatools settings", None, QtGui.QApplication.UnicodeUTF8))
        self.autoGeneratePreviewCheckBox.setText(QtGui.QApplication.translate("MetatoolsSettingsDialog", "Auto generate preview", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), QtGui.QApplication.translate("MetatoolsSettingsDialog", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultProfileLabel.setText(QtGui.QApplication.translate("MetatoolsSettingsDialog", "Default profile", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.isoTab), QtGui.QApplication.translate("MetatoolsSettingsDialog", "ISO 19115", None, QtGui.QApplication.UnicodeUTF8))

