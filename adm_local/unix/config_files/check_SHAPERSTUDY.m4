dnl Copyright (C) 2007-2019  CEA/DEN, EDF R&D, OPEN CASCADE
dnl
dnl Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
dnl CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
dnl
dnl This library is free software; you can redistribute it and/or
dnl modify it under the terms of the GNU Lesser General Public
dnl License as published by the Free Software Foundation; either
dnl version 2.1 of the License, or (at your option) any later version.
dnl
dnl This library is distributed in the hope that it will be useful,
dnl but WITHOUT ANY WARRANTY; without even the implied warranty of
dnl MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
dnl Lesser General Public License for more details.
dnl
dnl You should have received a copy of the GNU Lesser General Public
dnl License along with this library; if not, write to the Free Software
dnl Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
dnl
dnl See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
dnl

#  Check availability of SHAPERSTUDY binary distribution
#
#  Author : Marc Tajchman (CEA, 2002)
#------------------------------------------------------------

AC_DEFUN([CHECK_SHAPERSTUDY],[

AC_CHECKING(for SHAPERSTUDY)

SHAPERSTUDY_ok=no

AC_ARG_WITH(SHAPERSTUDY,
	    --with-shaperstudy=DIR root directory path of SHAPERSTUDY installation,
	    SHAPERSTUDY_DIR="$withval",SHAPERSTUDY_DIR="")

if test "x$SHAPERSTUDY_DIR" = "x" ; then

# no --with-py-hello option used

  if test "x$SHAPERSTUDY_ROOT_DIR" != "x" ; then

    # SHAPERSTUDY_ROOT_DIR environment variable defined
    SHAPERSTUDY_DIR=$SHAPERSTUDY_ROOT_DIR

  else

    # search SHAPERSTUDY binaries in PATH variable
    AC_PATH_PROG(TEMP, SHAPERSTUDYGUI.py)
    if test "x$TEMP" != "x" ; then
      SHAPERSTUDY_BIN_DIR=`dirname $TEMP`
      SHAPERSTUDY_DIR=`dirname $SHAPERSTUDY_BIN_DIR`
    fi

  fi
#
fi

if test -f ${SHAPERSTUDY_DIR}/bin/salome/SHAPERSTUDY.py  ; then
  SHAPERSTUDY_ok=yes
  AC_MSG_RESULT(Using SHAPERSTUDY distribution in ${SHAPERSTUDY_DIR})

  if test "x$SHAPERSTUDY_ROOT_DIR" == "x" ; then
    SHAPERSTUDY_ROOT_DIR=${SHAPERSTUDY_DIR}
  fi
  AC_SUBST(SHAPERSTUDY_ROOT_DIR)
else
  AC_MSG_WARN("Cannot find compiled SHAPERSTUDY distribution")
fi
  
AC_MSG_RESULT(for SHAPERSTUDY: $SHAPERSTUDY_ok)
 
])dnl
 
