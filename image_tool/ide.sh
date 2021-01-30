# rm -rf build
mkdir -p build
cd build
mycmake -DCMAKE_BUILD_TYPE=Debug -G "CodeBlocks - Unix Makefiles" .. || exit 1

codeblocks image_tool.cbp
echo "done."
