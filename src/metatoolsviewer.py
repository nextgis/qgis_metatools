# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Metatools Viewer
                                 A QGIS plugin
 Metadata browser/editor
                             -------------------
        begin                : 2011-02-21
        copyright            : (C) 2011 by NextGIS
        email                : info@nextgis.ru
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4.QtXmlPatterns  import *

from qgis.core import *
from ui_viewer import Ui_MetatoolsViewer


#debug
class Handler(QAbstractMessageHandler):
    def handleMessage(self, msg_type, desc, identifier, loc):
        QMessageBox.information(QWidget(), 'Error', desc + " " + identifier.toString() + " " + QString(str(loc.line())))


# create the dialog for zoom to point
class MetatoolsViewer(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_MetatoolsViewer()
        self.ui.setupUi(self)

    def setContent(self, metaFilePath, xsltFilePath):
        xsltFile = QFile(xsltFilePath)
        srcFile = QFile(metaFilePath)

        xsltFile.open(QIODevice.ReadOnly)
        srcFile.open(QIODevice.ReadOnly)

        xslt = QString(xsltFile.readAll())
        src = QString(srcFile.readAll())

        xsltFile.close()
        srcFile.close()

        qry = QXmlQuery(QXmlQuery.XSLT20)

        self.handler = Handler();
        qry.setMessageHandler(self.handler)

        qry.setFocus(src)
        qry.setQuery(xslt)

        #if qry.isValid():
        #    QMessageBox.information(self, 'Valid', "Valid!")
        #else:
        #    QMessageBox.information(self, 'Valid', "Invalid!")

        result = QString()
        qry.setMessageHandler(self.handler)
        #success = qry.evaluateTo(result)

        #if success:
        #    QMessageBox.information(self, 'success', "success!")
        #else:
        #    QMessageBox.information(self, 'success', "Unsuccess!")
        result = qry.evaluateToString()
        if result:
            self.ui.webView.setHtml(QString.fromUtf8(result))
