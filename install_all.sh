#!/bin/bash
pip install -e framework/codegen_test_support || exit 1
pip install -e framework/item_lang[dev] || exit 1
pip install -e framework/item_codegen_cpp[dev] || exit 1
pip install -e framework/item_codegen_python[dev] || exit 1
pip install -e framework/algo_lang[dev] || exit 1
pip install -e framework/algo_codegen_cpp[dev] || exit 1
pip install -e framework/algo_codegen_python[dev] || exit 1
pip install -e framework/mdsd_support_library_python || exit 1
pip install -e framework/project_tool || exit 1

