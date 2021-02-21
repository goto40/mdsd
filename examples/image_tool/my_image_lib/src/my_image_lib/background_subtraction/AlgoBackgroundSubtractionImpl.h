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
        my_image_lib::Tictoc tictoc{"median2D"};
        my_image_lib::median2D( input, params.x, params.y, output.threshold, 4 );
        for (auto &pixel: output.threshold.pixel) {
            pixel = pixel + params.threshold;
        }
        output.result.w = output.threshold.w;
        output.result.h = output.threshold.h;
        output._GET_WRAPPER().adjust_array_sizes_and_variants();
        for (size_t idx=0;idx<output.result.pixel.size(); idx++) {
            if (input.pixel[idx]<output.threshold.pixel[idx]) {
                output.result.pixel[idx]=0.0;
            }
            else {
                output.result.pixel[idx]=1.0;
            }
        }
    }
};

}