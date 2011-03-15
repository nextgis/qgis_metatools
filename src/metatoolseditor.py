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
from PyQt4.QtCore import SIGNAL, QFile, QVariant, QCoreApplication
from PyQt4.QtGui import QDialogButtonBox, QDialog, QMessageBox
from PyQt4.QtXml import QDomDocument
from qgis.core import *

#Import plugin code
from dom_model import DomModel
from ui_editor import Ui_MetatoolsEditor
import codecs


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


    def setContent(self, metaFilePath):
        self.metaFilePath = metaFilePath
        self.file = QFile(metaFilePath)
        self.metaXML = QDomDocument()
        self.metaXML.setContent(self.file)

        self.model = DomModel(self.metaXML, self)
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.hideColumn(1) #hide attrs
        self.ui.treeView.resizeColumnToContents(0) #resize value column

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


    def collapsedExpanded(self, mindex):
        self.ui.treeView.resizeColumnToContents(0)

    def valueTextChanged(self):
        self.ui.valueButtonBox.setEnabled(True)

    def valueButtonClicked(self, button):
        if self.ui.valueButtonBox.standardButton(button) == QDialogButtonBox.Apply:
            self.model.setData(self.mindex, self.ui.valueTextEdit.toPlainText())
            self.ui.mainButtonBox.button(QDialogButtonBox.Save).setEnabled(True) #Enable Save button on first edit
        else:
            self.ui.valueTextEdit.setPlainText(self.text.toString())
        self.ui.valueButtonBox.setEnabled(False)

    def mainButtonClicked(self, button):
        #need make user request!
        if self.ui.mainButtonBox.standardButton(button) == QDialogButtonBox.Save:
            try:
                metafile = codecs.open(self.metaFilePath, 'w', encoding='utf-8')
                metafile.write(unicode(self.metaXML.toString().toUtf8(), 'utf-8'))
                metafile.close()
                self.ui.mainButtonBox.button(QDialogButtonBox.Save).setEnabled(False) #Disable Save button
            except:
                QMessageBox.critical(self, QCoreApplication.translate("Metatools", "Metatools"), QCoreApplication.translate("Metatools", "Metadata file can't be saved!"))
        else:
            self.reject()


