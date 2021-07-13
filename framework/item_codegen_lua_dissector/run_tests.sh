#!/bin/bash

pip install -e .
coverage run --source item_codegen_lua_dissector -m py.test --junit-xml=test_results.xml tests || exit 1
flake8 || exit 1
coverage report --fail-under 90 || exit 1
coverage xml || exit 1
echo "OK"
