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

import sys

from ui_license_editor import Ui_LicenseEditorDialog
from license_template_manager import LicenseTemplateManager, LicenseTemplate

class LicenseEditorDialog( QDialog, Ui_LicenseEditorDialog ):
  def __init__( self, basePluginPath ):
    QDialog.__init__( self )
    self.setupUi( self )

    # env vars
    self.basePluginPath = basePluginPath

    # internal vars
    self.licenseTemplateManager = LicenseTemplateManager( self.basePluginPath )
    self.licenseTemplate = LicenseTemplate()

    # events
    QObject.connect( self.addButton, SIGNAL( "clicked()" ), self.addButtonClicked )
    QObject.connect( self.removeButton, SIGNAL( "clicked()" ), self.removeButtonClicked )
    QObject.connect( self.nameLineEdit, SIGNAL( "textEdited(QString)" ), self.valueChanged )
    QObject.connect( self.versionLineEdit, SIGNAL( "textEdited(QString)" ), self.valueChanged )
    QObject.connect( self.descTextEdit, SIGNAL( "textEdited(QString)" ), self.valueChanged )
    QObject.connect( self.licenseButtonBox, SIGNAL( "clicked(QAbstractButton*)" ), self.licenseButtonBoxClicked )
    QObject.connect( self.licenseComboBox, SIGNAL( "currentIndexChanged(QString)" ), self.licenseComboBoxIndexChanged )

    # set interface
    self.reloadTemplatesList()

  # create new license template
  def addButtonClicked( self ):
    self.clearFormFields()
    self.licenseTemplate = LicenseTemplate()
    self.licenseGroupBox.setEnabled( True )
    self.licenseButtonBox.setEnabled( False )

  def reloadTemplatesList( self ):
    licenseTemplatesList = self.licenseTemplateManager.getLicenseTemplateList()
    self.licenseComboBox.clear()
    self.licenseComboBox.addItems( licenseTemplatesList )

  def removeButtonClicked( self ):
    if self.licenseTemplate.name and self.licenseTemplate.name != "":
      self.licenseTemplateManager.removeLicenseTemplate( self.licenseTemplate.name )
      self.reloadTemplatesList()

  # clear all form fields
  def clearFormFields( self ):
    self.nameLineEdit.clear()
    self.versionLineEdit.clear()
    self.descTextEdit.clear()

  # set license template to the form
  def setLicenseTemplateToForm( self, template ):
    self.nameLineEdit.setText( template.name or "" )
    self.versionLineEdit.setText( template.version or "" )
    self.descTextEdit.setPlainText( template.description or "" )

  # get license template from form
  def getLicenseTemplateFromForm( self ):
    template = LicenseTemplate()
    template.name = self.nameLineEdit.text()
    template.version = self.versionLineEdit.text()
    template.description = self.descTextEdit.toPlainText()
    return template

  # unlock save\cancel buttons
  def valueChanged( self ):
    self.licenseButtonBox.setEnabled( True )

  # Save or cancel changes
  def licenseButtonBoxClicked( self, button ):
    if self.licenseButtonBox.standardButton( button ) == QDialogButtonBox.Save:
      template = self.getLicenseTemplateFromForm()
      # check template
      if template.name is None or template.name == "":
        QMessageBox.warning( self, self.tr( "License template editor" ), self.tr( "The name must be specified!" ) )
        return
      # try save template
      try:
        # delete old template
        if self.licenseTemplate.name and self.licenseTemplate.name != "":
            self.licenseTemplateManager.removeLicenseTemplate( self.licenseTemplate.name )
        # save new version
        self.licenseTemplateManager.saveLicenseTemplate( template )
      except:
        QMessageBox.warning( self, self.tr( "License template editor" ), self.tr( "Template can't be saved: ") + str( sys.exc_info()[ 1 ] ) )
        return
      # reload form
      self.reloadTemplatesList()
      # set editable item:
      index = self.licenseComboBox.findText( template.name )
      if index != -1:
        self.licenseComboBox.setCurrentIndex( index )
    else:
      self.setLicenseTemplateToForm( self.licenseTemplate )
    self.licenseButtonBox.setEnabled( False )

  # Selected license changes
  def licenseComboBoxIndexChanged( self, templateName ):
    if templateName and templateName != "":
      try:
        self.licenseTemplate = self.licenseTemplateManager.loadLicenseTemplate( templateName )
        self.setLicenseTemplateToForm( self.licenseTemplate )
        self.licenseGroupBox.setEnabled( True )
        self.licenseButtonBox.setEnabled( False )
      except:
        pass
    else:
      self.licenseTemplate = LicenseTemplate()
      self.clearFormFields()
      self.licenseGroupBox.setEnabled( False )
      self.licenseButtonBox.setEnabled( False )
