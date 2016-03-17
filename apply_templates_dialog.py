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

from organization_editor_dialog import OrganizationEditorDialog
from organization_template_manager import OrganizationTemplateManager

from datatype_editor_dialog import DataTypeEditorDialog
from datatype_template_manager import DatatypeTemplateManager

from ui_apply_templates import Ui_ApplyTemplatesDialog

from standard import MetaInfoStandard
from metadata_provider import FileMetadataProvider
import utils

currentPath = os.path.abspath(os.path.dirname(__file__))

class ApplyTemplatesDialog(QDialog, Ui_ApplyTemplatesDialog):
  def __init__(self, iface):
    QDialog.__init__(self)
    self.setupUi(self)
    self.iface = iface

    self.layers = []

    self.translatedNoneLabel = QCoreApplication.translate("Metatools", "None")

    self.licenseTemplateManager = LicenseTemplateManager(currentPath)
    self.workflowTemplateManager = WorkflowTemplateManager(currentPath)
    self.datatypeTemplateManager = DatatypeTemplateManager(currentPath)
    path = os.path.join(currentPath, "templates/institutions.xml")
    self.orgsTemplateManager = OrganizationTemplateManager(path)

    self.btnApply = QPushButton(self.tr("Apply"))
    self.btnClose = QPushButton(self.tr("Close"))
    self.buttonBox.clear()
    self.buttonBox.addButton(self.btnApply, QDialogButtonBox.AcceptRole)
    self.buttonBox.addButton(self.btnClose, QDialogButtonBox.RejectRole)

    self.chkExternalFiles.stateChanged.connect(self.toggleExternalFiles)
    self.lstLayers.itemSelectionChanged.connect(self.updateLayerList)

    self.btnSelectDataFiles.clicked.connect(self.selectExternalFiles)
    self.btnManageLicenses.clicked.connect(self.manageLicenses)
    self.btnManageOrgs.clicked.connect(self.manageOrganizations)
    self.btnManageWorkflows.clicked.connect(self.manageWorkflows)
    self.btnManageDatatypes.clicked.connect(self.manageDatatypes)
    self.btnSelectLogFile.clicked.connect(self.selectLogFile)

    self.buttonBox.accepted.disconnect(self.accept)
    self.btnApply.clicked.connect(self.applyTemplates)

    self.manageGui()

  def manageGui(self):
    # read settings and restore checkbox state
    self.__loadSettings()

    # populate layer list
    self.fillLstLayers()

    # populate comboboxes with templates
    self.updateLicenseTemplatesList()
    self.updateWorkflowTemplatesList()
    self.updateOrgsTemplatesList()
    self.updateDatatypesTemplatesList()

    # disable Apply button when there are no layers
    if len(self.layers) == 0:
      self.btnApply.setEnabled(False)

  #version from trunk
  def fillLstLayers(self):
    self.lstLayers.clear()
    layers = utils.getSupportedLayers()
    for (name, source) in layers:
        item = QListWidgetItem(name, self.lstLayers)
        item.setData(Qt.UserRole, source)
        item.setData(Qt.ToolTipRole, source)

  def toggleExternalFiles(self):
    self.btnApply.setEnabled(False)
    if self.chkExternalFiles.isChecked():
      self.lstLayers.clear()
      self.lstLayers.setSelectionMode(QAbstractItemView.NoSelection)
      self.btnSelectDataFiles.setEnabled(True)
      self.layers = []
    else:
      self.fillLstLayers()
      self.lstLayers.setSelectionMode(QAbstractItemView.ExtendedSelection)
      self.btnSelectDataFiles.setEnabled(False)
      self.updateLayerList()

  def selectExternalFiles(self):
    files = QFileDialog.getOpenFileNames(self,
                                         self.tr("Select files"),
                                         ".",
                                         self.tr("All files (*.*)")
                                        )

    if len(files) == 0:
      return

    self.layers = files
    self.lstLayers.addItems(files)
    self.btnApply.setEnabled(True)

  def manageLicenses(self):
    oldValue = self.cmbLicense.currentText()

    dlg = LicenseEditorDialog()
    dlg.exec_()

    self.updateLicenseTemplatesList()

    # try to restore previous value
    index = self.cmbLicense.findText(oldValue)
    if index != -1:
      self.cmbLicense.setCurrentIndex(index)

  def manageDatatypes(self):
    oldValue = self.cmbDatatype.currentText()

    dlg = DataTypeEditorDialog()
    dlg.exec_()

    self.updateDatatypesTemplatesList()

    # try to restore previous value
    index = self.cmbDatatype.findText(oldValue)
    if index != -1:
      self.cmbDatatype.setCurrentIndex(index)

  def manageWorkflows(self):
    oldValue = self.cmbWorkflow.currentText()

    dlg = WorkflowEditorDialog()
    dlg.exec_()

    self.updateWorkflowTemplatesList()

    # try to restore previous value
    index = self.cmbWorkflow.findText(oldValue)
    if index != -1:
      self.cmbWorkflow.setCurrentIndex(index)

  def manageOrganizations(self):
    oldValue = self.cmbOrganization.currentText()

    dlg = OrganizationEditorDialog()
    dlg.exec_()

    self.orgsTemplateManager.reloadTemplates()
    self.updateOrgsTemplatesList()

    # try to restore previous value
    index = self.cmbOrganization.findText(oldValue)
    if index != -1:
      self.cmbOrganization.setCurrentIndex(index)

  def selectLogFile(self):
    # TODO: need to save last dir and set it in dialog
    logFileName = QFileDialog.getOpenFileName(self,
                                              self.tr("Select log file"),
                                              ".",
                                              self.tr("Text files (*.txt);;Log files (*.log);;All files (*)"),
                                              options=QFileDialog.ReadOnly
                                             )
    self.leLogFile.setText(logFileName)
    self.leLogFile.setToolTip(logFileName)

  def updateLicenseTemplatesList(self):
    self.cmbLicense.clear()
    self.cmbLicense.addItem(self.translatedNoneLabel)
    self.cmbLicense.addItems(self.licenseTemplateManager.getTemplateList())

  def updateWorkflowTemplatesList(self):
    self.cmbWorkflow.clear()
    self.cmbWorkflow.addItem(self.translatedNoneLabel)
    self.cmbWorkflow.addItems(self.workflowTemplateManager.getTemplateList())

  def updateOrgsTemplatesList(self):
    self.cmbOrganization.clear()
    self.cmbOrganization.addItem(self.translatedNoneLabel)
    self.cmbOrganization.addItems(self.orgsTemplateManager.tempalateNames())

  def updateDatatypesTemplatesList(self):
    self.cmbDatatype.clear()
    self.cmbDatatype.addItem(self.translatedNoneLabel)
    self.cmbDatatype.addItems(self.datatypeTemplateManager.getTemplateList())

  def updateLayerList(self):
    self.layers = []
    selection = self.lstLayers.selectedItems()
    for item in selection:
      layerSource = item.data(Qt.UserRole)
      self.layers.append(layerSource)
      #my old version
      #layer = utils.getRasterLayerByName(item.text())
      #self.layers.append(layer.source())

    if len(self.layers) != 0:
      self.btnApply.setEnabled(True)

  def applyTemplates(self):
    # TODO: !!! Remake to metaprovider !!!
    # TODO: !!! Adding standard check !!!

    # TODO: check if there are some templates selected

    # get profile from settings
    settings = QSettings("NextGIS", "metatools")
    profile = settings.value("general/defaultProfile", "")
    if profile == "":
      QMessageBox.warning(self,
                          self.tr("No profile"),
                          self.tr("No profile selected. Please set default profile in plugin settings")
                         )
      return

    profilePath = unicode(QDir.toNativeSeparators(os.path.join(currentPath, "xml_profiles", unicode(profile))))

    try:
      for layer in self.layers:
        # get metadata file path
        metaFilePath = utils.mdPathFromLayerPath(layer)

        # check if metadata file exists and create it if necessary
        if not os.path.exists(metaFilePath):
          try:
            shutil.copyfile(profilePath, metaFilePath)
          except:
            QMessageBox.warning(self,
                                self.tr("Metatools"),
                                self.tr("Metadata file can't be created: ") + unicode(sys.exc_info()[1])
                               )
            continue

        # check metadata standard
        metaprovider = FileMetadataProvider(unicode(layer)) #temporary code
        standard = MetaInfoStandard.tryDetermineStandard(metaprovider)
        if standard != MetaInfoStandard.ISO19115:
          QMessageBox.warning(self,
                              self.tr("Metatools"),
                              self.tr("File %s has unsupported metadata standard! Only ISO19115 supported now!") % (layer))
          continue

        if os.path.splitext(unicode(layer))[1].lower() not in (".shp", ".mif", ".tab"):
            # extract image specific information
            if self.chkUpdateImageInfo.isChecked():
              utils.writeRasterInfo(layer, metaFilePath)

            # generate preview
            if self.chkGeneratePreview.isChecked():
              utils.generatePreview(layer)
        else:
            if self.chkUpdateImageInfo.isChecked():
              utils.writeVectorInfo(layer, metaFilePath)

        # load metadata file
        metadata_file = QFile(metaFilePath)
        metaXML = QDomDocument()
        metaXML.setContent(metadata_file)

        # apply templates (BAD version - change to applier with standard)
        self.applyInstitutionTemplate(metaXML)
        self.applyLicenseTemplate(metaXML)
        self.applyWorkflowTemplate(metaXML)
        self.applyDatatypeTemplate(metaXML)
        self.applyLogFile(metaXML)

        # save metadata file (hmm.. why not QFile?)
        metafile = codecs.open(metaFilePath, "w", encoding="utf-8")
        metafile.write(unicode(metaXML, "utf-8"))
        metafile.close()

      QMessageBox.information(self,
                              self.tr("Metatools"),
                              self.tr("Done!")
                             )

      # clear selection and disable Apply button
      self.lstLayers.clearSelection()
      self.layers = []
      self.btnApply.setEnabled(False)

      # save settings
      self.__saveSettings()
    except:
      QMessageBox.warning(self,
                          self.tr("Metatools"),
                          self.tr("Operation can't be completed: ") + unicode(sys.exc_info()[1])
                         )

  # ----------- Appliers -----------

  def applyInstitutionTemplate(self, metaXML):
    # TODO: make more safe
    #if self.cmbOrganization.currentIndex() == -1:
    if self.cmbOrganization.currentText() == self.translatedNoneLabel:
      return

    template = self.orgsTemplateManager.organizations[self.cmbOrganization.currentText()]

    root = metaXML.documentElement()
    mdContact = utils.getOrCreateChild(root, "contact")
    mdResponsibleParty = utils.getOrCreateChild(mdContact, "CI_ResponsibleParty")

    # individualName
    mdIndividualName = utils.getOrCreateChild(mdResponsibleParty, "individualName")
    mdCharStringElement = utils.getOrCreateChild(mdIndividualName, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.person)

    # organisationName
    mdOrganisationName = utils.getOrCreateChild(mdResponsibleParty, "organisationName")
    mdCharStringElement = utils.getOrCreateChild(mdOrganisationName, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.name)

    # positionName
    mdPositionName = utils.getOrCreateChild(mdResponsibleParty, "positionName")
    mdCharStringElement = utils.getOrCreateChild(mdPositionName, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.position)

    # go deeper... fill contactInfo
    mdContactInfo = utils.getOrCreateChild(mdResponsibleParty, "contactInfo")
    mdCIContact = utils.getOrCreateChild(mdContactInfo, "CI_Contact")

    # hours of service
    mdHours = utils.getOrCreateChild(mdCIContact, "hoursOfService")
    mdCharStringElement = utils.getOrCreateChild(mdHours, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.hours)

    # fill phones
    mdPhone = utils.getOrCreateChild(mdCIContact, "phone")
    mdCIPhone = utils.getOrCreateChild(mdPhone, "CI_Telephone")

    mdVoice = utils.getOrCreateChild(mdCIPhone, "voice")
    mdCharStringElement = utils.getOrCreateChild(mdVoice, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.phone)

    mdFacsimile = utils.getOrCreateChild(mdCIPhone, "facsimile")
    mdCharStringElement = utils.getOrCreateChild(mdFacsimile, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.phone)

    # fill address
    mdAddress = utils.getOrCreateChild(mdCIContact, "address")
    mdCIAddress = utils.getOrCreateChild(mdAddress, "CI_Address")

    # deliveryPoint
    mdDeliveryPoint = utils.getOrCreateChild(mdCIAddress, "deliveryPoint")
    mdCharStringElement = utils.getOrCreateChild(mdDeliveryPoint, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.deliveryPoint)

    # city
    mdCity = utils.getOrCreateChild(mdCIAddress, "city")
    mdCharStringElement = utils.getOrCreateChild(mdCity, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.city)

    # administrativeArea
    mdAdminArea = utils.getOrCreateChild(mdCIAddress, "administrativeArea")
    mdCharStringElement = utils.getOrCreateChild(mdAdminArea, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.adminArea)

    # postalCode
    mdPostalCode = utils.getOrCreateChild(mdCIAddress, "postalCode")
    mdCharStringElement = utils.getOrCreateChild(mdPostalCode, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.postalCode)

    # country
    mdCountry = utils.getOrCreateChild(mdCIAddress, "country")
    mdCharStringElement = utils.getOrCreateChild(mdCountry, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.country)

    # email
    mdEmail = utils.getOrCreateChild(mdCIAddress, "electronicMailAddress")
    mdCharStringElement = utils.getOrCreateChild(mdEmail, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(template.email)

  def applyLicenseTemplate(self, metaXML):
    # TODO: make more safe
    #if self.cmbLicense.currentIndex() == -1:
    if self.cmbLicense.currentText() == self.translatedNoneLabel:
      return

    licenseTemplate = self.licenseTemplateManager.loadTemplate(self.cmbLicense.currentText())

    root = metaXML.documentElement()

    mdIdentificationInfo = utils.getOrCreateChild(root, "identificationInfo")
    mdDataIdentification = utils.getOrCreateChild(mdIdentificationInfo, "MD_DataIdentification")

    mdResourceConstraints = utils.getOrIsertAfterChild(mdDataIdentification, "resourceConstraints", ["resourceSpecificUsage", "descriptiveKeywords", "resourceFormat", "graphicOverview", "resourceMaintenance", "pointOfContact", "status", "credit", "purpose", "abstract"])
    mdLegalConstraintsElement = utils.getOrCreateChild(mdResourceConstraints, "MD_LegalConstraints")

    # useLimitation
    mdUseLimitationElement = utils.getOrCreateChild(mdLegalConstraintsElement, "useLimitation")
    mdCharStringElement = utils.getOrCreateChild(mdUseLimitationElement, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(licenseTemplate.stringRepresentation())

    # useConstraints
    mdUseConstraintsElement = utils.getOrCreateChild(mdLegalConstraintsElement, "useConstraints")
    mdRestrictionCodeElement = utils.getOrCreateChild(mdUseConstraintsElement, "MD_RestrictionCode")

    mdRestrictionCodeElement.setAttribute("codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_RestrictionCode")
    mdRestrictionCodeElement.setAttribute("codeListValue", "license")

    textNode = utils.getOrCreateTextChild(mdRestrictionCodeElement)
    textNode.setNodeValue("license")

  def applyWorkflowTemplate(self, metaXML):
    # TODO: make more safe
    #if self.cmbWorkflow.currentIndex() == -1:
    if self.cmbWorkflow.currentText() == self.translatedNoneLabel:
        return

    workflowTemplate = self.workflowTemplateManager.loadTemplate(self.cmbWorkflow.currentText())

    root = metaXML.documentElement()

    mdDataQualityInfo = utils.getOrIsertAfterChild(root, "dataQualityInfo", ["distributionInfo", "contentInfo", "identificationInfo"])
    mdDQData = utils.getOrCreateChild(mdDataQualityInfo, "DQ_DataQuality")

    # check requirements (not need for workflow)
    if mdDQData.firstChildElement("scope").isNull():
      mdScope = utils.getOrIsertTopChild(mdDQData, "scope")
      mdDQScope = utils.getOrCreateChild(mdScope, "DQ_Scope")
      mdLevel = utils.getOrIsertTopChild(mdDQScope, "level")
      mdScopeCode = utils.getOrCreateChild(mdLevel, "MD_ScopeCode")

      mdScopeCode.setAttribute("codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_ScopeCode")
      mdScopeCode.setAttribute("codeListValue", "dataset")

      textNode = utils.getOrCreateTextChild(mdScopeCode)
      textNode.setNodeValue("dataset")

    mdLineage = utils.getOrCreateChild(mdDQData, "lineage")
    mdLiLineage = utils.getOrCreateChild(mdLineage, "LI_Lineage")
    mdStatement = utils.getOrIsertTopChild(mdLiLineage, "statement")

    mdCharStringElement = utils.getOrCreateChild(mdStatement, "gco:CharacterString")

    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(workflowTemplate.stringRepresentation())

  def applyDatatypeTemplate(self, metaXML):
    # TODO: make more safe
    if self.cmbDatatype.currentText() == self.translatedNoneLabel:
      return

    datatypeTemplate = self.datatypeTemplateManager.loadTemplate(self.cmbDatatype.currentText())

    root = metaXML.documentElement()

    mdIdentificationInfo = utils.getOrCreateChild(root, "identificationInfo")
    mdDataIdentification = utils.getOrCreateChild(mdIdentificationInfo, "MD_DataIdentification")

    #insert type of data
    mdSpatialRep = utils.getOrIsertAfterChild(mdDataIdentification, "spatialRepresentationType", ["aggregationInfo", "resourceConstraints", "resourceSpecificUsage", "descriptiveKeywords", "resourceFormat", "graphicOverview", "resourceMaintenance", "pointOfContact", "status", "credit", "purpose", "abstract"])
    mdSpatialRepTypeCode = utils.getOrCreateChild(mdSpatialRep, "MD_SpatialRepresentationTypeCode")
    mdSpatialRepTypeCode.setAttribute("codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode")
    textNode = utils.getOrCreateTextChild(mdSpatialRepTypeCode)

    if datatypeTemplate.type == "vector":
      mdSpatialRepTypeCode.setAttribute("codeListValue", "vector")
      textNode.setNodeValue("vector")
    else:
      mdSpatialRepTypeCode.setAttribute("codeListValue", "grid")
      textNode.setNodeValue("grid")
      #adding raster type
      mdContentInfo = utils.getOrCreateChild(root, "contentInfo")
      mdImageDescription = utils.getOrCreateChild(mdContentInfo, "MD_ImageDescription")
      mdContentType = utils.getOrIsertAfterChild(mdImageDescription, "contentType", ["attributeDescription"])
      mdContentTypeCode = utils.getOrCreateChild(mdContentType, "MD_CoverageContentTypeCode")
      mdContentTypeCode.setAttribute("codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_CoverageContentTypeCode")
      mdContentTypeCode.setAttribute("codeListValue", datatypeTemplate.type)
      textNode = utils.getOrCreateTextChild(mdContentTypeCode)
      textNode.setNodeValue(datatypeTemplate.type)

    #insert keywords
    mdDescKeywords = utils.getOrIsertAfterChild(mdDataIdentification, "descriptiveKeywords", ["resourceFormat", "graphicOverview", "resourceMaintenance", "pointOfContact", "status", "credit", "purpose", "abstract"])
    mdKeywords = utils.getOrCreateChild(mdDescKeywords, "MD_Keywords")
    for keyword in datatypeTemplate.keywords:
      mdKeyword = utils.insertAfterChild(mdKeywords, "keyword", ["keyword",])
      mdString = utils.getOrCreateChild(mdKeyword, "gco:CharacterString")
      textNode = utils.getOrCreateTextChild(mdString)
      textNode.setNodeValue(keyword)
    mdType = utils.getOrIsertAfterChild(mdKeywords, "type", ["keyword",])
    mdTypeCode = utils.getOrCreateChild(mdType, "MD_KeywordTypeCode")
    mdTypeCode.setAttribute("codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode")
    mdTypeCode.setAttribute("codeListValue", "theme")
    textNode = utils.getOrCreateTextChild(mdTypeCode)
    textNode.setNodeValue("theme")

    #drop all spatial scale/accuracy
    while not mdDataIdentification.firstChildElement("spatialResolution").isNull():
      mdDataIdentification.removeChild(mdDataIdentification.firstChildElement("spatialResolution"))

    #insert spatial scale
    mdSpatialResolution = utils.insertAfterChild(mdDataIdentification, "spatialResolution", ["spatialRepresentationType", "aggregationInfo", "resourceConstraints", "resourceSpecificUsage", "descriptiveKeywords", "resourceFormat", "graphicOverview", "resourceMaintenance", "pointOfContact", "status", "credit", "purpose", "abstract"])
    mdResolution = utils.getOrCreateChild(mdSpatialResolution, "MD_Resolution")
    mdEqScale = utils.getOrIsertTopChild(mdResolution, "equivalentScale")
    mdFraction = utils.getOrCreateChild(mdEqScale, "MD_RepresentativeFraction")
    mdDenominator = utils.getOrCreateChild(mdFraction, "denominator")
    mdInteger = utils.getOrCreateChild(mdDenominator, "gco:Integer")
    textNode = utils.getOrCreateTextChild(mdInteger)
    textNode.setNodeValue(datatypeTemplate.scale)

    #insert spatial accuracy
    mdSpatialResolution = utils.insertAfterChild(mdDataIdentification, "spatialResolution", ["spatialResolution", "spatialRepresentationType", "aggregationInfo", "resourceConstraints", "resourceSpecificUsage", "descriptiveKeywords", "resourceFormat", "graphicOverview", "resourceMaintenance", "pointOfContact", "status", "credit", "purpose", "abstract"])
    mdResolution = utils.getOrCreateChild(mdSpatialResolution, "MD_Resolution")
    mdDistance = utils.getOrCreateChild(mdResolution, "distance")
    mdGcoDistance = utils.getOrCreateChild(mdDistance, "gco:Distance")
    textNode = utils.getOrCreateTextChild(mdGcoDistance)
    textNode.setNodeValue(datatypeTemplate.accuracy)
    mdGcoDistance.setAttribute("uom", "M")

    #insert thematic accurancy??????
    return

  def applyLogFile(self, metaXML):
    # TODO: make more safe
    if self.leLogFile.text() == "":
      return

    logFile = codecs.open(self.leLogFile.text(), "r", encoding="utf-8")
    logFileContent = logFile.read()
    logFile.close()

    root = metaXML.documentElement()

    mdDataQualityInfo = utils.getOrIsertAfterChild(root, "dataQualityInfo", ["distributionInfo", "contentInfo", "identificationInfo"])
    mdDQData = utils.getOrCreateChild(mdDataQualityInfo, "DQ_DataQuality")

    # check requirements (not need for log file)
    if mdDQData.firstChildElement("scope").isNull():
      mdScope = utils.getOrIsertTopChild(mdDQData, "scope")
      mdDQScope = utils.getOrCreateChild(mdScope, "DQ_Scope")
      mdLevel = utils.getOrIsertTopChild(mdDQScope, "level")
      mdScopeCode = utils.getOrCreateChild(mdLevel, "MD_ScopeCode")

      mdScopeCode.setAttribute("codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode")
      mdScopeCode.setAttribute("codeListValue", "dataset")
      textNode = utils.getOrCreateTextChild(mdScopeCode)
      textNode.setNodeValue("dataset")

    mdLineage = utils.getOrCreateChild(mdDQData, "lineage")
    mdLiLineage = utils.getOrCreateChild(mdLineage, "LI_Lineage")

    mdProcessStep = utils.getOrCreateChild(mdLiLineage, "processStep")
    mdLIProcessStep = utils.getOrCreateChild(mdProcessStep, "LI_ProcessStep")
    mdDescription = utils.getOrIsertTopChild(mdLIProcessStep, "description")
    mdCharStringElement = utils.getOrCreateChild(mdDescription, "gco:CharacterString")
    textNode = utils.getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(logFileContent)

  def __loadSettings(self):
    settings = QSettings("NextGIS", "metatools")

    self.chkUpdateImageInfo.setCheckState(int(settings.value("templates/extractLayerInfo", 0)))
    self.chkGeneratePreview.setCheckState(int(settings.value("templates/generatePreview", 0)))

  def __saveSettings(self):
    settings = QSettings("NextGIS", "metatools")

    settings.setValue("templates/extractLayerInfo", self.chkUpdateImageInfo.checkState())
    settings.setValue("templates/generatePreview",  self.chkGeneratePreview.checkState())

  def accept(self):
    QDialog.accept(self)
