#ifndef XTENSOR_TOOLS_TOOLS_H
#define XTENSOR_TOOLS_TOOLS_H

#include <xtensor/xview.hpp>
#include <xtensor/xadapt.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xbuilder.hpp> // zeros
#include <type_traits>
#include <stdexcept>
#include <sstream>
#include <algorithm>

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

    template <class T>
    inline xt::xarray<unsigned char> gray2rgb(const T &gray)
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

    template <class T>
    inline xt::xarray<unsigned char> hsv2rgb(const T &hsv)
    {
        auto shape = hsv.shape();
        if (shape.size() != 3 || shape[2] != 3)
        {
            throw std::runtime_error("no hsv image");
        }
        float mi = xt::amin(hsv)[0];
        if (mi < 0.0)
        {
            throw std::runtime_error("no hsv image with values >= 1.0");
        }
        float ma = xt::amax(hsv)[0];
        if (ma > 1.0)
        {
            throw std::runtime_error("no hsv image with values <= 1.0");
        }

        T rgb = xt::zeros<typename T::value_type>(shape);
        auto r = xt::view(rgb, xt::all(), xt::all(), 0);
        auto g = xt::view(rgb, xt::all(), xt::all(), 1);
        auto b = xt::view(rgb, xt::all(), xt::all(), 2);

        //https://de.wikipedia.org/wiki/HSV-Farbraum
        auto h = xt::view(hsv, xt::all(), xt::all(), 0);
        auto s = xt::view(hsv, xt::all(), xt::all(), 1);
        auto v = xt::view(hsv, xt::all(), xt::all(), 2);
        auto hi = xt::floor(h * 360.0 / 60.0);
        auto f = (h * 360.0 / 60.0) - hi;
        auto p = v * (1.0 - s);
        auto q = v * (1.0 - s * f);
        auto t = v * (1.0 - s * (1.0 - f));

        for (size_t y = 0; y < shape[0]; y++)
        {
            for (size_t x = 0; x < shape[1]; x++)
            {
                switch (static_cast<int>(hi(y, x)))
                {
                case 0:
                case 6:
                    r(y, x) = v(y, x);
                    g(y, x) = t(y, x);
                    b(y, x) = p(y, x);
                    break;
                case 1:
                    r(y, x) = q(y, x);
                    g(y, x) = v(y, x);
                    b(y, x) = p(y, x);
                    break;
                case 2:
                    r(y, x) = p(y, x);
                    g(y, x) = v(y, x);
                    b(y, x) = t(y, x);
                    break;
                case 3:
                    r(y, x) = p(y, x);
                    g(y, x) = q(y, x);
                    b(y, x) = v(y, x);
                    break;
                case 4:
                    r(y, x) = t(y, x);
                    g(y, x) = p(y, x);
                    b(y, x) = v(y, x);
                    break;
                case 5:
                    r(y, x) = v(y, x);
                    g(y, x) = p(y, x);
                    b(y, x) = q(y, x);
                    break;
                default:
                    throw std::runtime_error("unexpected hi");
                };
            }
        }
        return xt::cast<unsigned char>(rgb * 255.0);
    }

    template <class T, class U>
    xt::xarray<float> motion2hsv(const U &im2, const T &motion_hw_vyvx)
    {
        auto shape = motion_hw_vyvx.shape();
        if (shape.size() != 4)
        {
            throw std::runtime_error("no motion block");
        }
        size_t h = shape[0];
        size_t w = shape[1];
        size_t ivyn = shape[2];
        size_t ivxn = shape[3];
        auto hsv = xt::zeros<float>({h, w, static_cast<size_t>(3)});
        float ivy2 = (ivyn / 2); // integer round!
        float ivx2 = (ivxn / 2);
        float global_maxv = std::max(0.0001f, static_cast<float>(xt::amax(motion_hw_vyvx)[0]));
        float max_speed = sqrt(pow(ivx2, 2.0f) + pow(ivy2, 2.0f));

        xt::xarray<float> vx = xt::zeros<float>({h, w});
        xt::xarray<float> vy = xt::zeros<float>({h, w});
        xt::xarray<float> maxv = xt::zeros<float>({h, w});
        for (size_t ivy = 0; ivy < ivyn; ivy++)
        {
            for (size_t ivx = 0; ivx < ivxn; ivx++)
            {
                float cvx = (static_cast<float>(ivx) - ivx2);
                float cvy = (static_cast<float>(ivy) - ivy2);
                auto v = xt::view(motion_hw_vyvx, xt::all(), xt::all(), ivy, ivx);
                vx = cvx * xt::cast<float>(maxv < v) + vx * xt::cast<float>(maxv >= v);
                vy = cvy * xt::cast<float>(maxv < v) + vy * xt::cast<float>(maxv >= v);
                maxv = xt::maximum(maxv, v);
            }
        }
        auto a = xt::eval(xt::fmod((xt::atan2(vy, vx) + 2.0 * M_PI) / (2.0 * M_PI), 1.0));
        auto speed = xt::eval(xt::sqrt(xt::pow(vx, 2) + xt::pow(vy, 2)));

        if (im2.shape().size() != 2)
        {
            throw std::runtime_error("no gray image");
        }
        float mi = xt::amin(im2)[0];
        float ma = xt::amax(im2)[0];
        float norm = ma - mi;
        if (norm < 1e-10)
        {
            norm = 1;
        }

        xt::view(hsv, xt::all(), xt::all(), 0) = a;
        xt::view(hsv, xt::all(), xt::all(), 1) = pow(speed / max_speed, 0.25);
        xt::view(hsv, xt::all(), xt::all(), 2) = (0.5 + (im2 - mi) / norm * 0.5) * (maxv / pow(global_maxv + 0.00001, 0.5));

        return hsv;
    }
}

#endif
