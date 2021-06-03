#ifndef XTENSOR_TOOLS_VISION_H
#define XTENSOR_TOOLS_VISION_H

#include <xtensor/xview.hpp>
#include <xtensor/xadapt.hpp>
#include <type_traits>
#include <stdexcept>
#include <sstream>

namespace xtensor_tools
{

    inline xt::xarray<float> rgb2gray(const xt::xarray<unsigned char> &rgb)
    {
        if (rgb.shape().size() == 3 || rgb.shape()[2] == 3) // rgb
        {
            auto im = xt::sum(xt::cast<float>(rgb), 2) / 3.0 / 255.0;
            return xt::eval(im);
        }
        else if (rgb.shape().size() == 3 || rgb.shape()[2] == 1) // gray
        {
            auto im = xt::sum(xt::cast<float>(rgb), 2) / 3.0 / 255.0;
            return xt::eval(im);
        }
        else
        {
            std::ostringstream o;
            o << "no rgb/gray image: shape = " << xt::adapt(rgb.shape());
            throw std::runtime_error(o.str());
        }
    }

    inline xt::xarray<unsigned char> gray2rgb(const xt::xarray<float> &gray)
    {
        if (gray.shape().size() != 2)
        {
            throw std::runtime_error("no gray image");
        }
        float mi = xt::amin(gray)[0];
        float ma = xt::amax(gray)[0];
        float norm = ma - mi;
        if (norm < 1e-10)
        {
            norm = 1;
        }
        auto im256 = xt::cast<unsigned char>((gray - mi) / norm * 255.0);
        auto im = xt::stack(xt::xtuple(im256, im256, im256), 2);
        return xt::eval(im);
    }

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
        if (im.shape().size() != 2)
        {
            throw std::runtime_error("no gray image");
        }

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
            conv1d(xt::view(im, y, xt::all()), mask, a);
            xt::view(im, y, xt::all()).assign(a);
        }
    }

    template <class T, class U>
    void conv2d_1d_y(T &im, U &mask)
    {
        if (im.shape().size() != 2)
        {
            throw std::runtime_error("no gray image");
        }

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
            conv1d(xt::view(im, xt::all(), x), mask, a);
            xt::view(im, xt::all(), x).assign(a);
        }
    }

    template <class T>
    xt::xarray<T> hanning1d(size_t n)
    {
        return -xt::cos(2.0 * (xt::arange<T>(n) + 1.0) * M_PI / (static_cast<T>(n) + 1.0)) + 1.0;
    }

    template <class T>
    void center_surround(const T &im, size_t sourround_size, T &res)
    {
        auto mask = hanning1d<typename T::value_type>(sourround_size);
        res = im;
        conv2d_1d_x(res, mask);
        conv2d_1d_y(res, mask);
        T norm = xt::sum(mask);
        res = im - res / (norm * norm);
    }
}

#endif
