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
include my_image_lib/CMakeFiles/Tester.exe.dir/depend.make

# Include the progress variables for this target.
include my_image_lib/CMakeFiles/Tester.exe.dir/progress.make

# Include the compile flags for this target's objects.
include my_image_lib/CMakeFiles/Tester.exe.dir/flags.make

my_image_lib/CMakeFiles/Tester.exe.dir/tests/basic.cpp.o: my_image_lib/CMakeFiles/Tester.exe.dir/flags.make
my_image_lib/CMakeFiles/Tester.exe.dir/tests/basic.cpp.o: ../my_image_lib/tests/basic.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object my_image_lib/CMakeFiles/Tester.exe.dir/tests/basic.cpp.o"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/my_image_lib && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/Tester.exe.dir/tests/basic.cpp.o -c /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/my_image_lib/tests/basic.cpp

my_image_lib/CMakeFiles/Tester.exe.dir/tests/basic.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Tester.exe.dir/tests/basic.cpp.i"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/my_image_lib && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/my_image_lib/tests/basic.cpp > CMakeFiles/Tester.exe.dir/tests/basic.cpp.i

my_image_lib/CMakeFiles/Tester.exe.dir/tests/basic.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Tester.exe.dir/tests/basic.cpp.s"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/my_image_lib && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/my_image_lib/tests/basic.cpp -o CMakeFiles/Tester.exe.dir/tests/basic.cpp.s

my_image_lib/CMakeFiles/Tester.exe.dir/tests/main.cpp.o: my_image_lib/CMakeFiles/Tester.exe.dir/flags.make
my_image_lib/CMakeFiles/Tester.exe.dir/tests/main.cpp.o: ../my_image_lib/tests/main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object my_image_lib/CMakeFiles/Tester.exe.dir/tests/main.cpp.o"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/my_image_lib && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/Tester.exe.dir/tests/main.cpp.o -c /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/my_image_lib/tests/main.cpp

my_image_lib/CMakeFiles/Tester.exe.dir/tests/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Tester.exe.dir/tests/main.cpp.i"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/my_image_lib && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/my_image_lib/tests/main.cpp > CMakeFiles/Tester.exe.dir/tests/main.cpp.i

my_image_lib/CMakeFiles/Tester.exe.dir/tests/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Tester.exe.dir/tests/main.cpp.s"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/my_image_lib && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/my_image_lib/tests/main.cpp -o CMakeFiles/Tester.exe.dir/tests/main.cpp.s

# Object files for target Tester.exe
Tester_exe_OBJECTS = \
"CMakeFiles/Tester.exe.dir/tests/basic.cpp.o" \
"CMakeFiles/Tester.exe.dir/tests/main.cpp.o"

# External object files for target Tester.exe
Tester_exe_EXTERNAL_OBJECTS =

my_image_lib/Tester.exe: my_image_lib/CMakeFiles/Tester.exe.dir/tests/basic.cpp.o
my_image_lib/Tester.exe: my_image_lib/CMakeFiles/Tester.exe.dir/tests/main.cpp.o
my_image_lib/Tester.exe: my_image_lib/CMakeFiles/Tester.exe.dir/build.make
my_image_lib/Tester.exe: my_image_lib/CMakeFiles/Tester.exe.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX executable Tester.exe"
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/my_image_lib && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/Tester.exe.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
my_image_lib/CMakeFiles/Tester.exe.dir/build: my_image_lib/Tester.exe

.PHONY : my_image_lib/CMakeFiles/Tester.exe.dir/build

my_image_lib/CMakeFiles/Tester.exe.dir/clean:
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/my_image_lib && $(CMAKE_COMMAND) -P CMakeFiles/Tester.exe.dir/cmake_clean.cmake
.PHONY : my_image_lib/CMakeFiles/Tester.exe.dir/clean

my_image_lib/CMakeFiles/Tester.exe.dir/depend:
	cd /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/my_image_lib /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/my_image_lib /home/pierre/checkouts/cpp_course/slides2.0/addon/mdsd/image_tool/build/my_image_lib/CMakeFiles/Tester.exe.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : my_image_lib/CMakeFiles/Tester.exe.dir/depend

