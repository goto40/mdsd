#ifndef IM2_HISTOGRAM_H
#define IM2_HISTOGRAM_H

#include "Image.h"
#include <cmath>
#include <iostream>
#include <iomanip>
#include <algorithm>
#include <numeric>

namespace my_image_lib {

template<class T=uint8_t, class C=size_t, size_t W=50>
struct Histogram {
    size_t histosize;
    std::vector<C> h={};
    std::vector<T> bins={};
    C operator[](size_t idx) const { return h[idx]; }

    template<class IM>
    Histogram(const IM& im, size_t _histosize, bool init=true) : histosize(_histosize) {
        static_assert(std::is_same_v<T, std::remove_const_t<typename IM::type>>);
        h.resize(histosize);
        bins.resize(histosize);
        auto mima = std::minmax_element(im.begin(), im.end());
        for(size_t i=0;i<histosize;i++) bins[i] = *mima.first + (*mima.second-*mima.first)*i/histosize;
        if (init) fill(im);
        else clear();
    }

    Histogram(size_t _histosize, T mi, T ma) : histosize(_histosize) {
        h.resize(histosize);
        bins.resize(histosize);
        for(size_t i=0;i<histosize;i++) bins[i] = mi + (ma-mi)*i/histosize;
        clear();
    }

    void clear() {
        std::fill(h.begin(),h.end(),static_cast<size_t>(0));
    }

    template<class IM>
    void fill(const IM& im) {
        static_assert(std::is_same_v<T, std::remove_const_t<typename IM::type>>);
        clear();
        for(auto v: im) inc(v);
    }

    size_t get_pos(T value) {
        auto diff = bins.back()-bins.front();
        if (diff==0) {
            return 0;
        }
        else if (value < bins.front()) {
            return 0;
        }
        else {
            auto pos = static_cast<size_t>(std::floor((value - bins.front())*histosize/diff));
            if (pos>=histosize) pos = histosize-1;
            return pos;
        }
    }
    void inc(T value, C num=1) {
        size_t pos = get_pos(value);
        h[pos]+=num;
    }

    void dec(T value, C num=1) {
        auto pos = get_pos(value);
        if (h[pos]>num) h[pos]-=num;
        else h[pos]=0;
    }

    T get_approx_median(size_t sum=0) {
        if (sum==0) sum=std::accumulate(h.begin(), h.end(), static_cast<size_t>(0));
        size_t csum=0;
        for(size_t i=0;i<histosize;i++) {
            csum+=h[i];
            if (csum>sum/2) {
                return bins[i];
            }
        }
        return bins[0];
    }

    friend std::ostream& operator<<(std::ostream &o, const Histogram& h) {
        auto m = *std::max_element(h.h.begin(), h.h.end());
        for(size_t i=0;i<h.h.size();i++) {
            auto n = h[i]*W/m;
            o << std::setw(3) << i << ":" << std::string(n,'#') << "\n";
        }
        return o;
    }

};

/*template<class IM>
my_image_lib::ImageImpl<typename IM::type> histeq(const IM& im, int N=256) {
    auto [h,b] = hist(im, N);
    std::vector<size_t> cumsum;
    std::partial_sum(h.begin(), h.end(),std::back_inserter(cumsum));
    im2::ImageImpl<typename IM::type> out(im.getWidth(), im.getHeight());
    auto outi = out.begin();
    auto mima = std::minmax_element(im.begin(), im.end());
    std::transform(im.begin(), im.end(), outi, [&](auto x){
        size_t i = (x-*mima.first)*N/(*mima.second-*mima.first);
        if (i>=N) i =N-1;
        return cumsum[i];
    });
    return out;
}*/

template<class T=uint8_t, class C=size_t>
struct HistogramForQuantile {
    size_t histosize;
    size_t quantile_pos=0;
    float quantile = 0.5; // 0.5 = median
    C total_sum=0;
    std::vector<C> h={};
    std::vector<C> cumsum={};
    std::vector<T> bins={};
    C operator[](size_t idx) const { return h[idx]; }

    template<class IM>
    HistogramForQuantile(const IM& im, size_t _histosize, bool init=true) : histosize(_histosize) {
        static_assert(std::is_same_v<T, std::remove_const_t<typename IM::type>>);
        h.resize(histosize);
        bins.resize(histosize);
        cumsum.resize(histosize);
        auto mima = std::minmax_element(im.begin(), im.end());
        for(size_t i=0;i<histosize;i++) bins[i] = *mima.first + (*mima.second-*mima.first)*i/histosize;
        if (init) fill(im);
        else clear();
    }

    HistogramForQuantile(size_t _histosize, T mi, T ma) : histosize(_histosize) {
        h.resize(histosize);
        bins.resize(histosize);
        cumsum.resize(histosize);
        for(size_t i=0;i<histosize;i++) bins[i] = mi + (ma-mi)*i/histosize;
        clear();
    }

    void clear() {
        std::fill(h.begin(),h.end(),static_cast<size_t>(0));
        std::fill(cumsum.begin(),cumsum.end(),static_cast<size_t>(0));
        quantile_pos = 0;
        total_sum = 0;
    }

    template<class IM>
    void fill(const IM& im) {
        static_assert(std::is_same_v<T, std::remove_const_t<typename IM::type>>);
        clear();
        for(auto v: im) inc(v);
    }

    size_t get_pos(T value) {
        auto diff = bins.back()-bins.front();
        if (diff==0) {
            return 0;
        }
        else if (value < bins.front()) {
            return 0;
        }
        else {
            auto pos = static_cast<size_t>(std::floor((value - bins.front())*histosize/diff));
            if (pos>=histosize) pos = histosize-1;
            return pos;
        }
    }
    void inc(T value, C num=1) {
        size_t pos = get_pos(value);
        h[pos] += num;
        total_sum += num;
        quantile_pos = std::min(quantile_pos, pos);
    }

    void dec(T value, C num=1) {
        auto pos = get_pos(value);
        if (h[pos]>num) h[pos]-=num;
        else h[pos]=0;
        if (total_sum>num) total_sum -= num;
        else total_sum=0;
        quantile_pos = std::min(quantile_pos, pos);
    }

    T get_approx_quantile() {
        adjust_quantile();
        if (quantile_pos>=histosize) return bins.back();
        else return bins[quantile_pos];
    }
private:

    void adjust_quantile() {
        if (quantile_pos>0) {
            cumsum[quantile_pos] = cumsum[quantile_pos-1]+h[quantile_pos];
        }
        C target_sum = std::llround(quantile * total_sum);
        while (quantile_pos>0 && cumsum[quantile_pos]>target_sum) quantile_pos--;
        while(cumsum[quantile_pos]<target_sum && quantile_pos<histosize) {
            quantile_pos++;
            if (quantile_pos<histosize) {
                cumsum[quantile_pos] = cumsum[quantile_pos-1] + h[quantile_pos];
            } 
        }
    }

};


}

#endif
