# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Metatools templates applyer
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
#PyQt and QGIS imports 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4.QtXmlPatterns  import *

from qgis.core import *

#sys imports
import sys, os, codecs, shutil

#plugin imports
from ui_apply_templates import Ui_ApplyTemplatesDialog
from license_editor_dialog import LicenseEditorDialog
from license_template_manager import LicenseTemplateManager
from standard import MetaInfoStandard
import utils
from cgitb import text


class ApplyTemplatesDialog(QDialog):
    def __init__(self, basePluginPath, mapLayers):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_ApplyTemplatesDialog()
        self.ui.setupUi(self)

        #shortcuts
        self.translatedNoneLabel = QCoreApplication.translate("Metatools", "None")

        #env vars
        self.basePluginPath = basePluginPath
        self.mapLayers = mapLayers

        #internal vars
        self.licenseTemplateManager = LicenseTemplateManager(self.basePluginPath)

        #events
        self.connect(self.ui.licenseManageButton, SIGNAL("clicked()"), self.licenseManageButtonClick)
        self.connect(self.ui.organizationManageButton, SIGNAL("clicked()"), self.organizationManageButtonClick)
        self.connect(self.ui.workflowManageButton, SIGNAL("clicked()"), self.workflowManageButtonClick)
        self.connect(self.ui.mainButtonBox, SIGNAL("clicked(QAbstractButton*)"), self.mainButtonClicked)

        #init gui
        self.updateLicenseTemplatesList()

        self.ui.organizationComboBox.addItem(self.translatedNoneLabel)

        self.ui.workflowComboBox.addItem(self.translatedNoneLabel)

        for layer in mapLayers:
            if layer.type() == QgsMapLayer.RasterLayer:
                self.ui.layerListView.addItem(layer.name())


    def licenseManageButtonClick(self):
        dlg = LicenseEditorDialog(self.basePluginPath)
        dlg.show()
        result = dlg.exec_()

        oldValue = self.ui.licenseComboBox.currentText()

        self.updateLicenseTemplatesList()

        #try restore old selected value
        index = self.ui.licenseComboBox.findText(oldValue)
        if index != -1:
            self.ui.licenseComboBox.setCurrentIndex(index)

    def organizationManageButtonClick(self):
        QMessageBox.information(self, "Metatools", "Not implemented!")

    def workflowManageButtonClick(self):
        QMessageBox.information(self, "Metatools", "Not implemented!")

    def updateLicenseTemplatesList(self):
        licenseTemplatesList = self.licenseTemplateManager.getLicenseTemplateList()
        self.ui.licenseComboBox.clear()
        self.ui.licenseComboBox.addItem(self.translatedNoneLabel)
        self.ui.licenseComboBox.addItems(licenseTemplatesList)

    def mainButtonClicked(self, button):
        # shortcuts
        translatedMetatools = QCoreApplication.translate("Metatools", "Metatools")
        mainWindow = self

        if self.ui.mainButtonBox.standardButton(button) == QDialogButtonBox.Apply:
            try:
                for layer in self.mapLayers:
                    if layer.type() != QgsMapLayer.RasterLayer:
                        continue

                    #get metafile path 
                    metaFilePath = utils.getMetafilePath(layer)

                    # check metadata file exists
                    if not os.path.exists(metaFilePath):
                        result = QMessageBox.question (mainWindow, translatedMetatools, QCoreApplication.translate("Metatools", "The layer %1 does not have metadata! Create metadata file?").arg(layer.name()) , QDialogButtonBox.Yes, QDialogButtonBox.No)
                        if result == QDialogButtonBox.Yes:
                            #TODO: get profile name from standart&settings
                            try:
                                profilePath = os.path.join(str(self.basePluginPath), 'xml_profiles/csir_sac_profile.xml') #BAD!
                                shutil.copyfile(profilePath, metaFilePath)
                            except:
                                QMessageBox.warning(mainWindow, translatedMetatools, QCoreApplication.translate("Metatools", "Metadata file can't be created: ") + str(sys.exc_info()[1]))
                                continue
                        else:
                            continue

                    #check metadata standard
                    standard = MetaInfoStandard.tryDetermineStandard(metaFilePath)
                    if standard != MetaInfoStandard.ISO19115:
                        QMessageBox.critical(mainWindow, translatedMetatools, QCoreApplication.translate("Metatools", "Layer %1 has unsupported metadata standard! Only ISO19115 support now!").arg(layer.name()))
                        continue

                    #load metadata file
                    file = QFile(metaFilePath)
                    metaXML = QDomDocument()
                    metaXML.setContent(file)

                    #apply templates (BAD version - change to applyer with standard) 
                    self.applyLicenseTemplate(metaXML)

                    #save metadata file (hmm.. why not QFile?)
                    metafile = codecs.open(metaFilePath, 'w', encoding='utf-8')
                    metafile.write(unicode(metaXML.toString().toUtf8(), 'utf-8'))
                    metafile.close()

                QMessageBox.information(self, QCoreApplication.translate("Metatools", "Metatools"), QCoreApplication.translate("Metatools", "Templates successfully applied!"))
                self.accept()
            except:
                QMessageBox.critical(self, QCoreApplication.translate("Metatools", "Metatools"), QCoreApplication.translate("Metatools", "Templates can't be applied: ") + str(sys.exc_info()[1]))
        else:
            self.reject()

    def applyLicenseTemplate(self, metaXML):
        #TODO: make more safe
        if self.ui.licenseComboBox.currentText() == self.translatedNoneLabel:
            return

        licenseTemplate = self.licenseTemplateManager.loadLicenseTemplate(self.ui.licenseComboBox.currentText())

        root = metaXML.documentElement()

        mdIdentificationInfo = self.getOrCreateChild(root, "identificationInfo")
        mdDataIdentification = self.getOrCreateChild(mdIdentificationInfo, "MD_DataIdentification")

        mdResourceConstraints = self.getOrIsertAfterChild(mdDataIdentification, "resourceConstraints", ['resourceSpecificUsage', 'descriptiveKeywords', 'resourceFormat', 'graphicOverview', 'resourceMaintenance', 'pointOfContact', 'status', 'credit', 'purpose', 'abstract'])
        mdLegalConstraintsElement = self.getOrCreateChild(mdResourceConstraints, "MD_LegalConstraints")

        #useLimitation
        mdUseLimitationElement = self.getOrCreateChild(mdLegalConstraintsElement, "useLimitation")
        mdCharStringElement = self.getOrCreateChild(mdUseLimitationElement, "gco:CharacterString")
        textNode = self.getOrCreateTextChild(mdCharStringElement)
        textNode.setNodeValue(licenseTemplate.stringRepresentation())

        #useConstraints
        mdUseConstraintsElement = self.getOrCreateChild(mdLegalConstraintsElement, "useConstraints")
        mdRestrictionCodeElement = self.getOrCreateChild(mdUseConstraintsElement, "MD_RestrictionCode")

        mdRestrictionCodeElement.setAttribute("codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode")
        mdRestrictionCodeElement.setAttribute("codeListValue", "license")

        textNode = self.getOrCreateTextChild(mdRestrictionCodeElement)
        textNode.setNodeValue("license")


    def getOrCreateChild(self, element, childName):
        child = element.firstChildElement(childName)
        if child.isNull():
            child = element.ownerDocument().createElement(childName)
            element.appendChild(child)
        return child

    def getOrIsertAfterChild(self, element, childName, prevChildsName):
        child = element.firstChildElement(childName)
        if child.isNull():
            child = element.ownerDocument().createElement(childName)

            #search previous element
            for elementName in prevChildsName:
                prevElement = element.firstChildElement(elementName)
                if not prevElement.isNull():
                    element.insertAfter(child, prevElement)
                    return child

            #if not found, simple append
            element.appendChild(child)
        return child

    def getOrCreateTextChild(self, element):
        childTextNode = element.childNodes().at(0) #bad! need full search and type checker
        if childTextNode.isNull():
            childTextNode = element.ownerDocument().createTextNode('')
            element.appendChild(childTextNode)
        return childTextNode






