# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Metatools
# ---------------------------------------------------------
# Metadata browser/editor
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
# ******************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *

from qgis.core import *
from qgis.gui import *

import os

from osgeo import gdal, ogr, osr

from metadata_provider import MetadataProvider

META_EXT = ".xml"
PREVIEW_SUFFIX = "_preview"


def getMetafilePath(layer):
    # not standard implementation in original plugin
    originalFilePath = unicode(layer.source())
    # originalFileName = os.path.splitext(originalFilePath)
    # metaFilePath = originalFileName[0] + META_EXT
    metaFilePath = originalFilePath + META_EXT
    return metaFilePath


def previewPathFromLayerPath(layerPath):
    settings = QSettings("NextGIS", "metatools")
    format_preview = settings.value("preview/format", "jpg")

    originalFileName = os.path.splitext(unicode(layerPath))
    metaFilePath = originalFileName[0] + PREVIEW_SUFFIX + "." + format_preview
    return metaFilePath


def mdPathFromLayerPath(layerPath):
    # not standard implementation in original plugin
    # originalFileName = os.path.splitext(unicode(layerPath))
    # metaFilePath = originalFileName[0] + META_EXT
    metaFilePath = layerPath + META_EXT
    return metaFilePath


def getSupportedLayerNames():
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    layerList = []
    for name, layer in layermap.iteritems():
        if MetadataProvider.IsLayerSupport(layer)[0]:
            layerList.append(layer.name())
    return layerList


def getSupportedLayers():
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    layers = []
    for name, layer in layermap.iteritems():
        if MetadataProvider.IsLayerSupport(layer)[0]:
            layers.append((layer.name(), layer.source()))
    return layers


def getRasterLayerByName(layerName):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.type() == QgsMapLayer.RasterLayer:
            if layer.providerType() != "gdal":
                continue
            if layer.name() == layerName:
                return layer
    return None


def getRasterLayerByPath(layerPath):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.type() == QgsMapLayer.RasterLayer:
            if layer.providerType() != "gdal":
                continue
            if layer.source() == layerPath:
                return layer
    return None


# helper functions for raster metadata


def getGeneralRasterInfo(path):
    raster = gdal.Open(unicode(path).encode("utf8"))
    bands = raster.RasterCount

    width = raster.RasterXSize
    height = raster.RasterYSize

    gt = raster.GetGeoTransform()

    xMin = gt[0]
    yMin = gt[3] + width * gt[4] + height * gt[5]
    xMax = gt[0] + width * gt[1] + height * gt[2]
    yMax = gt[3]

    rasterSR = raster.GetProjectionRef()
    layerSR = osr.SpatialReference()
    layerSR.ImportFromWkt(rasterSR)
    # create wgs84 SR
    wgsSR = osr.SpatialReference()
    wgsSR.ImportFromEPSG(4326)

    # transform coord if layer CRS is defined otherwise assume WGS84
    if (layerSR is not None) and (not wgsSR.IsSame(layerSR)):
        transform = osr.CoordinateTransformation(layerSR, wgsSR)
        coord = transform.TransformPoints([(xMin, yMin), (xMax, yMax)])
        xMin = coord[0][0]
        yMin = coord[0][1]
        xMax = coord[1][0]
        yMax = coord[1][1]
        transform = None

    raster = None

    return bands, [xMin, yMin, xMax, yMax]


def getBandInfo(path, bandNumber):
    raster = gdal.Open(unicode(path).encode("utf8"))
    band = raster.GetRasterBand(bandNumber)

    min_value, max_value = band.ComputeRasterMinMax()
    if not min_value:
        min_value = 0
    if not max_value:
        max_value = 0

    dataType = band.DataType
    bytes_in_types = {
        0: -1,
        1: 8,
        2: 16,
        3: 16,
        4: 32,
        5: 32,
        6: 32,
        7: 64,
        8: 16,
        9: 32,
        10: 32,
        11: 64,
    }
    dataType = bytes_in_types[dataType]

    # QMessageBox.information(QWidget(), "Metatools", "Min: "+str(min_value)+" Max: "+str(max_value)+" Dt: "+str(band.DataType) + " Byte: "+str(dataType)) #debug

    band = None
    raster = None

    return min_value, max_value, dataType


