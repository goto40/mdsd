cmake_minimum_required(VERSION 3.0)

project(my_image_lib)

set(TSTNAME Tester.exe)

FIND_PROGRAM(TEXTX_PATH textx)
message("textx found at ${TEXTX_PATH}")

# determine whether this is a standalone project or included by other projects
set(GSL_STANDALONE_PROJECT OFF)
if (CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
  set(GSL_STANDALONE_PROJECT ON)
endif ()

set(CMAKE_CXX_FLAGS "-Wall -Wextra -Weffc++ -pedantic -pthread")
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
set(CMAKE_LINKER_FLAGS "-pthread")

# set compiler flags
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED on)

# -------------------------------------------------------------
set(SRCGEN src-gen)
add_custom_target(
    my_image_lib_item_code
    COMMAND ${TEXTX_PATH} generate model/*.item --overwrite --target cpp  --output-path=${SRCGEN}
    COMMAND ${TEXTX_PATH} generate model/*.algo --overwrite --target cpp  --output-path=${SRCGEN}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
)

# -------------------------------------------------------------

# add include_directories
include_directories(src)
include_directories(${SRCGEN})

file(GLOB_RECURSE INCGEN "${SRCGEN}/*.h")
file(GLOB_RECURSE INC "src/*.h")
file(GLOB_RECURSE MODEL "model/*.item")

add_library(my_image_lib INTERFACE)
target_sources(my_image_lib INTERFACE ${INC} ${INCGEN} ${MODEL})
target_include_directories(my_image_lib INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/src/)
target_include_directories(my_image_lib INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/${SRCGEN}/)
add_dependencies(my_image_lib my_image_lib_item_code)

install(DIRECTORY src/ DESTINATION include FILES_MATCHING PATTERN "*.h")
install(DIRECTORY src-gen/ DESTINATION include FILES_MATCHING PATTERN "*.h")
# -------------------------------------------------------------
# define tester
set(TSTSRC tests)
file(GLOB_RECURSE TSTFILES "${TSTSRC}/*.cpp")
add_executable(${TSTNAME} ${TSTFILES})
target_link_libraries(${TSTNAME})
add_dependencies(${TSTNAME} my_image_lib_item_code)
