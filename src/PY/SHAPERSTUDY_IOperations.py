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
import SHAPERSTUDY_ORB
import SHAPERSTUDY_Object
import GEOM
from SHAPERSTUDY_utils import getStudy

import StudyData_Swig

class SHAPERSTUDY_IShapesOperations(SHAPERSTUDY_ORB__POA.IShapesOperations):
    """
    Construct an instance of SHAPERSTUDY IShapesOperations.
    """
    def __init__ ( self, *args):
        self.done = False
        self.myop = StudyData_Swig.StudyData_Operation()
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
        aList = self.myop.GetAllSubShapesIDs(theShape.getShape(), theShapeType, isSorted)
        self.done = not aList.empty()
        return aList

    def GetSharedShapes( self, theShape1, theShape2, theShapeType ):
        """
        Get sub-shapes, shared by input shapes.

        Parameters:
            theShape1 Shape to find sub-shapes in.
            theShape2 Shape to find shared sub-shapes with.
            theShapeType Type of sub-shapes to be retrieved.
        """
        aList = self.myop.GetSharedShapes(theShape1.getShape(), theShape2.getShape(), theShapeType)
        self.done = not aList.empty()
        return aList

    def GetSubShapeIndex( self, theMainShape, theSubShape ):
        """
        Get global index of theSubShape in theMainShape.
        """
        anIndex = self.myop.GetSubShapeIndex(theMainShape.getShape(), theSubShape.getShape())
        self.done = anIndex != 0
        return anIndex

    def GetSubShape( self, theMainShape, theID ):
        """
        Get a sub-shape defined by its unique ID within theMainShape
        """
        aShape = self.myop.GetSubShape(theMainShape.getShape(), theID)
        self.done = aShape != 0
        if not self.done:
          return None

        # create a shape-object that contain the internal shape only
        aShapeObj = SHAPERSTUDY_Object.SHAPERSTUDY_Object()
        aShapeObj.SetShapeByPointer(aShape)
        return aShapeObj

    def GetInPlace( self, theShapeWhere, theShapeWhat ):
        """
        Get sub-shape(s) of \a theShapeWhere, which are
        coincident with \a theShapeWhat or could be a part of it.
        """
        # not done
        return SHAPERSTUDY_Object()._this()
        
    def GetInPlaceMap( self, theShapeWhere, theShapeWhat ):
        """
        A sort of GetInPlace functionality, returning for each sub-shape ID of
        \a theShapeWhat a list of corresponding sub-shape IDs of \a theShapeWhere.
        """
        # not done
        return [[]]

    def IsDone( self ):
        """
        To know, if the operation was successfully performed
        """
        return self.done

    pass

class SHAPERSTUDY_IGroupOperations(SHAPERSTUDY_ORB__POA.IGroupOperations):
    """
    Construct an instance of SHAPERSTUDY IShapesOperations.
    """
    def __init__ ( self, *args):
        self.done = False
        pass

    def CreateGroup( self, theMainShape, theShapeType ):
        """
        Creates a new group which will store sub-shapes of theMainShape
        """
        if theShapeType != 7 and theShapeType != 6 and theShapeType != 4 and theShapeType != 2: 
          print("Error: You could create group of only next type: vertex, edge, face or solid")
          return None

        aGroup = SHAPERSTUDY_Object.SHAPERSTUDY_Group()
        aGroupPtr = aGroup._this()
        aGroup.SetSelectionType(theShapeType) # create a new field specific for the group python object
        self.done = True
        return aGroupPtr

    def FindGroup(self, theOwner, theEntry):
        """
        Searches existing group of theOwner shape by the entry. Returns NULL if can not find.
        """
        aStudy = getStudy()
        anIter = aStudy.NewChildIterator(theOwner.GetSO())
        while anIter.More():
          aGroupObj = anIter.Value().GetObject()
          if aGroupObj:
            if aGroupObj.GetEntry() == theEntry:
              self.done = True
              return aGroupObj
          anIter.Next()
        self.done = False
        return None # not found

    def UnionList( self, theGroup, theSubShapes ):
        """
        Adds to the group all the given shapes. No errors, if some shapes are already included.

        Parameters:
            theGroup is a GEOM group to which the new sub-shapes are added.
            theSubShapes is a list of sub-shapes to be added.
        """
        # Not needed while SHAPER-STUDY has no sub-shapes in the structure, so, 
        # theSubShapes can not be filled or treated
        return

    def IsDone( self ):
        """
        To know, if the operation was successfully performed
        """
        return self.done

    def GetMainShape( self, theGroup ):
        """
        Returns a main shape associated with the group
        """
        aSO = theGroup.GetSO()
        aFatherSO = aSO.GetFather()
        return aFatherSO.GetObject()

    def GetType( self, theGroup ):
        """
        Returns a type (int) of sub-objects stored in the group
        """
        return theGroup.GetSelectionType()

    def GetObjects( self, theGroup ):
        """
        Returns a list of sub-objects ID stored in the group
        """
        return theGroup.GetSelection()

    pass

class SHAPERSTUDY_IFieldOperations(SHAPERSTUDY_ORB__POA.IFieldOperations):
    """
    Construct an instance of SHAPERSTUDY IFieldOperations.
    """
    def __init__ ( self, *args):
        pass

    def CreateFieldByType( self, theMainShape, theShapeType):
        """
        Creates a new group which will store sub-shapes of theMainShape
        """
        if theShapeType != 8 and theShapeType != 7 and theShapeType != 6 and theShapeType != 4 and theShapeType != 2: 
          print("Error: You could create field of only next type: vertex, edge, face or solid, whole part")
          return None

        aField = SHAPERSTUDY_Object.SHAPERSTUDY_Field()
        aFieldPtr = aField._this()
        aField.SetSelectionType(theShapeType) # create a new field specific for the group python object
        return aFieldPtr

    def FindField(self, theOwner, theEntry):
        """
        Searches existing field of theOwner shape by the entry. Returns NULL if can not find.
        """
        aStudy = getStudy()
        anIter = aStudy.NewChildIterator(theOwner.GetSO())
        while anIter.More():
          aFieldObj = anIter.Value().GetObject()
          if aFieldObj:
            if aFieldObj.GetEntry() == theEntry:
              return aFieldObj
          anIter.Next()
        return None # not found


    def GetFields( self, shape ):
        """
        Returns all fields on a shape
        """
        aResList = []
        aStudy = getStudy()
        anIter = aStudy.NewChildIterator(shape.GetSO())
        while anIter.More():
          aFieldObj = anIter.Value().GetObject()
          if aFieldObj and isinstance(aFieldObj, SHAPERSTUDY_ORB._objref_SHAPER_Field):
            aResList.append(aFieldObj)
        return aResList

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
