# -*- coding: utf-8 -*-

# ******************************************************************************
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
# ******************************************************************************

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

import os

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "ui/settings.ui")
)

currentPath = os.path.abspath(os.path.dirname(__file__))


class MetatoolsSettings(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(MetatoolsSettings, self).__init__(parent)
        self.setupUi(self)

        self.settings = QSettings("NextGIS", "metatools")
        self.gbFGDCTools.setSettings(self.settings)

        self.manageGui()

        self.readSettings()

        self.btnSelectFilter.clicked.connect(self.updateFilter)
        self.btnSelectTkme.clicked.connect(self.selectTkme)
        self.btnSelectMp.clicked.connect(self.selectMp)
        self.btnSelectErr2Html.clicked.connect(self.selectErr2Html)

    def manageGui(self):
        # populate profiles combobox
        profilesDir = QDir(
            QDir.toNativeSeparators(os.path.join(currentPath, "xml_profiles"))
        )
        profilesDir.setFilter(
            QDir.Files | QDir.NoSymLinks | QDir.NoDotAndDotDot
        )
        fileFilter = ["*.xml", "*.XML"]
        profilesDir.setNameFilters(fileFilter)
        profiles = profilesDir.entryList()
        self.defaultProfileComboBox.addItems(profiles)

        # populate iso and fgdc stylesheet comboboxes
        xslDir = QDir(
            QDir.toNativeSeparators(os.path.join(currentPath, "xsl"))
        )
        xslDir.setFilter(QDir.Files | QDir.NoSymLinks | QDir.NoDotAndDotDot)
        fileFilter = ["*.xsl", "*.XSL"]
        xslDir.setNameFilters(fileFilter)
        xsls = xslDir.entryList()
        self.cmbIsoViewStylesheet.addItems(xsls)
        self.cmbFgdcViewStylesheet.addItems(xsls)

        # populate image format combobox
        formats = ["jpg", "tiff", "png", "bmp"]
        self.cmbImgFormat.addItems(formats)

    def readSettings(self):
        self.leFilterFileName.setText(
            self.settings.value("general/filterFile", "")
        )

        # restore default profile
        profile = self.settings.value("general/defaultProfile", "")
        self.defaultProfileComboBox.setCurrentIndex(
            self.defaultProfileComboBox.findText(profile)
        )

        # restore preview image format
        preview_format = self.settings.value("preview/format", "jpg")
        self.cmbImgFormat.setCurrentIndex(
            self.cmbImgFormat.findText(preview_format)
        )

        # restore iso stylesheet
        isoXsl = self.settings.value("iso19115/stylesheet", "iso19115.xsl")
        self.cmbIsoViewStylesheet.setCurrentIndex(
            self.cmbIsoViewStylesheet.findText(isoXsl)
        )

        # restore fgdc stylesheet
        fgdcXsl = self.settings.value("fgdc/stylesheet", "fgdc.xsl")
        self.cmbFgdcViewStylesheet.setCurrentIndex(
            self.cmbFgdcViewStylesheet.findText(fgdcXsl)
        )

        # FGDC tools
        self.leTkmePath.setText(self.settings.value("tools/tkme", ""))
        self.leMpPath.setText(self.settings.value("tools/mp", ""))
        self.leErr2HtmlPath.setText(self.settings.value("tools/err2html", ""))

    def updateFilter(self):
        fileName = QFileDialog.getOpenFileName(
            self,
            self.tr("Select filter"),
            ".",
            self.tr("Text files (*.txt *.TXT)"),
        )

        if fileName == "":
            return

        self.leFilterFileName.setText(fileName)

    def selectTkme(self):
        fileName = QFileDialog.getOpenFileName(
            self,
            self.tr("Select file"),
            ".",
            self.tr("Executable files (*.exe *.EXE);;All files (*)"),
        )

        if fileName == "":
            return

        self.leTkmePath.setText(fileName)

    def selectMp(self):
        fileName = QFileDialog.getOpenFileName(
            self,
            self.tr("Select file"),
            ".",
            self.tr("Executable files (*.exe *.EXE);;All files (*)"),
        )

        if fileName == "":
            return

        self.leMpPath.setText(fileName)

    def selectErr2Html(self):
        fileName = QFileDialog.getOpenFileName(
            self,
            self.tr("Select file"),
            ".",
            self.tr("Executable files (*.exe *.EXE);;All files (*)"),
        )

        if fileName == "":
            return

        self.leErr2HtmlPath.setText(fileName)

    def accept(self):
        # save settings
        self.settings.setValue(
            "general/filterFile", self.leFilterFileName.text()
        )

        self.settings.setValue(
            "general/defaultProfile", self.defaultProfileComboBox.currentText()
        )

        self.settings.setValue(
            "preview/format", self.cmbImgFormat.currentText()
        )

        self.settings.setValue(
            "iso19115/stylesheet", self.cmbIsoViewStylesheet.currentText()
        )

        self.settings.setValue(
            "fgdc/stylesheet", self.cmbFgdcViewStylesheet.currentText()
        )

        self.settings.setValue("tools/hasFGDC", self.gbFGDCTools.isChecked())
        self.settings.setValue("tools/tkme", self.leTkmePath.text())
        self.settings.setValue("tools/mp", self.leMpPath.text())
        self.settings.setValue("tools/err2html", self.leErr2HtmlPath.text())

        # close dialog
        QDialog.accept(self)
