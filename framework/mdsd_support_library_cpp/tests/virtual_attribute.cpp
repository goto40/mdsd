#include "catch.hpp"
#include "items/ColoredTriangle.h"
#include "mdsd/virtual_attribute_support.h"

using namespace items;

TEST_CASE( "attributewrapper1", "[to_string]" ) {
  ColoredTriangle t;
  mdsd::AttributeWrapper<ColoredTriangle::META::color> w(t);
  w.from_string("[11 22 33]");
  REQUIRE( t.color[0] == Approx(11));
  REQUIRE( t.color[1] == Approx(22));
  REQUIRE( t.color[2] == Approx(33));
  w.get_ref()[2] = 9;
  REQUIRE( t.color[2] == Approx(9));
  REQUIRE( w.to_string() == "[ 11 22 9 ]");
}
