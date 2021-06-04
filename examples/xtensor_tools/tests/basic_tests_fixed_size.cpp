#include "catch.hpp"

#include <xtensor/xfixed.hpp>
#include <xtensor/xio.hpp>

TEST_CASE("first steps: fixed size", "[xtensor]")
{
    xt::xtensor_fixed<double, xt::xshape<2, 3>> a2 = {{10., 2., 3.}, {4., 5., 6.}};

    //std::cout << a2 << "\n";
    CHECK(a2(0, 0) == Approx(10.0));
    CHECK(a2(0, 1) == Approx(2.0));
    CHECK(a2(1, 2) == Approx(6.0));
}
