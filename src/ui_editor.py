# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_editor.ui'
#
# Created: Mon Apr 11 00:42:27 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MetatoolsEditor(object):
    def setupUi(self, MetatoolsEditor):
        MetatoolsEditor.setObjectName(_fromUtf8("MetatoolsEditor"))
        MetatoolsEditor.resize(800, 600)
        self.verticalLayout = QtGui.QVBoxLayout(MetatoolsEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(MetatoolsEditor)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.treeFull = QtGui.QTreeView(self.tab)
        self.treeFull.setObjectName(_fromUtf8("treeFull"))
        self.verticalLayout_2.addWidget(self.treeFull)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.tbwFiltered = QtGui.QTableWidget(self.tab_2)
        self.tbwFiltered.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tbwFiltered.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tbwFiltered.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tbwFiltered.setShowGrid(True)
        self.tbwFiltered.setGridStyle(QtCore.Qt.SolidLine)
        self.tbwFiltered.setCornerButtonEnabled(True)
        self.tbwFiltered.setRowCount(0)
        self.tbwFiltered.setColumnCount(2)
        self.tbwFiltered.setObjectName(_fromUtf8("tbwFiltered"))
        self.tbwFiltered.setColumnCount(2)
        self.tbwFiltered.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tbwFiltered.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tbwFiltered.setHorizontalHeaderItem(1, item)
        self.tbwFiltered.horizontalHeader().setVisible(False)
        self.tbwFiltered.horizontalHeader().setStretchLastSection(True)
        self.tbwFiltered.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.tbwFiltered)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.groupBox = QtGui.QGroupBox(self.splitter)
        self.groupBox.setEnabled(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.lblNodePath = QtGui.QLabel(self.groupBox)
        self.lblNodePath.setWordWrap(True)
        self.lblNodePath.setObjectName(_fromUtf8("lblNodePath"))
        self.verticalLayout_4.addWidget(self.lblNodePath)
        self.textValue = QtGui.QTextEdit(self.groupBox)
        self.textValue.setObjectName(_fromUtf8("textValue"))
        self.verticalLayout_4.addWidget(self.textValue)
        self.editorButtonBox = QtGui.QDialogButtonBox(self.groupBox)
        self.editorButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Discard)
        self.editorButtonBox.setObjectName(_fromUtf8("editorButtonBox"))
        self.verticalLayout_4.addWidget(self.editorButtonBox)
        self.verticalLayout.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(MetatoolsEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MetatoolsEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MetatoolsEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MetatoolsEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(MetatoolsEditor)

    def retranslateUi(self, MetatoolsEditor):
        MetatoolsEditor.setWindowTitle(QtGui.QApplication.translate("MetatoolsEditor", "Metadata editor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MetatoolsEditor", "Full view", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MetatoolsEditor", "To set filtered view please check sample.txt in the filter directory for the filtering format and point to it at the plugin settings page.", None, QtGui.QApplication.UnicodeUTF8))
        self.tbwFiltered.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MetatoolsEditor", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.tbwFiltered.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MetatoolsEditor", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MetatoolsEditor", "Filtered view", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MetatoolsEditor", "Edit value", None, QtGui.QApplication.UnicodeUTF8))
        self.lblNodePath.setText(QtGui.QApplication.translate("MetatoolsEditor", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

