#ifndef MDSD_ITEM_VIRTUAL_ATTRIBUTE_SUPPORT
#define MDSD_ITEM_VIRTUAL_ATTRIBUTE_SUPPORT

#include <memory>
#include <string_view>


namespace mdsd {

struct AttributeBase {
  virtual ~AttributeBase() {}
  virtual std::string get_name() const=0;
  virtual std::string to_string() const=0;
  virtual void from_string(const std::string &text)=0;
};

template<class META>
struct AttributeWrapper : AttributeBase {
  typename META::STRUCT& s;
  AttributeWrapper(typename META::STRUCT &__s) : s(__s) {}
  AttributeWrapper(const AttributeWrapper&) = default;
  AttributeWrapper& operator=(const AttributeWrapper&) = default;
  std::string get_name() const override { return META::__name(); }
  std::string to_string() const override { return mdsd::to_string_with_meta<META>(s); }
  void from_string(const std::string &text) override { mdsd::from_string_with_meta<META>(text, s); }
#ifndef SWIG
  auto& get_ref() { return META::__get_ref(s); }
  const auto& get_ref() const { return META::__get_ref(s); }
#endif
};


struct CreateAttributeWrapperVisitor {
  template<class META, class T> void visit_scalar(const T&) {

  }
  template<class META, class T>
  void visit_item_scalar(const T& x) {
      accept(ConstVisitor{*this}, x);
  }
  template<class META, class T> void visit_array(const T&) {

  }
  template<class META, class T> void visit_string(const T&) {

  }
  template<class META, class T>
  void visit_item_array(const T& x) {
    for (size_t i=0;i<x.size();i++) {
      accept(ConstVisitor{*this}, x[i]);
    }
  }
};


template<class STRUCT>
std::unique_ptr<AttributeBase> createAttributeWrapper(STRUCT &s, std::string_view path) {
    CreateAttributeWrapperVisitor v{s};
    //accept(ConstVisitor{v});
    return nullptr;
}

}

#endif
