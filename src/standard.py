# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Metainfo Standards
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


class MetaInfoStandard:
    UNKNOWN, ISO19138, FGDC, DC=range(4)
    
    @staticmethod
    def tryDetermineStandard(metaFilePath):
        metaFile = open(metaFilePath,"r")
        text  = metaFile.read()
        metaFile.close()
    
        #simple test for iso doc
        if text.find('MD_Metadata')>=0:
            return MetaInfoStandard.ISO19138
    
        #only iso support now
        return MetaInfoStandard.UNKNOWN