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

from qgis.core import *
from qgis.gui import *

import codecs, sys

from dom_model import DomModel, FilterDomModel

from ui_editor import Ui_MetatoolsEditor

class MetatoolsEditor( QDialog, Ui_MetatoolsEditor ):
  def __init__( self ):
    QDialog.__init__( self )
    self.setupUi( self )

    self.tabWidget.setCurrentIndex( 0 )
    self.lblNodePath.setText( "" )

    self.btnSave = self.buttonBox.button( QDialogButtonBox.Save )
    self.btnClose = self.buttonBox.button( QDialogButtonBox.Close )

    self.btnApply = QPushButton( self.tr( "Apply" ) )
    self.btnDiscard = QPushButton( self.tr( "Discard" ) )
    self.editorButtonBox.clear()
    self.editorButtonBox.addButton( self.btnApply, QDialogButtonBox.AcceptRole )
    self.editorButtonBox.addButton( self.btnDiscard, QDialogButtonBox.RejectRole )

    # full metadata view
    QObject.connect( self.treeFull, SIGNAL( "clicked( QModelIndex )" ), self.itemSelected )
    QObject.connect( self.treeFull, SIGNAL( "collapsed( QModelIndex )" ), self.collapsedExpanded )
    QObject.connect( self.treeFull, SIGNAL( "expanded( QModelIndex )" ), self.collapsedExpanded )
    # filtered metadata view
    QObject.connect( self.treeFiltered, SIGNAL( "clicked( QModelIndex )" ), self.itemSelected )
    QObject.connect( self.treeFiltered, SIGNAL( "collapsed( QModelIndex )" ), self.collapsedExpanded )
    QObject.connect( self.treeFiltered, SIGNAL( "expanded( QModelIndex )" ), self.collapsedExpanded )

    QObject.connect( self.textValue, SIGNAL( "textChanged()" ), self.valueModified )
    QObject.connect( self.tabWidget, SIGNAL( "currentChanged( int )" ), self.tabChanged )

    QObject.connect( self.btnApply, SIGNAL( "clicked()" ), self.applyEdits )
    QObject.connect( self.btnDiscard, SIGNAL( "clicked()" ), self.resetEdits )

    #QObject.connect( self.buttonBox, SIGNAL( "clicked( QAbstractButton* )" ), self.mainButtonClicked )
    QObject.disconnect( self.buttonBox, SIGNAL( "accepted()" ), self.accept )
    QObject.connect( self.btnSave, SIGNAL( "clicked()" ), self.saveMetadata )

  def setContent( self, metaFilePath ):
    self.metaFilePath = metaFilePath
    self.file = QFile( metaFilePath )
    self.metaXML = QDomDocument()
    self.metaXML.setContent( self.file )

    self.model = DomModel( self.metaXML, self )

    filter = self.loadFilter()

    self.proxyModel = FilterDomModel( filter, self )
    self.proxyModel.setDynamicSortFilter( True )
    self.proxyModel.setSourceModel( self.model )

    self.treeFull.setModel( self.model )
    self.treeFull.hideColumn( 1 ) # hide attrs
    self.treeFull.resizeColumnToContents( 0 ) # resize value column

    self.treeFiltered.setModel( self.proxyModel )
    self.treeFiltered.hideColumn( 1 ) # hide attrs
    self.treeFiltered.resizeColumnToContents( 0 ) # resize value column

    self.btnSave.setEnabled( False )

  def itemSelected( self, mindex ):
    # Display item selected in TreeView in edit box.
    self.textValue.clear()

    path = ""
    editable = False
    self.text = QVariant()

    if self.tabWidget.currentIndex() == 0:
      # full view
      self.mindex = self.model.index( mindex.row(), 2, mindex.parent() )
      path = self.model.nodePath( self.mindex )
      editable = self.model.isEditable( self.mindex )
      self.text = self.model.data( self.mindex, 0 )
    else:
      # filtered view
      self.mindex = self.proxyModel.index( mindex.row(), 2, mindex.parent() )
      path = self.proxyModel.sourceModel().nodePath( self.proxyModel.mapToSource( self.mindex ) )
      editable = self.proxyModel.sourceModel().isEditable( self.proxyModel.mapToSource( self.mindex ) )
      self.text = self.proxyModel.data( self.mindex, 0 )

    self.lblNodePath.setText( path )
    if editable:
      self.textValue.setPlainText( self.text.toString() )
      self.groupBox.setEnabled( True )
      self.editorButtonBox.setEnabled( False )
    else:
      self.textValue.clear()
      self.groupBox.setEnabled( False )

  def collapsedExpanded( self, mindex ):
    if self.tabWidget.currentIndex() == 0:
      self.treeFull.resizeColumnToContents( 0 )
    else:
      self.treeFiltered.resizeColumnToContents( 0 )

  def valueModified( self ):
    self.editorButtonBox.setEnabled( True )

  def tabChanged( self, tab ):
    self.textValue.clear()

    path = ""
    editable = False
    self.text = QVariant()

    if tab == 0:
      mindex = self.treeFull.currentIndex()
      self.mindex = self.model.index( mindex.row(), 2, mindex.parent() )
      path = self.model.nodePath( self.mindex )
      editable = self.model.isEditable( self.mindex )
      self.text = self.model.data( self.mindex, 0 )
    else:
      mindex = self.treeFiltered.currentIndex()
      self.mindex = self.proxyModel.index( mindex.row(), 2, mindex.parent() )
      path = self.proxyModel.sourceModel().nodePath( self.proxyModel.mapToSource( self.mindex ) )
      editable = self.proxyModel.sourceModel().isEditable( self.proxyModel.mapToSource( self.mindex ) )
      self.text = self.proxyModel.data( self.mindex, 0 )

    self.lblNodePath.setText( path )
    if editable:
      self.textValue.setPlainText( self.text.toString() )
      self.groupBox.setEnabled( True )
      self.editorButtonBox.setEnabled( False )
    else:
      self.textValue.clear()
      self.groupBox.setEnabled( False )

  def applyEdits( self ):
    if self.tabWidget.currentIndex() == 0:
      self.model.setData( self.mindex, self.textValue.toPlainText() )
      self.text = self.model.data( self.mindex, 0 )
    else:
      self.proxyModel.setData( self.mindex, self.filterValueTextEdit.toPlainText() )
      self.text = self.proxyModel.data( self.mindex, 0 )
    self.btnSave.setEnabled( True )
    self.editorButtonBox.setEnabled( False )

  def resetEdits( self ):
    self.textValue.setPlainText( self.text.toString() )
    self.editorButtonBox.setEnabled( False )

  def saveMetadata( self ):
    try:
      metafile = codecs.open( self.metaFilePath, "w", encoding="utf-8" )
      metafile.write( unicode( self.metaXML.toString().toUtf8(), "utf-8" ) )
      metafile.close()
      self.btnSave.setEnabled( False )
    except:
      QMessageBox.warning(self, self.tr( "Metatools" ), self.tr( "Metadata file can't be saved:\n" ) + str( sys.exc_info()[ 0 ] ) )

  def loadFilter( self ):
    settings = QSettings( "NextGIS", "metatools" )
    fileName = settings.value( "general/filterFile", QVariant() ).toString()

    if fileName.isEmpty():
      return []

    # read filter from file
    filter = []
    f = QFile( fileName )
    if not f.open( QIODevice.ReadOnly ):
      QMessageBox.warning( self, self.tr( 'I/O error' ), self.tr( "Can't open file %1" ).arg( fileName ) )
      return []

    stream = QTextStream( f )
    while not stream.atEnd():
      line = stream.readLine()
      filter.append( line )
    f.close()

    return filter
