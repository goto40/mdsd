cmake_minimum_required(VERSION 3.7)

PROJECT(simple)
SET(wxWidgets_USE_LIBS)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_CXX_FLAGS "-Wall -Wextra -Weffc++ -pedantic")
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

set(SRCDIR src)
include_directories(${SRCDIR})
file(GLOB_RECURSE SRC "${SRCDIR}/*.cpp")

#FIND_LIBRARY(WXEXT_LIBRARY NAMES wxExt REQUIRED)
#FIND_PACKAGE(wxExt)
#FIND_PACKAGE(my_image_lib)
SET(WXEXT_LIBRARY wxExt)

#message("***************** MY_IMAGE_LIB_INCLUDE_DIR=${MY_IMAGE_LIB_INCLUDE_DIR}")
#include_directories(${MY_IMAGE_LIB_INCLUDE_DIR})

FIND_PACKAGE(wxWidgets)
IF(wxWidgets_FOUND)
   INCLUDE("${wxWidgets_USE_FILE}")
   ADD_EXECUTABLE(${PROJECT_NAME} ${SRC})
   TARGET_LINK_LIBRARIES(${PROJECT_NAME} ${wxWidgets_LIBRARIES} ${WXEXT_LIBRARY})
ELSE(wxWidgets_FOUND)
   MESSAGE("wxWidgets not found!")
ENDIF(wxWidgets_FOUND)


