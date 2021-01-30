#include <iostream>
#include <chrono>
#include <thread>

namespace my_image_lib {
    struct Tictoc 
    {
        std::string info = {};
        using DiffType=std::chrono::milliseconds;
        std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
        ~Tictoc() {
            DiffType res = std::chrono::duration_cast<DiffType>(std::chrono::steady_clock::now()-start);
            std::cout << info << " tictoc: " << res.count() << " ms\n";
        }
    };
}
