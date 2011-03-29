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
from qgis.gui import *

import os

META_EXT = '.xml'

def getMetafilePath( layer ):
  originalFilePath = str( layer.source() )
  originalFileName = os.path.splitext( originalFilePath )
  metaFilePath = originalFileName[ 0 ] + META_EXT
  return metaFilePath

def mdPathFromLayerPath( layerPath ):
  originalFileName = os.path.splitext( str( layerPath ) )
  metaFilePath = originalFileName[ 0 ] + META_EXT
  return metaFilePath

def getRasterLayerNames():
  layermap = QgsMapLayerRegistry.instance().mapLayers()
  layerList = QStringList()
  for name, layer in layermap.iteritems():
    if layer.type() == QgsMapLayer.RasterLayer:
      if layer.usesProvider() and layer.providerKey() != 'gdal':
        continue
      layerList << layer.name()
  return layerList

def getRasterLayerByName( layerName ):
  layermap = QgsMapLayerRegistry.instance().mapLayers()
  for name, layer in layermap.iteritems():
    if layer.type() == QgsMapLayer.RasterLayer:
      if layer.usesProvider() and layer.providerKey() != "gdal":
        continue
      if layer.name() == layerName:
        return layer
      else:
        return None
