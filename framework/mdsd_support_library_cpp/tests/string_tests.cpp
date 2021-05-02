#include "catch.hpp"
#include "big_example/Info.h"
#include "mdsd/item_support.h"
#include <sstream>

using namespace mdsd;

TEST_CASE( "string ostream", "[string basic test]" ) {
    std::array<char,3> data;
    mdsd::String s{data};
    s.container[0]='A';
    s.container[1]='B';
    s.container[2]='C';
    {
        std::ostringstream o;
        o << s;
        REQUIRE(o.str() == std::string_view("\"ABC\""));
    }
    REQUIRE(s.size() == 3);
    REQUIRE(s == std::string_view("ABC"));
    s.container[1]='\0';
    {
        std::ostringstream o;
        o << s;
        REQUIRE(o.str() == "\"A\"");
    }
    REQUIRE(s.string_size() == 1);
    REQUIRE(s.max_size() == 3);
    REQUIRE(s.size() == 3);
    REQUIRE(s == std::string_view("A"));
}

TEST_CASE( "string istream", "[string basic test]" ) {
    std::array<char,3> data;
    mdsd::String s{data};
    std::istringstream i("> Hello A AB ABC DEFG");
    i >> s;
    REQUIRE(s == std::string_view(">"));
    i >> s;
    REQUIRE(s == std::string_view("Hel"));
    i >> s;
    REQUIRE(s == std::string_view("A"));
    i >> s;
    REQUIRE(s == std::string_view("AB"));
    i >> s;
    REQUIRE(s == std::string_view("ABC"));
    i >> s;
    REQUIRE(s == std::string_view("DEF"));
}

TEST_CASE( "Simple.pprint with string", "[string basic test]" ) {
  big_example::Info i;
  mdsd::init_default_values(i);
  {
    std::ostringstream stream;
    //mdsd::print(i, std::cout);
    mdsd::print(i, stream);
    REQUIRE(stream.str() == R"(Info {
  text1 = "This is text1"
  n = 16
  text2 = "This is text2 AB"
  c = 'P'
}
)");
  }
}

TEST_CASE( "Simple.scan with string", "[string basic test]" ) {
  big_example::Info i;
  mdsd::init_default_values(i);
  {
    std::istringstream stream(R"(Info {
      text1 = "Hallo"
      n = 2
      text2 = "Welt"
      c = '+'
    }
    )");
    mdsd::scan(i, stream);
    //mdsd::print(i, std::cout);
    REQUIRE(mdsd::String(i.text1).strv() == std::string("Hallo"));
    REQUIRE(mdsd::String(i.text2).strv() == std::string("We"));
    REQUIRE(i.c == '+');
    REQUIRE(i.n == 2);
  }
}
