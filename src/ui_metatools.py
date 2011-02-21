# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_metatools.ui'
#
# Created: Mon Feb 21 11:59:51 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Metatools(object):
    def setupUi(self, Metatools):
        Metatools.setObjectName(_fromUtf8("Metatools"))
        Metatools.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Metatools)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(Metatools)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Metatools.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Metatools.reject)
        QtCore.QMetaObject.connectSlotsByName(Metatools)

    def retranslateUi(self, Metatools):
        Metatools.setWindowTitle(QtGui.QApplication.translate("Metatools", "Metatools", None, QtGui.QApplication.UnicodeUTF8))

