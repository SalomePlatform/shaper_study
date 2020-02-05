

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
