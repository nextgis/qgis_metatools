# -*- coding: utf-8 -*-

#******************************************************************************
#
# Metatools
# ---------------------------------------------------------
# Metadata browser/editor
#
# Copyright (C) 2011 NextGIS (info@nextgis.ru)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4.QtXmlPatterns  import *

from qgis.core import *
from qgis.gui import *

from ui_viewer import Ui_MetatoolsViewer

# need this for debug
class Handler( QAbstractMessageHandler ):
  def handleMessage( self, msg_type, desc, identifier, loc ):
    QMessageBox.information( None, "Error", desc + " " + identifier.toString() + " " + QString( str( loc.line() ) ) )

class MetatoolsViewer( QDialog, Ui_MetatoolsViewer ):
  def __init__( self ):
    QDialog.__init__( self )
    self.setupUi( self )

  def setContent( self, metaFilePath, xsltFilePath ):
    xsltFile = QFile( xsltFilePath )
    srcFile = QFile( metaFilePath )

    xsltFile.open( QIODevice.ReadOnly )
    srcFile.open( QIODevice.ReadOnly )

    xslt = QString( xsltFile.readAll() )
    src = QString( srcFile.readAll() )

    xsltFile.close()
    srcFile.close()

    qry = QXmlQuery( QXmlQuery.XSLT20 )

    self.handler = Handler();
    qry.setMessageHandler( self.handler )

    qry.setFocus( src )
    qry.setQuery( xslt )

    #if qry.isValid():
    #  QMessageBox.information( self, "Valid", "Valid!" )
    #else:
    #  QMessageBox.information( self, "Valid", "Invalid!" )

    result = QString()
    qry.setMessageHandler( self.handler )
    #success = qry.evaluateTo( result )

    #if success:
    #  QMessageBox.information(self, "success", "success!")
    #else:
    #  QMessageBox.information(self, "success", "Unsuccess!")
    result = qry.evaluateToString()
    if result:
      self.webView.setHtml( QString.fromUtf8( result ) )
