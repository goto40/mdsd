 #include "my_image_lib/background_subtraction/AlgoBackgroundSubtraction.h"

namespace my_image_lib::background_subtraction {

class AlgoBackgroundSubtractionImpl : public my_image_lib::background_subtraction::AlgoBackgroundSubtraction {
    inline static struct __Init {
        __Init() {
            std::cout << "**INIT* *\n";
            my_image_lib::background_subtraction::AlgoBackgroundSubtraction::set_factory(
                []()
                { return std::make_shared<my_image_lib::background_subtraction::AlgoBackgroundSubtractionImpl>(); }
            ); 
        }
    } __init;
public:
    virtual void compute(
        const my_image_lib::GrayImage& input, 
        my_image_lib::background_subtraction::BackgroundSubtractionResults& output
    ) {

    }
};

}