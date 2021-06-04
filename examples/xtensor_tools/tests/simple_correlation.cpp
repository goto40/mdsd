#include "catch.hpp"

#include <xtensor-io/ximage.hpp>
#include "xtensor_tools.h"
#include <xtensor/xio.hpp>
#include <xtensor/xview.hpp>

TEST_CASE("simple_correlation", "[xtensor]")
{
    auto im1 = xtensor_tools::rgb2gray(xt::load_image("../tests/data/exampleD/exampleD_000.png"));
    auto im2 = xtensor_tools::rgb2gray(xt::load_image("../tests/data/exampleD/exampleD_001.png"));
    xt::xtensor<float, 2> cs1, cs2;
    xtensor_tools::center_surround(im1, 3, cs1);
    xtensor_tools::center_surround(im2, 3, cs2);

    xt::xtensor<float, 4> motion;

    constexpr size_t v_n = 11;
    constexpr size_t v0 = v_n / 2;
    motion.resize({1, 1, v_n, v_n});

    xtensor_tools::simple_correlation(cs1, cs2, 7, motion);

    using namespace xt::placeholders; // required for `_` to work

    // no likelihood < 0
    CHECK(xt::eval(xt::amin(motion))[0] >= 0.0);

    // eval global likelihoods
    auto sum_vyvx = xt::sum(motion, {0, 1});
    //std::cout << "sum_vyvx: " << sum_vyvx << "\n";
    xt::dump_image("simple_correlation_sum_vyvx.png", xtensor_tools::gray2rgb(sum_vyvx)); // should not throw

    // box is moving right/downwards +3,+3
    CHECK(sum_vyvx(v0 + 3, v0 + 3) > 0.01);
    //CHECK(sum_vyvx(v0 + 3, v0 + 3) == xt::eval(xt::amax(xt::view(sum_vyvx, xt::range(v0 + 0, _), xt::all())))[0]);
    CHECK(sum_vyvx(v0 + 3, v0 + 3) == xt::eval(xt::amax(xt::view(sum_vyvx, xt::all(), xt::all())))[0]);

    // stick is moving leftwards 0,-3
    std::cout << "sum_vyvx[0,:]: " << sum_vyvx << "\n";
    CHECK(sum_vyvx(v0 + 0, v0 - 3) > 0.01);
    CHECK(sum_vyvx(v0 + 0, v0 - 3) > sum_vyvx(v0 + 0, v0 - 4));
    CHECK(sum_vyvx(v0 + 0, v0 - 3) > sum_vyvx(v0 + 0, v0 - 2));

    auto hsv = xtensor_tools::motion2hsv(im2, motion);
    xt::dump_image("simple_correlation_hsv.png", xtensor_tools::hsv2rgb(hsv)); // should not throw
}
