pip install -e .
coverage run --source swig_tool -m py.test tests || exit 1
coverage report --fail-under 90 # || exit 1
echo "OK"
