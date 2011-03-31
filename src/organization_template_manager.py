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

class OrganizationTemplate:
  def __init__( self, name = None, deliveryPoint = None, city = None, adminArea = None, \
                postalCode = None, country = None, phone = None, fax = None, email = None, \
                person = None, title = None, position = None, hours = None ):
    self.name = name
    #self.address = address
    self.deliveryPoint = deliveryPoint
    self.city = city
    self.adminArea = adminArea
    self.postalCode = postalCode
    self.county = country
    self.phone = phone
    self.fax = fax
    self.email = email
    self.person = person
    self.title = title
    self.position = position
    self.hours = hours

class OrganizationTemplateManager:
  def __init__( self, fileName ):
    self.templatesFile = fileName
    self.organizations = {}
    self.loadTemplates()

  def loadTemplates( self ):
    doc = QDomDocument( "metatools_institution" )
    f = QFile( self.templatesFile )
    if not f.open( QFile.ReadOnly ):
      print "Couldn't open the templates file:", self.templatesFile
      return

    if not doc.setContent( f ):
      print "Couldn't parse the templates file:", self.templatesFile
      return

    f.close()

    docElem = doc.documentElement()
    if docElem.tagName() != "metatools_institution":
      print "Incorrect root tag in file:", docElem.tagName()
      return

    # load organizations
    orgsElement = docElem.firstChildElement( "institutions" )
    if not orgsElement.isNull():
      e = orgsElement.firstChildElement()
      while not e.isNull():
        if e.tagName() == "institution":
          org = self.loadInstitution( e )
          if org != None:
            self.organizations[ e.attribute( "name" ) ] = org
        else:
          print "Unknown tag: ", e.tagName()
        e = e.nextSiblingElement()

  def loadInstitution( self, root ):
    if root.attribute( "name" ).isEmpty():
      return None
    org = OrganizationTemplate()
    org.name = root.attribute( "name" )
    e = root.elementsByTagName( "address" ).at( 0 ).toElement()
    # parse address
    child = e.elementsByTagName( "deliveryPoint" ).at( 0 )
    org.deliveryPoint = child.childNodes().at( 0 ).nodeValue()
    child = e.elementsByTagName( "city" ).at( 0 )
    org.city = child.childNodes().at( 0 ).nodeValue()
    child = e.elementsByTagName( "administrativeArea" ).at( 0 )
    org.adminArea = child.childNodes().at( 0 ).nodeValue()
    child = e.elementsByTagName( "postalCode" ).at( 0 )
    org.postalCode = child.childNodes().at( 0 ).nodeValue()
    child = e.elementsByTagName( "country" ).at( 0 )
    org.country = child.childNodes().at( 0 ).nodeValue()
    
    e = root.elementsByTagName( "phone" ).at( 0 )
    org.phone = e.childNodes().at( 0 ).nodeValue()
    e = root.elementsByTagName( "fax" ).at( 0 )
    org.fax = e.childNodes().at( 0 ).nodeValue()
    e = root.elementsByTagName( "email" ).at( 0 )
    org.email = e.childNodes().at( 0 ).nodeValue()
    e = root.elementsByTagName( "person" ).at( 0 )
    org.person = e.childNodes().at( 0 ).nodeValue()
    e = root.elementsByTagName( "title" ).at( 0 )
    org.title = e.childNodes().at( 0 ).nodeValue()
    e = root.elementsByTagName( "position" ).at( 0 )
    org.position = e.childNodes().at( 0 ).nodeValue()
    e = root.elementsByTagName( "hours" ).at( 0 )
    org.hours = e.childNodes().at( 0 ).nodeValue()
    return org

  def saveTemplates( self ):
    doc = QDomDocument( "metatools_institution" )
    root = doc.createElement( "metatools_institution" )
    doc.appendChild( root )

    orgsElem = doc.createElement( "institutions" )
    for name, org in self.organizations.iteritems():
      el = self.saveInstitution( org, doc )
      orgsElem.appendChild( el )

    root.appendChild( orgsElem )

    f = QFile( self.templatesFile )
    if not f.open( QFile.WriteOnly ):
      print "Couldn't open file for writing:", self.templatesFile
      return

    stream = QTextStream( f )
    doc.save( stream, 2 )
    f.close()

  def saveInstitution( self, org, doc ):
    root = doc.createElement( "institution" )
    root.setAttribute( "name", org.name )

    elem = doc.createElement( "address" )
    # create nested elements
    e = doc.createElement( "deliveryPoint" )
    node = doc.createTextNode( org.deliveryPoint )
    e.appendChild( node )
    elem.appendChild( e )
    e = doc.createElement( "city" )
    node = doc.createTextNode( org.city )
    e.appendChild( node )
    elem.appendChild( e )
    e = doc.createElement( "administrativeArea" )
    node = doc.createTextNode( org.adminArea )
    e.appendChild( node )
    elem.appendChild( e )
    e = doc.createElement( "postalCode" )
    node = doc.createTextNode( org.postalCode )
    e.appendChild( node )
    elem.appendChild( e )
    e = doc.createElement( "country" )
    node = doc.createTextNode( org.country )
    e.appendChild( node )
    elem.appendChild( e )
    
    root.appendChild( elem )

    elem = doc.createElement( "phone" )
    node = doc.createTextNode( org.phone )
    elem.appendChild( node )
    root.appendChild( elem )

    elem = doc.createElement( "fax" )
    node = doc.createTextNode( org.fax )
    elem.appendChild( node )
    root.appendChild( elem )

    elem = doc.createElement( "email" )
    node = doc.createTextNode( org.email )
    elem.appendChild( node )
    root.appendChild( elem )

    elem = doc.createElement( "person" )
    node = doc.createTextNode( org.person )
    elem.appendChild( node )
    root.appendChild( elem )

    elem = doc.createElement( "title" )
    node = doc.createTextNode( org.title )
    elem.appendChild( node )
    root.appendChild( elem )

    elem = doc.createElement( "position" )
    node = doc.createTextNode( org.position )
    elem.appendChild( node )
    root.appendChild( elem )

    elem = doc.createElement( "hours" )
    node = doc.createTextNode( org.hours )
    elem.appendChild( node )
    root.appendChild( elem )

    return root
  
  def reloadTemplates( self ):
    self.organizations = {}
    self.loadTemplates()

  def addTemplate( self, templateName, template ):
    # delete previous template if any
    if self.organizations.has_key( templateName ):
      del self.organizations[ templateName ]

    self.organizations[ templateName ] = template

  def removeTemplate( self, templateName ):
    if self.organizations.has_key( templateName ):
      del self.organizations[ templateName ]

  def tempalateNames( self ):
    return self.organizations.keys()
