#!/bin/bash

sh build.sh || exit 1
./build/my_image_lib/Tester.exe -r console -r xml -o test_results.xml || exit 1

