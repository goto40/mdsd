# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.13

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
CMAKE_SOURCE_DIR = /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib/build

# Include any dependencies generated for this target.
include CMakeFiles/wxExt.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/wxExt.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/wxExt.dir/flags.make

CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.o: CMakeFiles/wxExt.dir/flags.make
CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.o: ../src/wxExt/wxImagesZip.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.o -c /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib/src/wxExt/wxImagesZip.cpp

CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib/src/wxExt/wxImagesZip.cpp > CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.i

CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib/src/wxExt/wxImagesZip.cpp -o CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.s

# Object files for target wxExt
wxExt_OBJECTS = \
"CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.o"

# External object files for target wxExt
wxExt_EXTERNAL_OBJECTS =

libwxExt.a: CMakeFiles/wxExt.dir/src/wxExt/wxImagesZip.cpp.o
libwxExt.a: CMakeFiles/wxExt.dir/build.make
libwxExt.a: CMakeFiles/wxExt.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libwxExt.a"
	$(CMAKE_COMMAND) -P CMakeFiles/wxExt.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/wxExt.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/wxExt.dir/build: libwxExt.a

.PHONY : CMakeFiles/wxExt.dir/build

CMakeFiles/wxExt.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/wxExt.dir/cmake_clean.cmake
.PHONY : CMakeFiles/wxExt.dir/clean

CMakeFiles/wxExt.dir/depend:
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib/build /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib/build /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/cpp_wx_ext_lib/build/CMakeFiles/wxExt.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/wxExt.dir/depend

