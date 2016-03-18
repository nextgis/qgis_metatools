# -*- coding: utf-8 -*-

#******************************************************************************
#
# Metatools
# ---------------------------------------------------------
# Metadata browser/editor
#
# Copyright (C) 2011-2016 NextGIS (info@nextgis.com)
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

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtXml import *

import os, codecs

class LicenseTemplateManager:
  SUBFOLDER = 'templates/license'
  EXT = '.xml'

  def __init__(self, basePluginPath):
    self.basePluginPath = unicode(basePluginPath)

  def getTemplatesPath(self):
    return os.path.join(self.basePluginPath, self.SUBFOLDER)

  def getTemplateFilePath(self, templateName):
    return os.path.join(self.getTemplatesPath(), unicode(templateName) + self.EXT)

  def getTemplateList(self):
    templatesList = []
    for filename in os.listdir(self.getTemplatesPath()):
      name, ext = os.path.splitext(filename)
      if ext == self.EXT:
        templatesList.append(name)
    return templatesList

  def loadTemplate(self, templateName):
    # TODO: more cheks on struct!
    template = LicenseTemplate()
    templateFile = QFile(self.getTemplateFilePath(templateName))

    xmlTemplate = QDomDocument()
    xmlTemplate.setContent(templateFile)

    root = xmlTemplate.documentElement()
    nameElement = root.elementsByTagName("Name").at(0)
    versionElement = root.elementsByTagName("Version").at(0)
    descriptionElement = root.elementsByTagName("Description").at(0)

    template.name = nameElement.childNodes().at(0).nodeValue()
    template.version = versionElement.childNodes().at(0).nodeValue()
    template.description = descriptionElement.childNodes().at(0).nodeValue()

    return template

  def saveTemplate(self, template):
    xmlTemplate = QDomDocument()

    # create root
    root = xmlTemplate.createElement("LicenseTemplate")
    xmlTemplate.appendChild(root)

    # set name
    element = xmlTemplate.createElement("Name")
    textNode = xmlTemplate.createTextNode(template.name)
    element.appendChild(textNode)
    root.appendChild(element)

    # set version
    element = xmlTemplate.createElement("Version")
    textNode = xmlTemplate.createTextNode(template.version)
    element.appendChild(textNode)
    root.appendChild(element)

    # set desc
    element = xmlTemplate.createElement("Description")
    textNode = xmlTemplate.createTextNode(template.description)
    element.appendChild(textNode)
    root.appendChild(element)

    templateFile = codecs.open(self.getTemplateFilePath(template.name), "w", encoding="utf-8")
    templateFile.write(unicode(xmlTemplate.toString()))
    templateFile.close()

  def removeTemplate(self, templateName):
    os.remove(self.getTemplateFilePath(templateName))

class LicenseTemplate:
  def __init__(self, name = None, version = None, description = None):
    self.name = name
    self.version = version
    self.description = description

  def stringRepresentation(self):
    return self.name + '::' + self.version + '::' + self.description
