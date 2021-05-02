#include "catch.hpp"
#include "items/Point.h"
#include "items/VariantExample.h"
#include "items/Polygon.h"
#include "big_example/MultiMessage.h"
#include "big_example/AllInOne.h"
#include "mdsd/item_support.h"
#include "mdsd/item_io.h"
#include "mdsd/virtual_struct.h"
#include <fstream>

using namespace items;
using namespace mdsd;

TEST_CASE( "Simple.io", "[io_tests]" ) {
  Point p{ 12.3,45.6 };
  Point q{ 0,0 };

  std::array<std::byte, 1000> mem;
  size_t n = mdsd::copy_to_mem(p,mem.data(), mem.size());

  REQUIRE( n==sizeof(float)*2 );
  REQUIRE( q.x != p.x );
  REQUIRE( q.y != p.y );

  size_t m = copy_from_mem(mem.data(), n, q);
  REQUIRE( n==m );

  REQUIRE( q.x == p.x );
  REQUIRE( q.y == p.y );
}

TEST_CASE( "Simple.io2", "[io_tests]" ) {
  VariantExample v1;
  VariantExample v2;

  v1.selector = 20; // Polygon
  adjust_array_sizes_and_variants(v1);
  std::get<Polygon>(v1.payload).header.n = 3;
  adjust_array_sizes_and_variants(v1);
  REQUIRE( std::get<Polygon>(v1.payload).points.size()==3 );
  std::get<Polygon>(v1.payload).points[2].x = 3.14;
  std::get<Polygon>(v1.payload).points[2].y = 5.19;

  v2.selector = 11;
  adjust_array_sizes_and_variants(v2);

  std::array<std::byte, 10000> mem;
  size_t n = mdsd::copy_to_mem(v1,mem.data(), mem.size());

  REQUIRE( n>0 );

  size_t m = copy_from_mem(mem.data(), n, v2);

  REQUIRE(std::get<Polygon>(v1.payload).points[2].x == std::get<Polygon>(v2.payload).points[2].x);
  REQUIRE(std::get<Polygon>(v1.payload).points[2].y == std::get<Polygon>(v2.payload).points[2].y);

  v1.selector = 0; // ColoredTriangle (with rawtype array)
  adjust_array_sizes_and_variants(v1);

  REQUIRE( v1.selector == 0 );

  size_t n2 = mdsd::copy_to_mem(v1,mem.data(), mem.size());

  REQUIRE( n2>0 );

  REQUIRE( v2.selector == 20 );
  size_t m2 = copy_from_mem(mem.data(), n2, v2);
  REQUIRE( v2.selector == 0 );

  REQUIRE( m2 == n2 );
  REQUIRE_NOTHROW(check_array_sizes_and_variants(v2));

}

TEST_CASE( "virtual struct io", "[io_tests]" ) {
  std::array<std::byte, 10000> mem;
  mdsd::Struct<Polygon> p;
  p.data.header.n = 2;
  p.adjust_array_sizes_and_variants();
  size_t n1 = p.copy_to_mem(mem.data(), mem.size());
  REQUIRE( n1 == p.count_bytes() );
  mdsd::Struct<Polygon> q;
  q.copy_from_mem(mem.data(),n1);
  REQUIRE( q.data.header.n == p.data.header.n );

  p.data.header.n = 3;
  p.adjust_array_sizes_and_variants();
  size_t n2 = p.copy_to_mem(mem.data(), mem.size());
  REQUIRE( n2>n1 );

  REQUIRE_THROWS(q.copy_from_mem(mem.data(),n1));

  q.copy_from_mem(mem.data(),n2);
  REQUIRE( q.data.header.n == p.data.header.n );
}

TEST_CASE( "file io, embedded1", "[io_tests]" ) {
  std::array<std::byte, 10000> mem;
  mdsd::Struct<big_example::MultiMessage> p;
  p.data.header.id = big_example::TypeSelector::POLY;
  p.adjust_array_sizes_and_variants();
  std::get<big_example::Polygon>(p.data.payload).n = 4;
  p.adjust_array_sizes_and_variants();
  p.data.code(44);
  REQUIRE( p.data.code() == 44);
  p.data.code(-33);
  REQUIRE( p.data.code() == -33);
  std::cout << "-----IO-----------\n";
  print(p.data,std::cout);
  std::cout << "-----IO-----------\n";
}

TEST_CASE( "file io, embedded2", "[io_tests]" ) {
  std::array<std::byte, 10000> mem;
  mdsd::Struct<big_example::MultiMessage> p;
  p.data.header.id = big_example::TypeSelector::POLY;
  p.adjust_array_sizes_and_variants();
  std::get<big_example::Polygon>(p.data.payload).n = 4;
  p.adjust_array_sizes_and_variants();
  p.data.code(44);
  REQUIRE( p.data.code() == 44);
  p.data.code(-33);
  REQUIRE( p.data.code() == -33);
  std::cout << "-----IO-----------\n";
  print(p.data,std::cout);
  std::cout << "-----IO-----------\n";
}

TEST_CASE( "file_io_AllInOne_default", "[io_tests]" ) {
  std::vector<std::byte> mem;
  std::ifstream f("tests/io_tests/AllInOne_default.bin", std::ios::binary);
  REQUIRE(f);
  while(f) {
    char c;
    f.read(c,1);
    if (f) mem.push_back(static_cast<std::byte>(c));
  }
  big_example::AllInOne obj;
  mdsd::copy_from_mem(mem.data(), mem.size(), obj);
  std::cout << "-----IO AllInOne_default.bin -----------\n";
  print(obj,std::cout);
  std::cout << "-----IO AllInOne_default.bin-----------\n";
}
