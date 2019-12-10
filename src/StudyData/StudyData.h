


#ifndef StudyData_H
#define StudyData_H

#if defined WIN32
#  if defined StudyData_EXPORTS || defined STUDYDATA_EXPORTS
#    define StudyData_EXPORT __declspec( dllexport )
#  else
#    define StudyData_EXPORT __declspec( dllimport )
#  endif
#else
#  define StudyData_EXPORT
#endif

#endif // StudyData_H
