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

from qgis.core import *

import os, sys, shutil

import utils
from standard import MetaInfoStandard

from metatoolssettings import MetatoolsSettings

import resources

minQtVersion = '4.6.0'
currentPath = os.path.abspath( os.path.dirname( __file__ ) )

class MetatoolsPlugin:
  def __init__( self, iface ):
    self.iface = iface

    try:
      self.QgisVersion = unicode( QGis.QGIS_VERSION_INT )
    except:
      self.QgisVersion = unicode( QGis.qgisVersion )[ 0 ]

    # Get plugin folder
    userPluginPath = QFileInfo( QgsApplication.qgisUserDbFilePath() ).path() + "/python/plugins/metatools"
    systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/metatools"

    if QFileInfo( userPluginPath ).exists():
      self.pluginPath = userPluginPath
    else:
      self.pluginPath = systemPluginPath

    # i18n support
    overrideLocale = QSettings().value( "locale/overrideFlag", QVariant( False ) ).toBool()
    if not overrideLocale:
      localeFullName = QLocale.system().name()
    else:
      localeFullName = QSettings().value( "locale/userLocale", QVariant("") ).toString()

    self.localePath = self.pluginPath + "/i18n/metatools_" + localeFullName + ".qm"

    if QFileInfo( self.localePath ).exists():
      self.translator = QTranslator()
      self.translator.load( self.localePath )
      QCoreApplication.installTranslator( self.translator )

  def initGui( self ):
    if int( self.QgisVersion ) < 10500:
      QMessageBox.warning( self.iface.mainWindow(), "Metatools",
                           QCoreApplication.translate( "Metatools", "Quantum GIS version detected: %1.%2\n" ).arg( self.QgisVersion )[ 0 ] ).arg( self.QgisVersion )[ 2 ] ) +
                           QCoreApplication.translate( "Metatools", "This version of Metatools requires at least QGIS version 1.5.0\nPlugin will not be enabled." ) )
      return None

    # Create editAction that will start editor window
    self.editAction = QAction( QIcon( ":/plugins/metatools/icons/edit.png" ), QCoreApplication.translate( "Metatools", "Edit metadata" ), self.iface.mainWindow() )
    self.editAction.setStatusTip( QCoreApplication.translate( "Metatools", "Edit metadata" ) )
    self.editAction.setWhatsThis( QCoreApplication.translate( "Metatools", "Edit metadata" ) )

    # Create applyTemplateAction that will start templates window
    self.applyTemplatesAction = QAction( QIcon( ":/plugins/metatools/icons/templates.png" ), QCoreApplication.translate( "Metatools", "Apply templates" ), self.iface.mainWindow() )
    self.applyTemplatesAction.setStatusTip( QCoreApplication.translate( "Metatools", "Edit and apply templates" ) )
    self.applyTemplatesAction.setWhatsThis( QCoreApplication.translate( "Metatools", "Edit and apply templates" ) )

    # Create viewAction that will start viewer window
    self.viewAction = QAction( QIcon( ":/plugins/metatools/icons/view.png" ), QCoreApplication.translate( "Metatools", "View metadata" ), self.iface.mainWindow() )
    self.viewAction.setStatusTip( QCoreApplication.translate( "Metatools", "View metadata" ) )
    self.viewAction.setWhatsThis( QCoreApplication.translate( "Metatools", "View metadata" ) )

    # Create configAction that will start plugin configuration
    self.configAction = QAction( QIcon( ":/plugins/metatools/icons/settings.png" ), QCoreApplication.translate( "Metatools", "Configure Metatools plugin" ), self.iface.mainWindow() )
    self.configAction.setStatusTip( QCoreApplication.translate( "Metatools", "Сonfigure plugin" ) )
    self.configAction.setWhatsThis( QCoreApplication.translate( "Metatools", "Configure plugin" ) )

    QObject.connect( self.editAction, SIGNAL( "triggered()" ), self.doEdit )
    QObject.connect( self.applyTemplatesAction, SIGNAL( "triggered()" ), self.doApplyTemplates )
    QObject.connect( self.viewAction, SIGNAL( "triggered()" ), self.doView )
    QObject.connect( self.configAction, SIGNAL( "triggered()" ), self.doConfigure )

    # Add menu items
    self.iface.addPluginToMenu( "Metatools", self.viewAction )
    self.iface.addPluginToMenu( "Metatools", self.editAction )
    self.iface.addPluginToMenu( "Metatools", self.applyTemplatesAction )
    self.iface.addPluginToMenu( "Metatools", self.configAction )

    # Add toolbar and buttons
    self.toolBar = self.iface.addToolBar( QCoreApplication.translate( "Metatools", "Metatools" ) )
    self.toolBar.setObjectName( QCoreApplication.translate( "Metatools", "Metatools" ) )

    self.toolBar.addAction( self.viewAction )
    self.toolBar.addAction( self.editAction )
    self.toolBar.addAction( self.applyTemplatesAction )
    self.toolBar.addAction( self.configAction )

  def unload( self ):
    # Remove the plugin menu items and toolbar
    self.iface.removePluginMenu( "Metatools", self.editAction )
    self.iface.removePluginMenu( "Metatools", self.applyTemplatesAction )
    self.iface.removePluginMenu( "Metatools", self.viewAction )
    self.iface.removePluginMenu( "Metatools", self.configAction )

    del self.toolBar

  # Edit metadata
  def doEdit( self ):
    try:
      from metatoolseditor import MetatoolsEditor
    except:
      QMessageBox.critical( self.iface.mainWindow(),
                            QCoreApplication.translate( "Metatools", "Metatools" ),
                            QCoreApplication.translate( "Metatools", "Plugin can't be loaded: Qt version must be higher than %1!\nCurrently running: %2" )
                            .arg( minQtVersion )
                            .arg( qVersion() ) )
      return

    # get active layer
    layer = self.iface.activeLayer()
    if not layer:
      QMessageBox.information( self.iface.mainWindow(),
                               QCoreApplication.translate( "Metatools", "Metatools" ),
                               QCoreApplication.translate( "Metatools", "Choose any map layer" ) )
      return

    # check layer type
    if layer.type() == QgsMapLayer.VectorLayer:
      QMessageBox.warning( self.iface.mainWindow(),
                           QCoreApplication.translate( "Metatools", "Metatools" ),
                           QCoreApplication.translate( "Metatools", "Vector layers are not supported yet!" ) )
      return

    if layer.type() != QgsMapLayer.RasterLayer:
      QMessageBox.critical( self.iface.mainWindow(),
                            QCoreApplication.translate( "Metatools", "Metatools" ),
                            QCoreApplication.translate( "Metatools", "Unknow layer type!" ) )
      return

    #TODO: check layer DS type (local, DB, service)

    # get metafile path
    metaFilePath = utils.getMetafilePath( layer )

    # check if metadata file exists
    if not os.path.exists( metaFilePath ):
      result = QMessageBox.question( self.iface.mainWindow(),
                                     QCoreApplication.translate( "Metatools", "Metatools" ),
                                     QCoreApplication.translate( "Metatools", "The layer does not have metadata! Create metadata file?"),
                                     QDialogButtonBox.Yes, QDialogButtonBox.No )
      if result == QDialogButtonBox.Yes:
        try:
          settings = QSettings( "NextGIS", "metatools" )
          profile = settings.value( "iso19115/defaultProfile", QVariant( "" ) ).toString()
          if profile.isEmpty():
            QMessageBox.warning( self, self.tr( "No profile" ), self.tr( "No profile selected. Please set default profile in plugin settings" ) )
            return

          profilePath = QDir( QDir.toNativeSeparators( os.path.join( currentPath, "xml_profiles", str( profile ) ) ) ).absolutePath()
          shutil.copyfile( str( profilePath ), metaFilePath )
        except:
          QMessageBox.warning( self.iface.mainWindow(),
                               QCoreApplication.translate( "Metatools", "Metatools" ),
                               QCoreApplication.translate( "Metatools", "Metadata file can't be created: " ) + str( sys.exc_info()[ 1 ] ) )
          return
      else:
        return

    # check matadata standard
    standard = MetaInfoStandard.tryDetermineStandard( metaFilePath )
    if standard != MetaInfoStandard.ISO19115:
      QMessageBox.critical( self.iface.mainWindow(),
                            QCoreApplication.translate( "Metatools", "Metatools" ),
                            QCoreApplication.translate( "Metatools", "Unsupported metadata standard! Only ISO19115 supported now!" ) )
      return

    dlg = MetatoolsEditor()
    dlg.setContent( metaFilePath )
    dlg.exec_()

  #### NEED REMOVE COMMON CODE!

  # View metadata
  def doView(self):
    try:
      from metatoolsviewer import MetatoolsViewer
    except:
      QMessageBox.critical( self.iface.mainWindow(),
                            QCoreApplication.translate( "Metatools", "Metatools" ),
                            QCoreApplication.translate( "Metatools", "Plugin can't be loaded: Qt version must be higher than %1!\nCurrently running: %2" )
                            .arg( minQtVersion )
                            .arg( qVersion() ) )
      return

    # get active layer
    layer = self.iface.activeLayer()
    if not layer:
      QMessageBox.information( self.iface.mainWindow(),
                               QCoreApplication.translate( "Metatools", "Metatools" ),
                               QCoreApplication.translate( "Metatools", "Choose any map layer" ) )
      return

    # check layer type
    if layer.type() == QgsMapLayer.VectorLayer:
      QMessageBox.warning( self.iface.mainWindow(),
                           QCoreApplication.translate( "Metatools", "Metatools" ),
                           QCoreApplication.translate( "Metatools", "Vector layers are not supported yet!" ) )
      return

    if layer.type() != QgsMapLayer.RasterLayer:
      QMessageBox.critical( self.iface.mainWindow(),
                            QCoreApplication.translate( "Metatools", "Metatools" ),
                            QCoreApplication.translate( "Metatools", "Unknow layer type!" ) )
      return

    #TODO: check layer DS type (local, DB, service)

    # get metafile path
    metaFilePath = utils.getMetafilePath( layer )

    # check if metadata file exists
    if not os.path.exists( metaFilePath ):
      result = QMessageBox.question( self.iface.mainWindow(),
                                     QCoreApplication.translate( "Metatools", "Metatools" ),
                                     QCoreApplication.translate( "Metatools", "The layer does not have metadata! Create metadata file?" ),
                                     QDialogButtonBox.Yes, QDialogButtonBox.No )
      if result == QDialogButtonBox.Yes:
        try:
          settings = QSettings( "NextGIS", "metatools" )
          profile = settings.value( "iso19115/defaultProfile", QVariant( "" ) ).toString()
          if profile.isEmpty():
            QMessageBox.warning( self, self.tr( "No profile" ), self.tr( "No profile selected. Please set default profile in plugin settings" ) )
            return

          profilePath = QDir( QDir.toNativeSeparators( os.path.join( currentPath, "xml_profiles", str( profile ) ) ) ).absolutePath()
          shutil.copyfile( str( profilePath ), metaFilePath )
        except:
          QMessageBox.warning( self.iface.mainWindow(),
                               QCoreApplication.translate( "Metatools", "Metatools" ),
                               QCoreApplication.translate( "Metatools", "Metadata file can't be created: " ) + str( sys.exc_info()[ 1 ] ) )
          return
      else:
        return

    # check matadata standard
    standard = MetaInfoStandard.tryDetermineStandard( metaFilePath )
    if standard != MetaInfoStandard.ISO19115:
      QMessageBox.critical( self.iface.mainWindow(),
                            QCoreApplication.translate( "Metatools", "Metatools" ),
                            QCoreApplication.translate( "Metatools", "Unsupported metadata standard! Only ISO19115 supported now!" ) )
      return

    # TODO: validate metadata file

    # get xsl file path
    # TODO: select xls by metadata type and settings
    xsltFilePath = self.pluginPath + '/xsl/iso19115.xsl'

    dlg = MetatoolsViewer()
    dlg.setContent( metaFilePath, xsltFilePath )
    dlg.exec_()

  def doApplyTemplates( self ):
    try:
      from apply_templates_dialog import ApplyTemplatesDialog
    except ImportError:
      QMessageBox.critical( self.iface.mainWindow(),
                            QCoreApplication.translate( "Metatools", "Metatools"),
                            QCoreApplication.translate( "Metatools", "Plugin can't be loaded: Qt version must be higher than %1! Currently running: %2")
                            .arg( minQtVersion )
                            .arg( qVersion() ) )
      return

    mapLayers = QgsMapLayerRegistry.instance().mapLayers()

    dlg = ApplyTemplatesDialog( self.pluginPath, mapLayers )
    dlg.exec_()

  def doConfigure( self ):
    dlg = MetatoolsSettings()
    dlg.exec_()
