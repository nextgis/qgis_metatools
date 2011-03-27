"""
/***************************************************************************
 MetatoolsSettings
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os

from ui_settings import Ui_MetatoolsSettingsDialog

currentPath = os.path.abspath( os.path.dirname( __file__ ) )

class MetatoolsSettings(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_MetatoolsSettingsDialog()
        self.ui.setupUi(self)

        self.manageGui()

        self.readSettings()

        self.connect(self.ui.btnSelectFilter, SIGNAL("clicked()"), self.updateFilter)

    def manageGui( self ):
        # populate profiles combobox
        profilesDir = QDir( QDir.toNativeSeparators( os.path.join( currentPath, "xml_profiles" ) ) )
        profilesDir.setFilter( QDir.Files | QDir.NoSymLinks | QDir.NoDotAndDotDot )
        fileFilter = QStringList() << "*.xml" << "*.XML"
        profilesDir.setNameFilters( fileFilter )
        profiles = profilesDir.entryList()
        self.ui.defaultProfileComboBox.addItems( profiles )

    def readSettings( self ):
        settings = QSettings( "NextGIS", "metatools" )
        self.ui.leFilterFileName.setText( settings.value( "general/filterFile", QVariant() ).toString() )

        # restore default profile
        profile = settings.value( "iso19115/defaultProfile", QVariant() ).toString()
        self.ui.defaultProfileComboBox.setCurrentIndex( self.ui.defaultProfileComboBox.findText( profile ) )


    def updateFilter( self ):
        fileName = QFileDialog.getOpenFileName( self, self.tr( 'Select filter' ), '.', self.tr( 'Text files (*.txt *.TXT)' ) )

        if fileName.isEmpty():
            return

        self.ui.leFilterFileName.setText( fileName )

    def accept( self ):
        # save settings
        settings = QSettings( "NextGIS", "metatools" )
        settings.setValue( "general/filterFile", self.ui.leFilterFileName.text() )

        settings.setValue( "iso19115/defaultProfile",  self.ui.defaultProfileComboBox.currentText()  )

        # close dialog
        QDialog.accept( self )
