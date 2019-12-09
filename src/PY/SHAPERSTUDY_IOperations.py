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

class SHAPERSTUDY_IShapesOperations(SHAPERSTUDY_ORB__POA.IShapesOperations):
    """
    Construct an instance of SHAPERSTUDY IShapesOperations.
    """
    def __init__ ( self, *args):
        pass

    def GetAllSubShapesIDs( self, theShape, theShapeType, isSorted ):
        """
        Explode a shape on sub-shapes of a given type.

        Parameters:
            theShape Shape to be exploded.
            theShapeType Type of sub-shapes to be retrieved.
            isSorted If this parameter is TRUE, sub-shapes will be
            sorted by coordinates of their gravity centers.
        """
        return [1]

    def GetSharedShapes( self, theShape1, theShape2, theShapeType ):
        """
        Get sub-shapes, shared by input shapes.

        Parameters:
            theShape1 Shape to find sub-shapes in.
            theShape2 Shape to find shared sub-shapes with.
            theShapeType Type of sub-shapes to be retrieved.
        """
        return [ SHAPERSTUDY_Object()._this() ]

    def GetSubShapeIndex( self, theMainShape, theSubShape ):
        """
        Get global index of theSubShape in theMainShape.
        """
        return 2

    def GetSubShape( self, theMainShape, theID ):
        """
        Get a sub-shape defined by its unique ID within theMainShape
        """
        return SHAPERSTUDY_Object()._this()

    def GetInPlace( self, theShapeWhere, theShapeWhat ):
        """
        Get sub-shape(s) of \a theShapeWhere, which are
        coincident with \a theShapeWhat or could be a part of it.
        """
        return SHAPERSTUDY_Object()._this()
        
    def GetInPlaceMap( self, theShapeWhere, theShapeWhat ):
        """
        A sort of GetInPlace functionality, returning for each sub-shape ID of
        \a theShapeWhat a list of corresponding sub-shape IDs of \a theShapeWhere.
        """
        return [[]]

    def IsDone( self ):
        """
        To know, if the operation was successfully performed
        """
        return False

    pass
    

class SHAPERSTUDY_IGroupOperations(SHAPERSTUDY_ORB__POA.IGroupOperations):
    """
    Construct an instance of SHAPERSTUDY IShapesOperations.
    """
    def __init__ ( self, *args):
        pass

    def CreateGroup( self, theMainShape, theShapeType ):
        """
        Creates a new group which will store sub-shapes of theMainShape
        """
        return SHAPERSTUDY_Object()._this()

    def UnionList( self, theGroup, theSubShapes ):
        """
        Adds to the group all the given shapes. No errors, if some shapes are already included.

        Parameters:
            theGroup is a GEOM group to which the new sub-shapes are added.
            theSubShapes is a list of sub-shapes to be added.
        """
        return

    def IsDone( self ):
        """
        To know, if the operation was successfully performed
        """
        return False

    def GetMainShape( self, theGroup ):
        """
        Returns a main shape associated with the group
        """
        return SHAPERSTUDY_Object()._this()

    def GetType( self, theGroup ):
        """
        Returns a type (int) of sub-objects stored in the group
        """
        return SHAPERSTUDY_Object()._this()

    def GetObjects( self, theGroup ):
        """
        Returns a list of sub-objects ID stored in the group
        """
        return [2]

    pass

class SHAPERSTUDY_IFieldOperations(SHAPERSTUDY_ORB__POA.IFieldOperations):
    """
    Construct an instance of SHAPERSTUDY IFieldOperations.
    """
    def __init__ ( self, *args):
        pass

    def GetFields( self, shape ):
        """
        Returns all fields on a shape
        """
        return [ SHAPERSTUDY_Field() ]

    pass


class SHAPERSTUDY_IMeasureOperations(SHAPERSTUDY_ORB__POA.IMeasureOperations):
    """
    Construct an instance of SHAPERSTUDY IMeasureOperations.
    """
    def __init__ ( self, *args):
        pass

    def GetVertexByIndex( self, theShape, theIndex, theUseOri ):
        """
        Get a vertex sub-shape by index.

        Parameters:
        theShape Shape to find sub-shape.
        theIndex Index to find vertex by this index (starting from zero)
        theUseOri To consider edge/wire orientation or not
        """
        return [ SHAPERSTUDY_Field() ]

    pass
