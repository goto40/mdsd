#include "catch.hpp"

#include <xtensor-io/ximage.hpp>
#include <xtensor/xview.hpp>

TEST_CASE("first steps: read_im", "[xtensor]")
{
    auto im = xt::load_image("../tests/data/blume2.png"); // should not throw
    xt::dump_image("test.png", im);                       // should not throw

    size_t h = im.shape()[0];

    for (size_t y = 0; y < h; y++)
    {
        auto v = xt::view(im, 0, xt::all());
        for (auto &p : v)
        {
            p *= static_cast<float>(y) / static_cast<float>(h);
        }
    }
    xt::dump_image("test2.png", im); // should not throw
}
