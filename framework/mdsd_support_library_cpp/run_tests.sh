#!/bin/bash

rm -rf src-gen
rm -rf build
mkdir -p build
cd build
mycmake ..&& make && ./Tester.exe || exit 1
cd -

