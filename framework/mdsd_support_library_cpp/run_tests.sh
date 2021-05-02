#!/bin/bash

rm -rf src-gen
rm -rf build
mkdir -p build
cd build

if ! command -v mycmake &> /dev/null
then
	cmake -DCMAKE_BUILD_TYPE=Debug -DCODE_COVERAGE=ON ..&& make || exit 1
else
	mycmake -DCMAKE_BUILD_TYPE=Debug -DCODE_COVERAGE=ON ..&& make || exit 1
fi

cd -

./build/Tester.exe -r console -r junit -o test_results.xml || exit 1

bash eval_coverage.sh
