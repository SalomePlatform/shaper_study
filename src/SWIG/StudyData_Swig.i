

%module StudyData_Swig

%{
#include "StudyData_Object.h"
#include "StudyData_Operation.h"
%}

// standard definitions
%include "typemaps.i"
%include "std_string.i"
%include "std_list.i"

#define StudyData_EXPORT

%include "StudyData_Object.h"
%include "StudyData_Operation.h"

%template(LongList) std::list<long>;
%template(PtrsList) std::list<long long>;
