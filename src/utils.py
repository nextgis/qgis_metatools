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
from PyQt4.QtXml import *

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

def getRasterLayerInfo( layer ):
  bands = layer.bandCount()
  extent = layer.extent()
  return bands, extent

# helper functions for XML processing

def getOrCreateChild( element, childName ):
  child = element.firstChildElement( childName )
  if child.isNull():
    child = element.ownerDocument().createElement( childName )
    element.appendChild( child )
  return child

def getOrIsertAfterChild( element, childName, prevChildsName ):
  child = element.firstChildElement( childName )
  if child.isNull():
    child = element.ownerDocument().createElement( childName )

    # search previous element
    for elementName in prevChildsName:
      prevElement = element.firstChildElement( elementName )
      if not prevElement.isNull():
        element.insertAfter( child, prevElement )
        return child

    # if not found, simply append
    element.appendChild( child )
  return child

def getOrIsertTopChild( element, childName ):
  child = element.firstChildElement( childName )
  if child.isNull():
    child = element.ownerDocument().createElement( childName )
    element.insertBefore( child, QDomNode() )
  return child

def getOrCreateTextChild( element ):
  childTextNode = element.childNodes().at( 0 ) # bad! need full search and type checker
  if childTextNode.isNull():
    childTextNode = element.ownerDocument().createTextNode( "" )
    element.appendChild( childTextNode )
  return childTextNode

def writeRasterInfo( metadataFile, bands, extent ):
  f = QFile( metadataFile )
  f.open( QFile.ReadOnly )
  metaXML = QDomDocument()
  metaXML.setContent( f )
  f.close()

  root = metaXML.documentElement()

  # geographic bounding box
  mdIdentificationInfo = getOrCreateChild( root, "identificationInfo" )
  mdDataIdentification = getOrCreateChild( mdIdentificationInfo, "MD_DataIdentification" )
  mdExtent = getOrCreateChild( mdDataIdentification, "extent" )
  mdEXExtent = getOrCreateChild( mdExtent, "EX_Extent" )
  mdGeorgaphicElement = getOrCreateChild( mdEXExtent, "geographicElement" )
  mdGeoBbox = getOrCreateChild( mdGeorgaphicElement, "EX_GeographicBoundingBox" )

  mdWestBound = getOrCreateChild( mdGeoBbox, "westBoundLongitude" )
  mdCharStringElement = getOrCreateChild( mdWestBound, "gco:Decimal" )
  textNode = getOrCreateTextChild( mdCharStringElement )
  textNode.setNodeValue( str( extent.xMinimum() ) )

  mdEastBound = getOrCreateChild( mdGeoBbox, "eastBoundLongitude" )
  mdCharStringElement = getOrCreateChild( mdEastBound, "gco:Decimal" )
  textNode = getOrCreateTextChild( mdCharStringElement )
  textNode.setNodeValue( str( extent.xMaximum() ) )

  mdSouthBound = getOrCreateChild( mdGeoBbox, "southBoundLatitude" )
  mdCharStringElement = getOrCreateChild( mdSouthBound, "gco:Decimal" )
  textNode = getOrCreateTextChild( mdCharStringElement )
  textNode.setNodeValue( str( extent.yMinimum() ) )

  mdNorthBound = getOrCreateChild( mdGeoBbox, "northBoundLatitude" )
  mdCharStringElement = getOrCreateChild( mdNorthBound, "gco:Decimal" )
  textNode = getOrCreateTextChild( mdCharStringElement )
  textNode.setNodeValue( str( extent.yMaximum() ) )

  # raster bands
  #mdContentInfo = getOrCreateChild( root, "contentInfo" )
  #mdImageDescription = getOrCreateChild( mdContentInfo, "MD_ImageDescription" )
  #mdDimension = getOrCreateChild( mdImageDescription, "dimension" )

  #bandInMetadata = mdDimension.elementsByTagName( "MD_Band" ).count()
  #if bandInMetadata < bands:
    # create additional bands
  #  pass

  f = QFile( metadataFile )
  f.open( QFile.WriteOnly )
  stream = QTextStream( f )
  metaXML.save( stream, 2 )
  f.close()
