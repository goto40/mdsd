cmake_minimum_required(VERSION 3.0)

project(mdsd_support_library)

set(TSTNAME Tester.exe)

# set compiler flags
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED on)

# -------------------------------------------------------------
set(SRCGEN src-gen)
add_custom_target(
    mdsd_support_library_cpp_item_code
    COMMAND textx generate ../mdsd_support_library_common/model/*.item --overwrite --target cpp  --output-path=${SRCGEN}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
)

# -------------------------------------------------------------
include_directories(src)

# add include_directories
include_directories(${SRCGEN})
file(GLOB_RECURSE INC "src/*.h")

add_library(mdsd_support_library INTERFACE)
target_include_directories(mdsd_support_library INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/src/)

install(DIRECTORY src/ DESTINATION include FILES_MATCHING PATTERN "*.h")
# -------------------------------------------------------------
# define tester
set(TSTSRC tests)
file(GLOB_RECURSE TSTFILES "${TSTSRC}/*.cpp")
add_executable(${TSTNAME} ${TSTFILES})
target_sources(${TSTNAME} PUBLIC ${INC})
target_link_libraries(${TSTNAME})
add_dependencies(${TSTNAME} mdsd_support_library_cpp_item_code)
