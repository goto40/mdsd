#include "catch.hpp"
#include "big_example/VersionedData.h"
#include "mdsd/item_support.h"
#include <sstream>

TEST_CASE( "version_tests", "[version_tests1]" ) {
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
}

