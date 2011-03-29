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

import codecs, sys

from dom_model import DomModel, FilterDomModel

from ui_editor import Ui_MetatoolsEditor

class MetatoolsEditor( QDialog, Ui_MetatoolsEditor ):
  def __init__( self ):
    QDialog.__init__( self )
    self.setupUi( self )
    
    self.tabWidget.setCurrentIndex( 0 )

    # events
    QObject.connect( self.treeView, SIGNAL( "clicked( QModelIndex )" ), self.item_select )
    QObject.connect( self.treeView, SIGNAL( "collapsed( QModelIndex )" ), self.collapsedExpanded )
    QObject.connect( self.treeView, SIGNAL( "expanded( QModelIndex )" ), self.collapsedExpanded )
    QObject.connect( self.valueTextEdit, SIGNAL( "textChanged()" ), self.valueTextChanged )
    QObject.connect( self.valueButtonBox, SIGNAL( "clicked( QAbstractButton* )" ), self.valueButtonClicked )
    QObject.connect( self.mainButtonBox, SIGNAL( "clicked( QAbstractButton* )" ), self.mainButtonClicked )

    QObject.connect( self.filterTreeView, SIGNAL( "clicked( QModelIndex )" ), self.filter_item_select )
    QObject.connect( self.filterTreeView, SIGNAL( "collapsed( QModelIndex )" ), self.filterCollapsedExpanded )
    QObject.connect( self.filterTreeView, SIGNAL( "expanded( QModelIndex )" ), self.filterCollapsedExpanded )
    QObject.connect( self.filterValueTextEdit, SIGNAL( "textChanged()" ), self.filterValueTextChanged )
    QObject.connect( self.filterValueButtonBox, SIGNAL( "clicked( QAbstractButton* )" ), self.filterValueButtonClicked )

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

    self.treeView.setModel( self.model )
    self.treeView.hideColumn( 1 ) # hide attrs
    self.treeView.resizeColumnToContents( 0 ) # resize value column

    self.filterTreeView.setModel( self.proxyModel )
    self.filterTreeView.hideColumn( 1 ) # hide attrs
    self.filterTreeView.resizeColumnToContents( 0 ) # resize value column

    self.mainButtonBox.button( QDialogButtonBox.Save ).setEnabled( False ) # Disable Save button

  def item_select( self, mindex ):
    '''Item selected in TreeView will be displayed in edit box.'''
    self.text = QVariant()
    self.mindex = self.model.index( mindex.row(), 2, mindex.parent() )

    self.valueTextEdit.clear()
    self.nodePathLabel.setText( self.model.nodePath( self.mindex ) )

    if self.model.isEditable( self.mindex ):
      self.text = self.model.data( self.mindex, 0 )
      self.valueTextEdit.setPlainText( self.text.toString() )
      self.editorGroupBox.setEnabled( True )
      self.valueButtonBox.setEnabled( False ) # disable buttons
    else:
      self.editorGroupBox.setEnabled( False )

  def filter_item_select( self, mindex ):
    '''Item selected in TreeView will be displayed in edit box.'''
    self.text = QVariant()
    self.mindex = self.proxyModel.index( mindex.row(), 2, mindex.parent() )

    self.filterValueTextEdit.clear()
    path = self.proxyModel.sourceModel().nodePath( self.proxyModel.mapToSource( self.mindex ) )
    self.filterNodePathLabel.setText( path )

    editable = self.proxyModel.sourceModel().isEditable( self.proxyModel.mapToSource( self.mindex ) )
    if editable:
      self.text = self.proxyModel.data( self.mindex, 0 )
      self.filterValueTextEdit.setPlainText( self.text.toString() )
      self.filterEditorGroupBox.setEnabled( True )
      self.filterValueButtonBox.setEnabled( False ) # disable buttons
    else:
      self.filterEditorGroupBox.setEnabled( False )

  def collapsedExpanded( self, mindex ):
    self.treeView.resizeColumnToContents( 0 )

  def filterCollapsedExpanded( self, mindex ):
    self.filterTreeView.resizeColumnToContents( 0 )

  def valueTextChanged( self ):
    self.valueButtonBox.setEnabled( True )

  def filterValueTextChanged( self ):
    self.filterValueButtonBox.setEnabled( True )

  def valueButtonClicked( self, button ):
    if self.valueButtonBox.standardButton( button ) == QDialogButtonBox.Apply:
      self.model.setData( self.mindex, self.valueTextEdit.toPlainText() )
      self.text = self.model.data( self.mindex, 0 ) # reload value!
      self.mainButtonBox.button( QDialogButtonBox.Save ).setEnabled( True ) # Enable Save button on first edit
    else:
      self.valueTextEdit.setPlainText( self.text.toString() )
    self.valueButtonBox.setEnabled( False )

  def filterValueButtonClicked( self, button ):
    if self.filterValueButtonBox.standardButton( button ) == QDialogButtonBox.Apply:
      self.proxyModel.setData( self.mindex, self.filterValueTextEdit.toPlainText() )
      self.text = self.proxyModel.data( self.mindex, 0 ) # reload value!
      self.mainButtonBox.button( QDialogButtonBox.Save ).setEnabled( True ) # Enable Save button on first edit
    else:
      self.filterValueTextEdit.setPlainText( self.text.toString() )
    self.filterValueButtonBox.setEnabled( False )

  def mainButtonClicked( self, button ):
    # need make user request!
    if self.mainButtonBox.standardButton( button ) == QDialogButtonBox.Save:
      try:
        metafile = codecs.open( self.metaFilePath, "w", encoding="utf-8" )
        metafile.write( unicode( self.metaXML.toString().toUtf8(), "utf-8" ) )
        metafile.close()
        self.mainButtonBox.button( QDialogButtonBox.Save ).setEnabled( False ) # Disable Save button
      except:
        QMessageBox.critical(self, self.tr( "Metatools" ), self.tr( "Metadata file can't be saved!" ) + str( sys.exc_info()[ 0 ] ) )
    else:
      self.reject()

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
