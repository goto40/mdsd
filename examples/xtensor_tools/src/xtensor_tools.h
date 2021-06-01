#ifndef XTENSOR_TOOLS_TOOLS_H
#define XTENSOR_TOOLS_TOOLS_H

#include "imagepair_collector.h"
#include <xtensor/xview.hpp>
#include <type_traits>

namespace xtensor_tools
{

    template <class T, class U, class V>
    void conv1d(T &&im, U &&mask, V &&a)
    {
        using ValueType = typename std::remove_reference<T>::type::value_type;
        using ValueType_2 = typename std::remove_reference<U>::type::value_type;
        using ValueType_3 = typename std::remove_reference<V>::type::value_type;
        static_assert(std::is_same<ValueType, ValueType_2>::value, "unexpected");
        static_assert(std::is_same<ValueType, ValueType_3>::value, "unexpected");

        size_t w = im.size();
        size_t n = mask.size();
        size_t n2 = n / 2;
        size_t w2 = w - n + n2;

        for (size_t x = 0; x < n2; x++)
        {
            size_t m0 = n - n2 - x;
            ValueType res = 0;
            for (size_t k = 0; k < n2; k++)
            {
                res += mask(m0 + k) * im(k);
            }
            for (size_t k = 0; k < m0; k++)
            {
                res += mask(k) * im(0);
            }
            a(x) = res;
        }

        for (size_t x = 0; x < w - n; x++)
        {
            auto v = xt::view(im, xt::range(x, x + n));
            a(x + n2) = xt::sum(v * mask)(0);
        }

        for (size_t x = w2; x < w; x++)
        {
            size_t x0 = x - n2;
            ValueType res = 0;
            for (size_t k = 0; k < w - x0; k++)
            {
                res += mask(k) * im(x0 + k);
            }
            for (size_t k = x0; k < n; k++)
            {
                res += mask(k) * im(w - 1);
            }
            a(x) = res;
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