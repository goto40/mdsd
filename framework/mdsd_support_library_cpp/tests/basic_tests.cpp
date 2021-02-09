#include "catch.hpp"
#include "items/Image.h"
#include "items/VariantExample.h"
#include "mdsd/item_support.h"

using namespace items;
using namespace mdsd;


TEST_CASE( "struct vector test", "[basic]" ) {
  Struct<Image> i;
  i.data.w = 11;
  i.data.h = 2;
  i.adjust_array_sizes_and_variants();
  CHECK_NOTHROW(i.check_array_sizes_and_variants());
  REQUIRE(i.data.pixel.size() == 22);
  i.data.pixel.resize(21);
  CHECK_THROWS(i.check_array_sizes_and_variants());
 
}

TEST_CASE( "struct variant test", "[basic]" ) {
  Struct<VariantExample> i;
  i.data.selector = 20;
  i.adjust_array_sizes_and_variants();
  CHECK_NOTHROW(i.check_array_sizes_and_variants());
  i.data.selector = 21;
  CHECK_THROWS(i.check_array_sizes_and_variants());
}
