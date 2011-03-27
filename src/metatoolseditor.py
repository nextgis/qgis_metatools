"""
/***************************************************************************
 MetatoolsDialog
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from qgis.core import *

#Import plugin code
from dom_model import DomModel, FilterDomModel
from ui_editor import Ui_MetatoolsEditor
import codecs,sys


class MetatoolsEditor(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_MetatoolsEditor()
        self.ui.setupUi(self)

        #events
        self.connect(self.ui.treeView, SIGNAL("clicked(QModelIndex)"), self.item_select)
        self.connect(self.ui.treeView, SIGNAL("collapsed(QModelIndex)"), self.collapsedExpanded)
        self.connect(self.ui.treeView, SIGNAL("expanded(QModelIndex)"), self.collapsedExpanded)
        self.connect(self.ui.valueTextEdit, SIGNAL("textChanged()"), self.valueTextChanged)
        self.connect(self.ui.valueButtonBox, SIGNAL("clicked(QAbstractButton*)"), self.valueButtonClicked)
        self.connect(self.ui.mainButtonBox, SIGNAL("clicked(QAbstractButton*)"), self.mainButtonClicked)

        self.connect(self.ui.filterTreeView, SIGNAL("clicked(QModelIndex)"), self.filter_item_select)
        self.connect(self.ui.filterTreeView, SIGNAL("collapsed(QModelIndex)"), self.filterCollapsedExpanded)
        self.connect(self.ui.filterTreeView, SIGNAL("expanded(QModelIndex)"), self.filterCollapsedExpanded)
        self.connect(self.ui.filterValueTextEdit, SIGNAL("textChanged()"), self.filterValueTextChanged)
        self.connect(self.ui.filterValueButtonBox, SIGNAL("clicked(QAbstractButton*)"), self.filterValueButtonClicked)


    def setContent(self, metaFilePath):
        self.metaFilePath = metaFilePath
        self.file = QFile(metaFilePath)
        self.metaXML = QDomDocument()
        self.metaXML.setContent(self.file)

        self.model = DomModel(self.metaXML, self)

        filter = self.loadFilter()

        self.proxyModel = FilterDomModel( filter, self )
        self.proxyModel.setDynamicSortFilter( True )
        self.proxyModel.setSourceModel(self.model)

        self.ui.treeView.setModel(self.model)
        self.ui.treeView.hideColumn(1) #hide attrs
        self.ui.treeView.resizeColumnToContents(0) #resize value column

        self.ui.filterTreeView.setModel(self.proxyModel)
        self.ui.filterTreeView.hideColumn(1) #hide attrs
        self.ui.filterTreeView.resizeColumnToContents(0) #resize value column

        self.ui.mainButtonBox.button(QDialogButtonBox.Save).setEnabled(False) #Disable Save button

    def item_select(self, mindex):
        '''Item selected in TreeView will be displayed in edit box.'''
        self.text = QVariant()
        self.mindex = self.model.index(mindex.row(), 2, mindex.parent())

        self.ui.valueTextEdit.clear()
        self.ui.nodePathLabel.setText(self.model.nodePath(self.mindex))

        if(self.model.isEditable(self.mindex)):
            self.text = self.model.data(self.mindex, 0)
            self.ui.valueTextEdit.setPlainText(self.text.toString())
            self.ui.editorGroupBox.setEnabled(True)
            self.ui.valueButtonBox.setEnabled(False) #disable buttons
        else:
            self.ui.editorGroupBox.setEnabled(False)

    def filter_item_select(self, mindex):
        '''Item selected in TreeView will be displayed in edit box.'''
        self.text = QVariant()
        self.mindex = self.proxyModel.index(mindex.row(), 2, mindex.parent())

        self.ui.filterValueTextEdit.clear()
        path = self.proxyModel.sourceModel().nodePath( self.proxyModel.mapToSource( self.mindex ) )
        self.ui.filterNodePathLabel.setText(path)

        editable = self.proxyModel.sourceModel().isEditable( self.proxyModel.mapToSource( self.mindex ) )
        if(editable):
            self.text = self.proxyModel.data(self.mindex, 0)
            self.ui.filterValueTextEdit.setPlainText(self.text.toString())
            self.ui.filterEditorGroupBox.setEnabled(True)
            self.ui.filterValueButtonBox.setEnabled(False) #disable buttons
        else:
            self.ui.filterEditorGroupBox.setEnabled(False)

    def collapsedExpanded(self, mindex):
        self.ui.treeView.resizeColumnToContents(0)

    def filterCollapsedExpanded(self, mindex):
        self.ui.filterTreeView.resizeColumnToContents(0)

    def valueTextChanged(self):
        self.ui.valueButtonBox.setEnabled(True)

    def filterValueTextChanged(self):
        self.ui.filterValueButtonBox.setEnabled(True)

    def valueButtonClicked(self, button):
        if self.ui.valueButtonBox.standardButton(button) == QDialogButtonBox.Apply:
            self.model.setData(self.mindex, self.ui.valueTextEdit.toPlainText())
            self.text = self.model.data(self.mindex, 0) #reload value!
            self.ui.mainButtonBox.button(QDialogButtonBox.Save).setEnabled(True) #Enable Save button on first edit
        else:
            self.ui.valueTextEdit.setPlainText(self.text.toString())
        self.ui.valueButtonBox.setEnabled(False)

    def filterValueButtonClicked(self, button):
        if self.ui.filterValueButtonBox.standardButton(button) == QDialogButtonBox.Apply:
            QMessageBox.warning(self, "DEBUG", self.ui.filterValueTextEdit.toPlainText())
            self.proxyModel.setData(self.mindex, self.ui.filterValueTextEdit.toPlainText())
            self.text = self.proxyModel.data(self.mindex, 0) #reload value!
            self.ui.mainButtonBox.button(QDialogButtonBox.Save).setEnabled(True) #Enable Save button on first edit
        else:
            self.ui.filterValueTextEdit.setPlainText(self.text.toString())
        self.ui.filterValueButtonBox.setEnabled(False)

    def mainButtonClicked(self, button):
        #need make user request!
        if self.ui.mainButtonBox.standardButton(button) == QDialogButtonBox.Save:
            try:
                metafile = codecs.open(self.metaFilePath, 'w', encoding='utf-8')
                metafile.write(unicode(self.metaXML.toString().toUtf8(), 'utf-8'))
                metafile.close()
                self.ui.mainButtonBox.button(QDialogButtonBox.Save).setEnabled(False) #Disable Save button
            except:
                QMessageBox.critical(self, QCoreApplication.translate("Metatools", "Metatools"), QCoreApplication.translate("Metatools", "Metadata file can't be saved!")+str(sys.exc_info()[0]))
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
