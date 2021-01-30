#ifndef MDSD_ITEM_INIT_DEFAULT_VALUES_H
#define MDSD_ITEM_INIT_DEFAULT_VALUES_H
#ifndef SWIG

#include "mdsd/item/basic_visitors.h"

namespace mdsd {
inline namespace item {

struct InitDefaultValuesVisitor {
  template<class META, class T> void visit_scalar(T& x) {
    if constexpr (META::__has_defaultValue) {
      x = META::defaultValue();
    }
    else if constexpr (META::__has_char_content) {
      if constexpr (META::__has_defaultStringValue) {
        x = META::defaultStringValue()[0];
      }
    }
  }
  template<class META, class T>
  void visit_item_scalar(T& x) {
      accept(InitVisitor{*this}, x);
  }
  template<class META, class T> void visit_array(T& x) {
    if constexpr (META::__has_defaultValue) {
      std::fill(x.begin(), x.end(), META::defaultValue());
    }
  }
  template<class META, class T> void visit_string(T& str) {
    if constexpr (META::__has_defaultStringValue) {
      str = std::string(META::defaultStringValue());
    }
    else {
      visit_array<META>(str.container);
    }
  }
  template<class META, class T>
  void visit_item_array(T& x) {
    for (size_t i=0;i<x.size();i++) {
      accept(InitVisitor{*this}, x[i]);
    }
  }
};
template<class T>
void init_default_values(T& s) {
    InitDefaultValuesVisitor iv{};
    accept(InitVisitor{iv}, s);
}

}}

#endif
#endif