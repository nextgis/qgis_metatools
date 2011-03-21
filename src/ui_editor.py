# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_editor.ui'
#
# Created: Sun Mar 20 02:44:29 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MetatoolsEditor(object):
    def setupUi(self, MetatoolsEditor):
        MetatoolsEditor.setObjectName("MetatoolsEditor")
        MetatoolsEditor.resize(1280, 800)
        MetatoolsEditor.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(MetatoolsEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(MetatoolsEditor)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(5)
        self.splitter.setObjectName("splitter")
        self.treeView = QtGui.QTreeView(self.splitter)
        self.treeView.setAnimated(True)
        self.treeView.setObjectName("treeView")
        self.editorGroupBox = QtGui.QGroupBox(self.splitter)
        self.editorGroupBox.setEnabled(False)
        self.editorGroupBox.setObjectName("editorGroupBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.editorGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.nodePathLabel = QtGui.QLabel(self.editorGroupBox)
        self.nodePathLabel.setText("")
        self.nodePathLabel.setWordWrap(True)
        self.nodePathLabel.setObjectName("nodePathLabel")
        self.verticalLayout_2.addWidget(self.nodePathLabel)
        self.valueTextEdit = QtGui.QTextEdit(self.editorGroupBox)
        self.valueTextEdit.setObjectName("valueTextEdit")
        self.verticalLayout_2.addWidget(self.valueTextEdit)
        self.valueButtonBox = QtGui.QDialogButtonBox(self.editorGroupBox)
        self.valueButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Discard)
        self.valueButtonBox.setObjectName("valueButtonBox")
        self.verticalLayout_2.addWidget(self.valueButtonBox)
        self.verticalLayout.addWidget(self.splitter)
        self.mainButtonBox = QtGui.QDialogButtonBox(MetatoolsEditor)
        self.mainButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.mainButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.mainButtonBox.setObjectName("mainButtonBox")
        self.verticalLayout.addWidget(self.mainButtonBox)

        self.retranslateUi(MetatoolsEditor)
        QtCore.QMetaObject.connectSlotsByName(MetatoolsEditor)

    def retranslateUi(self, MetatoolsEditor):
        MetatoolsEditor.setWindowTitle(QtGui.QApplication.translate("MetatoolsEditor", "Metadata editor", None, QtGui.QApplication.UnicodeUTF8))
        self.editorGroupBox.setTitle(QtGui.QApplication.translate("MetatoolsEditor", "Edit value", None, QtGui.QApplication.UnicodeUTF8))

