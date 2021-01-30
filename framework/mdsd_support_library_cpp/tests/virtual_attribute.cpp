#include "catch.hpp"
#include "items/ColoredTriangle.h"
#include "items/VariantExample.h"
#include "mdsd/virtual_attribute_support.h"
#include "mdsd/item_support.h"

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

  auto attrs_in_color_triangle = mdsd::get_all_attributes(t);
  REQUIRE( attrs_in_color_triangle.size()==2 );
  REQUIRE( attrs_in_color_triangle[0]->get_name() == "color" );
  REQUIRE( attrs_in_color_triangle[1]->get_name() == "points" );
  REQUIRE_THROWS( attrs_in_color_triangle[1]->get_all_attributes_in_struct());
  auto attrs_in_point1 = attrs_in_color_triangle[1]->get_all_attributes_in_struct(1);
  REQUIRE( attrs_in_point1[0]->get_name() == "x" );
  REQUIRE( attrs_in_point1[1]->get_name() == "y" );  
  REQUIRE( attrs_in_point1[1]->to_string() == std::string("456"));
}

TEST_CASE( "attributewrapper2", "[virtual access]" ) {
  VariantExample v1;

  v1.selector = 20; // Polygon
  mdsd::adjust_array_sizes_and_variants(v1);
  std::get<Polygon>(v1.payload).header.n = 3;

  auto n = mdsd::get_attribute(v1, "payload")
              ->get_attribute_in_struct("header")
              ->get_attribute_in_struct("n");
  REQUIRE( n->to_string() == std::string("3"));

  auto attrs_in_v1 = mdsd::get_all_attributes(v1);
  REQUIRE( attrs_in_v1.size()==2 );
  REQUIRE_THROWS( attrs_in_v1[1]->get_all_attributes_in_struct(1));
  auto attrs_in_payload = attrs_in_v1[1]->get_all_attributes_in_struct();
  REQUIRE( attrs_in_payload[0]->get_name() == "header" );
  REQUIRE( attrs_in_payload[1]->get_name() == "points" );
}
