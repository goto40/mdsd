#ifndef MY_IMAGE_LIB_TOOLS_H
#define MY_IMAGE_LIB_TOOLS_H

#include "my_image_lib/GrayImage.h"
#include "mdsd/item_support.h"

#include <algorithm>
#include <future>

namespace my_image_lib {

    inline float min(const my_image_lib::GrayImage &im) {
        mdsd::check_array_sizes_and_variants(im);
        return *std::min_element(im.pixel.begin(), im.pixel.end());
    }

    inline float max(const my_image_lib::GrayImage &im) {
        mdsd::check_array_sizes_and_variants(im);
        return *std::max_element(im.pixel.begin(), im.pixel.end());
    }

    namespace details {

        inline void __median1D(const float* data_in, float* data_res, size_t data_size, size_t data_stride, size_t n) {
            std::vector<float> tmp(n);
            size_t n2l = n/2;
            size_t n2r = n-n2l;
            for(size_t x=0;x<data_size;x++) {
                size_t x0 = (x>=n2l)?x-n2l:0;
                size_t x1 = (x+n2r<=data_size)?x+n2r:data_size;
                for(size_t pos=0;pos<x1-x0;pos++) {
                    tmp[pos] = data_in[(x0+pos)*data_stride];
                }
                size_t p = (x1-x0)/2;
                std::nth_element(tmp.begin(), tmp.begin()+p, tmp.begin()+(x1-x0));
                data_res[x*data_stride] = tmp[p];
            }
        }

    }

    /** this compute the median filter in x or y (separately).
     * Even the median filter cannot be separated, this gives
     * usabe estimations of the background and is much faster */
    inline void median1D(const my_image_lib::GrayImage &im, size_t n, bool xdir, my_image_lib::GrayImage &res, size_t N=1) {
        mdsd::check_array_sizes_and_variants(im);
        res.w = im.w;
        res.h = im.h;
        mdsd::adjust_array_sizes_and_variants(res);

        if (xdir) {
            // 1D:x
            std::vector<std::future<void>> threads;
            for (size_t T=0;T<N;++T) {
                threads.push_back( std::async(std::launch::async, [&, T=T](){
                    for(size_t y=T;y<im.h;y+=N) {
                        size_t pos_line = y*im.w;
                        details::__median1D(
                            &(im.pixel[pos_line]),
                            &(res.pixel[pos_line]),
                            im.w,
                            1,
                            n
                        );
                    }
                }));
            }
            for (auto & t : threads) {
                t.get(); // wait for result
            }
        }
        else {
            // 1D:y
            std::vector<std::future<void>> threads;
            for (size_t T=0;T<N;++T) {
                threads.push_back( std::async(std::launch::async, [&, T=T](){
                    std::vector<float> tmp(n);
                    for(size_t x=T;x<im.w;x+=N) {
                        size_t pos_col = x;
                        details::__median1D(
                            &(im.pixel[pos_col]),
                            &(res.pixel[pos_col]),
                            im.h,
                            im.w,
                            n
                        );
                    }
                }));
            }
            for (auto & t : threads) {
                t.get(); // wait for result
            }
        }
    }

    /** this compute the median filter in x/y */
    inline void median2D(const my_image_lib::GrayImage &im, size_t nx, size_t ny, my_image_lib::GrayImage &res, size_t N=1) {
        mdsd::check_array_sizes_and_variants(im);
        res.w = im.w;
        res.h = im.h;
        mdsd::adjust_array_sizes_and_variants(res);
        size_t nx2l = nx/2;
        size_t ny2l = ny/2;
        size_t nx2r = nx-nx2l;
        size_t ny2r = ny-ny2l;

        std::vector<std::future<void>> threads;
        for (size_t T=0;T<N;++T) {
            threads.push_back( std::async(std::launch::async, [&, T=T](){
                std::vector<float> tmp(nx*ny);
                for(size_t y=T;y<im.h;y+=N) {
                    size_t y0 = (y>=ny2l)?y-ny2l:0;
                    size_t y1 = (y+ny2r<=im.h)?y+ny2r:im.h;

                    for(size_t x=0;x<im.w;x++) {
                        size_t x0 = (x>=nx2l)?x-nx2l:0;
                        size_t x1 = (x+nx2r<=im.w)?x+nx2r:im.w;

                        size_t pos=0;
                        for(size_t posx=0;posx<x1-x0;posx++) {
                            for(size_t posy=0;posy<y1-y0;posy++) {
                                tmp[pos++] = im.pixel[x0+posx+(y0+posy)*im.w];
                            }
                        }
                        size_t pos2 = pos/2;
                        std::nth_element(tmp.begin(), tmp.begin()+pos2, tmp.begin()+pos);
                        res.pixel[y*im.w+x] = tmp[pos2];
                    }
                }
            }));
        }
        for (auto & t : threads) {
            t.get(); // wait for result
        }
    }


}

#endif
