#!/bin/bash

PyDirs=(

	"framework/item_lang"
	"framework/item_codegen_cpp"
	"framework/item_codegen_python"
	
	"framework/algo_lang"
	"framework/algo_codegen_cpp"
	"framework/algo_codegen_python"
	
	"framework/mdsd_support_library_python"
	
	"framework/project_tool"
)
 
for d in ${PyDirs[@]}; do
	{
	cd $d
	./run_black.sh || exit 1
	cd -
	}
done

