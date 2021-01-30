#ifndef MDSD_ITEM_VIRTUAL_ATTRIBUTE_SUPPORT
#define MDSD_ITEM_VIRTUAL_ATTRIBUTE_SUPPORT

#include "mdsd/item/basic_visitors.h"
#include <memory>
#include <string_view>


namespace mdsd {

struct AttributeBase {
  virtual ~AttributeBase() {}
  virtual std::string get_name() const=0;
  virtual std::string to_string() const=0;
  virtual void from_string(const std::string &text)=0;
  virtual bool is_array()=0;
  virtual bool is_struct()=0;
  virtual bool is_variant()=0;
  virtual size_t get_dim()=0;
  virtual std::unique_ptr<AttributeBase> get_attribute_in_struct(std::string_view name)=0;
  virtual std::unique_ptr<AttributeBase> get_attribute_in_struct(size_t idx, std::string_view name)=0;
};

template<class STRUCT>
std::unique_ptr<AttributeBase> get_attribute(STRUCT &s, std::string_view path);

template<class META>
struct AttributeWrapper : AttributeBase {
  typename META::STRUCT& s;
  AttributeWrapper(typename META::STRUCT &__s) : s(__s) {}
  AttributeWrapper(const AttributeWrapper&) = default;
  AttributeWrapper& operator=(const AttributeWrapper&) = default;
  std::string get_name() const override { return META::__name(); }
  std::string to_string() const override { return mdsd::to_string_with_meta<META>(s); }
  void from_string(const std::string &text) override { mdsd::from_string_with_meta<META>(text, s); }
  bool is_array() override { return META::__is_array; }
  bool is_struct() override { return META::__is_struct || META::__is_variant; }
  bool is_variant() override { return META::__is_variant; }
  size_t get_dim() override { 
    if constexpr (META::__is_array) 
      return META::__get_dim(s);
    else
      throw std::runtime_error("get_dim called for non-array attribute");
  }
  std::unique_ptr<AttributeBase> get_attribute_in_struct(std::string_view name) override { 
    if constexpr (!META::__is_array && META::__is_struct) 
      return get_attribute(META::__get_ref(s), name);
    else if constexpr (META::__is_variant) 
      throw std::runtime_error("TODO");
    else
      throw std::runtime_error("get_attribute_in_struct(name) called for array attribute or non-struct");
  }
  std::unique_ptr<AttributeBase> get_attribute_in_struct(size_t idx, std::string_view name) override { 
    if constexpr (META::__is_array && META::__is_struct) 
      return get_attribute(META::__get_ref(s)[idx], name); 
    else
      throw std::runtime_error("get_attribute_in_struct(idx, name) called for non-array or  non-struct  attribute");
  }

#ifndef SWIG
  auto& get_ref() { return META::__get_ref(s); }
  const auto& get_ref() const { return META::__get_ref(s); }
#endif
};

template<class STRUCT>
struct CreateAttributeWrapperVisitor {
  STRUCT &s;
  std::unique_ptr<AttributeBase> result = {};
  CreateAttributeWrapperVisitor(STRUCT&_s) : s(_s) {}
  template<class META> void visit(std::string_view &name) {
    if (std::string_view(META::__name()) == name) {
      result = std::make_unique<AttributeWrapper<META>>(s);
    }
  }
};

template<class STRUCT>
std::unique_ptr<AttributeBase> get_attribute(STRUCT &s, std::string_view path) {
    CreateAttributeWrapperVisitor v{s};
    STRUCT::META::template __accept_varargs<STRUCT>(v, path);
    if (v.result==nullptr) {
      throw std::runtime_error(std::string(path)+" not found.");
    }
    return std::move(v.result);
}

}

#endif
