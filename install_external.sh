#!/bin/bash
mkdir -p external
cd external
git clone $1 $2 || exit 1
cd $2
mkdir -p build
cd build
mycmake .. || exit 1
make install || exit 1

