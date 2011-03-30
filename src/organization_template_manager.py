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

import os, codecs
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtXml import *

class OrganizationTemplateManager:
    ORG_SUBFOLDER = 'templates/organization'
    ORG_EXT = '.xml'

    def __init__(self, basePluginPath):
        self.basePluginPath = str(basePluginPath)

    def getOrganizationTemplatesPath(self):
        return os.path.join(self.basePluginPath, self.ORG_SUBFOLDER)

    def getTemplateFilePath(self, templateName):
        return os.path.join(self.getOrganizationTemplatesPath(), str(templateName) + self.ORG_EXT)

    def getTemplateList(self):
        templatesList = []
        for filename in os.listdir(self.getOrganizationTemplatesPath()):
            name, ext = os.path.splitext(filename)
            if ext == self.ORG_EXT:
                templatesList.append(name)
        return templatesList

    def loadTemplate(self, templateName):
        # TODO: more checks on struct!
        organizationTemplate = OrganizationTemplate()
        templateFile = QFile(self.getTemplateFilePath(templateName.toUtf8()))

        xmlTemplate = QDomDocument()
        xmlTemplate.setContent(templateFile)

        root = xmlTemplate.documentElement()
                
        organizationTemplate.name = root.elementsByTagName("Name").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.email=root.elementsByTagName("Email").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.phone=root.elementsByTagName("Phone").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.fax=root.elementsByTagName("Fax").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.delivery=root.elementsByTagName("Delivery").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.city=root.elementsByTagName("City").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.adm=root.elementsByTagName("Adm").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.postal=root.elementsByTagName("Postal").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.country=root.elementsByTagName("Country").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.contactTitle=root.elementsByTagName("ContactTitle").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.contactPosition=root.elementsByTagName("ContactPosition").at(0).childNodes().at(0).nodeValue()
        organizationTemplate.hours=root.elementsByTagName("Hours").at(0).childNodes().at(0).nodeValue()
        
        return organizationTemplate

    def saveTemplate(self, orgTemplate):
        # create doc and root
        xmlTemplate = QDomDocument()
        root = xmlTemplate.createElement("LicenseTemplate")
        xmlTemplate.appendChild(root)

        #set props
        self.addChildWithValue(xmlTemplate, root, "Name", orgTemplate.name)
        self.addChildWithValue(xmlTemplate, root, "Email", orgTemplate.email)
        self.addChildWithValue(xmlTemplate, root, "Phone", orgTemplate.phone)
        self.addChildWithValue(xmlTemplate, root, "Fax", orgTemplate.fax)
        self.addChildWithValue(xmlTemplate, root, "Delivery", orgTemplate.delivery)
        self.addChildWithValue(xmlTemplate, root, "City", orgTemplate.city)
        self.addChildWithValue(xmlTemplate, root, "Adm", orgTemplate.adm)
        self.addChildWithValue(xmlTemplate, root, "Postal", orgTemplate.postal)
        self.addChildWithValue(xmlTemplate, root, "Country", orgTemplate.country)
        self.addChildWithValue(xmlTemplate, root, "ContactTitle", orgTemplate.contactTitle)
        self.addChildWithValue(xmlTemplate, root, "ContactPosition", orgTemplate.contactPosition)
        self.addChildWithValue(xmlTemplate, root, "Hours", orgTemplate.hours)
        
        #save
        templateFile = codecs.open(self.getTemplateFilePath(licenseTemplate.name.toUtf8()), 'w', encoding='utf-8')
        templateFile.write(unicode(xmlTemplate.toString().toUtf8(), 'utf-8'))
        templateFile.close()
    
    def addChildWithValue(self, doc, root, elementName, elementValue):
        element = doc.createElement(elementName)
        textNode = doc.createTextNode(elementValue)
        element.appendChild(textNode)
        root.appendChild(element)

    def removeTemplate(self, templateName):
        os.remove(self.getTemplateFilePath(templateName))


class OrganizationTemplate:
    def __init__(self, name=None, email=None, phone=None, fax=None, delivery=None, city=None, adm=None, postal=None, country=None, contactTitle=None, contactPosition=None, hours=None):
        self.name = name
        self.email=email
        self.phone=phone
        self.fax=fax
        self.delivery=delivery
        self.city=city
        self.adm=adm
        self.postal=postal
        self.country=country
        self.contactTitle=contactTitle
        self.contactPosition=contactPosition
        self.hours=hours
    
    def stringRepresentation(self):
        return self.name


