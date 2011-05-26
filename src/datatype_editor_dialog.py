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

import os, sys

from ui_datatype_editor import Ui_DataTypeEditorDialog

from datatype_template_manager import DatatypeTemplateManager, DatatypeTemplate

currentPath = os.path.abspath(os.path.dirname(__file__))

class DatatypeEditorDialog(QDialog, Ui_DataTypeEditorDialog):
  def __init__(self):
    QDialog.__init__(self)
    self.setupUi(self)

    self.datatypeTemplateManager = DatatypeTemplateManager(currentPath)
    self.datatypeTemplate = DatatypeTemplate()

    self.btnSave = self.buttonBox.button(QDialogButtonBox.Save)
    self.btnClose = self.buttonBox.button(QDialogButtonBox.Close)

    self.leSpatialAccuracy.setValidator(QDoubleValidator())
    self.leSpatialScale.setValidator(QIntValidator())

    for key, value in DatatypeTemplate.TYPES.iteritems():
      self.cmbType.addItem(value, key)

    QObject.connect(self.btnNew, SIGNAL("clicked()"), self.newDatatype)
    QObject.connect(self.btnRemove, SIGNAL("clicked()"), self.removeDatatype)

    QObject.connect(self.leName, SIGNAL("textEdited( QString )"), self.templateModified)
    QObject.connect(self.leSpatialAccuracy, SIGNAL("textEdited( QString )"), self.templateModified)
    QObject.connect(self.leSpatialScale, SIGNAL("textEdited( QString )"), self.templateModified)
    QObject.connect(self.textThematicAccuracy, SIGNAL("textChanged()"), self.templateModified)
    QObject.connect(self.cmbType, SIGNAL("currentIndexChanged( QString )"), self.templateModified)

    QObject.connect(self.cmbDatatype, SIGNAL("currentIndexChanged( QString )"), self.datatypeChanged)

    QObject.disconnect(self.buttonBox, SIGNAL("accepted()"), self.accept)
    QObject.connect(self.btnSave, SIGNAL("clicked()"), self.saveTemplate)


    QObject.connect(self.btnAddKeyword, SIGNAL("clicked()"), self.addKeyword)
    QObject.connect(self.btnEditKeyword, SIGNAL("clicked()"), self.editKeyword)
    QObject.connect(self.btnRemoveKeyword, SIGNAL("clicked()"), self.removeKeyword)

    self.manageGui()

  def manageGui(self):
    self.reloadTemplatesList()
    self.btnSave.setEnabled(False)

  def reloadTemplatesList(self):
    self.cmbDatatype.clear()
    self.cmbDatatype.addItems(self.datatypeTemplateManager.getTemplateList())

  def newDatatype(self):
    self.clearFormFields()
    self.datatypeTemplate = DatatypeTemplate()
    self.btnSave.setEnabled(True)

  def removeDatatype(self):
    if self.datatypeTemplate.name:
      self.datatypeTemplateManager.removeTemplate(self.datatypeTemplate.name)
      self.reloadTemplatesList()

    if self.cmbDatatype.count() == 0:
      self.clearFormFields()

  # enable save button when template edited
  def templateModified(self):
    self.btnSave.setEnabled(True)

  def datatypeChanged(self):
    templateName = self.cmbDatatype.currentText()
    if templateName.isEmpty():
      return

    self.datatypeTemplate = self.datatypeTemplateManager.loadTemplate(templateName)
    self.templateToForm(self.datatypeTemplate)
    self.btnSave.setEnabled(False)

  def saveTemplate(self):
    template = self.templateFromForm()

    # check template attrs
    if template.name is None or template.name == "":
      QMessageBox.warning(self, self.tr("Manage data types"), self.tr("The name of the data type template must be specified!"))
      return

    # try to save template
    try:
      # first delete old template
      if self.datatypeTemplate.name:
          self.datatypeTemplateManager.removeTemplate(self.datatypeTemplate.name)
      # save new version
      self.datatypeTemplateManager.saveTemplate(template)
    except:
      QMessageBox.warning(self, self.tr("Manage data types"), self.tr("Template can't be saved: ") + str(sys.exc_info()[ 1 ]))
      return

    # reload form
    self.reloadTemplatesList()

    # set combobox item
    index = self.cmbDatatype.findText(template.name)
    if index != -1:
      self.cmbDatatype.setCurrentIndex(index)

    self.btnSave.setEnabled(False)

  def reject(self):
    if self.btnSave.isEnabled() and QMessageBox.question(None, self.tr("Metatools"), self.tr("Template contains unsaved data. Close the window without saving?"), QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
      return
    QDialog.reject(self)

  def clearFormFields(self):
    self.leName.clear()
    self.leSpatialAccuracy.clear()
    self.leSpatialScale.clear()
    self.lstKeywords.clear()
    self.textThematicAccuracy.clear()

  # populate form with template data
  def templateToForm(self, template):
    self.clearFormFields()

    self.leName.setText(template.name or "")

    self.leSpatialAccuracy.setText(template.accuracy or "")
    self.leSpatialScale.setText(template.scale or "")

    index = self.cmbType.findData(template.type)
    if index != -1:
      self.cmbType.setCurrentIndex(index)

    for keyword in template.keywords:
      self.lstKeywords.addItem(keyword)

    self.textThematicAccuracy.setText(template.thematicAccuracy or "")

  # create template from entered values
  def templateFromForm(self):
    template = DatatypeTemplate()
    template.name = self.leName.text()

    template.accuracy = self.leSpatialAccuracy.text()
    template.scale = self.leSpatialScale.text()

    template.type = str(self.cmbType.itemData(self.cmbType.currentIndex()).toString())

    template.keywords = []
    for num in range(self.lstKeywords.count()):
      template.keywords.append(self.lstKeywords.item(num).text())

    template.thematicAccuracy = self.textThematicAccuracy.toPlainText()

    return template


  def addKeyword(self):
    keyword, result = QInputDialog.getText(self, self.tr("New keyword"), self.tr("Input keyword:"))
    if result and keyword:
      self.lstKeywords.addItem(keyword)
      self.templateModified()

  def editKeyword(self):
    if self.lstKeywords.currentRow() < 0:
      QMessageBox.information(self, self.tr("Metatools"), self.tr("Select keyword for edit"))
      return
    keyword, result = QInputDialog.getText(self, self.tr("New keyword"), self.tr("Input keyword:"), QLineEdit.Normal, self.lstKeywords.item(self.lstKeywords.currentRow()).text())

    if result and keyword:
      self.lstKeywords.item(self.lstKeywords.currentRow()).setText(keyword)
      self.templateModified()

  def removeKeyword(self):
    if self.lstKeywords.currentRow() < 0:
      QMessageBox.information(self, self.tr("Metatools"), self.tr("Select keyword for remove"))
      return

    if QMessageBox.question(None, self.tr("Metatools"), self.tr("Remove this keyword?"), QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
      self.lstKeywords.takeItem(self.lstKeywords.currentRow())
      self.templateModified()
