// Copyright (C) 2019-2022  CEA/DEN, EDF R&D
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

%module StudyData_Swig

%{
#include "StudyData_Object.h"
#include "StudyData_Operation.h"
#include "StudyData_XAO.h"

#include <Standard_Failure.hxx>
#include <Standard_ErrorHandler.hxx>
#include <stdexcept>

static PyObject* setOCCException(Standard_Failure& ex)
{
  std::string msg(ex.DynamicType()->Name());
  if ( ex.GetMessageString() && strlen( ex.GetMessageString() )) {
    msg += ": ";
    msg += ex.GetMessageString();
  }
  PyErr_SetString(PyExc_Exception, msg.c_str() );
  return NULL;
}
%}

%exception
{
  try {
    OCC_CATCH_SIGNALS;
    $action }
  catch (Standard_Failure& ex) {
    return setOCCException(ex);
  }
  catch (std::exception& ex) {
    PyErr_SetString(PyExc_Exception, ex.what() );
    return NULL;
  }
}

// standard definitions
%include "typemaps.i"
%include "std_string.i"
%include "std_list.i"

#define StudyData_EXPORT

%include "StudyData_Object.h"
%include "StudyData_Operation.h"
%include "StudyData_XAO.h"

%template(LongList) std::list<long>;
%template(PtrsList) std::list<long long>;
%template(DoublList) std::list<double>;
