#!/bin/bash
pip install -e framework/codegen_test_support || exit 1
pip install -e framework/item_lang[dev] || exit 1
pip install -e framework/item_codegen_cpp || exit 1
pip install -e framework/item_codegen_python || exit 1
pip install -e framework/algo_lang || exit 1
pip install -e framework/mdsd_support_library_python || exit 1
pip install -e framework/project_tool || exit 1

