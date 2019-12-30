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

#include "StudyData_Object.h"

#include <TopExp.hxx>
#include <BRep_Builder.hxx>
#include <BRepTools.hxx>
#include <BRepBuilderAPI_Copy.hxx>

StudyData_Object::StudyData_Object(const std::string theFile)
{
  std::istringstream streamBrep(theFile.c_str());
  BRep_Builder aBuilder;
  BRepTools::Read(myShape, streamBrep, aBuilder);
  myTick = 1;
  myStream = theFile;
}

StudyData_Object::StudyData_Object()
{
  myTick = 0; // when shape is defined, it will be increased to 1
}

int StudyData_Object::type() const
{
  if (myShape.IsNull())
    return 8; // GEOM.SHAPE
  return (int) myShape.ShapeType();
}

std::string StudyData_Object::shapeStream() const
{
  return myStream;
}

std::string StudyData_Object::oldShapeStream() const
{
  return myOldStream.empty() ? myStream : myOldStream;
}

long long StudyData_Object::shape() const
{
  return ((long long)(&myShape));
}

void StudyData_Object::updateShape(const std::string theFile)
{
  if (myStream == theFile) { // absolutely identical shapes, no need to store
    return;
  }
  // update the current shape
  std::istringstream streamBrep(theFile.c_str());
  BRep_Builder aBuilder;
  myOldShape = myShape;
  BRepTools::Read(myShape, streamBrep, aBuilder);
  myTick++;
  myOldStream = myStream;
  myStream = theFile;
}

int StudyData_Object::getTick() const
{
  return myTick;
}

void StudyData_Object::setTick(const int theValue)
{
  myTick = theValue;
}

void StudyData_Object::SetShapeByPointer(const long long theShape)
{
  myOldShape = myShape;
  myShape = *((TopoDS_Shape*)theShape);
  std::ostringstream aStreamBrep;
  if (!myShape.IsNull()) {
    BRepTools::Write(myShape, aStreamBrep);
  }
  myOldStream = myStream;
  myStream = aStreamBrep.str();
  myTick++;
}

long long StudyData_Object::groupShape(long long theMainShape, const std::list<long> theSelection)
{
  if (myShape.IsNull()) { // compute the cashed shape
    TopoDS_Shape* aShape = (TopoDS_Shape*)theMainShape;
    TopTools_IndexedMapOfShape anIndices;
    TopExp::MapShapes(*aShape, anIndices);

    TopoDS_Compound aResult;
    BRep_Builder aBuilder;
    aBuilder.MakeCompound(aResult);

    std::list<long>::const_iterator aSelIter = theSelection.cbegin();
    for(; aSelIter != theSelection.cend(); aSelIter++) {
      TopoDS_Shape aSel = anIndices.FindKey(*aSelIter);
      aBuilder.Add(aResult, aSel);
    }
    myShape = aResult;
  }
  return (long long)(&myShape);
}