# helper functions for vector metadata
def getGeneralVectorInfo(path):
    ogrDataSource = ogr.Open(unicode(path).encode("utf8"))
    layer = ogrDataSource[0]

    # get extent and layer SR
    (xMin, xMax, yMin, yMax) = layer.GetExtent()
    layerSR = layer.GetSpatialRef()

    # create wgs84 SR
    wgsSR = osr.SpatialReference()
    wgsSR.ImportFromEPSG(4326)

    # transform coord if layer CRS is defined otherwise assume WGS84
    if (layerSR is not None) and (not wgsSR.IsSame(layerSR)):
        transform = osr.CoordinateTransformation(layerSR, wgsSR)
        coord = transform.TransformPoints([(xMin, yMin), (xMax, yMax)])
        xMin = coord[0][0]
        yMin = coord[0][1]
        xMax = coord[1][0]
        yMax = coord[1][1]
        transform = None

    layer = None
    ogrDataSource = None

    return [xMin, yMin, xMax, yMax]


# helper functions for XML processing
def createChild(element, childName):
    child = element.ownerDocument().createElement(childName)
    element.appendChild(child)
    return child


def getOrCreateChild(element, childName):
    child = element.firstChildElement(childName)
    if child.isNull():
        child = element.ownerDocument().createElement(childName)
        element.appendChild(child)
    return child


def insertAfterChild(element, childName, prevChildsName):
    child = element.ownerDocument().createElement(childName)

    # search previous element
    for elementName in prevChildsName:
        prevElement = element.lastChildElement(elementName)
        if not prevElement.isNull():
            element.insertAfter(child, prevElement)
            return child

    # if not found, simply append
    element.appendChild(child)
    return child


def getOrIsertAfterChild(element, childName, prevChildsName):
    child = element.firstChildElement(childName)
    if child.isNull():
        child = element.ownerDocument().createElement(childName)

        # search previous element
        for elementName in prevChildsName:
            prevElement = element.lastChildElement(elementName)
            if not prevElement.isNull():
                element.insertAfter(child, prevElement)
                return child

        # if not found, simply append
        element.appendChild(child)
    return child


def getOrIsertTopChild(element, childName):
    child = element.firstChildElement(childName)
    if child.isNull():
        child = element.ownerDocument().createElement(childName)
        element.insertBefore(child, QDomNode())
    return child


def getOrCreateTextChild(element):
    childTextNode = element.childNodes().at(
        0
    )  # bad! need full search and type checker
    if childTextNode.isNull():
        childTextNode = element.ownerDocument().createTextNode("")
        element.appendChild(childTextNode)
    return childTextNode


# write raster information in metadata
def writeRasterInfo(dataFile, metadataFile):
    f = QFile(metadataFile)
    f.open(QFile.ReadOnly)
    metaXML = QDomDocument()
    metaXML.setContent(f)
    f.close()

    # general raster info
    bands, extent = getGeneralRasterInfo(dataFile)

    root = metaXML.documentElement()

    # geographic bounding box
    mdIdentificationInfo = getOrCreateChild(root, "identificationInfo")
    mdDataIdentification = getOrCreateChild(
        mdIdentificationInfo, "MD_DataIdentification"
    )
    mdExtent = getOrCreateChild(mdDataIdentification, "extent")
    mdEXExtent = getOrCreateChild(mdExtent, "EX_Extent")
    mdGeorgaphicElement = getOrCreateChild(mdEXExtent, "geographicElement")
    mdGeoBbox = getOrCreateChild(
        mdGeorgaphicElement, "EX_GeographicBoundingBox"
    )

    mdWestBound = getOrCreateChild(mdGeoBbox, "westBoundLongitude")
    mdCharStringElement = getOrCreateChild(mdWestBound, "gco:Decimal")
    textNode = getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(str(extent[0]))

    mdEastBound = getOrCreateChild(mdGeoBbox, "eastBoundLongitude")
    mdCharStringElement = getOrCreateChild(mdEastBound, "gco:Decimal")
    textNode = getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(str(extent[2]))

    mdSouthBound = getOrCreateChild(mdGeoBbox, "southBoundLatitude")
    mdCharStringElement = getOrCreateChild(mdSouthBound, "gco:Decimal")
    textNode = getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(str(extent[1]))

    mdNorthBound = getOrCreateChild(mdGeoBbox, "northBoundLatitude")
    mdCharStringElement = getOrCreateChild(mdNorthBound, "gco:Decimal")
    textNode = getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(str(extent[3]))

    # raster bands
    mdContentInfo = getOrCreateChild(root, "contentInfo")
    mdImageDescription = getOrCreateChild(mdContentInfo, "MD_ImageDescription")

    # drop all demensions
    while not (mdImageDescription.firstChildElement("dimension")).isNull():
        mdImageDescription.removeChild(
            mdImageDescription.firstChildElement("dimension")
        )

    mdDimension = insertAfterChild(
        mdImageDescription,
        "dimension",
        ["dimension", "contentType", "attributeDescription"],
    )  # profile version

    # create new demensions
    for bandNumber in range(1, bands + 1):
        min_value, max_value, dt = getBandInfo(dataFile, bandNumber)
        # mdDimension = insertAfterChild(mdImageDescription, "dimension", ["dimension", "contentType", "attributeDescription"]) #standard version
        # mdBand = getOrCreateChild(mdDimension, "MD_Band") #standard version
        mdBand = createChild(mdDimension, "MD_Band")  # profile version
        mdMaxValue = getOrCreateChild(mdBand, "maxValue")
        mdGcoReal = getOrCreateChild(mdMaxValue, "gco:Real")
        textNode = getOrCreateTextChild(mdGcoReal)
        textNode.setNodeValue(str(max_value))
        mdMinValue = getOrCreateChild(mdBand, "minValue")
        mdGcoReal = getOrCreateChild(mdMinValue, "gco:Real")
        textNode = getOrCreateTextChild(mdGcoReal)
        textNode.setNodeValue(str(min_value))
        mdBitsPerValue = getOrCreateChild(mdBand, "bitsPerValue")
        mdGcoInt = getOrCreateChild(mdBitsPerValue, "gco:Integer")
        textNode = getOrCreateTextChild(mdGcoInt)
        textNode.setNodeValue(str(dt))

    f = QFile(metadataFile)
    f.open(QFile.WriteOnly)
    stream = QTextStream(f)
    metaXML.save(stream, 2)
    f.close()


