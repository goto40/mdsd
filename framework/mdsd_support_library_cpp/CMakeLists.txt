cmake_minimum_required(VERSION 3.0)

project(mdsd_support_library)
FIND_PROGRAM(LCOV_PATH lcov)
FIND_PROGRAM(GENHTML_PATH genhtml)
find_path(CATCH_INCLUDE_PATH catch.hpp REQUIRED)
FIND_PROGRAM(TEXTX_PATH textx)
message("textx found at ${TEXTX_PATH}")
message("catch found at ${CATCH_INCLUDE_PATH}")

set(TARGET_NAME Tester.exe)

# set compiler flags
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED on)

# -------------------------------------------------------------
set(SRCGEN src-gen)
add_custom_target(
    mdsd_support_library_cpp_item_code
    COMMAND ${TEXTX_PATH} generate ../mdsd_support_library_common/model/*.item --overwrite --target cpp  --output-path=${SRCGEN}
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
add_executable(${TARGET_NAME} ${TSTFILES})
target_sources(${TARGET_NAME} PUBLIC ${INC})
target_link_libraries(${TARGET_NAME})
target_include_directories(${TARGET_NAME} SYSTEM PRIVATE ${CATCH_INCLUDE_PATH})
add_dependencies(${TARGET_NAME} mdsd_support_library_cpp_item_code)


#----------------------------------------------------------------------------------------
# from http://www.stablecoder.ca/2018/01/15/code-coverage.html
# and
# http://www.stablecoder.ca/2018/10/30/full-cmake-helper-suite.html
#
if(CMAKE_BUILD_TYPE STREQUAL "coverage" OR CODE_COVERAGE)
    if("${CMAKE_C_COMPILER_ID}" MATCHES "(Apple)?[Cc]lang" OR "${CMAKE_CXX_COMPILER_ID}" MATCHES "(Apple)?[Cc]lang")
        message("Building with llvm Code Coverage Tools")

        # Warning/Error messages
        if(NOT LLVM_COV_PATH)
            message(FATAL_ERROR "llvm-cov not found! Aborting.")
        endif()

        # set Flags
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fprofile-instr-generate -fcoverage-mapping")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-instr-generate -fcoverage-mapping")

    elseif(CMAKE_COMPILER_IS_GNUCXX)
        message("Building with lcov Code Coverage Tools")

        # Warning/Error messages
        if(NOT (CMAKE_BUILD_TYPE STREQUAL "Debug"))
            message(WARNING "Code coverage results with an optimized (non-Debug) build may be misleading")
        endif()
        if(NOT LCOV_PATH)
            message(FATAL_ERROR "lcov not found! Aborting...")
        endif()
        if(NOT GENHTML_PATH)
            message(FATAL_ERROR "genhtml not found! Aborting...")
        endif()

        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --coverage -fprofile-arcs -ftest-coverage")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage -fprofile-arcs -ftest-coverage")
    else()
        message(FATAL_ERROR "Code coverage requires Clang or GCC. Aborting.")
    endif()
endif()

