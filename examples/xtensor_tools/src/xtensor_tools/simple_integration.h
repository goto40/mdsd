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
void softmax_norm_vxvy(T& motion, size_t blurn, float pow_value=2.0f, float eps=0.00001f) {
    using VType = typename std::remove_reference_t<T>::value_type;
    auto [h, w, ivyn, ivxn] = motion.shape();
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

template<class T>
void blur_vxvy(T& motion, size_t blurn) {
    auto [h, w, ivyn, ivxn] = motion.shape();
    for (size_t y=0;y<h;y++) {
        for (size_t x=0;x<w;x++) {
            blur_inplace(xt::view(motion, y, x, xt::all(), xt::all()), blurn);
        }
    }
}

/** Note: mt is initialized with 0 in case its shape is not matching v1
 */
template<class T, class U>
void modulate_motion(T& v1, U& mt, float c, float f=1.0f, float p=2.0f) {
    auto [h, w, ivyn, ivxn] = v1.shape();
    if (v1.shape() != mt.shape()) {
        mt = xt::zeros<typename U::value_type>({h, w, ivyn, ivxn});
    }
    v1 *= c + f*pow(mt,p);
}

template<class T>
void predict_motion(T &motion) {
    using VType = typename std::remove_reference_t<T>::value_type;
    auto [full_h, full_w, ivyn, ivxn] = motion.shape();
    for (size_t ivy=0; ivy<ivyn; ivy++) {
        ssize_t sivy = static_cast<ssize_t>(ivy);
        ssize_t shift_y = sivy - static_cast<ssize_t>(ivyn) / 2;
        size_t h = full_h - static_cast<size_t>(std::abs(shift_y));
        size_t ys0 = static_cast<size_t>(-shift_y); // may be ununsed
        size_t yd0 = 0;
        if (shift_y>=0) { ys0 = 0; yd0 = static_cast<size_t>(shift_y); }

        for (size_t ivx=0; ivx<ivxn; ivx++) {
            ssize_t sivx = static_cast<ssize_t>(ivx);
            ssize_t shift_x = sivx - static_cast<ssize_t>(ivxn) / 2;
            size_t w = full_w - static_cast<size_t>(std::abs(shift_x));
            size_t xs0 = static_cast<size_t>(-shift_x); // may be ununsed
            size_t xd0 = 0;
            if (shift_x>=0) { xs0 = 0; xd0 = static_cast<size_t>(shift_x); }

            xt::xarray<VType> tmp = xt::zeros<VType>({full_h, full_w});
            xt::view(tmp, xt::range(yd0, yd0+h), xt::range(xd0,xd0+w)) = 
                xt::view(motion, xt::range(ys0, ys0+h), xt::range(xs0,xs0+w), ivy, ivx);
            xt::view(motion, xt::all(), xt::all(), ivy, ivx) = tmp;
        }
    }
}

} // end namespace
#endif