#ifndef MDSD_ITEM_IO_H
#define MDSD_ITEM_IO_H

#include "mdsd/item_support.h"
#include <algorithm>
#include <cstddef>
#include <iostream>

#ifndef SWIG

namespace mdsd {

struct CopyToMemVisitor {
  std::byte* const dest;
  const size_t n;
  size_t pos=0;
  template<class META, class T>
  void visit_scalar(const T& x) {
    if constexpr (!META::__is_embedded) {
      if (sizeof(T)+pos>n) {
        throw std::runtime_error("out of mem");
      }
      const std::byte* src = reinterpret_cast<const std::byte*>(&x);
      std::copy(src,src+sizeof(T),dest+pos);
      pos += sizeof(T);
    }
  }
  template<class META, class T>
  void visit_array(const T& x) {
    if constexpr (!META::__is_embedded) {
      if (sizeof(typename T::value_type)*x.size()+pos>n) {
        throw std::runtime_error("out of mem");
      }
      const std::byte* src = reinterpret_cast<const std::byte*>(x.data());
      std::copy(src,src+sizeof(typename T::value_type)*x.size(),dest+pos);
      pos += sizeof(typename T::value_type)*x.size();
    }
  }
  template<class META, class T>
  void visit_string(const T& x) {
    visit_array<META>(x.container);
  }
  template<class META, class T>
  void visit_item_scalar(const T& x) {
      size_t pos0 = pos;
      accept(ConstVisitor{*this}, x);
      if constexpr (META::__has_fixedSizeInBytes) {
        if (pos-pos0 > META::fixedSizeInBytes()) {
          throw std::runtime_error("unexpected struct size > fixedSizeInBytes.");
        }
        else if (pos-pos0 < META::fixedSizeInBytes()) {
          size_t fill_space = META::fixedSizeInBytes() - (pos-pos0);
          std::fill(dest+pos, dest+pos+fill_space, std::byte{0x0});
          pos += fill_space;
        }
      }
  }
  template<class META, class T>
  void visit_item_array(const T& x) {
    for (size_t i=0;i<x.size();i++) {
      size_t pos0 = pos;
      accept(ConstVisitor{*this}, x[i]);
      if constexpr (META::__has_fixedSizeInBytes) {
        if (pos-pos0 > META::fixedSizeInBytes()) {
          throw std::runtime_error("unexpected struct size > fixedSizeInBytes.");
        }
        else if (pos-pos0 < META::fixedSizeInBytes()) {
          size_t fill_space = META::fixedSizeInBytes() - (pos-pos0);
          std::fill(dest+pos, dest+pos+fill_space, std::byte{0x0});
          pos += fill_space;
        }
      }
    }
  }
};
template<class T>
size_t copy_to_mem(const T& s, std::byte* span_data, size_t span_size) {
    auto v = CopyToMemVisitor{ span_data, span_size };
    accept(ConstVisitor{v}, s);
    return v.pos;
}

struct CopyFromMemVisitor {
  const std::byte* const src;
  const size_t n;
  size_t pos=0;
  template<class META, class T>
  void visit_scalar(T& x) {
    if constexpr (!META::__is_embedded) {
      //std::cout << "visit_scalar " << META::__name() << "\n";
      if (sizeof(T)+pos>n) {
        throw std::runtime_error("out of mem");
      }
      std::byte* const dest = reinterpret_cast<std::byte*>(&x);
      std::copy(src+pos,src+pos+sizeof(T),dest);
      pos += sizeof(T);
    }
  }
  template<class META, class T>
  void visit_array(T& x) {
    if constexpr (!META::__is_embedded) {
      //std::cout << "visit_array " << META::__name() << "\n";
      if (sizeof(typename T::value_type)*x.size()+pos>n) {
        throw std::runtime_error("out of mem");
      }
      std::byte* const dest = reinterpret_cast<std::byte*>(x.data());
      std::copy(src+pos,src+pos+sizeof(typename T::value_type)*x.size(),dest);
      pos += sizeof(typename T::value_type)*x.size();
    }
  }
  template<class META, class T>
  void visit_string(T& x) {
    visit_array<META>(x.container);
  }
  template<class META, class T>
  void visit_item_scalar(T& x) {
      //std::cout << "visit_item_scalar " << META::__name() << "\n";
      size_t pos0 = pos;
      accept(InitVisitor{*this}, x);
      if constexpr (META::__has_fixedSizeInBytes) {
        if (pos-pos0 > META::fixedSizeInBytes()) {
          throw std::runtime_error("unexpected struct size > fixedSizeInBytes.");
        }
        else if (pos-pos0 < META::fixedSizeInBytes()) {
          pos += META::fixedSizeInBytes() - (pos-pos0);
        }
      }
  }
  template<class META, class T>
  void visit_item_array(T& x) {
    //std::cout << "visit_item_array " << META::__name() << "\n";
    for (size_t i=0;i<x.size();i++) {
      size_t pos0 = pos;
      accept(InitVisitor{*this}, x[i]);
      if constexpr (META::__has_fixedSizeInBytes) {
        if (pos-pos0 > META::fixedSizeInBytes()) {
          throw std::runtime_error("unexpected struct size > fixedSizeInBytes.");
        }
        else if (pos-pos0 < META::fixedSizeInBytes()) {
          pos += META::fixedSizeInBytes() - (pos-pos0);
        }
      }
    }
  }
};
template<class T>
size_t copy_from_mem(const std::byte* span_data, size_t span_size, T& s) {
    auto v = CopyFromMemVisitor{ span_data, span_size };
    accept(InitVisitor{v}, s);
    return v.pos;
}

struct ByteCountVisitor {
  size_t count=0;
  template<class META, class T>
  void visit_scalar(const T&) {
    if constexpr (META::__is_embedded) return;
    count += sizeof(typename META::__type);
  }
  template<class META, class T>
  void visit_array(const T& x) {
    if constexpr (META::__is_embedded) return;
    count += sizeof(typename META::__type)*x.size();
  }
  template<class META, class T>
  void visit_string(const T& x) {
    visit_array<META>(x.container);
  }
  template<class META, class T>
  void visit_item_scalar(const T& x) {
      size_t old_count=count;
      accept(ConstVisitor{*this}, x);
      if constexpr (META::__has_fixedSizeInBytes) {
        if (count-old_count > META::fixedSizeInBytes()) {
          throw std::runtime_error("unexpected struct size > fixedSizeInBytes.");
        }
        else if (count-old_count < META::fixedSizeInBytes()) {
          count += META::fixedSizeInBytes() - (count-old_count);
        }
      }
  }
  template<class META, class T>
  void visit_item_array(const T& x) {
    for (size_t i=0;i<x.size();i++) {
      size_t old_count=count;
      accept(ConstVisitor{*this}, x[i]);
      if constexpr (META::__has_fixedSizeInBytes) {
        if (count-old_count > META::fixedSizeInBytes()) {
          throw std::runtime_error("unexpected struct size > fixedSizeInBytes.");
        }
        else if (count-old_count < META::fixedSizeInBytes()) {
          count += META::fixedSizeInBytes() - (count-old_count);
        }
      }
    }
  }
};
template<class T>
size_t count_bytes(const T& s) {
    auto v = ByteCountVisitor{};
    accept(ConstVisitor{v}, s);
    return v.count;
}

}
#endif // SWIG
#endif
