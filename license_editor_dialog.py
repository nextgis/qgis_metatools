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

from ui.ui_license_editor import Ui_LicenseEditorDialog

from license_template_manager import LicenseTemplateManager, LicenseTemplate

currentPath = os.path.abspath(os.path.dirname(__file__))

class LicenseEditorDialog(QDialog, Ui_LicenseEditorDialog):
  def __init__(self):
    QDialog.__init__(self)
    self.setupUi(self)

    self.licenseTemplateManager = LicenseTemplateManager(currentPath)
    self.licenseTemplate = LicenseTemplate()

    self.btnSave = self.buttonBox.button(QDialogButtonBox.Save)
    self.btnClose = self.buttonBox.button(QDialogButtonBox.Close)

    QObject.connect(self.btnNew, SIGNAL("clicked()"), self.newLicense)
    QObject.connect(self.btnRemove, SIGNAL("clicked()"), self.removeLicense)
    QObject.connect(self.leName, SIGNAL("textEdited( QString )"), self.templateModified)
    QObject.connect(self.leVersion, SIGNAL("textEdited( QString )"), self.templateModified)
    QObject.connect(self.textDescription, SIGNAL("textChanged()"), self.templateModified)
    QObject.connect(self.cmbLicense, SIGNAL("currentIndexChanged( QString )"), self.licenseChanged)

    QObject.disconnect(self.buttonBox, SIGNAL("accepted()"), self.accept)
    QObject.connect(self.btnSave, SIGNAL("clicked()"), self.saveTemplate)

    self.manageGui()

  def manageGui(self):
    self.btnRemove.setEnabled(False)
    self.reloadTemplatesList()
    self.btnSave.setEnabled(False)

  def reloadTemplatesList(self):
    self.cmbLicense.clear()
    self.cmbLicense.addItems(self.licenseTemplateManager.getTemplateList())

  def newLicense(self):
    if self.btnSave.isEnabled() and QMessageBox.question(None, self.tr("Metatools"), self.tr("Template contains unsaved data. Create new template without saving?"), QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
      return
    self.clearFormFields()
    self.licenseTemplate = LicenseTemplate()
    self.btnSave.setEnabled(False)

  def removeLicense(self):
    if self.licenseTemplate.name:
      self.licenseTemplateManager.removeTemplate(self.licenseTemplate.name)
      self.reloadTemplatesList()

    if self.cmbLicense.count() == 0:
      self.clearFormFields()
      self.btnSave.setEnabled(False)

  # enable save button when template edited
  def templateModified(self):
    self.btnSave.setEnabled(True)

  def licenseChanged(self):
    templateName = self.cmbLicense.currentText()
    if templateName.isEmpty():
      self.licenseTemplate = LicenseTemplate()
      self.btnRemove.setEnabled(False)
      return

    self.licenseTemplate = self.licenseTemplateManager.loadTemplate(templateName)
    self.templateToForm(self.licenseTemplate)
    self.btnSave.setEnabled(False)
    self.btnRemove.setEnabled(True)

  def saveTemplate(self):
    template = self.templateFromForm()

    # check template attrs
    if template.name is None or template.name == "":
      QMessageBox.warning(self, self.tr("Manage licenses"), self.tr("The name of the license must be specified!"))
      return

    # try to save template
    try:
      # first delete old template
      if self.licenseTemplate.name and self.licenseTemplate.name != "":
          self.licenseTemplateManager.removeTemplate(self.licenseTemplate.name)
      # save new version
      self.licenseTemplateManager.saveTemplate(template)
    except:
      QMessageBox.warning(self, self.tr("Manage licenses"), self.tr("Template can't be saved: ") + str(sys.exc_info()[ 1 ]))
      return

    # reload form
    self.reloadTemplatesList()

    # set combobox item
    index = self.cmbLicense.findText(template.name)
    if index != -1:
      self.cmbLicense.setCurrentIndex(index)

    self.btnSave.setEnabled(False)

  def clearFormFields(self):
    self.leName.clear()
    self.leVersion.clear()
    self.textDescription.clear()

  # populate form with template data
  def templateToForm(self, template):
    self.leName.setText(template.name or "")
    self.leVersion.setText(template.version or "")
    self.textDescription.setPlainText(template.description or "")

  # create template from entered values
  def templateFromForm(self):
    template = LicenseTemplate()
    template.name = self.leName.text()
    template.version = self.leVersion.text()
    template.description = self.textDescription.toPlainText()
    return template

  def reject(self):
    if self.btnSave.isEnabled() and QMessageBox.question(None, self.tr("Metatools"), self.tr("Template contains unsaved data. Close the window without saving?"), QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
      return
    QDialog.reject(self)
