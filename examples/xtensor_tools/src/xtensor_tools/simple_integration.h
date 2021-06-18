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

/*
pub fn blur_vxvy(motion: &mut MotionBlock, blurn: usize) {
    let shape = motion.motion_hw_vyvx.raw_dim();
    let mask = hanningmask1d(blurn);
    for y in 0..shape[0] {
        for x in 0..shape[1] {
            let blurred = create_corr2_1d(&motion.motion_hw_vyvx.slice(s![y, x, .., ..]), &mask);
            motion
                .motion_hw_vyvx
                .slice_mut(s![y, x, .., ..])
                .assign(&blurred);
        }
    }
}

pub fn modulate_motion(v1: &mut MotionBlock, mt: &mut MotionBlock, c: f32, f: f32, pow: f32) {
    let shape = v1.motion_hw_vyvx.raw_dim();
    if shape != mt.motion_hw_vyvx.raw_dim() {
        mt.motion_hw_vyvx = Array4::zeros(shape);
    }
    Zip::from(&mut v1.motion_hw_vyvx)
        .and(&mt.motion_hw_vyvx)
        .for_each(|v1v, mtv| {
            *v1v *= c + f * mtv.powf(pow);
        });
}

pub fn predict_motion(motion: &mut MotionBlock) {
    let shape = motion.motion_hw_vyvx.raw_dim();
    for ivy in 0..shape[2] {
        let sivy = ivy as i32;
        let shift_y = sivy - shape[2] as i32 / 2;
        let h = shape[0] - shift_y.abs() as usize;
        let (ys0, yd0) = if shift_y < 0 {
            (-shift_y as usize, 0)
        } else {
            (0, shift_y as usize)
        };

        for ivx in 0..shape[3] {
            let sivx = ivx as i32;
            let shift_x = sivx - shape[3] as i32 / 2;
            let w = shape[1] - shift_x.abs() as usize;
            let (xs0, xd0) = if shift_x < 0 {
                (-shift_x as usize, 0)
            } else {
                (0, shift_x as usize)
            };
            let tmp = motion
                .motion_hw_vyvx
                .slice(s![ys0..ys0 + h, xs0..xs0 + w, ivy, ivx])
                .to_owned(); // copy
            motion
                .motion_hw_vyvx
                .slice_mut(s![yd0..yd0 + h, xd0..xd0 + w, ivy, ivx])
                .assign(&tmp);
        }
    }
}

*/

} // end namespace
#endif