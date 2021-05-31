#ifndef XTENSOR_TOOLS_TOOLS_H
#define XTENSOR_TOOLS_TOOLS_H

#include <xtensor/xview.hpp>

namespace xtensor_tools
{

    template <class T, class U, class V>
    void conv1d(T &&im, U &&mask, V &&a)
    {
        size_t w = im.size();
        size_t n = mask.size();
        size_t n2 = n / 2;
        for (size_t x = 0; x < w - n; x++)
        {
            auto v = xt::view(im, xt::range(x, x + n));
            a(x + n2) = xt::sum(v * mask)(0);
        }
    }

    template <class T, class U>
    void conv2d_1d_x(T &im, U &mask)
    {
        size_t h = im.shape()[0];
        size_t w = im.shape()[1];
        size_t n = mask.size();
        size_t n2 = n / 2;
        xt::xarray<typename T::value_type> a;
        a.resize({w});
        for (size_t x = 0; x < w; x++)
        {
            a[x] = 0.0;
        }
        for (size_t y = 0; y < h; y++)
        {
            for (size_t c = 0; c < 3; c++)
            {
                conv1d(xt::view(im, y, xt::all(), c), mask, a);
                xt::view(im, y, xt::all(), c).assign(a);
            }
        }
    }

    template <class T, class U>
    void conv2d_1d_y(T &im, U &mask)
    {
        size_t h = im.shape()[0];
        size_t w = im.shape()[1];
        size_t n = mask.size();
        size_t n2 = n / 2;
        xt::xarray<typename T::value_type> a;
        a.resize({h});
        for (size_t y = 0; y < h; y++)
        {
            a[y] = 0.0;
        }
        for (size_t x = 0; x < w; x++)
        {
            for (size_t c = 0; c < 3; c++)
            {
                conv1d(xt::view(im, xt::all(), x, c), mask, a);
                xt::view(im, xt::all(), x, c).assign(a);
            }
        }
    }

}

#endif