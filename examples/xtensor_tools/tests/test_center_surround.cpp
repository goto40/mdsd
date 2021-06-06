#include "catch.hpp"

#include <xtensor-io/ximage.hpp>
#include "xtensor_tools.h"
#include <xtensor/xio.hpp>

TEST_CASE("center surround", "[xtensor]")
{
    auto im = xtensor_tools::rgb2gray(xt::load_image("../tests/data/exampleD/exampleD_000.png"));
    xt::xarray<float> cs;
    xtensor_tools::center_surround(im, 5, cs);
    CHECK(xt::eval(xt::amin(cs))[0] < -0.05);
    CHECK(xt::eval(xt::amax(cs))[0] > +0.05);

    CHECK(xt::eval(xt::amin(im))[0] > -0.05); // input is positive...
}
