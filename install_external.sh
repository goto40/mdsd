#!/bin/bash
mkdir -p external
cd external
REPOSRC=$1
LOCALREPO=$2
[ -d $LOCALREPO ] || git clone $REPOSRC $LOCALREPO || exit 1
(cd $LOCALREPO; git pull $REPOSRC) || exit 1
cd $2
mkdir -p build
cd build
mycmake .. || exit 1
make install || exit 1

