#ifndef XTENSOR_TOOLS_SIMPLE_CORRELATION_H
#define XTENSOR_TOOLS_SIMPLE_CORRELATION_H

#include <xtensor/xview.hpp>
#include <xtensor_tools/vision.h>
#include <stdexcept>

namespace xtensor_tools
{
    template <class T, class U>
    void simple_correlation(const T &gray1, const T &gray2, size_t patch_size, U &motion_hw_vyvx)
    {
        // prepare/check memory
        auto im_shape = gray1.shape();
        if (motion_hw_vyvx.shape().size() != 4)
        {
            throw std::runtime_error("unexpected motion block size");
        }
        if (im_shape.size() != 2)
        {
            throw std::runtime_error("unexpected image size");
        }
        size_t h = im_shape[0];
        size_t w = im_shape[1];
        size_t ivyn = motion_hw_vyvx.shape()[2];
        size_t ivxn = motion_hw_vyvx.shape()[3];
        if (motion_hw_vyvx.shape()[0] != h || motion_hw_vyvx.shape()[1] != w)
        {
            motion_hw_vyvx = xt::zeros<U::value_type>({h, w, ivyn, ivxn});
        }
        else
        {
            motion_hw_vyvx.fill(0.0f);
        }

        // compute:
        auto e1 = xt::eval(gray1 * gray1);
        auto e2 = xt::eval(gray2 * gray2);
        xtensor_tools::blur_inplace(e1, patch_size, false);
        xtensor_tools::blur_inplace(e2, patch_size, false);
        e1 = xt::sqrt(e1);
        e2 = xt::sqrt(e2);

        size_t ivyn2 = ivyn / 2;
        size_t ivxn2 = ivyn / 2;
        for (size_t ivy = 0; ivy < ivyn; ivy++)
        {
            size_t eh, yi0, yo0;
            if (ivy < ivyn2)
            {
                eh = h + ivy - ivyn2;
                yi0 = ivyn2 - ivy;
                yo0 = 0;
            }
            else
            {
                eh = h - ivy + ivyn2;
                yi0 = 0;
                yo0 = ivy - ivyn2;
            }
            for (size_t ivx = 0; ivx < ivxn; ivx++)
            {
                size_t ew, xi0, xo0;
                if (ivx < ivxn2)
                {
                    ew = w + ivx - ivxn2;
                    xi0 = ivxn2 - ivx;
                    xo0 = 0;
                }
                else
                {
                    ew = w - ivx + ivxn2;
                    xi0 = 0;
                    xo0 = ivx - ivxn2;
                }

                auto sel1 = xt::view(gray1, xt::range(yi0, yi0 + eh), xt::range(xi0, xi0 + ew));
                auto sel2 = xt::view(gray2, xt::range(yo0, yo0 + eh), xt::range(xo0, xo0 + ew));
                auto sele1 = xt::view(e1, xt::range(yi0, yi0 + eh), xt::range(xi0, xi0 + ew));
                auto sele2 = xt::view(e2, xt::range(yo0, yo0 + eh), xt::range(xo0, xo0 + ew));
                auto tmp = xt::eval(sel1 * sel2);
                xtensor_tools::blur_inplace(tmp, patch_size, false);
                auto out = xt::view(motion_hw_vyvx, xt::range(yo0, yo0 + eh), xt::range(xo0, xo0 + ew), ivy, ivx);
                out = xt::eval(xt::minimum(0.0f, tmp / (sele1 * sele2 + 0.0001)));
            }
        }
    }
}

#endif
