#ifndef XTENSOR_TOOLS_TOOLS_H
#define XTENSOR_TOOLS_TOOLS_H

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

}

#endif
