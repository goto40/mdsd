# rm -rf build
mkdir -p build
cd build
mycmake -DCMAKE_BUILD_TYPE=Release .. && make || exit 1
cd ..


rm -rf build/swig_proj
mkdir -p build/swig_proj
projecttool python-i-file --require-pattern="ACTIVATE FOR SWIG" my_image_lib_swig build/swig_proj my_image_lib/src my_image_lib/src-gen ../../framework/mdsd_support_library_cpp/src/
swig -c++ -python -I../../framework/mdsd_support_library_cpp/src -Imy_image_lib/src -Imy_image_lib/src-gen -o build/swig_proj/wrapper.cpp build/swig_proj/my_image_lib_swig.i || exit 1
pip install -e build/swig_proj || exit 1


echo "done."
