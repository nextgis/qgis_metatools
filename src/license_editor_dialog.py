# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Metatools license template editor
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
import sys 

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4.QtXmlPatterns  import *

from qgis.core import *

#plugin imports
from ui_license_editor import Ui_LicenseEditorDialog
from license_template_manager import LicenseTemplateManager, LicenseTemplate


class LicenseEditorDialog(QDialog):
    def __init__(self, basePluginPath):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_LicenseEditorDialog()
        self.ui.setupUi(self)
        
        #env vars
        self.basePluginPath=basePluginPath
        
        #internal vars
        self.licenseTemplateManager=LicenseTemplateManager(self.basePluginPath)
        self.licenseTemplate=LicenseTemplate()
        
        #events
        self.connect(self.ui.addButton, SIGNAL("clicked()"),self.addButtonClicked)
        self.connect(self.ui.removeButton, SIGNAL("clicked()"),self.removeButtonClicked)
        self.connect(self.ui.nameLineEdit, SIGNAL("textEdited(QString)"),self.valueChanged)
        self.connect(self.ui.versionLineEdit, SIGNAL("textEdited(QString)"),self.valueChanged)
        self.connect(self.ui.descTextEdit, SIGNAL("textEdited(QString)"),self.valueChanged)
        self.connect(self.ui.licenseButtonBox, SIGNAL("clicked(QAbstractButton*)"), self.licenseButtonBoxClicked)
        self.connect(self.ui.licenseComboBox, SIGNAL("currentIndexChanged(QString)"), self.licenseComboBoxIndexChanged)
                
        #set interface
        self.reloadTemplatesList()
    
    #create new license template
    def addButtonClicked(self):
        self.clearFormFields()
        self.licenseTemplate=LicenseTemplate()        
        self.ui.licenseGroupBox.setEnabled(True)
        self.ui.licenseButtonBox.setEnabled(False)
    
    def reloadTemplatesList(self):
        licenseTemplatesList=self.licenseTemplateManager.getLicenseTemplateList()
        self.ui.licenseComboBox.clear()
        self.ui.licenseComboBox.addItems(licenseTemplatesList)
    
    def removeButtonClicked(self):
        if self.licenseTemplate.name and self.licenseTemplate.name!='':
                    self.licenseTemplateManager.removeLicenseTemplate(self.licenseTemplate.name)
                    self.reloadTemplatesList()
        
    #clear all form fields
    def clearFormFields(self):
        self.ui.nameLineEdit.clear()
        self.ui.versionLineEdit.clear()
        self.ui.descTextEdit.clear()
    
    #set license template to the form
    def setLicenseTemplateToForm(self, template):
        self.ui.nameLineEdit.setText(template.name or "")
        self.ui.versionLineEdit.setText(template.version or "")
        self.ui.descTextEdit.setPlainText(template.description or "")
        
    #get license template from form
    def getLicenseTemplateFromForm(self):
        template=LicenseTemplate()
        template.name= self.ui.nameLineEdit.text()
        template.version=self.ui.versionLineEdit.text()
        template.description= self.ui.descTextEdit.toPlainText()
        return template
    
    #unlock save\cancel buttons
    def valueChanged(self):
        self.ui.licenseButtonBox.setEnabled(True)
    
    #Save or cancel changes
    def licenseButtonBoxClicked(self, button):
        if self.ui.licenseButtonBox.standardButton(button) == QDialogButtonBox.Save:
            template=self.getLicenseTemplateFromForm()
            #check template
            if template.name is None or template.name=='':
                QMessageBox.warning(self, QCoreApplication.translate("Metatools", "License template editor"), QCoreApplication.translate("Metatools", "The name must be specified!"))
                return
            #try save template
            try:
                #delete old template
                if self.licenseTemplate.name and self.licenseTemplate.name!='':
                    self.licenseTemplateManager.removeLicenseTemplate(self.licenseTemplate.name)
                #save new version
                self.licenseTemplateManager.saveLicenseTemplate(template)
            except:
                QMessageBox.warning(self, QCoreApplication.translate("Metatools", "License template editor"), QCoreApplication.translate("Metatools", "Template can't be saved: ")+str(sys.exc_info()[1]))
                return
            #reload form
            self.reloadTemplatesList()
            #self.ui.licenseComboBox. #set 
        else:
            self.setLicenseTemplateToForm(self.licenseTemplate)
        self.ui.licenseButtonBox.setEnabled(False)
    
    #Selected license changes
    def licenseComboBoxIndexChanged(self, templateName):
        if templateName and templateName!='':
            try:
                self.licenseTemplate=self.licenseTemplateManager.loadLicenseTemplate(templateName)
                self.setLicenseTemplateToForm(self.licenseTemplate)
                self.ui.licenseGroupBox.setEnabled(True)
                self.ui.licenseButtonBox.setEnabled(False)
            except:
                pass
        else:
            self.licenseTemplate=LicenseTemplate()
            self.clearFormFields()
            self.ui.licenseGroupBox.setEnabled(False)
            self.ui.licenseButtonBox.setEnabled(False)
            
        
        
        
   