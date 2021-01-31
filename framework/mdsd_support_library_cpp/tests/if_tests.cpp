#include "catch.hpp"
#include "big_example/VersionedData.h"
#include "big_example/NDPoint.h"
#include "mdsd/item_support.h"
#include <sstream>

TEST_CASE( "version_tests", "[if_tests]" ) {
    {
        big_example::VersionedData i;
        std::istringstream s{R"(
            VersionedData {
                version = 0
                n = 3
                data = [ 1 2 3 ]
                data0 = [ 7 8 9 ]
            }
        )"};
        mdsd::scan(i, s);
        REQUIRE( i.data0.size() == 3 );
        REQUIRE( i.data1.size() == 0 );
    }

    {
        big_example::VersionedData i;
        std::istringstream s{R"(
            VersionedData {
                version = 1
                n = 3
                data = [ 1 2 3 ]
                data1 = [ 7 8 9 ]
            }
        )"};
        mdsd::scan(i, s);
        REQUIRE( i.data0.size() == 0 );
        REQUIRE( i.data1.size() == 3 );
        REQUIRE( i.data1[0] == 7 );
    }
}

TEST_CASE( "if test with NDPoint", "[if_tests]" ) {
    big_example::NDPoint i;
    i.dim=3;
    i.x=10;
    i.y=11;
    i.z=12;
    {
        std::ostringstream s;
        mdsd::print(i, s);
        REQUIRE( s.str().find("x") != std::string::npos );
        REQUIRE( s.str().find("y") != std::string::npos );
        REQUIRE( s.str().find("z") != std::string::npos );
    }
    {
        std::ostringstream s;
        i.dim = 2;
        mdsd::print(i, s);
        REQUIRE( s.str().find("x") != std::string::npos );
        REQUIRE( s.str().find("y") != std::string::npos );
        REQUIRE( s.str().find("z") == std::string::npos );
    }
    {
        std::ostringstream s;
        i.dim = 1;
        mdsd::print(i, s);
        REQUIRE( s.str().find("x") != std::string::npos );
        REQUIRE( s.str().find("y") == std::string::npos );
        REQUIRE( s.str().find("z") == std::string::npos );
    }
}

