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

import SHAPERSTUDY_ORB
import SHAPERSTUDY_ORB__POA
import GEOM
from SHAPERSTUDY_utils import getEngine, getStudy
import salome

import StudyData_Swig

# converter from the integer values to idl shape_type enumerations
__shape_types__ = {
  0:GEOM.COMPOUND, 1:GEOM.COMPSOLID, 2:GEOM.SOLID,
  3:GEOM.SHELL, 4:GEOM.FACE, 5:GEOM.WIRE,
  6:GEOM.EDGE, 7:GEOM.VERTEX, 8:GEOM.SHAPE, 9:GEOM.FLAT}


class SHAPERSTUDY_Object(SHAPERSTUDY_ORB__POA.SHAPER_Object):
    """
    Construct an instance of SHAPERSTUDY Object.
    """
    def __init__ ( self, *args):
        self.SO = None
        self.data = None
        self.entry = None
        self.type = 1 # by default it is a shape (Import feature in GEOMImpl_Types.hxx)
        pass

    def GetShapeType( self ):
        """
        Get a GEOM.shape_type of the object value.
        """
        if self.data is None:
            return GEOM.SHAPE
        global __shape_types__
        return __shape_types__[self.data.type()];

    def IsMainShape( self ):
        """
        Returns True if this object is not a sub-shape of another object.
        """
        return True

    def GetSubShapeIndices( self ):
        """
        Get a list of ID's of sub-shapes in the main shape.
        """
        return []

    def GetMainShape( self ):
        """
        Get a main shape object to which this object is a sub-shape.
        """
        return getShape()

    def getShape( self ):
        """
        Get the TopoDS_Shape, for collocated case only.
        Called by GEOM_Client to get TopoDS_Shape pointer
        """
        if self.data is None:
            return 0
        return self.data.shape()

    def GetShapeStream( self ):
        """
        Get geometric shape of the object as a byte stream in BRep format
        """
        if self.data is None:
            return b''
        return self.data.shapeStream().encode()

    def GetOldShapeStream( self ):
        """
        Get geometric shape of the object as a byte stream in BRep format
        """
        if self.data is None:
            return b''
        return self.data.oldShapeStream().encode()

    def SetShapeByStream(self, theStream):
        """
        Sets geometric shape content of the object as a byte stream in BRep format
        """
        if self.data:
          self.data.updateShape(theStream)
        else:
          self.data = StudyData_Swig.StudyData_Object(theStream)

    """
    Methods from BaseObject
    """
    def GetName( self ):
        """
        Get name of the object associated with this object.
        """
        return self.SO.GetName()

    def SetEntry( self, theInternalEntry ):
        """
        Sets internal (unique) entry of the object in the component's data tree.
        """
        self.entry = theInternalEntry

    def GetEntry( self ):
        """
        Get internal (unique) entry of the object in the component's data tree.
        """
        return self.entry

    def GetType( self ):
        """
        Get internal type of operation created this object.
        In SMESH is used to find out if an object is GROUP (type == 37)
        """
        return self.type

    def SetType( self, theType ):
        """
        Sets internal type of operation created this object.
        In SMESH is used to find out if an object is GROUP (type == 37, for shape it is default=1)
        """
        self.type = theType

    def GetTick( self ):
        """
        Get value of a modification counter of the object
        """
        if self.data:
          return self.data.getTick()
        return 0

    def GetStudyEntry( self ):
        """
        Get a Study entry where this object was published.
        """
        return self.SO.GetID()

    def IsShape( self ):
        """
        Return true if geom object represents a shape.
        For example, method return false for GEOM_MARKER
        """
        return True

    def IsSame( self, other ):
        """
        Return true if passed object is identical to this object
        """
        return self.GetType() == other.GetType() and self.GetEntry() == other.GetEntry()

    def GetGen( self ):
        """
        Return the engine creating this object
        """
        return getEngine()

    def SetSO( self, theSO ):
        """
        Sets SObject of this object (when it is published)
        """
        self.SO = theSO
        
    def GetSO( self ):
        """
        Returns SObject of this object
        """
        return self.SO

    def IsParametrical(self):
        """
        Returns true if the current object has connection to a parametrical model
        which can be modified by parameters change.
        """
        return not self.IsDead()

    def IsDead(self):
        """
        Returns true if the shape is dead - no parametrical link to the SHAPER exists
        """
        return self.GetEntry().startswith("dead")

    def MakeDead(self):
        """
        Makes the dead-copy of the shape and returns it.
        """
        aStudy = getStudy()
        aBuilder = aStudy.NewBuilder()
        aRes, aHistSO = self.SO.FindSubObject(2)
        if not aRes: # create a "history" folder if it does not exist
          aHistSO = aBuilder.NewObjectToTag(self.SO, 2)
          aHistSO.SetAttrString("AttributeName", "History")

        aDeadSO = aBuilder.NewObject(aHistSO)
        anIndex = aDeadSO.Tag()
        aDeadSO.SetAttrString("AttributeName", self.SO.GetName() + " (" + str(anIndex) + ")")
        aDead = SHAPERSTUDY_Object()
        aDeadEntry = "dead" + str(anIndex) + "_" + self.GetEntry()
        aDead.SetEntry(aDeadEntry)
        aDead.SetShapeByStream(self.data.oldShapeStream())
        aDeadObj = aDead._this()
        anIOR = salome.orb.object_to_string(aDeadObj)
        aDeadSO.SetAttrString("AttributeIOR", anIOR)
        aDead.SetSO(aDeadSO)
        if self.GetTick() > 2:
          aDead.data.setTick(self.GetTick() - 1) # set the tick of an old shape
        # make dead-copy also sub-groups
        aSOIter = aStudy.NewChildIterator(self.SO)
        while aSOIter.More():
          aGroupSO = aSOIter.Value()
          anIOR = aGroupSO.GetIOR()
          if len(anIOR):
            aGroup = salome.orb.string_to_object(anIOR)
            if isinstance(aGroup, SHAPERSTUDY_ORB._objref_SHAPER_Group):
              aDeadGroup = SHAPERSTUDY_Group()
              aDeadGroupEntry = "dead" + str(anIndex) + "_" + aGroup.GetEntry()
              aDeadGroup.SetEntry(aDeadGroupEntry)
              aDeadGroup.SetShapeByPointer(aGroup.getShape())
              aDeadGroup.SetSelectionType(aGroup.GetSelectionType())
              aDeadGroup.SetSelection(aGroup.GetSelection())
              aDeadGroupSO = aBuilder.NewObject(aDeadSO)
              aDeadGroup.SetSO(aDeadGroupSO)
              aDeadGroupSO.SetAttrString("AttributeName", aGroupSO.GetName() + " (" + str(anIndex) + ")")
              aDeadGroupObj = aDeadGroup._this()
              anIOR = salome.orb.object_to_string(aDeadGroupObj)
              aDeadGroupSO.SetAttrString("AttributeIOR", anIOR)
          aSOIter.Next()

        return aDeadObj
    
    def SetShapeByPointer(self, theShape):
        """
        Sets the shape by the pointer to the TopoDS_Shape
        """
        if not self.data:
          self.data = StudyData_Swig.StudyData_Object()
        self.data.SetShapeByPointer(theShape)

    pass

