#include "catch.hpp"
#include "items/Point.h"
#include "items/Line.h"
#include "items/Circle.h"
#include "items/Polygon.h"
#include "items/ColoredTriangle.h"
#include "items/VariantExample.h"
#include "items/more/Point3D.h"
#include "mdsd/item_support.h"

using namespace items;
using namespace mdsd;

TEST_CASE( "Simple.pprint", "[print_tests]" ) {
  items::more::Point3D p3{ 12.3,45.6,0 };
  Point p{ 12.3,45.6 };
  Line l{ Point{1,2}, Point{3,4} };
  Circle c{ Point{6,7}, 9.2 };
  ColoredTriangle t{{1.0, 0.0, 0.0},
    {Point{-1,0}, Point{-1,1}, Point{1,1}}};

  {
    std::ostringstream stream;
    print(p,stream);
    REQUIRE( stream.str() == R"(Point {
  x = 12.3
  y = 45.6
}
)");
  }
  std::ostringstream dummy;
  print(l,dummy);
  print(c,dummy);
  print(t,dummy);

  Polygon poly;
  poly.header.n = 3;
  adjust_array_sizes_and_variants(poly);
  print(poly,dummy);

  Polygon poly2;
  poly2.header = Header{2};
  adjust_array_sizes_and_variants(poly2);
  poly2.points = { Point{1,2}, Point{3,4} };
  print(poly2,dummy);

  Polygon poly3err;
  poly3err.header = Header{3};
  adjust_array_sizes_and_variants(poly3err);
  poly3err.points = { Point{1,2}, Point{3,4} };
  try {
    print(poly3err,dummy);
  }
  catch(std::exception &e) {
    //std::cout << "an execption as expected: " << e.what() << "\n";
  }

  VariantExample v;
  v.selector=10;
  adjust_array_sizes_and_variants(v);
  {
    std::ostringstream stream;
    print(v,stream);
    REQUIRE(stream.str() == R"(VariantExample {
  selector = 10
  payload =
    Point {
      x = 0
      y = 0
    }
}
)");
  }
  v.selector=11;
  adjust_array_sizes_and_variants(v);
  {
    std::ostringstream stream;
    print(v,stream);
    REQUIRE(stream.str() == R"(VariantExample {
  selector = 11
  payload =
    Line {
      p1 =
        Point {
          x = 0
          y = 0
        }
      p2 =
        Point {
          x = 0
          y = 0
        }
    }
}
)");
    }
  v.selector=99;
  REQUIRE_THROWS(adjust_array_sizes_and_variants(v));

  VariantExample vp;
  vp.selector = 10;
  vp.payload = Point{1,2};
  print(vp,dummy);

  VariantExample vp_err;
  vp_err.selector = 10;
  vp_err.payload = Line{Point{1,2}, Point{2,3}}; // wrong id
  REQUIRE_THROWS(print(vp_err));
}

TEST_CASE( "Simple.pprint with Struct<...>", "[print_tests]" ) {
  Struct<VariantExample> s;
  s.data.selector = 11;
  s.adjust_array_sizes_and_variants();
  {
    std::ostringstream stream;
    s.print_to_stream(stream);
    REQUIRE(stream.str() == R"(VariantExample {
  selector = 11
  payload =
    Line {
      p1 =
        Point {
          x = 0
          y = 0
        }
      p2 =
        Point {
          x = 0
          y = 0
        }
    }
}
)");
  }
}
