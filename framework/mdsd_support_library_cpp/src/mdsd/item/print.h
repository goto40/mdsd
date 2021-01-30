#ifndef MDSD_ITEM_PRINT_H
#define MDSD_ITEM_PRINT_H

#include "mdsd/item/basic_visitors.h"
#include <iostream>
#include <sstream>
#include <iomanip>
#ifndef SWIG

namespace mdsd {
inline namespace item {

template<class Item>
void print(const Item &i, std::ostream& stream=std::cout, size_t spaces=0);

namespace details {
  template<class META, class T>
  void print_to(std::ostream& o, const T &x) {
    o << x;
  }
  template<class META, class T>
  void __print_to(std::ostream& o, const T &x) {
    if constexpr (META::__has_char_content) {
      o << '\'' << x << '\'';
    }
    else {
      o << static_cast<int>(x);
    }
  }
  template<class META>
  void print_to(std::ostream& o, const uint8_t &x) { return __print_to<META,uint8_t>(o,x); }
  template<class META>
  void print_to(std::ostream& o, const int8_t &x) { return __print_to<META,int8_t>(o,x); }
  template<class META>
  void print_to(std::ostream& o, const char &x) { return __print_to<META,char>(o,x); }
}

struct PrintVisitor {
  std::ostream& stream;
  size_t spaces=0;
  bool suppress_first_name=false;
  template<class META, class T>
  void visit_scalar(T& x) {
    static_assert(!META::__is_struct);
    if (!suppress_first_name) stream << std::string(spaces, ' ') << META::__name() << " = ";
    else suppress_first_name = false;
    details::print_to<META>(stream, x);
    stream << "\n";
  }
  template<class META, class T>
  void visit_item_scalar(T& x) {
    if (!suppress_first_name) stream << std::string(spaces, ' ') << META::__name() << " =\n";
    else suppress_first_name = false;
    print(x,stream,spaces+2);
  }
  template<class META, class T>
  void visit_array(T& x) {
    if (!suppress_first_name) stream << std::string(spaces, ' ') << META::__name() << " = ";
    else suppress_first_name = false;
    stream << "[";
    for (size_t i=0;i<x.size();i++) {
      stream << " ";
      details::print_to<META>(stream, x[i]);
    }
    stream << " ]\n";
  }
  template<class META, class T>
  void visit_string(T& x) {
    if (!suppress_first_name) stream << std::string(spaces, ' ') << META::__name() << " = ";
    else suppress_first_name = false;
    details::print_to<META>(stream, x);
    stream << "\n";
  }
  template<class META, class T>
  void visit_item_array(T& x) {
    if (!suppress_first_name) stream << std::string(spaces, ' ') << META::__name() << " =\n";
    else suppress_first_name = false;
    stream << "[";
    for (size_t i=0;i<x.size();i++) {
      print(x[i],stream,spaces+2);
    }
    stream << std::string(spaces, ' ') << " ]\n";
  }
};

template<class Item>
void print(const Item &i, std::ostream& stream, size_t spaces) {
  stream << std::string(spaces, ' ')
    << std::remove_reference_t<Item>::META::__name()
    << " {\n";
  accept(ConstVisitor{PrintVisitor{stream, spaces+2}}, i);
  stream << std::string(spaces, ' ') << "}\n";
}

/** to_string_with_meta is a to_string that works with structs using a META info to determine the attribute */
template<class META>
std::string to_string_with_meta(const typename META::STRUCT &m, bool no_newlines=true) {
    std::ostringstream s;
    PrintVisitor iv{s,0,true};
    ConstVisitor<PrintVisitor> visitor{iv};
    visitor.template visit<META>(m);
    if (no_newlines) {
        std::string str;
        auto input = s.str();
        std::copy_if(input.begin(), input.end(), std::back_inserter(str),
        [last_was_space=false](char c) mutable {
            if (last_was_space && std::isspace(c)) return false;
            if (c=='\n') return false;
            last_was_space = std::isspace(c);
            return true;
        });
        return str;
    }
    else {
        return s.str();
    }
}

/** to_string that works with normal types AND structs */
template<class T>
std::enable_if_t<is_struct(static_cast<T*>(nullptr)), std::string> to_string(const T &v) {
    std::ostringstream s;
    print(v,s);
    return s.str();
}

/** to_string that works with normal types AND structs */
template<class T>
std::enable_if_t<!is_struct(static_cast<T*>(nullptr)), std::string> to_string(const T &v) {
    return std::to_string(v);
}

}}
#endif
#endif
