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
import SHAPERSTUDY_IOperations
import GEOM
import SMESH

import StudyData_Swig

__entry2IOR__ = {}
__entry2DumpName__ = {}

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
        GEOM.FLAT:"SHAPER_ICON_FACE"
        }

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
        if not theObject.GetEntry():
            return None # object not existing in shaper
        aStudy = getStudy()
        aBuilder = aStudy.NewBuilder()
        isGroup = theObject.GetType() == 37 or theObject.GetType() == 52
        if not theFather:
          if isGroup:
            return None # Group may be added only under the shape-father
          theFatherSO = findOrCreateComponent()
        else:
          theFatherSO = theFather.GetSO()
        aResultSO = None
        if isGroup: # add group to the third sub-label or later to keep space for reference and "History"
          aTag = 3
          anIter = aStudy.NewChildIterator(theFatherSO)
          while anIter.More():
            aCurrentTag = anIter.Value().Tag() + 1
            if aTag < aCurrentTag:
              aTag = aCurrentTag
            anIter.Next()
          aResultSO = aBuilder.NewObjectToTag(theFatherSO, aTag)
        else:
          aResultSO = aBuilder.NewObject(theFatherSO);
        aResultSO.SetAttrString("AttributeName", theName)
        if theObject is not None:
            anIOR = salome.orb.object_to_string(theObject)
            aResultSO.SetAttrString("AttributeIOR", anIOR)
            theObject.SetSO(aResultSO)
          
            aAttr = aBuilder.FindOrCreateAttribute(aResultSO, "AttributePixMap")
            aPixmap = aAttr._narrow(salome.SALOMEDS.AttributePixMap)
            aType = 0
            if isGroup:
              aType = SHAPERSTUDY_Object.__shape_types__[theObject.GetSelectionType()]
            else:
              aType = theObject.GetShapeType()
            aPixmap.SetPixMap(self.ShaperIcons[aType])
            
        # add a red-reference that means that this is an active reference to SHAPER result
        if not isGroup:
          aSub = aBuilder.NewObjectToTag(aResultSO, 1)
          aBuilder.Addreference(aSub, aResultSO)

        return aResultSO

    def AddSubShape( theMainShape, theIndices ):
        """
        Add a sub-shape defined by indices in theIndices
        (contains unique IDs of sub-shapes inside theMainShape)
        """
        # no sub-shapes for the moment
        go = SHAPERSTUDY_Object()._this()
        return go

    # For now it is impossible to remove anything from the SHAPER-STUDY
    def RemoveObject( self, theObject ):
        """
        Removes the object from the component
        """
        # can not be removed for the moment
        return

    def GetIFieldOperations( self ):
        """
        """
        return SHAPERSTUDY_IOperations.SHAPERSTUDY_IFieldOperations()._this()

    def GetIGroupOperations( self ):
        """
        """
        return SHAPERSTUDY_IOperations.SHAPERSTUDY_IGroupOperations()._this()

    def GetIShapesOperations( self ):
        """
        """
        return SHAPERSTUDY_IOperations.SHAPERSTUDY_IShapesOperations()._this()

    def GetIMeasureOperations( self ):
        """
        """
        return SHAPERSTUDY_IOperations.SHAPERSTUDY_IMeasureOperations()._this()

    def GetStringFromIOR( self, theObject ):
        """
        Returns a string which contains an IOR of the SHAPERSTUDY_Object
        """
        IOR = ""
        if theObject and getORB():
            IOR = getORB().object_to_string( theObject )
            pass
        return IOR

    def Save( self, component, URL, isMultiFile ):
        """
        Saves data: all objects into one file
        """
        aResult = "" # string-pairs of internal entries and shape streams
        aStudy = getStudy()
        # get all sub-SObjects with IOR defined
        anIters = [aStudy.NewChildIterator(findOrCreateComponent())]
        aSOList = []
        while len(anIters):
          aLast = anIters[len(anIters) - 1]
          if aLast.More():
            aSO = aLast.Value()
            anIOR = aSO.GetIOR()
            if len(anIOR):
              aSOList.append(aSO)
            anIters.append(aStudy.NewChildIterator(aSO))
            aLast.Next()
          else:
            anIters.remove(aLast)

        for aSO in aSOList: # for each sobject export shapes stream if exists
          anIOR = aSO.GetIOR()
          if not len(anIOR):
            continue
          anObj = salome.orb.string_to_object(anIOR)
          if type(anObj) == SHAPERSTUDY_ORB._objref_SHAPER_Group:
            if len(aResult):
              aResult += '|'
            # store internal entry, type and list of indices of the group selection (separated by spaces)
            aResult += anObj.GetEntry() + "|" + str(anObj.GetSelectionType())
            aSelList = anObj.GetSelection()
            aResult += "|" + str(' '.join(str(anI) for anI in aSelList))
          elif type(anObj) == SHAPERSTUDY_ORB._objref_SHAPER_Field:
            if len(aResult):
              aResult += '|'
            # same as for group, but in addition to the second string part - field specifics
            aResult += anObj.GetEntry() + "|" + str(anObj.GetSelectionType())
            aResult += " " + str(anObj.GetDataType()) # values type
            aSteps = anObj.GetSteps()
            aResult += " " + str(len(aSteps)) # number of steps
            aComps = anObj.GetComponents()
            aResult += " " + str(len(aComps)) # number of components
            for aComp in aComps: # components strings: but before remove spaces and '|'
              aCoded = aComp.replace(" ", "__space__").replace("|", "__vertical_bar__")
              aResult += " " + aCoded
            for aStepNum in range(len(aSteps)):
              aVals = anObj.GetStep(aStepNum + 1).GetValues()
              if aStepNum == 0:
                aResult += " " + str(len(aVals)) # first the number of values in the step
              aResult += " " + str(anObj.GetStep(aStepNum + 1).GetStamp()) # ID of stamp in step
              for aVal in aVals:
                aResult += " " + str(aVal) # all values of step
            aSelList = anObj.GetSelection()
            aResult += "|" + str(' '.join(str(anI) for anI in aSelList))
          elif isinstance(anObj, SHAPERSTUDY_ORB._objref_SHAPER_Object):
            if len(aResult):
              aResult += '|'
            # store internal entry, current and old shapes in BRep format
            aResult += anObj.GetEntry() + "|" + anObj.GetShapeStream().decode()
            aResult += "|" + anObj.GetOldShapeStream().decode()

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
          else: # create objects by 3 arguments
            anObj = None
            if anId.startswith('group') or (anId.startswith('dead') and anId.count("group") > 0): # group object
              anObj = SHAPERSTUDY_Object.SHAPERSTUDY_Group()
              if len(aSub):
                anObj.SetSelection([int(anI) for anI in aSub.split(' ')])
              anObj.SetSelectionType(int(aNewShapeStream))
            elif anId.startswith('field') or (anId.startswith('dead') and anId.count("field") > 0): # field object
              anObj = SHAPERSTUDY_Object.SHAPERSTUDY_Field()
              if len(aSub):
                anObj.SetSelection([int(anI) for anI in aSub.split(' ')])
              aParams = aNewShapeStream.split(" ")
              anObj.SetSelectionType(int(aParams[0]))
              aTypeStr = aParams[1]
              if (aTypeStr == "FDT_Bool"):
                anObj.SetValuesType(0)
              elif (aTypeStr == "FDT_Int"):
                anObj.SetValuesType(1)
              elif (aTypeStr == "FDT_Double"):
                anObj.SetValuesType(2)
              elif (aTypeStr == "FDT_String"):
                anObj.SetValuesType(3)
              aSteps = []
              aNumSteps = int(aParams[2])
              for aVal in range(aNumSteps):
                aSteps.append(aVal + 1)
              anObj.SetSteps(aSteps)
              aCompNum = int(aParams[3])
              aCompNames = []
              for aCompNameIndex in range(aCompNum):
                aCompName = aParams[4 + aCompNameIndex].replace("__space__", " ").replace("__vertical_bar__", "|")
                aCompNames.append(aCompName)
              anObj.SetComponents(aCompNames)
              aNumValsInStep = int(aParams[4 + aCompNum])
              for aStepNum in range(aNumSteps):
                aStepStartIndex = 4 + aCompNum + aStepNum * (aNumValsInStep + 1) + 1
                aStampId = int(aParams[aStepStartIndex])
                aVals = []
                for aValIndex in range(aNumValsInStep):
                  aVals.append(float(aParams[aStepStartIndex + aValIndex + 1]))
                anObj.AddFieldStep(aStampId, aStepNum + 1, aVals)
            else: # shape object by BRep in the stream: set old first then new
              anObj = SHAPERSTUDY_Object.SHAPERSTUDY_Object()
              if len(aSub):
                anObj.SetShapeByStream(aSub)
              anObj.SetShapeByStream(aNewShapeStream)
            if anObj:
              anObj.SetEntry(anId)
              anIOR = salome.orb.object_to_string(anObj._this())
              __entry2IOR__[anId] = anIOR
            aSubNum = 1
        return 1
        
    def IORToLocalPersistentID(self, sobject, IOR, isMultiFile, isASCII):
        """
        Gets persistent ID for the CORBA object.
        The internal entry of the Object is returned.
        """
        anObj = salome.orb.string_to_object(IOR)
        if anObj and (isinstance(anObj, SHAPERSTUDY_ORB._objref_SHAPER_Object) or \
                      isinstance(anObj, SHAPERSTUDY_ORB._objref_SHAPER_Field)):
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
    
    def UniqueDumpName( self, theBaseName, theID ):
        """
        Returns a unique name from the theBaseName. Keeps theBaseName if it was not used yet.
        Stores the newly generated name into the global map __entry2DumpName__.
        """
        global __entry2DumpName__
        aPrefix = 1
        # to avoid spaces and parenthesis in the variable name
        aBaseName = theBaseName.replace(" ", "_").replace("(", "").replace(")", "")
        aName = aBaseName
        while aName in __entry2DumpName__.values():
          aName = aBaseName + "_" + str(aPrefix)
          aPrefix = aPrefix + 1
        __entry2DumpName__[theID] = aName
        return aName


    def DumpPython( self, isPublished, isMultiFile ):
        """
        Dump module data to the Python script.
        """
        global __entry2DumpName__
        __entry2DumpName__.clear()
        anArchiveNum = 1
        # collect all shape-objects in the SHAPERSTUDY tree
        aShapeObjects = []
        aStudy = getStudy()
        aRoots = aStudy.NewChildIterator(findOrCreateComponent())
        while aRoots.More():
          aSO = aRoots.Value()
          anIOR = aSO.GetIOR()
          if len(anIOR):
            anObj = salome.orb.string_to_object(anIOR)
            if anObj and type(anObj) == SHAPERSTUDY_ORB._objref_SHAPER_Object:
              aShapeObjects.append(anObj)
          aRoots.Next()
        script = []
        if len(aShapeObjects):
          script.append("if 'model' in globals():")
          script.append("\tmodel.publishToShaperStudy()")
          script.append("import SHAPERSTUDY")
          for aShapeObj in aShapeObjects:
            # check this shape also has sub-groups and fields
            aGroupVarNames = []
            aSOIter = aStudy.NewChildIterator(anObj.GetSO())
            while aSOIter.More():
              aGroupSO = aSOIter.Value()
              anIOR = aGroupSO.GetIOR()
              if len(anIOR):
                aGroup = salome.orb.string_to_object(anIOR)
                if isinstance(aGroup, SHAPERSTUDY_ORB._objref_SHAPER_Group) or \
                   isinstance(aGroup, SHAPERSTUDY_ORB._objref_SHAPER_Field):
                  aGroupVarName = self.UniqueDumpName(aGroup.GetName(), aGroupSO.GetID())
                  aGroupVarNames.append(aGroupVarName)
              aSOIter.Next()
            aShapeVar = self.UniqueDumpName(anObj.GetName(), anObj.GetSO().GetID())
            aShapeStr = aShapeVar + ", "
            for aGName in aGroupVarNames:
              aShapeStr += aGName + ", "
            aShapeStr += "= SHAPERSTUDY.shape(\"" + anObj.GetEntry() +"\")"
            script.append(aShapeStr)
            # dump also dead-shapes with groups and fields in the XAO format
            aRes, aHistSO = aShapeObj.GetSO().FindSubObject(2) # the History folder
            if aRes:
              aDeads = aStudy.NewChildIterator(aHistSO)
              while aDeads.More():
                aDSO = aDeads.Value()
                aDIOR = aDSO.GetIOR()
                if len(aDIOR):
                  aDeadShape = salome.orb.string_to_object(aDIOR)
                  if aDeadShape and type(aDeadShape) == SHAPERSTUDY_ORB._objref_SHAPER_Object:
                    aDeadString = ""
                    aXAO = StudyData_Swig.StudyData_XAO()
                    aXAO.SetShape(aDeadShape.getShape())
                    anArchiveName = "archive_" + str(anArchiveNum) + ".xao"
                    if len(aStudy.GetDumpPath()):
                      anArchiveName = aStudy.GetDumpPath() + "/" + anArchiveName
                    anArchiveNum += 1
                    aDeadVarName = self.UniqueDumpName(aDeadShape.GetName(), aDSO.GetID())
                    aDeadString += aDeadVarName + ", "
                    aDGroupIter = aStudy.NewChildIterator(aDSO)

                    while aDGroupIter.More():
                      aDeadGroup = aDGroupIter.Value().GetObject()
                      if isinstance(aDeadGroup, SHAPERSTUDY_ORB._objref_SHAPER_Group):
                        aDGroupVarName = self.UniqueDumpName(aDeadGroup.GetName(), aDGroupIter.Value().GetID())
                        aDeadString += aDGroupVarName + ", "
                        aGroupID = aXAO.AddGroup(aDeadGroup.GetSelectionType(), aDGroupVarName)
                        for aSel in aDeadGroup.GetSelection():
                          aXAO.AddGroupSelection(aGroupID, aSel)
                      elif isinstance(aDeadGroup, SHAPERSTUDY_ORB._objref_SHAPER_Field):
                        aDeadField = aDeadGroup
                        aDFieldVarName = self.UniqueDumpName(aDeadField.GetName(), aDGroupIter.Value().GetID())
                        aDeadString += aDFieldVarName + ", "
                        aComponents = aDeadField.GetComponents()
                        aFieldID = aXAO.AddField(aDeadField.GetValuesType(), aDeadField.GetSelectionType(), \
                          len(aComponents), aDFieldVarName)
                        for aCompIndex in range(len(aComponents)):
                          aXAO.SetFieldComponent(aFieldID, aCompIndex, aComponents[aCompIndex])
                        aSteps = aDeadField.GetSteps()
                        for aStep in aSteps:
                          aFieldStep = aDeadField.GetStep(aStep)
                          aXAO.AddStep(aFieldID, aStep, aFieldStep.GetStamp())
                          aStepVals = aFieldStep.GetValues()
                          for aValue in aStepVals:
                            aXAO.AddStepValue(aFieldID, aStep, str(aValue))
                      aDGroupIter.Next()
                    aXAO.Export(anArchiveName)
                    aDeadString += " = SHAPERSTUDY.archive(" + aShapeVar + ", \"" + anArchiveName + "\")"
                    script.append(aDeadString)
                aDeads.Next()
          pass
        
        script.append("") # to have an end-line in the end
        result_str = "\n".join(script)
        encoded_str = result_str.encode() + b'\0' # to avoid garbage symbols in the end
        return (encoded_str, 1)

    def GetAllDumpNames( self ):
        """
        Returns all names with which Object's was dumped
        into python script to avoid the same names in SMESH script
        """
        global __entry2DumpName__
        aResultList = []
        for anEntry in __entry2DumpName__:
          aResultList.append(__entry2DumpName__[anEntry])
        return aResultList

    def GetDumpName( self, theStudyEntry ):
        """
        Returns a name with which a GEOM_Object was dumped into python script

        Parameters:
            theStudyEntry is an entry of the Object in the study
        """
        global __entry2DumpName__
        if theStudyEntry in __entry2DumpName__:
          return __entry2DumpName__[theStudyEntry]
        return ""

    def IsFather(theFather, theChild):
        """
        Returns true if theChild SObject is a child of theFather SObject
        """
        aChild = theChild.GetFather()
        while aChild.Depth() > theFather.Depth():
          aChild = aChild.GetFather()
        return aChild.GetID() == theFather.GetID()

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
        
        aMeshSObject = aSO.GetFather()
        aMeshObject = aMeshSObject.GetObject()

        aBuilder = aStudy.NewBuilder()
        aBuilder.RemoveReference(aSO) # reset reference to the dead shape
        aBuilder.Addreference(aSO, aDeadShape.GetSO())

        # check also sub-structure of the mesh to find references to sub-objects that become dead
        aRoot = aSO.GetFather()
        anIters = [aStudy.NewChildIterator(aRoot)]
        aSubList = []
        while len(anIters):
          aLast = anIters[len(anIters) - 1]
          if aLast.More():
            aSub = aLast.Value()
            aRes, aSubRef = aSub.ReferencedObject()
            if aRes and SHAPERSTUDY.IsFather(aSSO, aSubRef):
              aReferenced = aSubRef.GetObject()
              if aReferenced and not aReferenced.IsDead():
                aSubList.append(aSub)
            anIters.append(aStudy.NewChildIterator(aSub))
            aLast.Next()
          else:
            anIters.remove(aLast)
        if len(aSubList):
          # associate the number of sub-objects of the referenced objects
          aMapSubEntryToIndex = {}
          aSSOIter = aStudy.NewChildIterator(aSSO)
          anIndex = 1
          while aSSOIter.More():
            aSub = aSSOIter.Value()
            if aSub.GetIOR():
              aMapSubEntryToIndex[aSub.GetID()] = anIndex
              anIndex = anIndex + 1
            aSSOIter.Next()
          for aSubSO in aSubList:
            aRes, aSubRef = aSubSO.ReferencedObject()
            if aRes and aSubRef.GetID() in aMapSubEntryToIndex:
              anIndex = aMapSubEntryToIndex[aSubRef.GetID()]
              aDeadIter = aStudy.NewChildIterator(aDeadShape.GetSO())
              while aDeadIter.More(): # iterate dead subs to find object with the same index
                aDeadSubSO = aDeadIter.Value()
                if aDeadSubSO.GetIOR():
                  anIndex = anIndex - 1
                  if anIndex == 0:
                    # for a submesh there is no ReplaceShape, but the shape is not updated
                    # anyway, so no need to update it here
                    #aSubMeshSO = aSubSO.GetFather() # Replace shape object in the parent mesh
                    #aSubMeshObject = aSubMeshSO.GetObject()
                    #if aSubMeshObject:
                    #  aSubMeshObject.ReplaceShape(aDeadSubSO.GetObject())
                    aBuilder.RemoveReference(aSubSO) # reset reference to the dead shape
                    aBuilder.Addreference(aSubSO, aDeadSubSO)
                aDeadIter.Next()

        # Replace shape object in the parent mesh
        aMeshObject.ReplaceShape(aDeadShape)

