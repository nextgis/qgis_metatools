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

class MetaInfoStandard:
  UNKNOWN, ISO19115, FGDC, DC=range( 4 )

  @staticmethod
  def tryDetermineStandard( metaFilePath ):
    metaFile = open( metaFilePath, "r" )
    text  = metaFile.read()
    metaFile.close()

    # simple test for iso doc
    if text.find( "MD_Metadata" ) >= 0 or text.find( "MI_Metadata" ) >= 0:
        return MetaInfoStandard.ISO19115

    # only iso support now
    return MetaInfoStandard.UNKNOWN
