

%module StudyData_Swig

%{
#include "StudyData_Object.h"
%}

// standard definitions
%include "typemaps.i"
%include "std_string.i"

#define StudyData_EXPORT

%include "StudyData_Object.h"
