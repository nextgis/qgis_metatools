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

import sys, os

from ui_organization_editor import Ui_OrganizationEditorDialog
from organization_template_manager import OrganizationTemplateManager, OrganizationTemplate

currentPath = os.path.abspath( os.path.dirname( __file__ ) )

class OrganizationEditorDialog(QDialog,Ui_OrganizationEditorDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.organizationTemplateManager = OrganizationTemplateManager(currentPath)
        self.organizationTemplate = OrganizationTemplate()

        #events
        self.connect(self.addButton, SIGNAL("clicked()"), self.addButtonClicked)
        self.connect(self.removeButton, SIGNAL("clicked()"), self.removeButtonClicked)
        
        self.connect(self.nameLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.emailLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.voicePhoneLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.faxLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.deliveryLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.cityLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.admLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.postalLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.countryLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.contactTitleLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.contactPositionLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.hoursLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
                
        self.connect(self.orgButtonBox, SIGNAL("clicked(QAbstractButton*)"), self.orgButtonBoxClicked)
        self.connect(self.orgComboBox, SIGNAL("currentIndexChanged(QString)"), self.orgComboBoxIndexChanged)

        #set interface
        self.reloadTemplatesList()

    #create new organization template
    def addButtonClicked(self):
        self.clearFormFields()
        self.organizationTemplate = organizationTemplate()
        self.orgGroupBox.setEnabled(True)
        self.orgButtonBox.setEnabled(False)

    def reloadTemplatesList(self):
        orgTemplatesList = self.organizationTemplateManager.getTemplateList()
        self.orgComboBox.clear()
        self.orgComboBox.addItems(orgTemplatesList)

    def removeButtonClicked(self):
        if self.organizationTemplate.name and self.organizationTemplate.name != '':
                    self.organizationTemplateManager.removeTemplate(self.organizationTemplate.name)
                    self.reloadTemplatesList() 

    #clear all form fields
    def clearFormFields(self):
        self.nameLineEdit.clear()
        self.versionLineEdit.clear()
        self.descTextEdit.clear()

    #set license template to the form
    def setLicenseTemplateToForm(self, template):
        self.nameLineEdit.setText(template.name or "")
        self.versionLineEdit.setText(template.version or "")
        self.descTextEdit.setPlainText(template.description or "")

    #get license template from form
    def getLicenseTemplateFromForm(self):
        template = LicenseTemplate()
        template.name = self.nameLineEdit.text()
        template.version = self.versionLineEdit.text()
        template.description = self.descTextEdit.toPlainText()
        return template

    #unlock save\cancel buttons
    def valueChanged(self):
        self.orgButtonBox.setEnabled(True)

    #Save or cancel changes
    def orgButtonBoxClicked(self, button):
        if self.orgButtonBox.standardButton(button) == QDialogButtonBox.Save:
            template = self.getLicenseTemplateFromForm()
            #check template
            if template.name is None or template.name == '':
                QMessageBox.warning(self, QCoreApplication.translate("Metatools", "License template editor"), QCoreApplication.translate("Metatools", "The name must be specified!"))
                return
            #try save template
            try:
                #delete old template
                if self.licenseTemplate.name and self.licenseTemplate.name != '':
                    self.licenseTemplateManager.removeLicenseTemplate(self.licenseTemplate.name)
                #save new version
                self.licenseTemplateManager.saveLicenseTemplate(template)
            except:
                QMessageBox.warning(self, QCoreApplication.translate("Metatools", "License template editor"), QCoreApplication.translate("Metatools", "Template can't be saved: ") + str(sys.exc_info()[1]))
                return
            #reload form
            self.reloadTemplatesList()
            #self.ui.licenseComboBox. #set 
        else:
            self.setLicenseTemplateToForm(self.licenseTemplate)
        self.licenseButtonBox.setEnabled(False)

    #Selected license changes
    def orgComboBoxIndexChanged(self, templateName):
        if templateName and templateName != '':
            try:
                self.licenseTemplate = self.licenseTemplateManager.loadLicenseTemplate(templateName)
                self.setLicenseTemplateToForm(self.licenseTemplate)
                self.licenseGroupBox.setEnabled(True)
                self.licenseButtonBox.setEnabled(False)
            except:
                pass
        else:
            self.licenseTemplate = LicenseTemplate()
            self.clearFormFields()
            self.licenseGroupBox.setEnabled(False)
            self.licenseButtonBox.setEnabled(False)




