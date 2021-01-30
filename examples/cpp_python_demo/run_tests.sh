#!/bin/bash

PACKAGE_NAME=firsttest
SWIG_PACKAGE_NAME=swig_${PACKAGE_NAME}

./clean.sh

textx generate ../../framework/mdsd_support_library_common/model/*.item --overwrite --target cpp --output-path src-gen/cpp || exit 1
textx generate ../../framework/mdsd_support_library_common/model/*.item --overwrite --target python --output-path src-gen/python || exit 1
textx generate ../../framework/mdsd_support_library_common/model/*.algo --overwrite --target cpp --output-path src-gen/cpp || exit 1

projecttool generic-setup-file ${PACKAGE_NAME} src-gen/python
projecttool python-i-file --require-pattern="ACTIVATE FOR SWIG" ${SWIG_PACKAGE_NAME} src-gen/swig src/cpp src-gen/cpp/ ../../framework/mdsd_support_library_cpp/src/

swig -c++ -python -I../../framework/mdsd_support_library_cpp/src -Isrc/cpp -Isrc-gen/cpp -o src-gen/swig/wrapper.cpp src-gen/swig/${SWIG_PACKAGE_NAME}.i || exit 1

#python setup.py build sdist bdist_wheel || exit 1
pip install -e src-gen/swig || exit 1
pip install -e src-gen/python || exit 1

py.test tests/ || exit 1

#python demo.py
#python -i -m demo
