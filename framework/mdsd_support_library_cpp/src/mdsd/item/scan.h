#ifndef MDSD_ITEM_SCAN_H
#define MDSD_ITEM_SCAN_H
#ifndef SWIG

#include "mdsd/item/basic_visitors.h"
#include <iostream>
#include <sstream>
#include <iomanip>


namespace mdsd {
inline namespace item {
    
template<class Item>
void scan(Item &i, std::istream& stream);

namespace details {
  template<class META, class T>
  bool read_from(std::istream &i, T& x) {
    i >> x;
    return not i.fail();
  }
  template<class META, class T>
  bool __read_from(std::istream &i, T& x) {
    if (META::__has_char_content) {
      std::string value;
      i >> value;
      if (value.size()!=3 || value[0]!='\'' || value[2]!='\'') {
        return false;
      }
      else {
        x = static_cast<T>(value[1]);
      }
    }
    else {
      int v;
      i >> v;
      x = static_cast<T>(v);
      if (v<std::numeric_limits<T>::min() || v>std::numeric_limits<T>::max()) return false;
    }
    return not i.fail();
  }
  template<class META>
  bool read_from(std::istream &i, uint8_t& x) { return __read_from<META, uint8_t>(i,x); }
  template<class META>
  bool read_from(std::istream &i, int8_t& x) { return __read_from<META, int8_t>(i,x); }
  template<class META>
  bool read_from(std::istream &i, char& x) { return __read_from<META, char>(i,x); }
}

namespace details {
  template<class META>
  void __check_char(std::istream &stream, char c_search) {
    int c='?';
    while(stream && std::isspace(c=stream.get())) {}
    if (c!=c_search) throw std::runtime_error(std::string("expected '")+c_search+"' after "+META::__name()+", got '"+static_cast<char>(c)+"'.");
  }
  template<class META>
  void __check_name(std::istream &stream, char char_to_check_after_name='=') {
    std::string n;
    stream >> n;
    if (n!=META::__name()) throw std::runtime_error(std::string("expected ")+META::__name()+", got "+n);
    if (!stream) throw std::runtime_error(std::string("stream not ok reading name of ")+META::__name());
    __check_char<META>(stream, char_to_check_after_name);
  }
}

struct ScanVisitor {
  std::istream& stream;
  bool suppress_first_name_check = false;
  template<class META, class T>
  void visit_scalar(T& x) {
    if (!suppress_first_name_check) details::__check_name<META>(stream);
    else suppress_first_name_check = false;
    bool ok = details::read_from<META>(stream, x);
    if (!stream || !ok) throw std::runtime_error(std::string("stream not ok reading value of ")+META::__name());
  }
  template<class META, class T>
  void visit_item_scalar(T& x) {
    if (!suppress_first_name_check) details::__check_name<META>(stream);
    else suppress_first_name_check = false;
    scan(x,stream);
  }
  template<class META, class T>
  void visit_array(T& x) {
    if (!suppress_first_name_check) details::__check_name<META>(stream);
    else suppress_first_name_check = false;
    details::__check_char<META>(stream, '[');
    for (size_t i=0;i<x.size();i++) {
      bool ok = details::read_from<META>(stream, x[i]);
      if (!stream || !ok) throw std::runtime_error(std::string("stream not ok reading ")+std::to_string(i)+ "th value of "+META::__name());
    }
    details::__check_char<META>(stream, ']');
  }
  template<class META, class T>
  void visit_string(T& x) {
    if (!suppress_first_name_check) details::__check_name<META>(stream);
    else suppress_first_name_check = false;
    bool ok = details::read_from<META>(stream, x);
    if (!stream || !ok) throw std::runtime_error(std::string("stream not ok reading value of ")+META::__name());
  }
  template<class META, class T>
  void visit_item_array(T& x) {
    if (!suppress_first_name_check) details::__check_name<META>(stream);
    else suppress_first_name_check = false;
    details::__check_char<META>(stream, '[');
    for (size_t i=0;i<x.size();i++) {
      scan(x[i],stream);
    }
    details::__check_char<META>(stream, ']');
  }
};

template<class Item>
void scan(Item &i, std::istream& stream) {
  details::__check_name<typename std::remove_reference_t<Item>::META>(stream, '{');
  ScanVisitor iv{stream};
  accept(InitVisitor{iv}, i);
  details::__check_char<typename std::remove_reference_t<Item>::META>(stream, '}');
}

/** to_string_with_meta is a to_string that works with structs using a META info to determine the attribute */
template<class META>
void from_string_with_meta(const std::string &text, typename META::STRUCT &m) {
    std::istringstream s(text);
    ScanVisitor iv{s, true};
    InitVisitor visitor{iv};
    visitor.template visit<META>(m);
}

}}
#endif
#endif
