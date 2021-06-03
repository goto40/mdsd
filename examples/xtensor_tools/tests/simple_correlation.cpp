#include "catch.hpp"

#include <xtensor-io/ximage.hpp>
#include "xtensor_tools.h"
#include <xtensor/xio.hpp>

TEST_CASE("center surround", "[xtensor]")
{
    auto im1 = xtensor_tools::rgb2gray(xt::load_image("../tests/data/exampleD/exampleD_000.png"));
    auto im2 = xtensor_tools::rgb2gray(xt::load_image("../tests/data/exampleD/exampleD_001.png"));
    xt::xarray<float> cs1, cs2;
    xtensor_tools::center_surround(im1, 5, cs1);
    xtensor_tools::center_surround(im2, 5, cs2);
    xt::xarray<float> motion;
    motion.resize({1, 1, 15, 15});

    xtensor_tools::simple_correlation(cs1, cs2, 7, motion);

    CHECK(xt::eval(xt::amin(motion))[0] >= 0.0);
}
