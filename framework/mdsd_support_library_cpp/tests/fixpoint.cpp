#include "catch.hpp"
#include "big_example/FixpointExample2.h"
#include "mdsd/item_support.h"
#include <sstream>

TEST_CASE( "basic fixpoint test", "[fixpoint_tests]" ) {
    {
        big_example::FixpointExample2 i;
        i.u4( 11 );
        CHECK( i.u4() == 11 );
        i.s4( -11 );
        CHECK( i.s4() == -11 );
        CHECK( i.u4() == 11 );
        i.a4( 0, -14 );
        CHECK( i.a4(0) == -14 );
        CHECK( i.s4() == -11 );
        CHECK( i.u4() == 11 );
        i.a4( 1, -9 );
        CHECK( i.a4(1) == -9 );
        CHECK( i.a4(0) == -14 );
        CHECK( i.s4() == -11 );
        CHECK( i.u4() == 11 );
        std::istringstream s{R"(
            FixpointExample2 {
                u1 = 0.3
                s1 = -0.4
                as1 = [-1.1 2.2]
                u4 = 1.3
                s4 = -1.4
                a4 = [-1.3 1.2]
            }
        )"};
        mdsd::scan(i, s);
        CHECK(i.u1 == 3);
        CHECK(i.s1 == -4);
        CHECK(i.as1[0] == -11);
        CHECK(i.as1[1] == 22);
        CHECK((int)i.u4() == 13);
        CHECK((int)i.s4() == -14);
        CHECK((int)i.a4(0) == -13);
        CHECK((int)i.a4(1) == 12);

        i = big_example::FixpointExample2(
            1, -2, {-3, 4},
            5, -6, {-7, 8}
        );

        CHECK(i.u1 == 1);
        CHECK(i.s1 == -2);
        CHECK(i.as1[0] == -3);
        CHECK(i.as1[1] == 4);
        CHECK((int)i.u4() == 5);
        CHECK((int)i.s4() == -6);
        CHECK((int)i.a4(0) == -7);
        CHECK((int)i.a4(1) == 8);

    }
}
 //TODO out of bound for embeddeds...!