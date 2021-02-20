#!/bin/bash

rm -rf src-gen
textx generate ../mdsd_support_library_common/model/*.item --overwrite --target python  --output-path src-gen || exit 1
export PYTHONPATH=$(pwd)/src-gen
ls $PYTHONPATH
coverage run --omit tests --omit venv --source mdsd -m py.test --junit-xml=test_results.xml tests || exit 1
coverage report --fail-under 70 # || exit 1
coverage xml || exit 1

# Run this to generate html report
# coverage html --directory=coverage
#flake8 || exit 1
echo "OK" 
