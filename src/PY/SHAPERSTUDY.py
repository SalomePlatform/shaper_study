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
import SALOME_ComponentPy
import SALOME_DriverPy
import SALOMEDS
from SHAPERSTUDY_utils import findOrCreateComponent, moduleName, getStudy, getORB

__entry2IOR__ = {}

class SHAPERSTUDY(SHAPERSTUDY_ORB__POA.Gen,
                  SALOME_ComponentPy.SALOME_ComponentPy_i,
                  SALOME_DriverPy.SALOME_DriverPy_i):


    ShapeType = {"AUTO":-1, "COMPOUND":0, "COMPSOLID":1, "SOLID":2, "SHELL":3, "FACE":4, "WIRE":5, "EDGE":6, "VERTEX":7, "SHAPE":8, "FLAT":9}

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

    def publish( self, theShaperObj ):
        """
        Publish GEOM_Object corresponding to a given SHAPER object
        """
        return SHAPERSTUDY_Object()

    def AddInStudy( self, theObject, theName, theFather ):
        """
        Adds in theStudy a object theObject under theFather with a name theName,
        if theFather is not NULL the object is placed under theFather's SObject.
        Returns a SObject where theObject is placed
        """
        so = SALOMEDS.SALOMEDS_SObject()
        return so

    def AddSubShape( theMainShape, theIndices ):
        """
        Add a sub-shape defined by indices in theIndices
        (contains unique IDs of sub-shapes inside theMainShape)
        """
        go = SHAPERSTUDY_Object()._this()
        return go

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
        return ""


    def Save( self, component, URL, isMultiFile ):
        """
        Saves data.
        Nothing to do here because in our case all data
        are stored in the SALOMEDS attributes.
        """
        return ""

    def Load( self, component, stream, URL, isMultiFile ):
        """
        Loads data
        """
        global __entry2IOR__
        __entry2IOR__.clear()
        #
        return 1
        
    def IORToLocalPersistentID(self, sobject, IOR, isMultiFile, isASCII):
        """
        Gets persistent ID for the CORBA object.
        It's enough to use study entry.
        """
        return sobject.GetID()

    def LocalPersistentIDToIOR(self, sobject, persistentID, isMultiFile, isASCII):
        "Converts persistent ID of the object to its IOR."
        global __entry2IOR__
        if persistentID in __entry2IOR__:
            return __entry2IOR__[persistentID]
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

    def addToStudy( self, aShape, aName ):
        """
        Publish in study aShape with name aName
        """
        try:
            so = self.AddInStudy(aShape, aName, None )
            if so and aName: so.SetAttrString("AttributeName", aName)
        except:
            print("addToStudyInFather() failed")
            return ""
        return so.GetStudyEntry()

    def addToStudyInFather(self, aFather, aShape, aName):
        """
        Publish in study aShape with name aName as sub-object of previously published aFather
        """
        try:
            so = self.AddInStudy(aShape, aName, aFather )
            if so and aName: so.SetAttrString("AttributeName", aName)
        except:
            print("addToStudyInFather() failed")
            return ""
        return so.GetStudyEntry()
