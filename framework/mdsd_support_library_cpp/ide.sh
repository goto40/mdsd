#!/bin/bash

rm -rf src-gen
rm -rf build
mkdir -p build
cd build

mycmake .. -G "CodeBlocks - Unix Makefiles" || exit 1
codeblocks mdsd_support_library.cbp

#mycmake .. -G "CodeLite - Unix Makefiles" || exit 1
#codelite mdsd_support_library.workspace 

cd -

