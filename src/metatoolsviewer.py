"""
/***************************************************************************
 MetatoolsDialog
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

from PyQt4 import QtCore, QtGui, QtXml
from ui_viewer import Ui_MetatoolsViewer
# create the dialog for zoom to point
class MetatoolsViewer(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_MetatoolsViewer()
        self.ui.setupUi(self)

    def setContent(self, layer):
        #----test!
        #need check DS type and RasterLayer
        #originalFile = layer.source()
        self.ui.webView.setUrl(QtCore.QUrl('C:\Temp\Metadata\ORD_421119_20110202_20110202_SPOT-_V01_1\Metadata\ISOMetadata\DN_L1A\S5-_HRG_A--_CAM2_0143_00_0407_00_110127_075405_L1A-_ORBIT-.xml'))
        #----end test!
