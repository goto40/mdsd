#!/bin/bash

TestDirs=(

	"framework/item_lang"
	"framework/item_codegen_cpp"
	"framework/item_codegen_python"
	
	"framework/algo_lang"
	"framework/algo_codegen_cpp"
	"framework/algo_codegen_python"
	
	"framework/mdsd_support_library_python"
	"framework/mdsd_support_library_cpp"
	
	"framework/project_tool"

	"examples/cpp_python_demo"
)
 
for d in ${TestDirs[@]}; do
	{
	echo "=================================================="
	echo "= RUNNNING TESTS IN"
	echo "= $d"
	echo "=================================================="
	cd $d
	./run_tests.sh || exit 1
	cd -
	}
done