def shape(theEntry):
  """
  Searches a shape object by the SHAPER entry. Used in the python dump script
  """
  aStudy = getStudy()
  aRoots = aStudy.NewChildIterator(findOrCreateComponent())
  while aRoots.More():
    aSO = aRoots.Value()
    anIOR = aSO.GetIOR()
    if len(anIOR):
      anObj = salome.orb.string_to_object(anIOR)
      if anObj and type(anObj) == SHAPERSTUDY_ORB._objref_SHAPER_Object and anObj.GetEntry() == theEntry:
        aRes = (anObj,)
        # add groups and fields to the result
        aSOIter = aStudy.NewChildIterator(aSO)
        while aSOIter.More():
          aGroupSO = aSOIter.Value()
          anIOR = aGroupSO.GetIOR()
          if len(anIOR):
            aGroup = salome.orb.string_to_object(anIOR)
            if isinstance(aGroup, SHAPERSTUDY_ORB._objref_SHAPER_Group) or \
               isinstance(aGroup, SHAPERSTUDY_ORB._objref_SHAPER_Field):
              aRes = aRes + (aGroup,)
          aSOIter.Next()
        return aRes
  return None # not found

def archive(theShape, theXAOFile):
  """
  Creates a dead shapes under the theShape and restores these dead objects state basing on theXAOFile
  """
  theShape.MakeDead()
  aStudy = getStudy()
  # searching for the last dead
  aDeads = aStudy.NewChildIterator(theShape.GetSO().FindSubObject(2)[1])
  aLastDeadSO = aDeads.Value()
  while aDeads.More():
    aLastDeadSO = aDeads.Value()
    aDeads.Next()

  aDShape = aLastDeadSO.GetObject()
  if aDShape:
    aXAO = StudyData_Swig.StudyData_XAO()
    anError = aXAO.Import(theXAOFile)
    if (len(anError)):
      print("Error of XAO file import: " + anError)
      return None
    aDShape.SetShapeByPointer(aXAO.GetShape())
    aRes = (aDShape,)
    # add groups and fields to the result
    aGroupIndex = 0
    aFieldIndex = 0
    aSOIter = aStudy.NewChildIterator(aLastDeadSO)
    while aSOIter.More():
      aGroupSO = aSOIter.Value()
      anIOR = aGroupSO.GetIOR()
      if len(anIOR):
        aGroup = salome.orb.string_to_object(anIOR)
        if isinstance(aGroup, SHAPERSTUDY_ORB._objref_SHAPER_Group):
          aRes += (aGroup,)
          aGroup.SetSelectionType(aXAO.GetGroupDimension(aGroupIndex))
          aSelection = []
          for aSel in aXAO.GetGroupSelection(aGroupIndex):
            aSelection.append(aSel)
          aGroup.SetSelection(aSelection)
          aGroupIndex += 1
        elif isinstance(aGroup, SHAPERSTUDY_ORB._objref_SHAPER_Field):
          aField = aGroup
          aRes += (aField,)
          aValType = aXAO.GetValuesType(aFieldIndex)
          aField.SetValuesType(aValType)
          aField.SetSelectionType(aXAO.GetSelectionType(aFieldIndex))
          aCompNames = []
          for aCompName in aXAO.GetComponents(aFieldIndex):
            aCompNames.append(aCompName)
          aField.SetComponents(aCompNames)
          aField.ClearFieldSteps()
          aXAO.BeginSteps(aFieldIndex)
          while aXAO.More(aFieldIndex):
            aValsList = []
            for aVal in aXAO.GetValues():
              if aValType == 0: # boolean
                aValsList.append(int(aVal))
              elif aValType == 1: # int
                aValsList.append(int(aVal))
              elif aValType == 2: # double
                aValsList.append(float(aVal))
            aField.AddFieldStep(aXAO.GetStamp(), aXAO.GetStepIndex(), aValsList)
            aXAO.Next()
          aFieldIndex += 1
      aSOIter.Next()
    return aRes
  return None # not found
