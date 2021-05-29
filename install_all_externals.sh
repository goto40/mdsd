#!/bin/bash
./install_external.sh https://github.com/xtensor-stack/xtl.git xtl || exit 1
./install_external.sh https://github.com/xtensor-stack/xtensor.git xtensor || exit 1

./install_external.sh https://github.com/xtensor-stack/xsimd.git xsimd
