"""
/***************************************************************************
 Metatools
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


# Initialize Qt resources from file resources.py
import resources

# Import the code for the dialog
from metatoolsdialog import MetatoolsDialog

class MetatoolsPlugin:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        # Get QGIS version
        try:
            self.QgisVersion = unicode(QGis.QGIS_VERSION_INT)
        except:
            self.QgisVersion = unicode(QGis.qgisVersion)[ 0 ]

        # i18n support
        userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/Metatools"
        systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/Metatools"

        overrideLocale = QSettings().value("locale/overrideFlag", QVariant(False)).toBool()
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value("locale/userLocale", QVariant("")).toString()

        if QFileInfo(userPluginPath).exists():
            translationPath = userPluginPath + "/i18n/metatools_" + localeFullName + ".qm"
        else:
            translationPath = systemPluginPath + "/i18n/metatools_" + localeFullName + ".qm"

        self.localePath = translationPath
        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)




    def initGui(self):
        # Create editAction that will start plugin configuration
        self.editAction = QAction(QIcon(":/icon.png"), QCoreApplication.translate("Metatools", "Edit metadata"), self.iface.mainWindow())
        # connect the editAction to the doEdit method
        QObject.connect(self.editAction, SIGNAL("triggered()"), self.doEdit)

        # Create viewAction that will start plugin configuration
        self.viewAction = QAction(QIcon(":/python/plugins/Metatools/icon.png"), QCoreApplication.translate("Metatools", "View metadata"), self.iface.mainWindow())
        # connect the viewAction to the doView method
        QObject.connect(self.viewAction, SIGNAL("triggered()"), self.doView)

        # Create configAction that will start plugin configuration
        self.configAction = QAction(QIcon(":/icon.png"), QCoreApplication.translate("Metatools", "Configure metadata plugin"), self.iface.mainWindow())
        # connect the configAction to the doConfigure method
        QObject.connect(self.configAction, SIGNAL("triggered()"), self.doConfigure)

        # Add menu item
        self.iface.addPluginToMenu("&Metatools", self.editAction)
        self.iface.addPluginToMenu("&Metatools", self.viewAction)
        self.iface.addPluginToMenu("&Metatools", self.configAction)

        # Add toolbar
        self.toolBar = self.iface.addToolBar(QCoreApplication.translate("Metatools", "Metatools"))
        self.toolBar.setObjectName(QCoreApplication.translate("Metatools", "Metatools"))

        self.toolBar.addAction(self.editAction)
        self.toolBar.addAction(self.viewAction)
        self.toolBar.addAction(self.configAction)



    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&Metatools", self.editAction)
        self.iface.removePluginMenu("&Metatools", self.viewAction)
        self.iface.removePluginMenu("&Metatools", self.configAction)
        del self.toolBar

    # run method that performs all the real work
    def doEdit(self):
        # create and show the dialog
        dlg = MetatoolsDialog()
        # show the dialog
        dlg.show()
        result = dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code
            pass

    # run method that performs all the real work
    def doView(self):
        # create and show the dialog
        dlg = MetatoolsDialog()
        # show the dialog
        dlg.show()
        result = dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code
            pass

    # run method that performs all the real work
    def doConfigure(self):
        # create and show the dialog
        dlg = MetatoolsDialog()
        # show the dialog
        dlg.show()
        result = dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code
            pass
