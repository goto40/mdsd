#include "catch.hpp"
#include "items/Circle.h"
#include "items/Polygon.h"
#include "items/Line.h"
#include "items/ColoredTriangle.h"
#include "items/VariantExample.h"
#include "items/more/Point3D.h"
#include "mdsd/item_support.h"

using namespace items;
using namespace mdsd;

TEST_CASE( "Simple.scan", "[scan_tests]" ) {
  items::more::Point3D p3{ 12.3,45.6 };
  Point p{ 12.3,45.6 };
  Line l{ Point{1,2}, Point{3,4} };
  Circle c{ Point{6,7}, 9.2 };
  ColoredTriangle t{{1.0, 0.0, 0.0},
    {Point{-1,0}, Point{-1,1}, Point{1,1}}};

  {
    std::ostringstream ostream;
    mdsd::print(p,ostream);
    Point p2{};
    std::istringstream istream(ostream.str());
    scan(p2, istream);

    REQUIRE(p2.x == Approx(p.x));
    REQUIRE(p2.y == Approx(p.y));
  }
  Polygon poly;
  poly.header.n = 3;
  adjust_array_sizes_and_variants(poly);

  {
    std::ostringstream ostream;
    mdsd::print(poly,ostream);
    Polygon poly2{};
    Point p2{};
    {
        std::istringstream istream(ostream.str());
        REQUIRE_THROWS( scan(p2, istream) );
    }
    {
        std::istringstream istream(ostream.str());
        scan(poly2, istream);
    }

    REQUIRE(poly2.header.n == poly.header.n);
    REQUIRE(poly2.points.size() == poly.points.size());
  }

  VariantExample v;
  v.selector=10;
  adjust_array_sizes_and_variants(v);

  {
    std::ostringstream ostream;
    mdsd::print(v,ostream);
    VariantExample v2{};
    std::istringstream istream(ostream.str());
    scan(v2, istream);

    REQUIRE(v2.selector == v.selector);

    std::ostringstream ostream2;
    mdsd::print(v2,ostream2);

    REQUIRE(ostream.str() == ostream2.str());
    REQUIRE(ostream.str().size() > 0);
  }
}

