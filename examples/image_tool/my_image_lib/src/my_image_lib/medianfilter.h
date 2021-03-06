#ifndef IM2_MEDIAN_H
#define IM2_MEDIAN_H

#include "Image.h"
#include "histogram.h"

namespace my_image_lib {

template<class IM>
ImageImpl<typename IM::type> medianfilter(const IM& im, int n) {
    using T =typename IM::type;
    int w = im.getWidth()-n+1;
    int h = im.getHeight()-n+1;
    ImageImpl<typename IM::type> res{ im.getWidth(), im.getHeight() };

    std::vector<T> values(n*n);
    for (int y=0;y<h;y++) {
        for (int x=0;x<w;x++) {
            ImageSelectionImpl<const IM> sel{im,x,y,n,n};
            values.clear();
            for (int yy=0;yy<n;yy++) {
                //const float* line=sel.getline(yy); 
                for (int xx=0;xx<n;xx++) {
                    //values.push_back(line[xx]);
                    values.push_back(sel.get(xx,yy));
                }
            }
            size_t p = (n*n)/2;
            std::nth_element(values.begin(),values.begin()+p,values.end());
            //std::sort(values.begin(),values.end());
            res.set(x+n/2, y+n/2, values[p]);
        }
    }

    return res;
}

template<class IM>
ImageImpl<typename IM::type> medianfilter_par(const IM& im, int n, size_t num_threads=4) {
    using T =typename IM::type;
    int w = im.getWidth()-n+1;
    int h = im.getHeight()-n+1;
    ImageImpl<typename IM::type> res{ im.getWidth(), im.getHeight() };
    std::vector<std::future<void>> futures;    

    //std::cout << "num threads="<< num_threads << "\n";
    auto mode = std::launch::deferred;
    for (size_t t=0;t<num_threads;t++) {
        int _y0=t*(h/num_threads);
        int _y1=(t+1)*(h/num_threads);
        auto f=[&](auto y0, auto y1){
            std::vector<T> values(n*n);
            for (int y=y0;y<y1;y++) {
                for (int x=0;x<w;x++) {
                    if (x==0) {
                        ImageSelectionImpl<const IM> sel{im,x,y,n,n};
                        values.clear();
                        for (int yy=0;yy<n;yy++) {
                            for (int xx=0;xx<n;xx++) {
                                values.push_back(sel.get(xx,yy));
                            }
                        }
                        std::sort(values.begin(),values.end());
                    }
                    else {
                        auto sel_rm = im.sel(x-1,y,1,n);
                        auto sel_add = im.sel(x+n-1,y,1,n);
                        for (int yy=0;yy<n;yy++) {
                            values.erase(std::find(values.begin(), values.end(), sel_rm.get(0,yy)));
                        }
                        auto first_new = values.end();
                        for (int yy=0;yy<n;yy++) {
                            values.push_back(sel_add.get(0,yy));
                        }
                        std::sort(first_new, values.end());
                        std::inplace_merge(values.begin(),first_new,values.end());
                    }
                    size_t p = (n*n)/2;
                    res.set(x+n/2, y+n/2, values[p]);
                }
            }
        };
        futures.push_back(std::async(mode, f,_y0,_y1));
        mode = std::launch::async;
    }
    for (auto &t: futures) {
        t.wait();
    }

    return res;
}

template<class IM>
ImageImpl<typename std::remove_const_t<typename IM::type>> medianfilter_approx_par(const IM& im, int n, size_t histosize, size_t num_threads=4) {
    using T = std::remove_const_t<typename IM::type>;
    int w = im.getWidth()-n+1;
    int h = im.getHeight()-n+1;
    ImageImpl<T> res{ im.getWidth(), im.getHeight() };
    std::vector<std::future<void>> futures;

    //std::cout << "num threads="<< num_threads << "\n";
    auto mode = std::launch::deferred;
    for (size_t t=0;t<num_threads;t++) {
        int _y0=t*(h/num_threads);
        int _y1=(t+1)*(h/num_threads);
        auto f=[&](auto y0, auto y1){
            my_image_lib::Histogram<T, uint16_t> histogram(im, histosize, false);
            for (int y=y0;y<y1;y++) {
                for (int x=0;x<w;x++) {
                    if (x==0) {
                        auto sel = im.sel(x,y,n,n);
                        histogram.fill(sel);
                    }
                    else {
                        auto sel_rm = im.sel(x-1,y,1,n);
                        for (auto v: sel_rm) histogram.dec(v);
                        auto sel_add = im.sel(x+n-1,y,1,n);
                        for (auto v: sel_add) histogram.inc(v);
                    }
                    auto median = histogram.get_approx_median();
                    res.set(x+n/2, y+n/2, median);
                }
            }
        };
        futures.push_back(std::async(mode, f,_y0,_y1));
        mode = std::launch::async;
    }
    for (auto &t: futures) {
        t.wait();
    }

    return res;
}

template<class IM>
ImageImpl<typename std::remove_const_t<typename IM::type>> medianfilter_optimized_approx_par(const IM& im, int n, size_t histosize, size_t num_threads=4) {
    using T = std::remove_const_t<typename IM::type>;
    int w = im.getWidth()-n+1;
    int h = im.getHeight()-n+1;
    ImageImpl<T> res{ im.getWidth(), im.getHeight() };
    std::vector<std::future<void>> futures;

    std::cout << "num threads="<< num_threads << "\n";
    auto mode = std::launch::deferred;
    for (size_t t=0;t<num_threads;t++) {
        int _y0=t*(h/num_threads);
        int _y1=(t+1)*(h/num_threads);
        auto f=[&](auto y0, auto y1){
            my_image_lib::HistogramForQuantile<T, uint16_t> histogram(im, histosize, false);
            for (int y=y0;y<y1;y++) {
                for (int x=0;x<w;x++) {
                    if (x==0) {
                        auto sel = im.sel(x,y,n,n);
                        histogram.fill(sel);
                    }
                    else {
                        auto sel_rm = im.sel(x-1,y,1,n);
                        for (auto v: sel_rm) histogram.dec(v);
                        auto sel_add = im.sel(x+n-1,y,1,n);
                        for (auto v: sel_add) histogram.inc(v);
                    }
                    auto median = histogram.get_approx_quantile();
                    res.set(x+n/2, y+n/2, median);
                }
            }
        };
        futures.push_back(std::async(mode, f,_y0,_y1));
        mode = std::launch::async;
    }
    for (auto &t: futures) {
        t.wait();
    }

    return res;
}

}

#endif
