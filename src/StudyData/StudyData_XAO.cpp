// Copyright (C) 2007-2019  CEA/DEN, EDF R&D, OPEN CASCADE
//
// Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
// CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
//
// See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
//

#include "StudyData_XAO.h"

#include <XAO_Group.hxx>
#include <XAO_Field.hxx>
#include <XAO_Geometry.hxx>
#include <XAO_XaoExporter.hxx>
#include <XAO_BrepGeometry.hxx>


StudyData_XAO::StudyData_XAO() : myExport(NULL), myImport(NULL)
{}

void StudyData_XAO::SetShape(const long long theShapePtr)
{
  myShape = (TopoDS_Shape*)(theShapePtr);
  if (!myExport)
    myExport = new XAO::Xao();
  XAO::BrepGeometry* aGeometry = new XAO::BrepGeometry;
  myExport->setGeometry(aGeometry);
  aGeometry->setTopoDS_Shape(*myShape);
}

int StudyData_XAO::AddGroup(const int theSelType, const std::string theGroupName)
{
  if (!myExport)
    myExport = new XAO::Xao();
  XAO::Dimension aDimension;
  switch(theSelType) {
  case 7: aDimension = XAO::VERTEX; break;
  case 6: aDimension = XAO::EDGE; break;
  case 4: aDimension = XAO::FACE; break;
  case 2: aDimension = XAO::SOLID; break;
  default: aDimension = XAO::WHOLE;
  };
  XAO::Group* aNewGroup = myExport->addGroup(aDimension, theGroupName);
  int anID = (int)myGroups.size();
  myGroups[anID] = aNewGroup;
  return anID;
}

void StudyData_XAO::AddGroupSelection(const int theGroupID, const int theSelection)
{
  XAO::Group* aGroup = myGroups[theGroupID];
  aGroup->add(theSelection);
}

void StudyData_XAO::Export(const std::string theFileName)
{
  if (!myExport)
    myExport = new XAO::Xao();
  myExport->setAuthor("ShaperStudy");

  XAO::XaoExporter::saveToFile(myExport, theFileName, "");
}

std::string StudyData_XAO::Import(const std::string theFileName)
{
  std::string anError;
  myImport = new XAO::Xao();
  try {
    if (XAO::XaoExporter::readFromFile(theFileName, myImport)) {
      XAO::Geometry* aGeometry = myImport->getGeometry();
      XAO::Format aFormat = aGeometry->getFormat();
      if (aFormat == XAO::BREP) {
        if (XAO::BrepGeometry* aBrepGeometry = dynamic_cast<XAO::BrepGeometry*>(aGeometry))
          myShape = new TopoDS_Shape(aBrepGeometry->getTopoDS_Shape());
      } else {
        anError = "Unsupported XAO geometry format:" + XAO::XaoUtils::shapeFormatToString(aFormat);
      }
    } else {
      anError = "XAO object was not read successful";
    }
  } catch (XAO::XAO_Exception& e) {
    anError = e.what();
  }

  return anError;
}

long long StudyData_XAO::GetShape()
{
  return (long long)(myShape);
}

int StudyData_XAO::GetGroupDimension(const int theGroupID)
{
  XAO::Group* aXaoGroup = myImport->getGroup(theGroupID);
  switch(aXaoGroup->getDimension()) {
  case XAO::VERTEX: return 7;
  case XAO::EDGE: return 6;
  case XAO::FACE: return 4;
  case XAO::SOLID: return 2;
  default: return -1;
  }
  return -1;
}

std::list<long> StudyData_XAO::GetGroupSelection(const int theGroupID)
{
  XAO::Group* aXaoGroup = myImport->getGroup(theGroupID);
  std::list<long> aResult;
  for (int anElementIndex = 0; anElementIndex < aXaoGroup->count(); ++anElementIndex) {
    aResult.push_back(aXaoGroup->get(anElementIndex));
  }
  return aResult;
}
