#!/bin/bash

{
cd item_lang
./run_tests.sh || exit 1
cd -
}

{
cd algo_lang
./run_tests.sh || exit 1
cd -
}

{
cd mdsd_support_library_cpp
./run_tests.sh || exit 1
cd -
}

{
cd mdsd_support_library_python
./run_tests.sh || exit 1
cd -
}

{
cd project_tool
./run_tests.sh || exit 1
cd -
}

{
cd cpp_python_demo
./run_tests.sh || exit 1
cd -
}

{
cd motion_model_m4
./run_tests.sh || exit 1
cd -
}
