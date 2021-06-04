#include "catch.hpp"

#include <xtensor-io/ximage.hpp>
#include "xtensor_tools.h"
#include <xtensor/xio.hpp>
#include <xtensor/xadapt.hpp>

TEST_CASE("first steps: read_im", "[xtensor]")
{
    auto im0 = xt::load_image("../tests/data/blume2.png"); // should not throw
    auto im = xtensor_tools::rgb2gray(im0);
    //std::cout << "shape: " << xt::adapt(im.shape()) << "\n";
    xt::dump_image("test.png", xtensor_tools::gray2rgb(im)); // should not throw

    xt::xarray<float> mask = {-1.0f, 0.0f, 1.0f};
    xtensor_tools::conv2d_1d_x(im, mask);
    //xtensor_tools::conv2d_1d_y(im, mask);

    xt::dump_image("test2.png", xtensor_tools::gray2rgb(im)); // should not throw
}

TEST_CASE("read imagepair collector", "[xtensor]")
{
    xtensor_tools::ImagePairCollector pc("../tests/data/exampleD/exampleD_%03u.png", 0, 10);
    size_t cnt = 0;
    while (pc.read_next())
    {
        cnt++;
    }
    CHECK(cnt == 9);
}
