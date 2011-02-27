# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Metatools Utils
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
from qgis.core import *
from os import path
from PyQt4 import QtGui

META_EXT='.xml'

def getMetafilePath(layer):
    originalFilePath = str(layer.source())
    originalFileName=path.splitext(originalFilePath)
    metaFilePath=originalFileName[0]+META_EXT
    return metaFilePath


