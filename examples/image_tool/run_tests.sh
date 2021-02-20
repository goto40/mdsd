#!/bin/bash

sh build.sh || exit 1
./build/my_image_lib/Tester.exe -r console -r junit -o test_results.xml || exit 1

