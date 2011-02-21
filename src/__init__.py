# -*- coding: utf-8 -*-
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

pluginVersion = "0.1.0"

def name():
    return "Metatools"

def description():
    return "Metadata browser/editor"

def version():
    return pluginVersion

def icon():
    return "icon.png"

def qgisMinimumVersion():
    return "1.5"

def classFactory(iface):
    # load MetatoolsPlugin class from file Metatools
    from metatools import MetatoolsPlugin
    return MetatoolsPlugin(iface)
