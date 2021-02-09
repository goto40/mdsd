#!/bin/bash

rm -rf src-gen
rm -rf build
mkdir -p build
cd build
mycmake -DCMAKE_BUILD_TYPE=Debug -DCODE_COVERAGE=ON ..&& make && ./Tester.exe || exit 1
cd -

bash eval_coverage.sh
