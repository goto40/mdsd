pip install -e ../item_lang
pip install -e .
coverage run --source dissector_lang -m py.test --junit-xml=test_results.xml tests || exit 1
coverage report --fail-under 80 || exit 1
coverage xml || exit 1
echo "OK"
