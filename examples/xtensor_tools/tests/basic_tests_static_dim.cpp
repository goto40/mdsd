#include "catch.hpp"

#include <xtensor/xtensor.hpp>
#include <xtensor/xio.hpp>

TEST_CASE("first steps: static dim", "[xtensor]")
{
    xt::xtensor<double, 2>::shape_type shape = {2, 3};
    xt::xtensor<double, 2> a0(shape);
    xt::xtensor<double, 2> a1(shape, 2.5);
    xt::xtensor<double, 2> a2 = {{1., 2., 3.}, {4., 5., 6.}};
    auto a3 = xt::xtensor<double, 2>::from_shape(shape);

    //std::cout << a0 << "\n";
    CHECK(a0.shape()[0] == 2);
    CHECK(a0.shape()[1] == 3);

    //std::cout << a1 << "\n";
    CHECK(a1(0, 0) == Approx(2.5));
    //std::cout << a2 << "\n";
    CHECK(a2(0, 0) == Approx(1.0));
    CHECK(a2(0, 1) == Approx(2.0));
    CHECK(a2(1, 2) == Approx(6.0));
}
