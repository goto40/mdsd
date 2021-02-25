pip install -e .
coverage run --source project_tool -m py.test --junit-xml=test_results.xml tests || exit 1
coverage report --fail-under 40 || exit 1
coverage xml || exit 1
echo "OK"
