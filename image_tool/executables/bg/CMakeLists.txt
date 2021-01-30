cmake_minimum_required(VERSION 3.7)

PROJECT(bg)
SET(wxWidgets_USE_LIBS)
#SET(USE_PROPGRID=1)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_CXX_FLAGS "-Wall -Wextra -Weffc++ -pedantic -pthread")
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -mavx2")
set(CMAKE_LINKER_FLAGS "-pthread")

set(SRCDIR src)
set(SRCGEN src-gen)
include_directories(${SRCDIR})
include_directories(${SRCGEN})
file(GLOB_RECURSE SRC "${SRCDIR}/*.cpp")
file(GLOB_RECURSE MODEL "model/*.item")
file(GLOB_RECURSE INC "${SRCDIR}/*.h")
file(GLOB_RECURSE INCGEN "${SRCGEN}/*.h")

add_custom_target(
    executable_bg_item_code
    COMMAND textx generate model/*.item --overwrite --target cpp  --output-path=${SRCGEN}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
)

#FIND_LIBRARY(WXEXT_LIBRARY NAMES wxExt REQUIRED)
SET(WXEXT_LIBRARY wxExt)
#FIND_PACKAGE(wxExt)
#FIND_PACKAGE(my_image_lib)

FIND_PACKAGE(wxWidgets COMPONENTS propgrid REQUIRED)
#wx_option(wxUSE_PROPGRID "use wxPropertyGrid library")

IF(wxWidgets_FOUND)
   MESSAGE("------------------------> ${wxWidgets_LIBRARIES} <----")
   INCLUDE("${wxWidgets_USE_FILE}")
   ADD_EXECUTABLE(${PROJECT_NAME} ${SRC})
   TARGET_LINK_LIBRARIES(${PROJECT_NAME} ${wxWidgets_LIBRARIES} ${WXEXT_LIBRARY})
   add_dependencies(${PROJECT_NAME} executable_bg_item_code)
   #target_sources(${PROJECT_NAME} PUBLIC ${INC} ${INCGEN} ${MODEL})
ELSE(wxWidgets_FOUND)
   MESSAGE("wxWidgets not found!")
ENDIF(wxWidgets_FOUND)


