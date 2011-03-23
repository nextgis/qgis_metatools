# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Metatools workflow template editor
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
from ui_workflow_editor import Ui_WorkflowEditorDialog
from workflow_template_manager import WorkflowTemplateManager, WorkflowTemplate


class WorkflowEditorDialog(QDialog):
    def __init__(self, basePluginPath):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_WorkflowEditorDialog()
        self.ui.setupUi(self)

        #env vars
        self.basePluginPath = basePluginPath

        #internal vars
        self.workflowTemplateManager = WorkflowTemplateManager(self.basePluginPath)
        self.workflowTemplate = WorkflowTemplate()

        #events
        self.connect(self.ui.addButton, SIGNAL("clicked()"), self.addButtonClicked)
        self.connect(self.ui.removeButton, SIGNAL("clicked()"), self.removeButtonClicked)
        self.connect(self.ui.nameLineEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.ui.descTextEdit, SIGNAL("textEdited(QString)"), self.valueChanged)
        self.connect(self.ui.workflowButtonBox, SIGNAL("clicked(QAbstractButton*)"), self.workflowButtonBoxClicked)
        self.connect(self.ui.workflowComboBox, SIGNAL("currentIndexChanged(QString)"), self.workflowComboBoxIndexChanged)

        #set interface
        self.reloadTemplatesList()

    #create new workflow template
    def addButtonClicked(self):
        self.clearFormFields()
        self.workflowTemplate = WorkflowTemplate()
        self.ui.workflowGroupBox.setEnabled(True)
        self.ui.workflowButtonBox.setEnabled(False)

    def reloadTemplatesList(self):
        workflowTemplatesList = self.workflowTemplateManager.getWorkflowTemplateList()
        self.ui.workflowComboBox.clear()
        self.ui.workflowComboBox.addItems(workflowTemplatesList)

    def removeButtonClicked(self):
        if self.workflowTemplate.name and self.workflowTemplate.name != '':
                    self.workflowTemplateManager.removeWorkflowTemplate(self.workflowTemplate.name)
                    self.reloadTemplatesList()

    #clear all form fields
    def clearFormFields(self):
        self.ui.nameLineEdit.clear()
        self.ui.descTextEdit.clear()

    #set workflow template to the form
    def setWorkflowTemplateToForm(self, template):
        self.ui.nameLineEdit.setText(template.name or "")
        self.ui.descTextEdit.setPlainText(template.description or "")

    #get workflow template from form
    def getWorkflowTemplateFromForm(self):
        template = WorkflowTemplate()
        template.name = self.ui.nameLineEdit.text()
        template.description = self.ui.descTextEdit.toPlainText()
        return template

    #unlock save\cancel buttons
    def valueChanged(self):
        self.ui.workflowButtonBox.setEnabled(True)

    #Save or cancel changes
    def workflowButtonBoxClicked(self, button):
        if self.ui.workflowButtonBox.standardButton(button) == QDialogButtonBox.Save:
            template = self.getWorkflowTemplateFromForm()
            #check template
            if template.name is None or template.name == '':
                QMessageBox.warning(self, QCoreApplication.translate("Metatools", "Workflow template editor"), QCoreApplication.translate("Metatools", "The name must be specified!"))
                return
            #try save template
            try:
                #delete old template
                if self.workflowTemplate.name and self.workflowTemplate.name != '':
                    self.workflowTemplateManager.removeWorkflowTemplate(self.workflowTemplate.name)
                #save new version
                self.workflowTemplateManager.saveWorkflowTemplate(template)
            except:
                QMessageBox.warning(self, QCoreApplication.translate("Metatools", "Workflow template editor"), QCoreApplication.translate("Metatools", "Template can't be saved: ") + str(sys.exc_info()[1]))
                return
            #reload form
            self.reloadTemplatesList()
            #set editable item:
            index = self.ui.workflowComboBox.findText(template.name)
            if index != -1:
                self.ui.workflowComboBox.setCurrentIndex(index)
        else:
            self.setWorkflowTemplateToForm(self.workflowTemplate)
        self.ui.workflowButtonBox.setEnabled(False)

    #Selected workflow changes
    def workflowComboBoxIndexChanged(self, templateName):
        if templateName and templateName != '':
            try:
                self.workflowTemplate = self.workflowTemplateManager.loadWorkflowTemplate(templateName)
                self.setWorkflowTemplateToForm(self.workflowTemplate)
                self.ui.workflowGroupBox.setEnabled(True)
                self.ui.workflowButtonBox.setEnabled(False)
            except:
                pass
        else:
            self.workflowTemplate = WorkflowTemplate()
            self.clearFormFields()
            self.ui.workflowGroupBox.setEnabled(False)
            self.ui.workflowButtonBox.setEnabled(False)