class SHAPERSTUDY_Group(SHAPERSTUDY_ORB__POA.SHAPER_Group, SHAPERSTUDY_Object):
    """
    Construct an instance of SHAPERSTUDY Group
    """
    def __init__ ( self, *args):
        self.seltype = None
        self.selection = []
        self.SO = None
        self.data = None
        self.entry = None
        pass

    def SetSelectionType(self, theType):
        """
        Sets what is returned in the GEOM_IGroupOperations::GetType
        """
        self.seltype = theType

    def GetSelectionType(self):
        """
        Returns the type of the selected sub-shapes
        """
        return self.seltype

    def SetSelection(self, theSelection):
        """
        Sets what is returned in the GEOM_IGroupOperations::GetObjects
        """
        self.data = None # nullify the cashed shape when selection is changed
        self.selection = theSelection

    def GetSelection(self):
        """
        Returns the selected sub-shapes indices
        """
        return self.selection

    def GetMainShape( self ):
        """
        Main shape is groups owner
        """
        return self.SO.GetFather().GetObject()

    def getShape( self ):
        """
        Redefinition of the getShape method: here it creates a shape by the
        main shape and the group index.
        """
        if not self.data:
          self.data = StudyData_Swig.StudyData_Object()
        # convert selection to long list
        anArg = StudyData_Swig.LongList()
        for l in self.selection:
          anArg.append(l)
        return self.data.groupShape(self.GetMainShape().getShape(), anArg)
