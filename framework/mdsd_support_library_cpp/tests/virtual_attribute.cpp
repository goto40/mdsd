#include "catch.hpp"
#include "items/ColoredTriangle.h"
#include "mdsd/virtual_attribute_support.h"

using namespace items;

TEST_CASE( "attributewrapper1", "[to_string]" ) {
  ColoredTriangle t;
  t.points[1].x = 123;
  t.points[1].y = 456;
  mdsd::AttributeWrapper<ColoredTriangle::META::color> w(t);
  w.from_string("[11 22 33]");
  REQUIRE( t.color[0] == Approx(11));
  REQUIRE( t.color[1] == Approx(22));
  REQUIRE( t.color[2] == Approx(33));
  w.get_ref()[2] = 9;
  REQUIRE( t.color[2] == Approx(9));
  REQUIRE( w.to_string() == "[ 11 22 9 ]");

  auto color = mdsd::get_attribute(t, "color");
  REQUIRE( color->to_string() == std::string("[ 11 22 9 ]"));
  REQUIRE( color->is_array() );
  REQUIRE( color->get_dim() == 3 );
  REQUIRE( !color->is_struct() );
  auto points = mdsd::get_attribute(t, "points");
  REQUIRE( points->is_array() );
  REQUIRE( points->get_dim() == 3 );
  REQUIRE( points->is_struct() );
  std::string text = points->to_string();
  REQUIRE(text.find("Point") != std::string::npos);
  REQUIRE(text.find("123") != std::string::npos);
  REQUIRE(text.find("456") != std::string::npos);
  REQUIRE(text.find("XYZ") == std::string::npos);

  auto point1_x = points->get_attribute_in_struct(1,"x"); 
  auto point1_y = points->get_attribute_in_struct(1,"y");
  REQUIRE_THROWS(points->get_attribute_in_struct(1,"not_existent"));
  REQUIRE( point1_x->to_string() == std::string("123"));
  REQUIRE( point1_y->to_string() == std::string("456"));
}
