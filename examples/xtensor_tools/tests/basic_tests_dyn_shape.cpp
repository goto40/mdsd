#include "catch.hpp"

#include <xtensor/xio.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xview.hpp>

TEST_CASE("first steps: a3d array", "[xtensor]")
{
  xt::xarray<float> a3d = xt::zeros<float>({10, 10, 10});
  auto a0 = xt::view(a3d, 0, xt::all(), xt::all());
  auto a1 = xt::view(a3d, xt::all(), 1, xt::all());
  auto a2 = xt::view(a3d, xt::all(), xt::all(), 2);
  a0(0, 0) = 1;    // ok
  a1(0, 0) = 0.75; // ok
  a2(0, 0) = 0.5;  // produces "static_assert(I < sizeof...(Args), "I should be lesser than sizeof...(Args)");"

  CHECK(a3d(0, 0, 0) == Approx(1.0));
  CHECK(a3d(0, 1, 0) == Approx(0.75));
  CHECK(a3d(0, 0, 2) == Approx(0.5));
}

TEST_CASE("first steps: dynamic shape", "[xtensor]")
{
  xt::xarray<double>::shape_type shape = {2, 3};
  xt::xarray<double> a0(shape);
  xt::xarray<double> a1(shape, 2.5);
  xt::xarray<double> a2 = {{1., 2., 3.}, {4., 5., 6.}};
  auto a3 = xt::xarray<double>::from_shape(shape);

  //std::cout << a0 << "\n";
  CHECK(a0.shape()[0] == 2);
  CHECK(a0.shape()[1] == 3);

  //std::cout << a1 << "\n";
  CHECK(a1(0, 0) == Approx(2.5));
  //std::cout << a2 << "\n";
  CHECK(a2(0, 0) == Approx(1.0));
  CHECK(a2(0, 1) == Approx(2.0));
  CHECK(a2(1, 2) == Approx(6.0));
  //std::cout << a3 << "\n";
  CHECK(a3(1, 2) == Approx(0.0));

  auto v2 = xt::view(a2, 1, xt::all());
  CHECK(v2(2) == Approx(6.0));
  v2(2) = 1.2;
  CHECK(v2(2) == Approx(1.2));
  CHECK(a2(1, 2) == Approx(1.2));
}
