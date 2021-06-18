#ifndef XTENSOR_TOOLS_SIMPLE_INTEGRATION_H
#define XTENSOR_TOOLS_SIMPLE_INTEGRATION_H

#include <xtensor/xview.hpp>
#include <xtensor_tools/vision.h>
#include <stdexcept>

namespace xtensor_tools
{

template <class T>
void integrate_vxvy(const T &input, T& output, size_t n=7) {
    auto [h,w,ivyn, ivxn] = input.shape();
    if (input.shape() != output.shape()) {
        output = xt::zeros<typename T::value_type>({h, w, ivyn, ivxn});
    }
    for (size_t ivy=0; ivy<ivyn; ivy++) {
        for (size_t ivx=0; ivx<ivxn; ivx++) {
            xtensor_tools::blur(
                xt::view(input,xt::all(), xt::all(), ivy, ivy),
                xt::view(output,xt::all(), xt::all(), ivy, ivy),
                n
            );
        }
    }
}

template<class T>
void softmax_norm_vxvy(T& motion, size_t blurn, float pow_value=1.0f, float eps=0.0001f) {
    using VType = typename std::remove_reference_t<T>::value_type;
    auto [h,w,ivyn, ivxn] = motion.shape();
    xt::xarray<VType> norm = xt::zeros<VType>({h, w});
    for (size_t y=0; y<h; y++) {
        for (size_t x=0; x<w; x++) {
            auto data = xt::view(motion, y, x, xt::all(), xt::all());
            data = pow(data, pow_value);
            norm(y, x) = 1; //xt::sum(data)[0];
        }
    }
    xtensor_tools::blur_inplace(norm, blurn);
    for (size_t y=0; y<h; y++) {
        for (size_t x=0; x<w; x++) {
            auto data = xt::view(motion, y, x, xt::all(), xt::all());
            data /= norm(y, x) + eps;
        }
    }
}

} // end namespace
#endif