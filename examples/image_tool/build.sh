# rm -rf build
mkdir -p build
cd build
mycmake -DCMAKE_BUILD_TYPE=Release .. && make || exit 1

echo "done."
