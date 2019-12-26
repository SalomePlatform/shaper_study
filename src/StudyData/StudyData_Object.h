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

#ifndef StudyData_Object_H

#include "StudyData.h"

#include <SALOMEconfig.h>
#include CORBA_SERVER_HEADER(GEOM_Gen)

#include <TopoDS_Shape.hxx>

class StudyData_EXPORT StudyData_Object
{
public:
  StudyData_Object(const std::string theFile);

  int type() const;

  std::string shapeStream() const;
  std::string oldShapeStream() const;

  long long shape() const;

  // updates the current shape if needed
  void updateShape(const std::string theFile);

  // returns the version number of the shape starting from 1
  int getTick() const;

  // sets the version number of the shape starting from 1
  void setTick(const int theValue);

private:
  std::string myStream, myOldStream; // the current and old stream of a shape
  TopoDS_Shape myShape, myOldShape; // latest shape of this object and the old one
  int myTick; // version index of the shape
};

#endif // !StudyData_Object_H
