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
import SALOME_ComponentPy
import SALOME_DriverPy
import SALOMEDS
from SHAPERSTUDY_utils import findOrCreateComponent, moduleName, getStudy, getORB
import salome
import SHAPERSTUDY_Object
import GEOM

__entry2IOR__ = {}


class SHAPERSTUDY(SHAPERSTUDY_ORB__POA.Gen,
                  SALOME_ComponentPy.SALOME_ComponentPy_i,
                  SALOME_DriverPy.SALOME_DriverPy_i):


    ShapeType = {"AUTO":-1, "COMPOUND":0, "COMPSOLID":1, "SOLID":2, "SHELL":3, "FACE":4, "WIRE":5, "EDGE":6, "VERTEX":7, "SHAPE":8, "FLAT":9}
    
    ShaperIcons = {GEOM.COMPOUND:"SHAPER_ICON_COMPSOLID",
        GEOM.COMPSOLID:"SHAPER_ICON_COMPSOLID",
        GEOM.SOLID:"SHAPER_ICON_SOLID",
        GEOM.SHELL:"SHAPER_ICON_SHELL",
        GEOM.FACE:"SHAPER_ICON_FACE",
        GEOM.WIRE:"SHAPER_ICON_WIRE",
        GEOM.EDGE:"SHAPER_ICON_EDGE",
        GEOM.VERTEX:"SHAPER_ICON_VERTEX",
        GEOM.SHAPE:"SHAPER_ICON_SOLID",
        GEOM.FLAT:"SHAPER_ICON_FACE"}

    def __init__ ( self, orb, poa, contID, containerName, instanceName, interfaceName ):
        """
        Construct an instance of SHAPERSTUDY module engine.
        The class SHAPERSTUDY implements CORBA interface Gen (see SHAPERSTUDY_Gen.idl).
        It is inherited (via GEOM_Gen) from the classes SALOME_ComponentPy_i (implementation of
        Engines::EngineComponent CORBA interface - SALOME component) and SALOME_DriverPy_i
        (implementation of SALOMEDS::Driver CORBA interface - SALOME module's engine).
        """
        SALOME_ComponentPy.SALOME_ComponentPy_i.__init__(self, orb, poa,
                    contID, containerName, instanceName, interfaceName, False)
        SALOME_DriverPy.SALOME_DriverPy_i.__init__(self, interfaceName)
        #
        #self._naming_service = SALOME_ComponentPy.SALOME_NamingServicePy_i( self._orb )
        #
        pass

    def FindOrCreateShape( self, theInternalEntry ):
        """
        Searches existing or creates a new SHAPERSTUDY_Object to interact with SHAPER
        """
        # Searching in the study tree
        aComponent = findOrCreateComponent()
        aSOIter = getStudy().NewChildIterator(aComponent)
        while aSOIter.More():
          aSO = aSOIter.Value()
          anIOR = aSO.GetIOR()
          anObj = salome.orb.string_to_object(anIOR)
          if isinstance(anObj, SHAPERSTUDY_ORB._objref_SHAPER_Object):
            if anObj.GetEntry() == theInternalEntry:
              return anObj
          aSOIter.Next()

        aShapeObj = SHAPERSTUDY_Object.SHAPERSTUDY_Object()
        aShapeObj.SetEntry(theInternalEntry)
        return aShapeObj._this()

    def AddInStudy( self, theObject, theName, theFather ):
        """
        Adds in theStudy a object theObject under theFather with a name theName,
        if theFather is not NULL the object is placed under theFather's SObject.
        Returns a SObject where theObject is placed
        """
        aStudy = getStudy()
        aBuilder = aStudy.NewBuilder()
        if not theFather:
          theFather = findOrCreateComponent()
        aResultSO = aBuilder.NewObject(theFather);
        aResultSO.SetAttrString("AttributeName", theName)
        
        
        if theObject is not None:
            anIOR = salome.orb.object_to_string(theObject)
            aResultSO.SetAttrString("AttributeIOR", anIOR)
            theObject.SetSO(aResultSO)
          
            aType = theObject.GetShapeType()
            aAttr = aBuilder.FindOrCreateAttribute(aResultSO, "AttributePixMap")
            aPixmap = aAttr._narrow(salome.SALOMEDS.AttributePixMap)
            aPixmap.SetPixMap(SHAPERSTUDY.ShaperIcons[aType])
            
        # add a red-reference that means that this is an active reference to SHAPER result
        aSub = aBuilder.NewObject(aResultSO)
        aBuilder.Addreference(aSub, aResultSO)

        return aResultSO

    def AddSubShape( theMainShape, theIndices ):
        """
        Add a sub-shape defined by indices in theIndices
        (contains unique IDs of sub-shapes inside theMainShape)
        """
        go = SHAPERSTUDY_Object()._this()
        return go

    # For now it is impossible to remove anything from the SHAPER-STUDY
    def RemoveObject( self, theObject ):
        """
        Removes the object from the component
        """
        return

    def GetIFieldOperations( self ):
        """
        """
        return SHAPERSTUDY_IFieldOperations()

    def GetIGroupOperations( self ):
        """
        """
        return SHAPERSTUDY_IGroupOperations()

    def GetIShapesOperations( self ):
        """
        """
        return SHAPERSTUDY_IShapesOperations()

    def GetIMeasureOperations( self ):
        """
        """
        return SHAPERSTUDY_IMeasureOperations()

    def GetStringFromIOR( self, theObject ):
        """
        Returns a string which contains an IOR of the SHAPERSTUDY_Object
        """
        IOR = ""
        if theObject and getORB():
            IOR = getORB().object_to_string( theObject )
            pass
        return IOR

    def GetAllDumpNames( self ):
        """
        Returns all names with which Object's was dumped
        into python script to avoid the same names in SMESH script
        """
        return [""]

    def GetDumpName( self, theStudyEntry ):
        """
        Returns a name with which a GEOM_Object was dumped into python script

        Parameters:
            theStudyEntry is an entry of the Object in the study
        """
        return "test"

    def Save( self, component, URL, isMultiFile ):
        """
        Saves data: all objects into one file
        """
        aResult = "" # string-pairs of internal entries and shape streams
        aStudy = getStudy()
        aSOIter = aStudy.NewChildIterator(findOrCreateComponent())
        while aSOIter.More():
          aSOVal = aSOIter.Value()
          aSOList = [aSOVal]
          # collect also the history shape objects
          aRes, aHistSO = aSOVal.FindSubObject(2)
          if aRes:
            aSOIter2 = aStudy.NewChildIterator(aHistSO)
            while aSOIter2.More():
              aSOList.append(aSOIter2.Value())
              aSOIter2.Next()
          # for each sobject export shapes stream if exists
          for aSO in aSOList:
            anIOR = aSO.GetIOR()
            anObj = salome.orb.string_to_object(anIOR)
            if isinstance(anObj, SHAPERSTUDY_ORB._objref_SHAPER_Object):
              if len(aResult):
                aResult = aResult + '|'
              aResult = aResult + anObj.GetEntry() + "|" + anObj.GetShapeStream().decode()
              aResult = aResult + "|" + anObj.GetOldShapeStream().decode()

          aSOIter.Next()
        return aResult.encode()

    def Load( self, component, stream, URL, isMultiFile ):
        """
        Loads data
        """
        global __entry2IOR__
        __entry2IOR__.clear()
        
        aList=stream.decode().split('|')
        aSubNum = 1
        anId = ""
        aNewShapeStream = ""
        for aSub in aList:
          if aSubNum == 1:
            anId = aSub
            aSubNum = 2
          elif aSubNum == 2:
            aNewShapeStream = aSub
            aSubNum = 3
          else: # create shapes by BRep in the stream: set old first then new
            aShapeObj = SHAPERSTUDY_Object.SHAPERSTUDY_Object()
            if len(aSub):
              aShapeObj.SetShapeByStream(aSub)
            aShapeObj.SetShapeByStream(aNewShapeStream)
            aShapeObj.SetEntry(anId)
            anIOR = salome.orb.object_to_string(aShapeObj._this())
            __entry2IOR__[anId] = anIOR
            aSubNum = 1

        return 1
        
    def IORToLocalPersistentID(self, sobject, IOR, isMultiFile, isASCII):
        """
        Gets persistent ID for the CORBA object.
        The internal entry of the Object is returned.
        """
        anObj = salome.orb.string_to_object(IOR)
        if anObj and isinstance(anObj, SHAPERSTUDY_ORB._objref_SHAPER_Object):
          return anObj.GetEntry()
        return ""

    def LocalPersistentIDToIOR(self, sobject, persistentID, isMultiFile, isASCII):
        "Converts persistent ID of the object to its IOR."
        global __entry2IOR__
        if persistentID in __entry2IOR__:
          aRes = __entry2IOR__[persistentID]
          if len(aRes): # set SO from the study, the sobject param is temporary, don't store it
            salome.orb.string_to_object(aRes).SetSO(getStudy().FindObjectID(sobject.GetID()))
          return aRes
        return ""

    def DumpPython( self, isPublished, isMultiFile ):
        """
        Dump module data to the Python script.
        """
        return ("".encode(), 1)



    def CreateGroup( self, theMainShape, theShapeType ):
        """
        Creates a new group which will store sub-shapes of theMainShape
        """
        return GetIGroupOperations().CreateGroup( theMainShape, theShapeType );

    def ExtractShapes( self, aShape, aType, isSorted = False ):
        """
        Extract shapes (excluding the main shape) of given type.

        Parameters:
            aShape The shape.
            aType  The shape type (see geompy.ShapeType)
            isSorted Boolean flag to switch sorting on/off.

        Returns:
            List of sub-shapes of type aType, contained in aShape.
        """
        return [ SHAPERSTUDY_Object()._this() ]

    def GetSubShape( self, aShape, ListOfID ):
        """
        Obtain a composite sub-shape of aShape, composed from sub-shapes
        of aShape, selected by their unique IDs inside aShape

        Parameters:
            aShape Shape to get sub-shape of.
            ListOfID List of sub-shapes indices.
        """
        return SHAPERSTUDY_Object()._this()

    def GetSubShapeID( self, aShape, aSubShape ):
        """
        Obtain unique ID of sub-shape aSubShape inside aShape
        of aShape, selected by their unique IDs inside aShape

        Parameters:
           aShape Shape to get sub-shape of.
           aSubShape Sub-shapes of aShape.
        """
        return 1

    def MinDistance( self, theShape1, theShape2 ):
        """
        Get minimal distance between the given shapes.
        """
        return 0.

    def NumberOfEdges( self, theShape ):
        """
        Gives quantity of edges in the given shape.
        """
        return 0

    def NumberOfFaces( self,  ):
        """
        Gives quantity of faces in the given shape.
        """
        return 0

    def PointCoordinates( self, theVertex ):
        """
        Get point coordinates
        """
        return 0,0,0

    def SubShapeAll( self, aShape, aType ):
        """
        Explode a shape on sub-shapes of a given type.
        If the shape itself matches the type, it is also returned.
        """
        return [ SHAPERSTUDY_Object()._this() ]

    def SubShapeName( self, aSubObj, aMainObj ):
        """
        Get name for sub-shape aSubObj of shape aMainObj
        """
        return ""

    def SubShapes( self, aShape, anIDs ):
        """
        Get a set of sub-shapes defined by their unique IDs inside theMainShape
        """
        return  [ SHAPERSTUDY_Object()._this() ]

    def Tolerance( self, theShape ):
        """
        Get min and max tolerances of sub-shapes of theShape

        Returns:
            [FaceMin,FaceMax, EdgeMin,EdgeMax, VertMin,VertMax]
        """
        return [0,0, 0,0, 0,0]

    def UnionList( self, theGroup, theSubShapes ):
        """
        Adds to the group all the given shapes. No errors, if some shapes are already included.
        """
        return GetIGroupOperations().UnionList( theGroup, theSubShapes )

    def BreakLink(self, theEntry):
        """
        Breaks links to not-dead shape, make the shape as dead
        """
        aStudy = getStudy()
        aSO = aStudy.FindObjectID(theEntry)
        if not aSO:
          return
        aRes, aSSO = aSO.ReferencedObject()
        if not aRes:
          return # only SObjects referenced to the SHAPEr STUDY objects are allowed
        anIOR = aSSO.GetIOR()
        if not anIOR:
          return # must be referenced to the SHAPER STUDY shape
        anObj = salome.orb.string_to_object(anIOR)
        if not anObj or not isinstance(anObj, SHAPERSTUDY_ORB._objref_SHAPER_Object):
          return
        if anObj.IsDead():
          return # do nothing for reference to already dead shape
        aDeadShape = anObj.MakeDead()
        aBuilder = aStudy.NewBuilder()
        aBuilder.RemoveReference(aSO) # reset reference to the dead shape
        aBuilder.Addreference(aSO, aDeadShape.GetSO())
