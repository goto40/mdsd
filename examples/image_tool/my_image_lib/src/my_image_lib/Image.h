#ifndef IM2_IMAGE_H
#define IM2_IMAGE_H

#include <vector>
#ifdef __USE_STB_IMAGE
#include "stb_image.h"
#include "stb_image_write.h"
#endif
#include <thread>
#include <future>
#include <algorithm>

namespace my_image_lib {

template<class T=float>
class ImageImpl {
    int w,h;
    std::vector<T> data;
public:
    using type=T; 
#ifdef __USE_STB_IMAGE
    ImageImpl(const char* fn) {
        int c;
        stbi_uc *idata = stbi_load(fn, &w, &h, &c, 1);
        assert(idata);
        data.resize(w*h);
        if constexpr (std::is_floating_point_v<T>) {
            for(int i=0;i<w*h;i++) data[i]=static_cast<T>(idata[i])/255.0;
        }
        else {
            for(int i=0;i<w*h;i++) data[i]=static_cast<T>(idata[i]);
        }
        stbi_image_free(idata);        
    }
#endif
    ImageImpl(int _w, int _h) : w(_w), h(_h), data() {
        data.resize(w*h);
        std::fill(data.begin(), data.end(), 0.0);
    }
    type get(int x,int y) const { return data[x+y*w]; }
    void set(int x,int y, type v) { data[x+y*w]=v; }
    type* getline(int y) { return &data[y*w]; }
    const type* getline(int y) const { return &data[y*w]; }
    int getWidth() const  { return w; }
    int getHeight() const  { return h; }

    auto begin() { return data.begin(); }
    auto end() { return data.end(); }
    auto begin() const { return data.cbegin(); }
    auto end() const { return data.cend(); }

    auto sel(int x,  int y, int w, int h);
    auto sel(int x,  int y, int w, int h) const;
};

template<class T=float>
class PtrImageImpl {
    int w,h;
    T* data;
public:
    using type=T; 
    PtrImageImpl(T* _dataptr, int _w, int _h) : w(_w), h(_h), data(_dataptr){
    }
    type get(int x,int y) const { return data[x+y*w]; }
    void set(int x,int y, type v) { data[x+y*w]=v; }
    type* getline(int y) { return &data[y*w]; }
    const type* getline(int y) const { return &data[y*w]; }
    int getWidth() const  { return w; }
    int getHeight() const  { return h; }

    T* begin() { return data; }
    T* end() { return data+w*h; }
    const T* begin() const { return data; }
    const T* end() const { return data+w*h; }

    auto sel(int x,  int y, int w, int h);
    auto sel(int x,  int y, int w, int h) const;
};

template<class T, class IM>
struct Iter {
    IM* im;
    int y;
    T *ptr;
    T *end;
    Iter() :im(nullptr), y(0), ptr(nullptr), end(nullptr) {}
    Iter(IM& i, int _y, int _x) :im(&i), y(_y), ptr(im->getline(_y)+_x), end(im->getline(_y)+im->getWidth()) {}
    Iter(const Iter&) = default;
    Iter& operator=(const Iter&) = default;
    Iter(Iter&&) = default;
    Iter& operator=(Iter&&) = default;
    T& operator*() { return *ptr; }
    const T& operator*() const { return *ptr; }
    Iter& operator++() { ptr++; if (ptr==end) *this=Iter{*im, y+1, 0}; return *this; }
    bool operator!=(Iter o) { return ptr!=o.ptr; }
    bool operator==(Iter o) { return ptr==o.ptr; }
};

template<class IM, class T=typename IM::type>
class ImageSelectionImpl {
    IM &im;
    int x0,y0,w,h;
public:
    using type=T; 
    /** selects a subimage */
    ImageSelectionImpl(IM &_im, int _x0,int _y0, int _w, int _h) :
    im(_im), x0(_x0), y0(_y0), w(_w), h(_h) {}
    ImageSelectionImpl(ImageSelectionImpl&&) = default;
    ImageSelectionImpl& operator=(ImageSelectionImpl&&) = default;
    type get(int x,int y) const { return im.get(x+x0,y+y0); }
    void set(int x,int y, type v) { im.set(x+x0,y+y0, v); }
    type* getline(int y) { return im.getline(y+y0)+x0; }
    const type* getline(int y) const { return im.getline(y+y0)+x0; }
    int getWidth() const { return w; }
    int getHeight() const { return h; }

    auto begin() { return Iter<type,ImageSelectionImpl>{*this,0,0}; }
    auto end() { return Iter<type,ImageSelectionImpl>{*this,h,0}; }
    auto begin() const { return Iter<const type,const ImageSelectionImpl>{*this,0,0}; }
    auto end() const { return Iter<const type,const ImageSelectionImpl>{*this,h,0}; }

    auto sel(int x,  int y, int w, int h) {
        return ImageSelectionImpl<ImageSelectionImpl>{*this, x,y,w,h};
    }
    auto sel(int x,  int y, int w, int h) const {
        return ImageSelectionImpl<const ImageSelectionImpl, const type>{*this, x,y,w,h};
    }
};

template<class T>
auto ImageImpl<T>::sel(int x,  int y, int w, int h) {
    return ImageSelectionImpl<ImageImpl<T>>{*this, x,y,w,h};
}
template<class T>
auto ImageImpl<T>::sel(int x,  int y, int w, int h) const {
    return ImageSelectionImpl<const ImageImpl<T>, const T>{*this, x,y,w,h};
}
template<class T>
auto PtrImageImpl<T>::sel(int x,  int y, int w, int h) {
    return ImageSelectionImpl<PtrImageImpl<T>>{*this, x,y,w,h};
}
template<class T>
auto PtrImageImpl<T>::sel(int x,  int y, int w, int h) const {
    return ImageSelectionImpl<const PtrImageImpl<T>, const T>{*this, x,y,w,h};
}

#ifdef __USE_STB_IMAGE
template<class IM>
void write_png(const IM& im, const char* fn, bool autoscale=true) {
    using T =typename IM::type;
    int w = im.getWidth();
    int h = im.getHeight();
    std::vector<stbi_uc> idata(w*h);
    float black = 0.0;
    float white = 1.0;
    if constexpr (!std::is_floating_point_v<T>) {
        white = 255;
    }
    if (autoscale) {
        white = black = static_cast<float>(im.get(0,0));
        for(int y=0;y<h;y++) {
            for(int x=0;x<w;x++) {
                black = std::min(black, static_cast<float>(im.get(x,y)));
                white = std::max(white, static_cast<float>(im.get(x,y)));
            }
        }
    }
    int i=0;
    for(int y=0;y<h;y++) {
        for(int x=0;x<w;x++) {
            float v = (( static_cast<float>(im.get(x,y)) -black)/(white-black))*255.0;
            v = std::min<float>(v,255.0);
            v = std::max<float>(v,0.0);
            idata[i++]=static_cast<stbi_uc>(v+0.5f); // round
        }
    }
    stbi_write_png(fn, w, h, 1, idata.data(), w);
}
#endif

template<class IM>
auto mean(const IM& im) {
    std::remove_const_t<typename IM::type> sum=0;
    for(auto x: im) sum+= x;
    return sum / im.getWidth()*im.getHeight();
}

}

#endif