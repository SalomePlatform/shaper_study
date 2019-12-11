

%module StudyData_Swig

%{
#include "StudyData_Object.h"
%}

class StudyData_Object
{
public:
  StudyData_Object(const std::string theFile);
};
