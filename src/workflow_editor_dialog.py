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

from workflow_template_manager import WorkflowTemplateManager, WorkflowTemplate

from ui_workflow_editor import Ui_WorkflowEditorDialog

class WorkflowEditorDialog( QDialog, Ui_WorkflowEditorDialog ):
  def __init__( self, basePluginPath ):
    QDialog.__init__( self )
    self.setupUi( self )

    # env vars
    self.basePluginPath = basePluginPath

    # internal vars
    self.workflowTemplateManager = WorkflowTemplateManager( self.basePluginPath )
    self.workflowTemplate = WorkflowTemplate()

    # events
    QObject.connect( self.addButton, SIGNAL( "clicked()" ), self.addButtonClicked )
    QObject.connect( self.removeButton, SIGNAL( "clicked()" ), self.removeButtonClicked )
    QObject.connect( self.nameLineEdit, SIGNAL( "textEdited( QString )" ), self.valueChanged )
    QObject.connect( self.descTextEdit, SIGNAL( "textEdited( QString )" ), self.valueChanged )
    QObject.connect( self.workflowButtonBox, SIGNAL( "clicked( QAbstractButton* )" ), self.workflowButtonBoxClicked )
    QObject.connect( self.workflowComboBox, SIGNAL( "currentIndexChanged( QString )" ), self.workflowComboBoxIndexChanged )

    # set interface
    self.reloadTemplatesList()

  # create new workflow template
  def addButtonClicked( self ):
    self.clearFormFields()
    self.workflowTemplate = WorkflowTemplate()
    self.workflowGroupBox.setEnabled( True )
    self.workflowButtonBox.setEnabled( False )

  def reloadTemplatesList( self ):
    workflowTemplatesList = self.workflowTemplateManager.getWorkflowTemplateList()
    self.workflowComboBox.clear()
    self.workflowComboBox.addItems( workflowTemplatesList )

  def removeButtonClicked( self ):
    if self.workflowTemplate.name and self.workflowTemplate.name != "":
      self.workflowTemplateManager.removeWorkflowTemplate( self.workflowTemplate.name )
      self.reloadTemplatesList()

  # clear all form fields
  def clearFormFields( self ):
    self.nameLineEdit.clear()
    self.descTextEdit.clear()

  # set workflow template to the form
  def setWorkflowTemplateToForm( self, template ):
    self.nameLineEdit.setText( template.name or "" )
    self.descTextEdit.setPlainText( template.description or "" )

  # get workflow template from form
  def getWorkflowTemplateFromForm( self ):
    template = WorkflowTemplate()
    template.name = self.nameLineEdit.text()
    template.description = self.descTextEdit.toPlainText()
    return template

  # unlock save\cancel buttons
  def valueChanged( self ):
    self.workflowButtonBox.setEnabled( True )

  # Save or cancel changes
  def workflowButtonBoxClicked( self, button ):
    if self.workflowButtonBox.standardButton( button ) == QDialogButtonBox.Save:
      template = self.getWorkflowTemplateFromForm()
      # check template
      if template.name is None or template.name == "":
        QMessageBox.warning( self, self.tr( "Workflow template editor" ), self.tr( "The name must be specified!" ) )
        return
      # try save template
      try:
        # delete old template
        if self.workflowTemplate.name and self.workflowTemplate.name != "":
            self.workflowTemplateManager.removeWorkflowTemplate( self.workflowTemplate.name )
        # save new version
        self.workflowTemplateManager.saveWorkflowTemplate( template )
      except:
        QMessageBox.warning( self, self.tr( "Workflow template editor" ), self.tr( "Template can't be saved: ") + str( sys.exc_info()[ 1 ] ) )
        return
      # reload form
      self.reloadTemplatesList()
      # set editable item:
      index = self.workflowComboBox.findText( template.name )
      if index != -1:
        self.workflowComboBox.setCurrentIndex( index )
    else:
      self.setWorkflowTemplateToForm( self.workflowTemplate )
    self.workflowButtonBox.setEnabled( False )

  # Selected workflow changes
  def workflowComboBoxIndexChanged( self, templateName ):
    if templateName and templateName != "":
      try:
        self.workflowTemplate = self.workflowTemplateManager.loadWorkflowTemplate( templateName )
        self.setWorkflowTemplateToForm( self.workflowTemplate )
        self.workflowGroupBox.setEnabled( True )
        self.workflowButtonBox.setEnabled( False )
      except:
        pass
    else:
      self.workflowTemplate = WorkflowTemplate()
      self.clearFormFields()
      self.workflowGroupBox.setEnabled( False )
      self.workflowButtonBox.setEnabled( False )
