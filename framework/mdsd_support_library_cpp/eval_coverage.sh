echo "EVAL COVERAGE"
rm -rf coverage
mkdir -p coverage
# eval generated coverage data, excluding files in folder "tests"
gcovr -r . -e "tests/*" -e "src-gen/*" --html --html-details -o coverage/report.html
gcovr -r . -e "tests/*" -e "src-gen/*" --xml -o coverage/coverage.xml
gcovr -r . -e "tests/*" -e "src-gen/*" -s
echo xdg-open coverage/report.html 

