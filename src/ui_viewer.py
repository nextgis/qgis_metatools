# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_viewer.ui'
#
# Created: Wed Mar 30 16:36:25 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MetatoolsViewer(object):
    def setupUi(self, MetatoolsViewer):
        MetatoolsViewer.setObjectName(_fromUtf8("MetatoolsViewer"))
        MetatoolsViewer.resize(550, 350)
        MetatoolsViewer.setMinimumSize(QtCore.QSize(200, 100))
        self.verticalLayout = QtGui.QVBoxLayout(MetatoolsViewer)
        self.verticalLayout.setMargin(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(MetatoolsViewer)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.webView = QtWebKit.QWebView(self.frame)
        self.webView.setMinimumSize(QtCore.QSize(250, 150))
        self.webView.setStyleSheet(_fromUtf8(""))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout_2.addWidget(self.webView)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtGui.QDialogButtonBox(MetatoolsViewer)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MetatoolsViewer)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MetatoolsViewer.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MetatoolsViewer.reject)
        QtCore.QMetaObject.connectSlotsByName(MetatoolsViewer)

    def retranslateUi(self, MetatoolsViewer):
        MetatoolsViewer.setWindowTitle(QtGui.QApplication.translate("MetatoolsViewer", "Metadata viewer", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
