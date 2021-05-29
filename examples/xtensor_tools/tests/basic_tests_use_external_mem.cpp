#include "catch.hpp"
#include <cstddef>
#include <vector>
#include <array>

#include <xtensor/xadapt.hpp>
#include <xtensor/xio.hpp>
#include <xtensor/xfixed.hpp>

TEST_CASE("first steps: ext mem 1", "[xtensor]")
{
    std::vector<float> data = {5.1, 5.2, 5.3, 5.4, 5.5, 5.6};

    size_t shape[] = {2, 3};
    auto a2 = xt::adapt(data, shape);

    std::cout << a2 << "\n";
    CHECK(a2(0, 0) == Approx(5.1));
    CHECK(a2(0, 1) == Approx(5.2));
    CHECK(a2(1, 2) == Approx(5.6));
}

TEST_CASE("first steps: ext mem 2", "[xtensor]")
{
    float data[] = {5.1, 5.2, 5.3, 5.4, 5.5, 5.6};

    std::array<size_t, 2> shape = {2, 3};
    auto a2 = xt::adapt(data, shape);

    std::cout << a2 << "\n";
    CHECK(a2(0, 0) == Approx(5.1));
    CHECK(a2(0, 1) == Approx(5.2));
    CHECK(a2(1, 2) == Approx(5.6));
}
