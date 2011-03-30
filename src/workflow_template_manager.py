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

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtXml import *

import os, codecs

class WorkflowTemplateManager:
  WORKFLOW_SUBFOLDER = "templates/workflow"
  WORKFLOW_EXT = ".xml"

  def __init__( self, basePluginPath ):
    self.basePluginPath = str( basePluginPath )

  def getWorkflowTemplatesPath( self ):
    return os.path.join( self.basePluginPath, self.WORKFLOW_SUBFOLDER )

  def getTemplateFilePath( self, templateName ):
    return os.path.join( self.getWorkflowTemplatesPath(), str( templateName ) + self.WORKFLOW_EXT )

  def getTemplateList( self ):
    templatesList = []
    for filename in os.listdir( self.getWorkflowTemplatesPath() ):
      name, ext = os.path.splitext( filename )
      if ext == self.WORKFLOW_EXT:
        templatesList.append( name )
    return templatesList

  def loadTemplate( self, templateName ):
    # TODO: more cheks on struct
    workflowTemplate = WorkflowTemplate()
    templateFile = QFile( self.getTemplateFilePath( templateName.toUtf8() ) )

    xmlTemplate = QDomDocument()
    xmlTemplate.setContent( templateFile )

    root = xmlTemplate.documentElement()
    nameElement = root.elementsByTagName( "Name" ).at( 0 )
    descriptionElement = root.elementsByTagName( "Description" ).at( 0 )

    workflowTemplate.name = nameElement.childNodes().at( 0 ).nodeValue()
    workflowTemplate.description = descriptionElement.childNodes().at( 0 ).nodeValue()

    return workflowTemplate

  def saveTemplate( self, workflowTemplate ):
    xmlTemplate = QDomDocument()

    # create root
    root = xmlTemplate.createElement( "WorkflowTemplate" )
    xmlTemplate.appendChild( root )

    # set name
    element = xmlTemplate.createElement( "Name" )
    textNode = xmlTemplate.createTextNode( workflowTemplate.name )
    element.appendChild( textNode )
    root.appendChild( element )

    # set desc
    element = xmlTemplate.createElement( "Description" )
    textNode = xmlTemplate.createTextNode( workflowTemplate.description )
    element.appendChild( textNode )
    root.appendChild( element )

    templateFile = codecs.open( self.getTemplateFilePath( workflowTemplate.name.toUtf8() ), "w", encoding="utf-8" )
    templateFile.write( unicode( xmlTemplate.toString().toUtf8(), "utf-8" ) )
    templateFile.close()

  def removeTemplate( self, templateName ):
    os.remove( self.getTemplateFilePath( templateName ) )

class WorkflowTemplate:
  def __init__( self, name = None, description = None ):
    self.name = name
    self.description = description

  def stringRepresentation( self ):
    return self.name + '::' + self.description