# write raster information in metadata
def writeVectorInfo(dataFile, metadataFile):
    f = QFile(metadataFile)
    f.open(QFile.ReadOnly)
    metaXML = QDomDocument()
    metaXML.setContent(f)
    f.close()

    # general raster info
    extent = getGeneralVectorInfo(dataFile)

    root = metaXML.documentElement()

    # geographic bounding box
    mdIdentificationInfo = getOrCreateChild(root, "identificationInfo")
    mdDataIdentification = getOrCreateChild(
        mdIdentificationInfo, "MD_DataIdentification"
    )
    mdExtent = getOrCreateChild(mdDataIdentification, "extent")
    mdEXExtent = getOrCreateChild(mdExtent, "EX_Extent")
    mdGeorgaphicElement = getOrCreateChild(mdEXExtent, "geographicElement")
    mdGeoBbox = getOrCreateChild(
        mdGeorgaphicElement, "EX_GeographicBoundingBox"
    )

    mdWestBound = getOrCreateChild(mdGeoBbox, "westBoundLongitude")
    mdCharStringElement = getOrCreateChild(mdWestBound, "gco:Decimal")
    textNode = getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(str(extent[0]))

    mdEastBound = getOrCreateChild(mdGeoBbox, "eastBoundLongitude")
    mdCharStringElement = getOrCreateChild(mdEastBound, "gco:Decimal")
    textNode = getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(str(extent[2]))

    mdSouthBound = getOrCreateChild(mdGeoBbox, "southBoundLatitude")
    mdCharStringElement = getOrCreateChild(mdSouthBound, "gco:Decimal")
    textNode = getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(str(extent[1]))

    mdNorthBound = getOrCreateChild(mdGeoBbox, "northBoundLatitude")
    mdCharStringElement = getOrCreateChild(mdNorthBound, "gco:Decimal")
    textNode = getOrCreateTextChild(mdCharStringElement)
    textNode.setNodeValue(str(extent[3]))

    f = QFile(metadataFile)
    f.open(QFile.WriteOnly)
    stream = QTextStream(f)
    metaXML.save(stream, 2)
    f.close()


def generatePreview(dataFile):
    # get raster
    rasterLayer = getRasterLayerByPath(dataFile)
    if not rasterLayer:
        rasterLayer = QgsRasterLayer(dataFile, "", True)

    # get size
    width = 512
    height = int(rasterLayer.height() * width / rasterLayer.width())
    preview = QPixmap(width, height)

    # generate preview
    rasterLayer.thumbnailAsPixmap(preview)
    preview.save(previewPathFromLayerPath(dataFile))
