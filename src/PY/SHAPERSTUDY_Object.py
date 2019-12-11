# Copyright (C) 2007-2019  CEA/DEN, EDF R&D, OPEN CASCADE
#
# Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
# CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

import SHAPERSTUDY_ORB__POA
import GEOM
from SHAPERSTUDY_utils import getEngine

import StudyData_Swig

class SHAPERSTUDY_BaseObject(SHAPERSTUDY_ORB__POA.BaseObject):
    """
    Construct an instance of SHAPER_BaseObject.
    """
    def __init__ ( self, *args):
        pass

    def GetName( self ):
        """
        Get name of the object associated with this object.
        """
        return ""

    def GetEntry( self ):
        """
        Get internal (unique) entry of the object in the component's data tree.
        """
        return '0:0:0:1'

    def GetType( self ):
        """
        Get internal type of operation created this object.
        In SMESH is used to find out if an object is GROUP (type == 37)
        """
        return 1

    def GetTick( self ):
        """
        Get value of a modification counter of the object
        """
        return 1

    def GetStudyEntry( self ):
        """
        Get a Study entry where this object was published.
        """
        return '0:0:0:1'

    def IsShape( self ):
        """
        Return true if geom object representes a shape.
        For example, method return false for GEOM_MARKER
        """
        return False

    def IsSame( self, other ):
        """
        Return true if passed object is identical to this object
        """
        return False

    def GetGen( self ):
        """
        Return the engine creating this object
        """
        return getEngine()

    pass



class SHAPERSTUDY_Object(SHAPERSTUDY_ORB__POA.SHAPER_Object):
    """
    Construct an instance of SHAPERSTUDY Object.
    """
    def __init__ ( self, *args):
        pass

    def GetShapeType( self ):
        """
        Get a GEOM.shape_type of the object value.
        """
        return GEOM.SHAPE

    def IsMainShape( self ):
        """
        Returns True if this object is not a sub-shape of another object.
        """
        return False

    def GetSubShapeIndices( self ):
        """
        Get a list of ID's of sub-shapes in the main shape.
        """
        return [1]

    def GetMainShape( self ):
        """
        Get a main shape object to which this object is a sub-shape.
        """
        return

    def getShape( self ):
        """
        Get the TopoDS_Shape, for colocated case only.
        Called by GEOM_Client to get TopoDS_Shape pointer
        """
        return 0

    def GetShapeStream( self ):
        """
        Get geometric shape of the object as a byte stream in BRep format
        """
        return ;

    def SetShapeByStream(self, theStream):
        """
        Sets geometric shape content of the object as a byte stream in BRep format
        """
        self.data = StudyData_Swig.StudyData_Object(theStream)

    pass
