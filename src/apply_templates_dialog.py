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
from PyQt4.QtXmlPatterns import *

from qgis.core import *
from qgis.gui import *

import sys, os, codecs, shutil

from license_editor_dialog import LicenseEditorDialog
from license_template_manager import LicenseTemplateManager
from workflow_editor_dialog import WorkflowEditorDialog
from workflow_template_manager import WorkflowTemplateManager

from ui_apply_templates import Ui_ApplyTemplatesDialog

from standard import MetaInfoStandard
import utils

currentPath = os.path.abspath( os.path.dirname( __file__ ) )

class ApplyTemplatesDialog( QDialog, Ui_ApplyTemplatesDialog ):
  def __init__( self, iface ):
    QDialog.__init__( self )
    self.setupUi( self )
    self.iface = iface

    self.basePluginPath = currentPath
    self.layers = []

    self.licenseTemplateManager = LicenseTemplateManager( self.basePluginPath )
    self.workflowTemplateManager = WorkflowTemplateManager( self.basePluginPath )

    QObject.connect( self.externalFilesCheckBox, SIGNAL( "stateChanged( int )" ), self.toggleExternalFiles )
    QObject.connect( self.layerListView, SIGNAL( "itemSelectionChanged()" ), self.updateLayerList )

    QObject.connect( self.btnSelectDataFiles, SIGNAL( "clicked()" ), self.selectExternalFiles )
    QObject.connect( self.licenseManageButton, SIGNAL( "clicked()" ), self.licenseManageButtonClick )
    QObject.connect( self.organizationManageButton, SIGNAL( "clicked()" ), self.organizationManageButtonClick )
    QObject.connect( self.workflowManageButton, SIGNAL( "clicked()" ), self.workflowManageButtonClick )
    QObject.connect( self.selectLogFileButton, SIGNAL( "clicked()" ), self.selectLogFileButtonClick )
    QObject.connect( self.mainButtonBox, SIGNAL( "clicked( QAbstractButton* )" ), self.mainButtonClicked )

    self.manageGui()

  def manageGui( self ):
    # populate layer list
    self.layerListView.addItems( utils.getRasterLayerNames() )

    # populate comboboxes with templates
    self.updateLicenseTemplatesList()
    self.updateWorkflowTemplatesList()

  def toggleExternalFiles( self ):
    if self.externalFilesCheckBox.isChecked():
      self.layerListView.setEnabled( False )
      self.btnSelectDataFiles.setEnabled( True )
      self.layers = []
    else:
      self.layerListView.setEnabled( True )
      self.btnSelectDataFiles.setEnabled( False )
      self.updateLayerList()

  def selectExternalFiles( self ):
    files = QFileDialog.getOpenFileNames( self, self.tr( "Select files" ), ".", self.tr( "All files (*.*)" ) )

    if files.isEmpty():
      return

    self.layers = files

  def licenseManageButtonClick( self ):
    oldValue = self.licenseComboBox.currentText()

    dlg = LicenseEditorDialog( self.basePluginPath )
    dlg.exec_()

    self.updateLicenseTemplatesList()

    # try to restore previous value
    index = self.licenseComboBox.findText( oldValue )
    if index != -1:
      self.licenseComboBox.setCurrentIndex( index )

  def workflowManageButtonClick( self ):
    oldValue = self.workflowComboBox.currentText()

    dlg = WorkflowEditorDialog( self.basePluginPath )
    dlg.exec_()

    self.updateWorkflowTemplatesList()

    # try to restore previous value
    index = self.workflowComboBox.findText( oldValue )
    if index != -1:
      self.workflowComboBox.setCurrentIndex( index )

  def organizationManageButtonClick( self ):
    QMessageBox.information( self, self.tr( "Metatools" ), self.tr( "Not implemented!" ) )

  def selectLogFileButtonClick( self ):
    # TODO: need to save last dir and set it in dialog
    logFileName = QFileDialog.getOpenFileName( self, self.tr( "Select log file" ), ".", self.tr( "Text files (*.txt);;Log files (*.log);;All files (*)" ), None, QFileDialog.ReadOnly )
    self.logFileLineEdit.setText( logFileName )
    self.logFileLineEdit.setToolTip( logFileName )

  def updateLicenseTemplatesList( self ):
    self.licenseComboBox.clear()
    self.licenseComboBox.addItems( self.licenseTemplateManager.getTemplateList() )

  def updateWorkflowTemplatesList( self ):
    self.workflowComboBox.clear()
    self.workflowComboBox.addItems( self.workflowTemplateManager.getTemplateList() )

  def updateOrgsTemplatesList( self ):
    self.organizationComboBox.clear()
    self.organizationComboBox.addItems( self.organizationComboBox.getTemplateList() )

  def updateLayerList( self ):
    self.layers = []
    selection = self.layerListView.selectedItems()
    for item in selection:
      layer = utils.getRasterLayerByName( item.text() )
      self.layers.append( layer.source() )

  def mainButtonClicked( self, button ):
    # get profile from settings
    settings = QSettings( "NextGIS", "metatools" )
    profile = settings.value( "iso19115/defaultProfile", QVariant( "" ) ).toString()
    if profile.isEmpty():
      QMessageBox.warning( self, self.tr( "No profile" ), self.tr( "No profile selected. Please set default profile in plugin settings" ) )
      return

    profilePath = str( QDir.toNativeSeparators( os.path.join( currentPath, "xml_profiles", str( profile ) ) ) )

    if self.mainButtonBox.standardButton( button ) == QDialogButtonBox.Apply:
      try:
        for layer in self.layers:
          # get metadata file path
          metaFilePath = utils.mdPathFromLayerPath( layer )

          # check if metadata file exists
          if not os.path.exists( metaFilePath ):
            try:
              shutil.copyfile( profilePath, metaFilePath )
            except:
              QMessageBox.warning( self, self.tr( "Metatools" ), self.tr( "Metadata file can't be created: ") + str( sys.exc_info()[ 1 ] ) )
              continue
          #if not os.path.exists( metaFilePath ):
          #  result = QMessageBox.question( self, self.tr( "Metatools" ),
          #                                 self.tr( "The layer %1 does not have metadata! Create metadata file?")
          #                                 .arg( layer.name() ),
          #                                 QDialogButtonBox.Yes, QDialogButtonBox.No )
          #  if result == QDialogButtonBox.Yes:
          #    try:
                # TODO: get profile name from standart&settings
                #profilePath = os.path.join( str( self.basePluginPath ), "xml_profiles/csir_sac_profile.xml" ) # BAD!
          #      shutil.copyfile( str( profilePath ), metaFilePath )
          #    except:
          #      QMessageBox.warning( self, self.tr( "Metatools" ), self.tr( "Metadata file can't be created: ") + str( sys.exc_info()[ 1 ] ) )
          #      continue
          #  else:
          #    continue

          # check metadata standard
          standard = MetaInfoStandard.tryDetermineStandard( metaFilePath )
          if standard != MetaInfoStandard.ISO19115:
            QMessageBox.warning( self, self.tr( "Metatools" ),
                                 self.tr( "File %1 has unsupported metadata standard! Only ISO19115 supported now!" )
                                 .arg( layer ) )
            continue

          # load metadata file
          file = QFile( metaFilePath )
          metaXML = QDomDocument()
          metaXML.setContent( file )

          # apply templates (BAD version - change to applier with standard)
          self.applyLicenseTemplate( metaXML )
          self.applyWorkflowTemplate( metaXML )
          self.applyLogFile( metaXML )

          # save metadata file (hmm.. why not QFile?)
          metafile = codecs.open( metaFilePath, "w", encoding="utf-8" )
          metafile.write( unicode( metaXML.toString().toUtf8(), "utf-8" ) )
          metafile.close()

        QMessageBox.information( self, self.tr( "Metatools" ), self.tr( "Templates successfully applied!" ) )
      except:
        QMessageBox.warning( self, self.tr( "Metatools" ), self.tr( "Templates can't be applied: " ) + str( sys.exc_info()[ 1 ] ) )
    else:
      self.reject()

  # ----------- Appliers -----------

  def applyLicenseTemplate( self, metaXML ):
    # TODO: make more safe
    if self.licenseComboBox.currentIndex() == -1:
      return

    licenseTemplate = self.licenseTemplateManager.loadLicenseTemplate( self.licenseComboBox.currentText() )

    root = metaXML.documentElement()

    mdIdentificationInfo = self.getOrCreateChild( root, "identificationInfo" )
    mdDataIdentification = self.getOrCreateChild( mdIdentificationInfo, "MD_DataIdentification" )

    mdResourceConstraints = self.getOrIsertAfterChild( mdDataIdentification, "resourceConstraints", [ "resourceSpecificUsage", "descriptiveKeywords", "resourceFormat", "graphicOverview", "resourceMaintenance", "pointOfContact", "status", "credit", "purpose", "abstract" ] )
    mdLegalConstraintsElement = self.getOrCreateChild( mdResourceConstraints, "MD_LegalConstraints" )

    # useLimitation
    mdUseLimitationElement = self.getOrCreateChild( mdLegalConstraintsElement, "useLimitation" )
    mdCharStringElement = self.getOrCreateChild( mdUseLimitationElement, "gco:CharacterString" )
    textNode = self.getOrCreateTextChild( mdCharStringElement )
    textNode.setNodeValue( licenseTemplate.stringRepresentation() )

    # useConstraints
    mdUseConstraintsElement = self.getOrCreateChild( mdLegalConstraintsElement, "useConstraints" )
    mdRestrictionCodeElement = self.getOrCreateChild( mdUseConstraintsElement, "MD_RestrictionCode" )

    mdRestrictionCodeElement.setAttribute( "codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode" )
    mdRestrictionCodeElement.setAttribute( "codeListValue", "license" )

    textNode = self.getOrCreateTextChild( mdRestrictionCodeElement )
    textNode.setNodeValue( "license" )

  def applyWorkflowTemplate( self, metaXML ):
    # TODO: make more safe
    if self.workflowComboBox.currentIndex() == -1:
        return

    workflowTemplate = self.workflowTemplateManager.loadWorkflowTemplate( self.workflowComboBox.currentText() )

    root = metaXML.documentElement()

    mdDataQualityInfo = self.getOrIsertAfterChild( root, "dataQualityInfo", [ "distributionInfo", "contentInfo", "identificationInfo" ] )
    mdDQData = self.getOrCreateChild( mdDataQualityInfo, "DQ_DataQuality" )

    # check requirements (not need for workflow)
    if mdDQData.firstChildElement( "scope" ).isNull():
      mdScope = self.getOrIsertTopChild( mdDQData, "scope" )
      mdDQScope = self.getOrCreateChild( mdScope, "DQ_Scope" )
      mdLevel = self.getOrIsertTopChild( mdDQScope, "level" )
      mdScopeCode = self.getOrCreateChild( mdLevel, "MD_ScopeCode" )

      mdScopeCode.setAttribute( "codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode" )
      mdScopeCode.setAttribute( "codeListValue", "dataset" )

      textNode = self.getOrCreateTextChild( mdScopeCode )
      textNode.setNodeValue( "dataset" )

    mdLineage = self.getOrCreateChild( mdDQData, "lineage" )
    mdLiLineage = self.getOrCreateChild( mdLineage, "LI_Lineage" )
    mdStatement = self.getOrIsertTopChild( mdLiLineage, "statement" )

    mdCharStringElement = self.getOrCreateChild( mdStatement, "gco:CharacterString" )

    textNode = self.getOrCreateTextChild( mdCharStringElement )
    textNode.setNodeValue( workflowTemplate.stringRepresentation() )

  def applyLogFile( self, metaXML ):
    # TODO: make more safe
    if self.logFileLineEdit.text().isEmpty():
      return

    logFile = codecs.open( self.logFileLineEdit.text(), "r", encoding="utf-8" )
    logFileContent = logFile.read()
    logFile.close()

    root = metaXML.documentElement()

    mdDataQualityInfo = self.getOrIsertAfterChild( root, "dataQualityInfo", [ "distributionInfo", "contentInfo", "identificationInfo" ] )
    mdDQData = self.getOrCreateChild( mdDataQualityInfo, "DQ_DataQuality" )

    # check requirements (not need for log file)
    if mdDQData.firstChildElement( "scope" ).isNull():
      mdScope = self.getOrIsertTopChild( mdDQData, "scope" )
      mdDQScope = self.getOrCreateChild( mdScope, "DQ_Scope" )
      mdLevel = self.getOrIsertTopChild( mdDQScope, "level" )
      mdScopeCode = self.getOrCreateChild( mdLevel, "MD_ScopeCode" )

      mdScopeCode.setAttribute( "codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode" )
      mdScopeCode.setAttribute( "codeListValue", "dataset" )
      textNode = self.getOrCreateTextChild( mdScopeCode )
      textNode.setNodeValue( "dataset" )

    mdLineage = self.getOrCreateChild( mdDQData, "lineage" )
    mdLiLineage = self.getOrCreateChild( mdLineage, "LI_Lineage" )

    mdProcessStep = self.getOrCreateChild( mdLiLineage, "processStep" )
    mdLIProcessStep = self.getOrCreateChild( mdProcessStep, "LI_ProcessStep" )
    mdDescription = self.getOrIsertTopChild( mdLIProcessStep, "description" )
    mdCharStringElement = self.getOrCreateChild( mdDescription, "gco:CharacterString" )
    textNode = self.getOrCreateTextChild( mdCharStringElement )
    textNode.setNodeValue( logFileContent )

  def applyOrganisationTemplate( self, metaXML ):
    pass

  # ----------- XML Helpers -----------

  def getOrCreateChild( self, element, childName ):
    child = element.firstChildElement( childName )
    if child.isNull():
      child = element.ownerDocument().createElement( childName )
      element.appendChild( child )
    return child

  def getOrIsertAfterChild( self, element, childName, prevChildsName ):
    child = element.firstChildElement( childName )
    if child.isNull():
      child = element.ownerDocument().createElement( childName )

      # search previous element
      for elementName in prevChildsName:
        prevElement = element.firstChildElement( elementName )
        if not prevElement.isNull():
          element.insertAfter( child, prevElement )
          return child

      # if not found, simply append
      element.appendChild( child )
    return child

  def getOrIsertTopChild( self, element, childName ):
    child = element.firstChildElement( childName )
    if child.isNull():
      child = element.ownerDocument().createElement( childName )
      element.insertBefore( child, QDomNode() )
    return child

  def getOrCreateTextChild( self, element ):
    childTextNode = element.childNodes().at( 0 ) # bad! need full search and type checker
    if childTextNode.isNull():
      childTextNode = element.ownerDocument().createTextNode( "" )
      element.appendChild( childTextNode )
    return childTextNode
