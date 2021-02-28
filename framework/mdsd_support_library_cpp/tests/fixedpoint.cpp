#include "catch.hpp"
#include "big_example/FixedpointExample2.h"
#include "mdsd/item_support.h"
#include <sstream>

TEST_CASE( "basic fixedpoint test", "[fixedpoint_tests]" ) {
    {
        big_example::FixedpointExample2 i;
        std::istringstream s{R"(
            FixedpointExample2 {
                u1 = 0.3
                s1 = -0.4
                as1 = [-100.1 200.2]
                u4 = 1.3
                s4 = -1.4
                a4 = [-200.1 400.2]
            }
        )"};
        mdsd::scan(i, s);
        REQUIRE(i.u1 == 3);
        REQUIRE(i.s1 == -4);
        REQUIRE(i.as1[0] == -1001);
        REQUIRE(i.as1[1] == 2002);
        CHECK((int)i.u4() == 13);
        CHECK((int)i.s4() == -14);
        CHECK((int)i.a4(0) == -2001);
        CHECK((int)i.a4(1) == 4002);
    }
}

// TODO init obj (constr. with params)
