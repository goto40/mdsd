#include "my_image_lib/background_subtraction/AlgoBackgroundSubtraction.h"
#include "my_image_lib/tools.h"
#include "my_image_lib/Image.h"
#include "my_image_lib/medianfilter.h"

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
        if (params.type==my_image_lib::background_subtraction::MedianType::HISTOGRAMBASED_MEDIAN_APPROX) {
            my_image_lib::Tictoc tictoc{"median approx"};
            output.threshold.w = input.w;
            output.threshold.h = input.h;
            output.threshold._GET_WRAPPER().adjust_array_sizes_and_variants();
            const my_image_lib::PtrImageImpl<const float> im{
                input.pixel.data(),
                static_cast<int>(input.w),
                static_cast<int>(input.h)
            };
            my_image_lib::ImageImpl res = my_image_lib::medianfilter_approx_par(
                im,
                params.n,
                params.histosize
            );
            for (size_t idx=0;idx<output.threshold.pixel.size(); idx++) {
                output.threshold.pixel[idx] = res.begin()[idx];
            }
        }
        else {
            my_image_lib::Tictoc tictoc{"normal median"};
            my_image_lib::median2D( input, params.n, params.n, output.threshold, std::thread::hardware_concurrency() );
        }
        for (auto &pixel: output.threshold.pixel) {
            pixel += params.threshold;
        }
        output.result.w = output.threshold.w;
        output.result.h = output.threshold.h;
        output.result._GET_WRAPPER().adjust_array_sizes_and_variants();
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