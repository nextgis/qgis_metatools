# -*- coding: utf-8 -*-

#******************************************************************************
#
# Metatools
# ---------------------------------------------------------
# Metadata browser/editor
#
# Copyright (C) 2011 BV (enickulin@bv.com)
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
from qgis.gui import *

import os, sys, shutil

from metatoolssettings import MetatoolsSettings
from standard import MetaInfoStandard
from error_handler import ErrorHandler
from metadata_provider import MetadataProvider

import utils
import resources_rc

minQtVersion = '4.6.0'
currentPath = os.path.abspath(os.path.dirname(__file__))


class MetatoolsPlugin:
  def __init__(self, iface):
    self.iface = iface
    self.loadingCanceled = False

    try:
      self.QgisVersion = unicode(QGis.QGIS_VERSION_INT)
    except:
      self.QgisVersion = unicode(QGis.qgisVersion)[ 0 ]

    # get plugin folder (more simple version of original plugin)
    self.pluginPath = currentPath

    # i18n support
    overrideLocale = QSettings().value("locale/overrideFlag", QVariant(False)).toBool()
    if not overrideLocale:
      localeFullName = QLocale.system().name()
    else:
      localeFullName = QSettings().value("locale/userLocale", QVariant("")).toString()

    self.localePath = self.pluginPath + "/i18n/metatools_" + localeFullName[0:2] + ".qm"

    if QFileInfo(self.localePath).exists():
      self.translator = QTranslator()
      self.translator.load(self.localePath)
      QCoreApplication.installTranslator(self.translator)

  def initGui(self):
    if int(self.QgisVersion) < 10500:
      QMessageBox.warning(self.iface.mainWindow(), "Metatools",
                           QCoreApplication.translate("Metatools", "Quantum GIS version detected: %1.%2\n").arg(self.QgisVersion[ 0 ]).arg(self.QgisVersion[ 2 ]) +
                           QCoreApplication.translate("Metatools", "This version of Metatools requires at least QGIS version 1.5.0\nPlugin will not be enabled."))
      self.loadingCanceled = True
      return None

    if qVersion() < minQtVersion:
      QMessageBox.warning(self.iface.mainWindow(), "Metatools",
                          QCoreApplication.translate("Metatools", "Qt version detected: %1\n").arg(qVersion()) +
                          QCoreApplication.translate("Metatools", "This version of Metatools requires at least Qt version %1\nPlugin will not be enabled.").arg(minQtVersion))
      self.loadingCanceled = True
      return None

    # create editAction that will start metadata editor
    self.editAction = QAction(QIcon(":/plugins/metatools/icons/edit.png"), QCoreApplication.translate("Metatools", "Edit metadata"), self.iface.mainWindow())
    self.editAction.setStatusTip(QCoreApplication.translate("Metatools", "Edit metadata"))
    self.editAction.setWhatsThis(QCoreApplication.translate("Metatools", "Edit metadata"))

    # create applyTemplateAction that will start templates manager
    self.applyTemplatesAction = QAction(QIcon(":/plugins/metatools/icons/templates.png"), QCoreApplication.translate("Metatools", "Apply templates"), self.iface.mainWindow())
    self.applyTemplatesAction.setStatusTip(QCoreApplication.translate("Metatools", "Edit and apply templates"))
    self.applyTemplatesAction.setWhatsThis(QCoreApplication.translate("Metatools", "Edit and apply templates"))

    # create viewAction that will start metadata viewer
    self.viewAction = QAction(QIcon(":/plugins/metatools/icons/view.png"), QCoreApplication.translate("Metatools", "View metadata"), self.iface.mainWindow())
    self.viewAction.setStatusTip(QCoreApplication.translate("Metatools", "View metadata"))
    self.viewAction.setWhatsThis(QCoreApplication.translate("Metatools", "View metadata"))

    # create configAction that will start plugin configuration
    self.configAction = QAction(QIcon(":/plugins/metatools/icons/settings.png"), QCoreApplication.translate("Metatools", "Configure Metatools plugin"), self.iface.mainWindow())
    self.configAction.setStatusTip(QCoreApplication.translate("Metatools", "Configure plugin"))
    self.configAction.setWhatsThis(QCoreApplication.translate("Metatools", "Configure plugin"))

    # create configAction that will start plugin configuration
    self.validateAction = QAction(QIcon(":/plugins/metatools/icons/check.png"), QCoreApplication.translate("Metatools", "Validate metadata"), self.iface.mainWindow())
    self.validateAction.setStatusTip(QCoreApplication.translate("Metatools", "Validate metadata"))
    self.validateAction.setWhatsThis(QCoreApplication.translate("Metatools", "Validate metadata"))


    # create configAction that will start plugin configuration
    self.usgsAction = QAction(QIcon(":/plugins/metatools/icons/usgs.png"), QCoreApplication.translate("Metatools", "USGS Tool"), self.iface.mainWindow())
    self.usgsAction.setStatusTip(QCoreApplication.translate("Metatools", "USGS Tool"))
    self.usgsAction.setWhatsThis(QCoreApplication.translate("Metatools", "USGS Tool"))

    # create configAction that will start plugin configuration
    self.mpAction = QAction(QIcon(":/plugins/metatools/icons/usgs_check.png"), QCoreApplication.translate("Metatools", "MP Tool"), self.iface.mainWindow())
    self.mpAction.setStatusTip(QCoreApplication.translate("Metatools", "MP Tool"))
    self.mpAction.setWhatsThis(QCoreApplication.translate("Metatools", "MP Tool"))

    self.importAction = QAction(QIcon(":/plugins/metatools/icons/import.png"), QCoreApplication.translate("Metatools", "Import metadata"), self.iface.mainWindow())
    self.importAction.setStatusTip(QCoreApplication.translate("Metatools", "Import metadata from file"))
    self.importAction.setWhatsThis(QCoreApplication.translate("Metatools", "Import metadata"))

    self.exportAction = QAction(QIcon(":/plugins/metatools/icons/export.png"), QCoreApplication.translate("Metatools", "Export metadata"), self.iface.mainWindow())
    self.exportAction.setStatusTip(QCoreApplication.translate("Metatools", "Export metadata"))
    self.exportAction.setWhatsThis(QCoreApplication.translate("Metatools", "Export metadata to file"))

    self.metaBrowserAction = QAction(QIcon(":/plugins/metatools/icons/view.png"), QCoreApplication.translate("Metatools", "Metadata browser"), self.iface.mainWindow())
    self.metaBrowserAction.setStatusTip(QCoreApplication.translate("Metatools", "Metadata browser"))
    self.metaBrowserAction.setWhatsThis(QCoreApplication.translate("Metatools", "Metadata browser"))



    QObject.connect(self.editAction, SIGNAL("triggered()"), self.doEdit)
    QObject.connect(self.applyTemplatesAction, SIGNAL("triggered()"), self.doApplyTemplates)
    QObject.connect(self.viewAction, SIGNAL("triggered()"), self.doView)
    QObject.connect(self.configAction, SIGNAL("triggered()"), self.doConfigure)
    QObject.connect(self.validateAction, SIGNAL("triggered()"), self.validateMetadataFile)
    QObject.connect(self.usgsAction, SIGNAL("triggered()"), self.execUsgs)
    QObject.connect(self.mpAction, SIGNAL("triggered()"), self.execMp)
    QObject.connect(self.importAction, SIGNAL("triggered()"), self.doImport)
    QObject.connect(self.exportAction, SIGNAL("triggered()"), self.doExport)


    # add menu items
    self.iface.addPluginToMenu("Metatools", self.usgsAction)
    self.iface.addPluginToMenu("Metatools", self.mpAction)
    self.iface.addPluginToMenu("Metatools", self.importAction)
    self.iface.addPluginToMenu("Metatools", self.exportAction)
    self.iface.addPluginToMenu("Metatools", self.viewAction)
    self.iface.addPluginToMenu("Metatools", self.editAction)
    self.iface.addPluginToMenu("Metatools", self.validateAction)
    self.iface.addPluginToMenu("Metatools", self.applyTemplatesAction)
    self.iface.addPluginToMenu("Metatools", self.configAction)


    # add toolbar and buttons
    self.toolBar = self.iface.addToolBar(QCoreApplication.translate("Metatools", "Metatools"))
    self.toolBar.setObjectName(QCoreApplication.translate("Metatools", "Metatools"))

    self.toolBar.addAction(self.usgsAction)
    self.toolBar.addAction(self.mpAction)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.importAction)
    self.toolBar.addAction(self.exportAction)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.viewAction)
    self.toolBar.addAction(self.editAction)
    self.toolBar.addAction(self.validateAction)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.applyTemplatesAction)
    self.toolBar.addAction(self.configAction)


    # track layer changing
    QObject.connect(self.iface, SIGNAL("currentLayerChanged( QgsMapLayer* )"), self.layerChanged)

    # disable some actions when there is no active layer
    self.layer = None
    self.disableLayerActions()

    # check already selected layers
    self.layerChanged()

  def unload(self):
    if self.loadingCanceled:
      return

    # disconnect signals
    QObject.disconnect(self.iface, SIGNAL("currentLayerChanged( QgsMapLayer* )"), self.layerChanged)

    # remove the plugin menu items and toolbar
    self.iface.removePluginMenu("Metatools", self.editAction)
    self.iface.removePluginMenu("Metatools", self.applyTemplatesAction)
    self.iface.removePluginMenu("Metatools", self.viewAction)
    self.iface.removePluginMenu("Metatools", self.configAction)
    self.iface.removePluginMenu("Metatools", self.validateAction)
    self.iface.removePluginMenu("Metatools", self.usgsAction)
    self.iface.removePluginMenu("Metatools", self.mpAction)
    self.iface.removePluginMenu("Metatools", self.importAction)
    self.iface.removePluginMenu("Metatools", self.exportAction)

    del self.toolBar

  def layerChanged(self):
    self.layer = self.iface.activeLayer()

    # check layer type - return (True/False, Desc)
    res = MetadataProvider.IsLayerSupport(self.layer)

    #print "Metatools debug: ", res[1] # debug

    if not res[0]:
      self.disableLayerActions()
      self.layer = None
      self.metaProvider = None
    else:
      self.enableLayerActions()
      self.metaProvider = MetadataProvider.getProvider(self.layer)
      # self.metaFilePath = utils.getMetafilePath(self.layer)



  def disableLayerActions(self):
    self.viewAction.setEnabled(False)
    self.editAction.setEnabled(False)
    self.usgsAction.setEnabled(False)
    self.mpAction.setEnabled(False)
    self.validateAction.setEnabled(False)
    self.importAction.setEnabled(False)
    self.exportAction.setEnabled(False)

  def enableLayerActions(self):
    self.viewAction.setEnabled(True)
    self.editAction.setEnabled(True)
    self.usgsAction.setEnabled(True)
    self.mpAction.setEnabled(True)
    self.validateAction.setEnabled(True)
    self.importAction.setEnabled(True)
    self.exportAction.setEnabled(True)



  def doEdit(self):
    try:
      from metatoolseditor import MetatoolsEditor
    except:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Editor can't be loaded: %1 %2!")
                            .arg(unicode(sys.exc_info()[0]))
                            .arg(unicode(sys.exc_info()[1])))
      return

    # check if metadata file exists
    if not self.checkMetadata():
      return

    # check matadata standard
    standard = MetaInfoStandard.tryDetermineStandard(self.metaProvider)
    if standard != MetaInfoStandard.ISO19115 and standard != MetaInfoStandard.FGDC:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Unsupported metadata standard! Only ISO19115 and FGDC supported now!"))
      return

    dlg = MetatoolsEditor()
    dlg.setContent(self.metaProvider)
    dlg.exec_()


  def doConfigure(self):
    dlg = MetatoolsSettings()
    dlg.exec_()
    
  
  def doApplyTemplates(self):
    try:
      from apply_templates_dialog import ApplyTemplatesDialog
    except ImportError:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Applyer can't be loaded: %1 %2!")
                            .arg(unicode(sys.exc_info()[0]))
                            .arg(unicode(sys.exc_info()[1])))
      return
    dlg = ApplyTemplatesDialog(self.iface)
    dlg.exec_()


  def doView(self):
    try:
      from metatoolsviewer import MetatoolsViewer
    except:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Viewer can't be loaded: %1 %2!")
                            .arg(unicode(sys.exc_info()[0]))
                            .arg(unicode(sys.exc_info()[1])))
      return

    # check metadata exists
    if not self.checkMetadata():
      return

    # check matadata standard
    standard = MetaInfoStandard.tryDetermineStandard(self.metaProvider)
    if standard != MetaInfoStandard.ISO19115 and standard != MetaInfoStandard.FGDC:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Unsupported metadata standard! Only ISO19115 and FGDC supported now!"))
      return

    # TODO: validate metadata file

    # get xsl file path
    settings = QSettings("NextGIS", "metatools")
    if standard == MetaInfoStandard.ISO19115:
        xsltFilePath = os.path.join(self.pluginPath, "xsl/") + settings.value("iso19115/stylesheet", QVariant('iso19115.xsl')).toString()
    if standard == MetaInfoStandard.FGDC:
        xsltFilePath = os.path.join(self.pluginPath, "xsl/") + settings.value("fgdc/stylesheet", QVariant('fgdc.xsl')).toString()


    dlg = MetatoolsViewer()
    if dlg.setContent(self.metaProvider, xsltFilePath):
      dlg.exec_()

  def checkMetadata(self):
    if not self.metaProvider.checkExists():
      result = QMessageBox.question(self.iface.mainWindow(),
                                     QCoreApplication.translate("Metatools", "Metatools"),
                                     QCoreApplication.translate("Metatools", "The layer does not have metadata! Create metadata?"),
                                     QDialogButtonBox.Yes, QDialogButtonBox.No)
      if result == QDialogButtonBox.Yes:
        try:
          settings = QSettings("NextGIS", "metatools")
          profile = settings.value("general/defaultProfile").toString()
          if profile.isEmpty():
            QMessageBox.warning(self.iface.mainWindow(),
                                 QCoreApplication.translate("Metatools", "Metatools"),
                                 QCoreApplication.translate("Metatools", "No profile selected. Please set default profile in plugin settings"))
            return False

          profilePath = unicode(QDir.toNativeSeparators(os.path.join(currentPath, "xml_profiles", unicode(profile))))
          self.metaProvider.ImportFromFile(profilePath)
        except:
          QMessageBox.warning(self.iface.mainWindow(),
                               QCoreApplication.translate("Metatools", "Metatools"),
                               QCoreApplication.translate("Metatools", "Metadata file can't be created: ") + str(sys.exc_info()[ 1 ]))
          return False
        return True
      else:
        return False
    else:
      return True

  # external tools

  def execUsgs(self):
    # check if metadata file exists
    if not self.checkMetadata():
      return

    # check matadata standard
    standard = MetaInfoStandard.tryDetermineStandard(self.metaProvider)

    if standard != MetaInfoStandard.FGDC:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "USGS tool support only FGDC standard!"))
      return

    # start tool
    from sys import platform
    toolPath = self.pluginPath + '/external_tools/tkme'
    if platform == 'win32':
        execFilePath = toolPath + '/tkme.exe'
    else:
        execFilePath = toolPath + '/tkme.kit'

        #bug in qgis plugin installer:
        tclkitFilePath = toolPath + '/tclkit'
        from os import chmod
        import stat
        chmod(execFilePath, stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR)
        chmod(tclkitFilePath, stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR)


    try:
      import subprocess
      prov = self.metaProvider
      temporaryMetafile = prov.SaveToTempFile()
      subprocess.Popen([unicode(execFilePath), unicode(temporaryMetafile)], cwd=toolPath).wait()
      prov.LoadFromTempFile(temporaryMetafile)
    except:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "USGS tool can't be runing: ") +
                            QString(str(sys.exc_info()[1])))

  def execMp(self):
    # check if metadata exists
    if not self.checkMetadata():
      return

    # check matadata standard
    standard = MetaInfoStandard.tryDetermineStandard(self.metaProvider)

    if standard != MetaInfoStandard.FGDC:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "MP tool support only FGDC standard!"))
      return

    # start tool
    from sys import platform
    toolPath = self.pluginPath + '/external_tools/mp'

    if platform == 'win32':
        mpFilePath = toolPath + '/mp.exe'
        errFilePath = toolPath + '/err2html.exe'
        throwShell = True
    else:
        mpFilePath = toolPath + '/mp.lnx'
        errFilePath = toolPath + '/err2html.lnx'
        throwShell = False

        #bug in qgis plugin installer:
        from os import chmod
        import stat
        chmod(mpFilePath, stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR)
        chmod(errFilePath, stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR)

    tempPath = os.tempnam()
    temporaryMetafile = self.metaProvider.SaveToTempFile()
    result = ''

    try:
      import subprocess
      subprocess.check_call([mpFilePath, "-e", tempPath, temporaryMetafile], shell=throwShell, cwd=toolPath)

      if sys.hexversion >= 34013184:
        result = subprocess.check_output([errFilePath, tempPath], shell=throwShell, cwd=toolPath)
      else:
        # workaround for python < 2.7
        # ... stderr=subprocess.STDOUT, stdin=subprocess.PIPE ... ! FUCKED Python 2.5 bug on windows! 
        err2htmlProc = subprocess.Popen([errFilePath, tempPath], shell=throwShell, cwd=toolPath, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        err2htmlProc.stdin.close()
        result = err2htmlProc.communicate()[0]

    except:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "MP tool can't be runing: ") +
                            QString(str(sys.exc_info()[1])))
      return
    finally:
      if os.path.exists(tempPath):
          os.remove(tempPath)
      # explicit kill temporary metafile
      if os.path.exists(temporaryMetafile):
          os.remove(temporaryMetafile)

    # show result
    from metatoolsviewer import MetatoolsViewer
    dlg = MetatoolsViewer()
    dlg.setHtml(result)
    dlg.setWindowTitle(QCoreApplication.translate("Metatools", "MP result"))
    dlg.exec_()






  # validator ----

  def validateMetadataFile(self):
    # check if metadata exists
    if not self.checkMetadata():
      return

    # check matadata standard
    standard = MetaInfoStandard.tryDetermineStandard(self.metaProvider)
    if standard != MetaInfoStandard.FGDC:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Unsupported metadata standard! Only FGDC supported now!"))
      return
    
    from PyQt4.QtXml import *
    from PyQt4.QtXmlPatterns import *


    # TODO: validate metadata file

    # setup xml schema
    schema = QXmlSchema()

    # setup handler
    self.handler = ErrorHandler(QCoreApplication.translate("Metatools", "Metadata is invalid"))
    schema.setMessageHandler(self.handler)

    # load schema from file
    xsdFilePath = self.pluginPath + '/xsd/fgdc/fgdc-std-001-1998.xsd'
    #if standard != MetaInfoStandard.FGDC:
    #    xsdFilePath = 'c:/xsd/gml/basicTypes.xsd' #   gmd/gmd.xsd'
    schemaUrl = QUrl(xsdFilePath)
    loadResult = schema.load(schemaUrl)
    if not loadResult or self.handler.errorOccured:
        QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Shcema for validate not loaded!"))
        return


    #setup validator
    validator = QXmlSchemaValidator(schema)
    validator.setMessageHandler(self.handler)

    #validate
    metadata = self.metaProvider.getMetadata().encode('utf-8')
    if validator.validate(metadata):
        QMessageBox.information(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Metadata is valid!"))


  # import\ export -----------------
  def doImport(self):
	# check if metadata exists
    if not self.checkMetadata():
      return
	
    fileName = QFileDialog.getOpenFileName(self.iface.mainWindow(),
                                           QCoreApplication.translate("Metatools", "Select metadata file"),
                                           "",
                                           QCoreApplication.translate("Metatools", 'XML files (*.xml);;Text files (*.txt *.TXT);;All files (*.*)'))

    if fileName.isEmpty():
      return

    try:
      self.metaProvider.ImportFromFile(unicode(fileName))
    except:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Metadata can't be imported: ") +
                            QString(str(sys.exc_info()[1])))
      return

    QMessageBox.information(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Metadata was imported successful!"))

  def doExport(self):
	# check if metadata exists
    if not self.checkMetadata():
      return
	  
    fileName = QFileDialog.getSaveFileName(self.iface.mainWindow(),
                                           QCoreApplication.translate("Metatools", "Save metadata to file"),
                                           "",
                                           QCoreApplication.translate("Metatools", 'XML files (*.xml);;Text files (*.txt *.TXT);;All files (*.*)'))

    if fileName.isEmpty():
      return

    try:
      self.metaProvider.ExportToFile(unicode(fileName))
    except:
      QMessageBox.critical(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Metadata can't be exported: ") +
                            QString(str(sys.exc_info()[1])))
      return

    QMessageBox.information(self.iface.mainWindow(),
                            QCoreApplication.translate("Metatools", "Metatools"),
                            QCoreApplication.translate("Metatools", "Metadata was exported successful!"))
