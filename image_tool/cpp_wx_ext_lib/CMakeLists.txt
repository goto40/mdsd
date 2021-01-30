cmake_minimum_required(VERSION 3.7)

PROJECT(wxExt)
SET(wxWidgets_USE_LIBS)

# determine whether this is a standalone project or included by other projects
set(GSL_STANDALONE_PROJECT OFF)
if (CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
  set(GSL_STANDALONE_PROJECT ON)
endif ()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_CXX_FLAGS "-Wall -Wextra -Weffc++ -pedantic -pthread")
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
set(CMAKE_LINKER_FLAGS "-pthread")

set(SRCDIR src)
set(SRCGENDIR src-gen)
set(RESDIR res)

include_directories(${SRCDIR})
include_directories(${SRCGENDIR})
file(GLOB_RECURSE SRC "${SRCDIR}/*.cpp")
file(GLOB_RECURSE INC "${SRCDIR}/*.h")

EXEC_PROGRAM(xxd ${CMAKE_CURRENT_SOURCE_DIR}
		ARGS --include ${RESDIR}/images.zip
		OUTPUT_VARIABLE IMAGES_ZIP_HEX)
CONFIGURE_FILE(${RESDIR}/images_zip.h.in ${CMAKE_CURRENT_SOURCE_DIR}/${SRCGENDIR}/images_zip.h)

#FIND_PACKAGE(my_image_lib)
FIND_PACKAGE(wxWidgets REQUIRED)
   
INCLUDE("${wxWidgets_USE_FILE}")

ADD_LIBRARY(wxExt STATIC ${SRC} ${INC})
TARGET_LINK_LIBRARIES(wxExt PUBLIC my_image_lib ${wxWidgets_LIBRARIES})
target_include_directories(wxExt INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/src/)

ADD_LIBRARY(wxExtDll SHARED ${SRC} ${INC})
TARGET_LINK_LIBRARIES(wxExtDll PUBLIC my_image_lib ${wxWidgets_LIBRARIES})
target_include_directories(wxExtDll INTERFACE src/)

set_target_properties(wxExtDll PROPERTIES OUTPUT_NAME wxExt)

install(DIRECTORY src/ DESTINATION include FILES_MATCHING PATTERN "*.h")
install(TARGETS wxExt EXPORT wxExt ARCHIVE DESTINATION lib)
install(TARGETS wxExtDll EXPORT wxExtDll LIBRARY DESTINATION lib)

