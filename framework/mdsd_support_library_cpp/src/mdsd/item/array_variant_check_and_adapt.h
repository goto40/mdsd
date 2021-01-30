#ifndef MDSD_ITEM_ARRAY_VARIANT_CHECK_AND_ADAPT
#define MDSD_ITEM_ARRAY_VARIANT_CHECK_AND_ADAPT

#ifndef SWIG

namespace mdsd {
inline namespace item {

struct EmptyNonConstVisitor {
  template<class META, class T> void visit_scalar(T&) {}
  template<class META, class T>
  void visit_item_scalar(T& x) {
      accept(InitVisitor{*this}, x);
  }
  template<class META, class T> void visit_array(T&) {}
  template<class META, class T> void visit_string(T&) {}
  template<class META, class T>
  void visit_item_array(T& x) {
    for (size_t i=0;i<x.size();i++) {
      accept(InitVisitor{*this}, x[i]);
    }
  }
};
template<class T>
void adjust_array_sizes_and_variants(T& s) {
    EmptyNonConstVisitor iv{};
    accept(InitVisitor{iv}, s);
}

struct EmptyConstVisitor {
  template<class META, class T> void visit_scalar(const T&) {}
  template<class META, class T>
  void visit_item_scalar(const T& x) {
      accept(ConstVisitor{*this}, x);
  }
  template<class META, class T> void visit_array(const T&) {}
  template<class META, class T> void visit_string(const T&) {}
  template<class META, class T>
  void visit_item_array(const T& x) {
    for (size_t i=0;i<x.size();i++) {
      accept(ConstVisitor{*this}, x[i]);
    }
  }
};
template<class T>
void check_array_sizes_and_variants(const T& s) {
    EmptyConstVisitor iv{};
    accept(ConstVisitor{iv}, s);
}

}}
#endif
#endif
