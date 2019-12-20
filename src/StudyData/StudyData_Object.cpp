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


int StudyData_Object::type() const
{
  if (myShape.IsNull())
    return 8; // GEOM.SHAPE
  return (int) myShape.ShapeType();
}


SALOMEDS::TMPFile* StudyData_Object::shapeStream() const
{
  if (myShape.IsNull())
    return NULL;

  //Returns the number of bytes that have been stored in the stream's buffer.
  int size = myStream.size();

  //Allocate octect buffer of required size
  CORBA::Octet* OctetBuf = SALOMEDS::TMPFile::allocbuf(size);

  //Copy ostrstream content to the octect buffer
  memcpy(OctetBuf, myStream.c_str(), size);

  //Create and return TMPFile
  SALOMEDS::TMPFile_var SeqFile = new SALOMEDS::TMPFile(size, size, OctetBuf, 1);
  return SeqFile._retn();
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
  BRepTools::Read(myShape, streamBrep, aBuilder);
  myTick++;
  myStream = theFile;
}

int StudyData_Object::getTick()
{
  return myTick;
}
