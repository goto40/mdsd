#ifndef MDSD_VIRTUAL_STRUCT_H
#define MDSD_VIRTUAL_STRUCT_H
// ACTIVATE FOR SWIG

#include "mdsd/item_support.h"
#include "mdsd/item_io.h"
#include <iostream>

namespace mdsd {

struct StructBase {
  virtual ~StructBase() {}
  virtual void check_array_sizes_and_variants() const=0;
  virtual void adjust_array_sizes_and_variants()=0;
  virtual void print_to_stream(std::ostream& stream=std::cout) const =0;
  virtual size_t copy_to_mem(std::byte* mem, size_t n) const =0;
  virtual size_t copy_from_mem(const std::byte* mem, size_t n) =0;
  virtual size_t count_bytes() const=0;
};

template<class S>
struct StructFunctions : StructBase {
  virtual S& get_data()=0;
  virtual const S& get_data() const=0;
  void check_array_sizes_and_variants() const override { mdsd::check_array_sizes_and_variants(get_data()); }
  void adjust_array_sizes_and_variants() override { mdsd::adjust_array_sizes_and_variants(get_data()); }
  void print_to_stream(std::ostream& stream=std::cout) const override { mdsd::print(get_data(), stream); }
  size_t copy_to_mem(std::byte* mem, size_t n) const override { return mdsd::copy_to_mem(get_data(),mem,n); };
  size_t copy_from_mem(const std::byte* mem, size_t n) override { return mdsd::copy_from_mem(mem,n,get_data()); };
  virtual size_t count_bytes() const { return mdsd::count_bytes(get_data()); }
};

template<class S>
struct Struct : StructFunctions<S> {
  S data = {};
  virtual S& get_data() { return data; }
  virtual const S& get_data() const { return data; }
};
template<class S>
struct StructWrapper : StructFunctions<S> {
  S *data = nullptr;
  StructWrapper(S* __data) : data(__data) {}
  StructWrapper(const StructWrapper&) = default; // needed by SWIG code...
#ifndef SWIG
  StructWrapper& operator=(const StructWrapper&) = default;
#endif
  virtual S& get_data() { return *data; }
  virtual const S& get_data() const { return *data; }
};

}
#endif
