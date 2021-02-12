#!/bin/bash

{
cd framework/item_lang
./run_tests.sh || exit 1
cd -
}

{
cd framework/item_codegen_cpp
./run_tests.sh || exit 1
cd -
}

{
cd framework/item_codegen_python
./run_tests.sh || exit 1
cd -
}

{
cd framework/algo_lang
./run_tests.sh || exit 1
cd -
}

{
cd framework/algo_codegen_cpp
./run_tests.sh || exit 1
cd -
}

{
cd framework/algo_codegen_python
./run_tests.sh || exit 1
cd -
}

{
cd framework/mdsd_support_library_cpp
./run_tests.sh || exit 1
cd -
}

{
cd framework/mdsd_support_library_python
./run_tests.sh || exit 1
cd -
}

{
cd framework/project_tool
./run_tests.sh || exit 1
cd -
}

{
cd examples/cpp_python_demo
./run_tests.sh || exit 1
cd -
}

#{
#cd framework/motion_model_m4
#./run_tests.sh || exit 1
#cd -
#}

