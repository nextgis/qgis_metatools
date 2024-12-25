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
from PyQt4.QtXml import *
from PyQt4.QtXmlPatterns import *

from qgis.core import *
from qgis.gui import *

import os

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "ui/organization_editor.ui")
)
from organization_template_manager import (
    OrganizationTemplateManager,
    OrganizationTemplate,
)

currentPath = os.path.abspath(os.path.dirname(__file__))


class OrganizationEditorDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(OrganizationEditorDialog, self).__init__(parent)
        self.setupUi(self)

        path = os.path.join(currentPath, "templates/institutions.xml")
        self.orgTemplateManager = OrganizationTemplateManager(path)
        self.orgTemplate = OrganizationTemplate()

        self.btnSave = self.buttonBox.button(QDialogButtonBox.Save)
        self.btnClose = self.buttonBox.button(QDialogButtonBox.Close)

        self.btnNew.clicked.connect(self.newOrganization)
        self.btnRemove.clicked.connect(self.removeOrganization)

        self.leName.textEdited.connect(self.templateModified)
        self.leDeliveryPoint.textEdited.connect(self.templateModified)
        self.leCity.textEdited.connect(self.templateModified)
        self.leAdminArea.textEdited.connect(self.templateModified)
        self.lePostCode.textEdited.connect(self.templateModified)
        self.leCountry.textEdited.connect(self.templateModified)
        self.lePhone.textEdited.connect(self.templateModified)
        self.leFax.textEdited.connect(self.templateModified)
        self.leEmail.textEdited.connect(self.templateModified)
        self.leContactPerson.textEdited.connect(self.templateModified)
        self.lePersonTitle.textEdited.connect(self.templateModified)
        self.lePersonPosition.textEdited.connect(self.templateModified)
        self.leOfficeHours.textEdited.connect(self.templateModified)

        self.cmbOrganization.currentIndexChanged.connect(
            self.organizationChanged
        )

        self.buttonBox.accepted.disconnect(self.accept)
        self.btnSave.clicked.connect(self.saveTemplate)

        self.manageGui()

    def manageGui(self):
        self.btnRemove.setEnabled(False)
        self.reloadTemplatesList()
        self.btnSave.setEnabled(False)

    def reloadTemplatesList(self):
        self.cmbOrganization.clear()
        self.cmbOrganization.addItems(self.orgTemplateManager.tempalateNames())

    def newOrganization(self):
        if (
            self.btnSave.isEnabled()
            and QMessageBox.question(
                None,
                self.tr("Metatools"),
                self.tr(
                    "Template contains unsaved data. Create new template without saving?"
                ),
                QMessageBox.Yes | QMessageBox.No,
            )
            == QMessageBox.No
        ):
            return
        self.clearFormFields()
        self.orgTemplate = OrganizationTemplate()
        self.btnSave.setEnabled(False)

    def removeOrganization(self):
        self.orgTemplateManager.removeTemplate(
            self.cmbOrganization.currentText()
        )
        self.reloadTemplatesList()

        if self.cmbOrganization.count() == 0:
            self.clearFormFields()

    # enable save button when template edited
    def templateModified(self):
        self.btnSave.setEnabled(True)

    def organizationChanged(self):
        templateName = self.cmbOrganization.currentText()
        if templateName == "":
            self.orgTemplate = OrganizationTemplate()
            self.btnRemove.setEnabled(False)
            return

        self.orgTemplate = self.orgTemplateManager.organizations[templateName]
        self.templateToForm(self.orgTemplate)
        self.btnSave.setEnabled(False)
        self.btnRemove.setEnabled(True)

    def saveTemplate(self):
        template = self.templateFromForm()

        self.orgTemplateManager.addTemplate(template.name, template)
        self.orgTemplateManager.saveTemplates()

        # reload form
        self.reloadTemplatesList()

        # set combobox item
        index = self.cmbOrganization.findText(template.name)
        if index != -1:
            self.cmbOrganization.setCurrentIndex(index)

        self.btnSave.setEnabled(False)

    def clearFormFields(self):
        self.leName.clear()
        self.leDeliveryPoint.clear()
        self.leCity.clear()
        self.leAdminArea.clear()
        self.lePostCode.clear()
        self.leCountry.clear()
        self.lePhone.clear()
        self.leFax.clear()
        self.leEmail.clear()
        self.leContactPerson.clear()
        self.lePersonTitle.clear()
        self.lePersonPosition.clear()
        self.leOfficeHours.clear()

    # populate form with template data
    def templateToForm(self, template):
        self.leName.setText(template.name or "")
        self.leDeliveryPoint.setText(template.deliveryPoint or "")
        self.leCity.setText(template.city or "")
        self.leAdminArea.setText(template.adminArea or "")
        self.lePostCode.setText(template.postalCode or "")
        self.leCountry.setText(template.country or "")
        self.lePhone.setText(template.phone or "")
        self.leFax.setText(template.fax or "")
        self.leEmail.setText(template.email or "")
        self.leContactPerson.setText(template.person or "")
        self.lePersonTitle.setText(template.title or "")
        self.lePersonPosition.setText(template.position or "")
        self.leOfficeHours.setText(template.hours or "")

    # create template from entered values
    def templateFromForm(self):
        template = OrganizationTemplate()
        template.name = self.leName.text()
        template.deliveryPoint = self.leDeliveryPoint.text()
        template.city = self.leCity.text()
        template.adminArea = self.leAdminArea.text()
        template.postalCode = self.lePostCode.text()
        template.country = self.leCountry.text()
        template.phone = self.lePhone.text()
        template.fax = self.leFax.text()
        template.email = self.leEmail.text()
        template.person = self.leContactPerson.text()
        template.title = self.lePersonTitle.text()
        template.position = self.lePersonPosition.text()
        template.hours = self.leOfficeHours.text()
        return template

    def reject(self):
        if (
            self.btnSave.isEnabled()
            and QMessageBox.question(
                None,
                self.tr("Metatools"),
                self.tr(
                    "Template contains unsaved data. Close the window without saving?"
                ),
                QMessageBox.Yes | QMessageBox.No,
            )
            == QMessageBox.No
        ):
            return
        QDialog.reject(self)

    def accept(self):
        QDialog.accept(self)
