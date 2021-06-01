#ifndef XTENSOR_TOOLS_IMAGEPAIRCOLLECTOR_H
#define XTENSOR_TOOLS_IMAGEPAIRCOLLECTOR_H

#include <xtensor-io/ximage.hpp>
#include "xtensor_tools.h"
#include <xtensor/xio.hpp>
#include <xtensor/xadapt.hpp>
#include <string>

namespace xtensor_tools
{
    struct ImagePairCollector
    {
        xt::xarray<unsigned char> im0 = {};
        xt::xarray<unsigned char> im1 = {};

    private:
        std::string pattern;
        size_t i0, i1;
        size_t i = 0;

    public:
        ImagePairCollector(std::string pattern, size_t i0, size_t i1) : pattern(pattern), i0(i0), i1(i1) {}

        bool read_next()
        {
            bool ret = read();
            if (i == 1 && ret)
            {
                ret = read();
            }
            return ret;
        }

    private:
        bool read()
        {
            if (i0 + i < i1)
            {
                char fname[1000];
                sprintf(fname, pattern.c_str(), i0 + i);

                im0 = im1;
                im1 = xt::load_image(fname); // should not throw

                i++;
                return true;
            }
            else
            {
                return false;
            }
        }
    };
}

#endif
