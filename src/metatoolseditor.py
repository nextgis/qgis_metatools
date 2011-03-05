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

from PyQt4 import QtCore, QtGui, QtXml
from dom_model import DomModel
from ui_editor import Ui_MetatoolsEditor


class MetatoolsEditor(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_MetatoolsEditor()
        self.ui.setupUi(self)
        #events
        self.connect(self.ui.treeView, QtCore.SIGNAL("clicked(QModelIndex)"), self.item_select)

    def setContent(self, metaFilePath):
        self.file = QtCore.QFile(metaFilePath)
        self.metaXML = QtXml.QDomDocument()
        self.metaXML.setContent(self.file)

        self.model = DomModel(self.metaXML, self)
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.hideColumn(1) #hide attrs
        self.ui.treeView.resizeColumnToContents(0) #aresize value column

    def item_select(self, mindex):
        '''Item selected in TreeView will be displayed in edit box.'''
        self.text = QtCore.QVariant()
        self.mindex = self.model.index(mindex.row(), 2, mindex.parent())

        self.text = self.model.data(self.mindex, 0)
        self.ui.textEdit.clear()

        #TODO: use the type detection to turn on things like date picker self.text.Type()
        self.ui.textEdit.insertPlainText(self.text.toString())
        #self.buttonBox.button(QDialogButtonBox.Apply).setDisabled(False)
