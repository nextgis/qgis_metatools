# -*- coding: utf-8 -*-

# ******************************************************************************
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
# ******************************************************************************

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtXml import *

import os, codecs


class DatatypeTemplateManager:
    SUBFOLDER = "templates/datatype"
    EXT = ".xml"

    def __init__(self, basePluginPath):
        self.basePluginPath = unicode(basePluginPath)

    def getTemplatesPath(self):
        return os.path.join(self.basePluginPath, self.SUBFOLDER)

    def getTemplateFilePath(self, templateName):
        return os.path.join(
            self.getTemplatesPath(), unicode(templateName) + self.EXT
        )

    def getTemplateList(self):
        templatesList = []
        for filename in os.listdir(self.getTemplatesPath()):
            name, ext = os.path.splitext(filename)
            if ext == self.EXT:
                templatesList.append(name)
        return templatesList

    def loadTemplate(self, templateName):
        # TODO: more cheks on struct!
        template = DatatypeTemplate()
        templateFile = QFile(self.getTemplateFilePath(templateName))

        xmlTemplate = QDomDocument()
        xmlTemplate.setContent(templateFile)

        root = xmlTemplate.documentElement()

        nameElement = root.elementsByTagName("Name").at(0)
        template.name = nameElement.childNodes().at(0).nodeValue()

        typeElement = root.elementsByTagName("Type").at(0)
        template.type = typeElement.childNodes().at(0).nodeValue()

        accuracyElement = root.elementsByTagName("Accuracy").at(0)
        template.accuracy = accuracyElement.childNodes().at(0).nodeValue()

        scaleElement = root.elementsByTagName("Scale").at(0)
        template.scale = scaleElement.childNodes().at(0).nodeValue()

        thematicAccuracyElement = root.elementsByTagName(
            "ThematicAccuracy"
        ).at(0)
        template.thematicAccuracy = (
            thematicAccuracyElement.childNodes().at(0).nodeValue()
        )

        template.keywords = []
        keywordsElements = root.elementsByTagName("Keyword")
        for number in range(keywordsElements.length()):
            template.keywords.append(
                keywordsElements.at(number).childNodes().at(0).nodeValue()
            )

        return template

    def saveTemplate(self, template):
        xmlTemplate = QDomDocument()

        # create root
        root = xmlTemplate.createElement("DatatypeTemplate")
        xmlTemplate.appendChild(root)

        # set name
        element = xmlTemplate.createElement("Name")
        textNode = xmlTemplate.createTextNode(template.name)
        element.appendChild(textNode)
        root.appendChild(element)

        # set type
        element = xmlTemplate.createElement("Type")
        textNode = xmlTemplate.createTextNode(template.type)
        element.appendChild(textNode)
        root.appendChild(element)

        # set accuracy
        element = xmlTemplate.createElement("Accuracy")
        textNode = xmlTemplate.createTextNode(template.accuracy)
        element.appendChild(textNode)
        root.appendChild(element)

        # set scale
        element = xmlTemplate.createElement("Scale")
        textNode = xmlTemplate.createTextNode(template.scale)
        element.appendChild(textNode)
        root.appendChild(element)

        # set thematicAccuracy
        element = xmlTemplate.createElement("ThematicAccuracy")
        textNode = xmlTemplate.createTextNode(template.thematicAccuracy)
        element.appendChild(textNode)
        root.appendChild(element)

        # set keywords
        for keyword in template.keywords:
            element = xmlTemplate.createElement("Keyword")
            textNode = xmlTemplate.createTextNode(keyword)
            element.appendChild(textNode)
            root.appendChild(element)

        templateFile = codecs.open(
            self.getTemplateFilePath(template.name), "w", encoding="utf-8"
        )
        templateFile.write(unicode(xmlTemplate.toString()))
        templateFile.close()

    def removeTemplate(self, templateName):
        os.remove(self.getTemplateFilePath(templateName))


class DatatypeTemplate:
    TYPES = {
        "vector": "Vector data",
        "image": "Imagery",
        "thematicClassification": "Thematic raster",
        "physicalMeasurement": "Physical measurement",
    }

    def __init__(
        self,
        name=None,
        type=None,
        accuracy=None,
        scale=None,
        keywords=[],
        thematicAccuracy=None,
    ):
        self.name = name
        self.type = type
        self.accuracy = accuracy
        self.scale = scale
        self.keywords = keywords
        self.thematicAccuracy = thematicAccuracy

    def stringRepresentation(self):
        return self.name + "::" + self.type
