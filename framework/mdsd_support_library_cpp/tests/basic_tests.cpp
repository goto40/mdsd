#include "catch.hpp"
#include "items/Image.h"
#include "mdsd/item_support.h"

using namespace items;
using namespace mdsd;


TEST_CASE( "struct vector test", "[basic]" ) {
  Struct<Image> i;
  i.data.w = 11;
  i.data.h = 2;
  i.adjust_array_sizes_and_variants();
  REQUIRE(i.data.pixel.size() == 22);
}
