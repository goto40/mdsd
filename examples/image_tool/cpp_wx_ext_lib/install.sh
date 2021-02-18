#!/bin/bash

rm -rf src-gen
rm -rf build
mkdir -p build
cd build
mycmake ..&& make && ./Tester.exe && make install || exit 1
cd -

