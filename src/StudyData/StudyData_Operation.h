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

#ifndef StudyData_Operation_H

#include "StudyData.h"

#include <list>

/// Class for specific shape operations call that can be implemented in C++ only
/// with usage of the OpenCascade shapes.
class StudyData_EXPORT StudyData_Operation
{
public:
  StudyData_Operation() {}

  /// Explode a shape on sub-shapes of a given type.
  /// If isSorted is true, sub-shapes will be sorted by coordinates of their gravity center
  std::list<long> GetAllSubShapesIDs(
    const long long theShape, const int theShapeType, const bool isSorted);

  /// Get pointers to sub-shapes, shared by input shapes.
  std::list<long long> GetSharedShapes(
    const long long theShape1, const long long theShape2, const int theShapeType);

  /// Returns the theSubShape index in theMainShape. Shapes are passed as pointers values.
  /// Returns zero if there is no such sub-shape in the main shape.
  int GetSubShapeIndex(const long long theMainShape, const long long theSubShape);

  /// Get a sub-shape defined by its unique ID within theMainShape.
  long long GetSubShape(const long long theMainShape, long theID);
};

#endif // !StudyData_Operation_H