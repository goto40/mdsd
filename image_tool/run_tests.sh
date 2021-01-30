#!/bin/bash

sh build.sh || exit 1
./build/my_image_lib/Tester.exe || exit 1

