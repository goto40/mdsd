#!/bin/bash

rm -rf src-gen
rm -rf build
mkdir -p build
cd build

if ! command -v mycmake &> /dev/null
then
	cmake -DCMAKE_BUILD_TYPE=Debug -DCODE_COVERAGE=ON ..&& make && ./Tester.exe || exit 1
else
	mycmake -DCMAKE_BUILD_TYPE=Debug -DCODE_COVERAGE=ON ..&& make && ./Tester.exe || exit 1
fi

cd -

bash eval_coverage.sh
