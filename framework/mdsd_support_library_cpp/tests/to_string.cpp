#include "catch.hpp"
#include "items/VariantExample.h"
#include "items/ColoredTriangle.h"
#include "mdsd/item_support.h"
#include "mdsd/virtual_struct.h"

using namespace items;

TEST_CASE( "to_string single value/item", "[to_string]" ) {
  mdsd::Struct<VariantExample> s;
  s.data.selector = 11;
  s.adjust_array_sizes_and_variants();
  {
    std::ostringstream stream;
    s.print_to_stream(stream);
    REQUIRE(stream.str() == mdsd::to_string(s.data));
    REQUIRE(std::string("11") == mdsd::to_string(s.data.selector));
  }
}

TEST_CASE( "to_string attr", "[to_string]" ) {
  ColoredTriangle t;
  {
    REQUIRE(std::string("[ 0 0 0 ]") == mdsd::to_string_with_meta<ColoredTriangle::META::color>(t));
  }
}

TEST_CASE( "to_string attr2", "[to_string]" ) {
  ColoredTriangle t;
  {
    REQUIRE(std::string("[ Point { x = 0 y = 0 } Point { x = 0 y = 0 } Point { x = 0 y = 0 } ]") == mdsd::to_string_with_meta<ColoredTriangle::META::points>(t));
  }
}

TEST_CASE( "from_string attr", "[to_string]" ) {
  ColoredTriangle t;
  mdsd::from_string_with_meta<ColoredTriangle::META::color>("[11 22 33]", t);
  REQUIRE( t.color[0] == Approx(11));
  REQUIRE( t.color[1] == Approx(22));
  REQUIRE( t.color[2] == Approx(33));
}

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
