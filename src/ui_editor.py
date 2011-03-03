# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_editor.ui'
#
# Created: Thu Mar  3 23:30:15 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MetatoolsEditor(object):
    def setupUi(self, MetatoolsEditor):
        MetatoolsEditor.setObjectName("MetatoolsEditor")
        MetatoolsEditor.resize(424, 337)
        self.verticalLayout = QtGui.QVBoxLayout(MetatoolsEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(MetatoolsEditor)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeView = QtGui.QTreeView(self.splitter)
        self.treeView.setObjectName("treeView")
        self.textEdit = QtGui.QTextEdit(self.splitter)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(MetatoolsEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MetatoolsEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), MetatoolsEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), MetatoolsEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(MetatoolsEditor)

    def retranslateUi(self, MetatoolsEditor):
        MetatoolsEditor.setWindowTitle(QtGui.QApplication.translate("MetatoolsEditor", "Metadata editor", None, QtGui.QApplication.UnicodeUTF8))

