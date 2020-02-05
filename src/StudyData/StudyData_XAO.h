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
#include <XAO_Xao.hxx>

#include <list>
#include <map>

class TopoDS_Shape;

class StudyData_XAO
{
  TopoDS_Shape* myShape; ///< the shape, part of XAO
  XAO::Xao* myExport; ///< the XAO instance for export
  XAO::Xao* myImport; ///< the XAO instance for export
  std::map<int, XAO::Group*> myGroups; ///< id of group to the group structure

public:
  StudyData_EXPORT StudyData_XAO();

  // defines the shape for XAO export
  StudyData_EXPORT void SetShape(const long long theShapePtr);

  // add a new group for export to XAO; returns id of this group
  StudyData_EXPORT int AddGroup(const int theSelType, const std::string theGroupName);
  // sets the selection for an already added group
  StudyData_EXPORT void AddGroupSelection(const int theGroupID, const int theSelection);

  // performs the export to XAO
  StudyData_EXPORT void Export(const std::string theFileName);

  // Imports the XAO data, returns the error string or empty one if it is ok.
  StudyData_EXPORT std::string Import(const std::string theFileName);

  // Returns a pointer to the shape from XAO after import
  StudyData_EXPORT long long GetShape();

  // Returns a selection type of the group
  StudyData_EXPORT int GetGroupDimension(const int theGroupID);

  // Returns a selection list of indices of the group
  StudyData_EXPORT std::list<long> GetGroupSelection(const int theGroupID);
};

#endif // !StudyData_XAO_H
