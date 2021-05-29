#include "catch.hpp"

#include <xtensor-io/ximage.hpp>

TEST_CASE("first steps: read_im", "[xtensor]")
{
    auto im = xt::load_image("../tests/data/blume2.png"); // should not throw
    xt::dump_image("test.png", im);                       // should not throw
}
