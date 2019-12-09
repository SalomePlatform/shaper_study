# Copyright (C) 2012-2019  CEA/DEN, EDF R&D, OPEN CASCADE
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#


# --- options ---
# additional include directories
INCLUDE_DIRECTORIES(
  ${KERNEL_INCLUDE_DIRS}
  ${GEOM_INCLUDE_DIRS}
  ${OpenCASCADE_INCLUDE_DIR}
  ${SHAPER_INCLUDE_DIRS}
)

# additional preprocessor / compiler flags
ADD_DEFINITIONS(
  ${OpenCASCADE_DEFINITIONS}
)

# libraries to link to
SET(_link_LIBRARIES
  # ${OpenCASCADE_ModelingAlgorithms_LIBRARIES}
  # ${OpenCASCADE_ModelingData_LIBRARIES}
  # ${OpenCASCADE_ApplicationFramework_LIBRARIES}
  # ${GEOM_NMTTools}
  # ${GEOM_GEOMUtils}
)

# --- headers ---

# header files / no moc processing
SET(SHAPERSTUDYCore_HEADERS
)

# --- sources ---

# sources / static
SET(SHAPERSTUDYCore_SOURCES
)

# --- rules ---

ADD_LIBRARY(SHAPERSTUDYCore ${SHAPERSTUDYCore_SOURCES})
IF(WIN32)
  TARGET_COMPILE_OPTIONS(SHAPERSTUDYCore PRIVATE /bigobj) 
ENDIF(WIN32)

TARGET_LINK_LIBRARIES(SHAPERSTUDYCore ${_link_LIBRARIES} )
INSTALL(TARGETS SHAPERSTUDYCore EXPORT ${PROJECT_NAME}TargetGroup DESTINATION ${SALOME_INSTALL_LIBS})

INSTALL(FILES ${SHAPERSTUDYCore_HEADERS} DESTINATION ${SALOME_INSTALL_HEADERS})
