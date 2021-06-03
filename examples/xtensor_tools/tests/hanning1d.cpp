#include "catch.hpp"

#include "xtensor_tools.h"

TEST_CASE("hanning1d", "[xtensor]")
{
    auto mask = xtensor_tools::hanning1d<float>(5);

    CHECK(mask[0] == mask[4]);
    CHECK(mask[1] == mask[3]);
    CHECK(mask[2] > mask[3]);
}
