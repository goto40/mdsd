# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/framework/mdsd_support_library_cpp

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/framework/mdsd_support_library_cpp/build

# Utility rule file for mdsd_support_library_cpp_item_code.

# Include the progress variables for this target.
include CMakeFiles/mdsd_support_library_cpp_item_code.dir/progress.make

CMakeFiles/mdsd_support_library_cpp_item_code:
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/framework/mdsd_support_library_cpp && textx generate ../mdsd_support_library_common/model/*.item --overwrite --target cpp --output-path=src-gen

mdsd_support_library_cpp_item_code: CMakeFiles/mdsd_support_library_cpp_item_code
mdsd_support_library_cpp_item_code: CMakeFiles/mdsd_support_library_cpp_item_code.dir/build.make

.PHONY : mdsd_support_library_cpp_item_code

# Rule to build all files generated by this target.
CMakeFiles/mdsd_support_library_cpp_item_code.dir/build: mdsd_support_library_cpp_item_code

.PHONY : CMakeFiles/mdsd_support_library_cpp_item_code.dir/build

CMakeFiles/mdsd_support_library_cpp_item_code.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/mdsd_support_library_cpp_item_code.dir/cmake_clean.cmake
.PHONY : CMakeFiles/mdsd_support_library_cpp_item_code.dir/clean

CMakeFiles/mdsd_support_library_cpp_item_code.dir/depend:
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/framework/mdsd_support_library_cpp/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/framework/mdsd_support_library_cpp /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/framework/mdsd_support_library_cpp /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/framework/mdsd_support_library_cpp/build /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/framework/mdsd_support_library_cpp/build /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/framework/mdsd_support_library_cpp/build/CMakeFiles/mdsd_support_library_cpp_item_code.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/mdsd_support_library_cpp_item_code.dir/depend

