#include "catch.hpp"
#include "my_image_lib/GrayImage.h"
#include "my_image_lib/tools.h"
#include "my_image_lib/Tictoc.h"
#include "mdsd/item_support.h"
#include "my_image_lib/background_subtraction/AlgoBackgroundSubtractionImpl.h"

#include <algorithm>
#include <numeric>

using namespace my_image_lib;
using namespace mdsd;

TEST_CASE( "Simple.pixeldata", "[basic]" ) {
    GrayImage im;
    im.w=320;
    im.h=200;
    adjust_array_sizes_and_variants(im);
    REQUIRE( im.pixel.size() == im.w*im.h );
}

TEST_CASE( "Simple.median1D1D", "[basic]" ) {
    GrayImage im, res;
    im.w=320;
    im.h=200;
    adjust_array_sizes_and_variants(im);
    std::fill( im.pixel.begin(), im.pixel.end(), 3);
    im.pixel[3249]=9;
    im.pixel[3250]=9;
    im.pixel[3251]=9;
    REQUIRE( im.pixel[3249] == 9 );
    REQUIRE( im.pixel[3250] == 9 );
    REQUIRE( im.pixel[3251] == 9 );
    REQUIRE( im.pixel[3252] == 3 );
    my_image_lib::median1D(im, 3, true, res);

    REQUIRE( res.pixel.size() == im.w*im.h );
    REQUIRE( res.pixel[3250] == 9 );

    my_image_lib::median1D(im, 7, true, res);
    REQUIRE( res.pixel.size() == im.w*im.h );
    REQUIRE( res.pixel[3250] == 3 );


    my_image_lib::median1D(im, 3, false, res);

    REQUIRE( res.pixel.size() == im.w*im.h );
    REQUIRE( res.pixel[3250] == 3 );
}

TEST_CASE( "Simple.median1D1D parallel x", "[basic]" ) {
    GrayImage im, res1, res2;
    im.w=320;
    im.h=200;
    adjust_array_sizes_and_variants(im);
    std::iota( im.pixel.begin(), im.pixel.end(), 0 );
    im.pixel[3249]=9;
    im.pixel[3250]=9;
    im.pixel[3251]=9;
    {
        my_image_lib::Tictoc tictoc{"xx1:"};
        my_image_lib::median1D(im, 3, false, res1, 1);
    }
    {
        my_image_lib::Tictoc tictoc{"xx4:"};
        my_image_lib::median1D(im, 3, false, res2, 4);
    }
    for (size_t i=0;i<im.w*im.h;i++) {
        REQUIRE( res1.pixel[i] == res2.pixel[i] );
    }
}

TEST_CASE( "Simple.median1D1D parallel y", "[basic]" ) {
    GrayImage im, res1, res2;
    im.w=320;
    im.h=200;
    adjust_array_sizes_and_variants(im);
    std::iota( im.pixel.begin(), im.pixel.end(), 0 );
    im.pixel[3249]=9;
    im.pixel[3250]=9;
    im.pixel[3251]=9;
    {
        my_image_lib::Tictoc tictoc{"yx1:"};
        my_image_lib::median1D(im, 3, true, res1, 1);
    }
    {
        my_image_lib::Tictoc tictoc{"yx4:"};
        my_image_lib::median1D(im, 3, true, res2, 4);
    }
    for (size_t i=0;i<im.w*im.h;i++) {
        REQUIRE( res1.pixel[i] == res2.pixel[i] );
    }
}

TEST_CASE( "AlgoBackground", "[basic]" ) {
    auto algo = my_image_lib::background_subtraction::AlgoBackgroundSubtraction::create();
    my_image_lib::background_subtraction::BackgroundSubtractionParameters params;
    params.type = my_image_lib::background_subtraction::MedianType::MEDIAN;
    params.threshold = 0;

    my_image_lib::GrayImage im;
    my_image_lib::background_subtraction::BackgroundSubtractionResults res;

    im.w=320;
    im.h=200;
    adjust_array_sizes_and_variants(im);
    std::iota( im.pixel.begin(), im.pixel.end(), 0 );
 
    // smoke test
    algo->compute(im, res);
}