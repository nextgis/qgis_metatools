# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_settings.ui'
#
# Created: Wed Mar 16 17:35:28 2011
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
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.autoGeneratePreviewCheckBox = QtGui.QCheckBox(self.tab)
        self.autoGeneratePreviewCheckBox.setObjectName(_fromUtf8("autoGeneratePreviewCheckBox"))
        self.verticalLayout_2.addWidget(self.autoGeneratePreviewCheckBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
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
        self.autoGeneratePreviewCheckBox.setText(QtGui.QApplication.translate("MetatoolsSettingsDialog", "Auto generate preview", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MetatoolsSettingsDialog", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MetatoolsSettingsDialog", "ISO 19139", None, QtGui.QApplication.UnicodeUTF8))

