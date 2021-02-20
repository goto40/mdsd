pip install -e ../item_lang
pip install -e .
coverage run --source item_lang -m py.test tests || exit 1
coverage report --fail-under 90 # || exit 1
coverage xml || exit 1
echo "OK"
