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
CMAKE_SOURCE_DIR = /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build

# Include any dependencies generated for this target.
include executables/bg/CMakeFiles/bg.dir/depend.make

# Include the progress variables for this target.
include executables/bg/CMakeFiles/bg.dir/progress.make

# Include the compile flags for this target's objects.
include executables/bg/CMakeFiles/bg.dir/flags.make

executables/bg/CMakeFiles/bg.dir/src/main.cpp.o: executables/bg/CMakeFiles/bg.dir/flags.make
executables/bg/CMakeFiles/bg.dir/src/main.cpp.o: ../executables/bg/src/main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object executables/bg/CMakeFiles/bg.dir/src/main.cpp.o"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/executables/bg && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/bg.dir/src/main.cpp.o -c /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/executables/bg/src/main.cpp

executables/bg/CMakeFiles/bg.dir/src/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/bg.dir/src/main.cpp.i"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/executables/bg && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/executables/bg/src/main.cpp > CMakeFiles/bg.dir/src/main.cpp.i

executables/bg/CMakeFiles/bg.dir/src/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/bg.dir/src/main.cpp.s"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/executables/bg && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/executables/bg/src/main.cpp -o CMakeFiles/bg.dir/src/main.cpp.s

# Object files for target bg
bg_OBJECTS = \
"CMakeFiles/bg.dir/src/main.cpp.o"

# External object files for target bg
bg_EXTERNAL_OBJECTS =

executables/bg/bg: executables/bg/CMakeFiles/bg.dir/src/main.cpp.o
executables/bg/bg: executables/bg/CMakeFiles/bg.dir/build.make
executables/bg/bg: cpp_wx_ext_lib/libwxExt.a
executables/bg/bg: executables/bg/CMakeFiles/bg.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable bg"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/executables/bg && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/bg.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
executables/bg/CMakeFiles/bg.dir/build: executables/bg/bg

.PHONY : executables/bg/CMakeFiles/bg.dir/build

executables/bg/CMakeFiles/bg.dir/clean:
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/executables/bg && $(CMAKE_COMMAND) -P CMakeFiles/bg.dir/cmake_clean.cmake
.PHONY : executables/bg/CMakeFiles/bg.dir/clean

executables/bg/CMakeFiles/bg.dir/depend:
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/executables/bg /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/executables/bg /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/executables/bg/CMakeFiles/bg.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : executables/bg/CMakeFiles/bg.dir/depend

