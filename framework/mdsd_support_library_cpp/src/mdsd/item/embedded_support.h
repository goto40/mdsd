#ifndef MDSD_ITEM_EMBEDDED_SUPPORT_H
#define MDSD_ITEM_EMBEDDED_SUPPORT_H

#include <sstream>

namespace mdsd {
inline namespace item {

template<class T,class TGetter, class TSetter>
struct Ref {
  TGetter getter;
  TSetter setter;
  constexpr Ref(TGetter _getter, TSetter _setter) : getter(_getter), setter(_setter) {}
  operator T() const {
    return getter();
  }
  Ref& operator=(T x) const {
    setter(x);
    return *this;
  }
  friend std::ostream& operator<<(std::ostream &o, const Ref& x) {
    o << static_cast<T>(x);
    return o;
  }
  friend std::istream& operator>>(std::istream &i, Ref &x) {
    T v;
    i >> v;
    x = v;
    return i;
  }
};

template<class T,class TGetter>
struct CRef {
  TGetter getter;
  constexpr CRef(TGetter _getter) : getter(_getter) {}
  operator T() const {
    return getter();
  }
  friend std::ostream& operator<<(std::ostream &o, const CRef& x) {
    o << static_cast<T>(x);
    return o;
  }
};

template<class T,class TGetter, class TSetter>
constexpr auto makeRef(TGetter _getter, TSetter _setter) {
  return Ref<T,TGetter,TSetter>{_getter, _setter};
}
template<class T,class TGetter>
constexpr auto makeCRef(TGetter _getter) {
  return CRef<T,TGetter>{_getter};
}

template<class T,class TGetter, class TSetter>
struct ArrayRef {
  TGetter getter;
  TSetter setter;
  size_t sz;
  constexpr ArrayRef(TGetter _getter, TSetter _setter, size_t _sz) : getter(_getter), setter(_setter), sz(_sz) {}
  auto operator[](size_t idx) {
    return makeRef<T>(
      [&getter=getter,idx](){ return getter(idx); },
      [&setter=setter,idx](T x){ setter(idx,x); }
    );
  }
  size_t size() const { return sz; } 
};

template<class T,class TGetter>
struct CArrayRef {
  TGetter getter;
  size_t sz;
  constexpr CArrayRef(TGetter _getter, size_t _sz) : getter(_getter), sz(_sz) {}
  auto operator[](size_t idx) const {
    return makeCRef<T>(
      [&getter=getter,idx](){ return getter(idx); }
    );
  }
  size_t size() const { return sz; } 
};

template<class T,class TGetter, class TSetter>
constexpr auto makeArrayRef(TGetter _getter, TSetter _setter, size_t sz) {
  return ArrayRef<T,TGetter,TSetter>{_getter, _setter,sz};
}
template<class T,class TGetter>
constexpr auto makeCArrayRef(TGetter _getter, size_t sz) {
  return CArrayRef<T,TGetter>{_getter, sz};
}

template<class T>
constexpr T get_bit_mask(size_t beginpos, size_t endpos) {
  auto m1 = static_cast<T>(
    static_cast<T>(
      (static_cast<T>(1)<<(beginpos-endpos+1))-1
      )<<endpos
  );
  return m1;
}

template<class T>
constexpr T signed_fill_mask(size_t b) {
  static_assert( std::is_signed_v<T> );
  auto m1 = static_cast<T>(-1) & (~(
    (static_cast<T>(1)<<(b+1)) - 1
  ));
  return m1;
}

template<class T, bool S=std::is_enum_v<T>>
struct EnumUnderlyingType {
    using type = T;
};
template<class T>
struct EnumUnderlyingType<T,true> {
    using type = std::underlying_type_t<T>;
};

template<class T, class CT>
constexpr T read_unsigned_from_container(CT c, size_t start_bit, size_t end_bit) {
     CT __mask = mdsd::get_bit_mask<CT>(start_bit, end_bit);
     return static_cast<T>((c & __mask) >> end_bit);
}

template<class T, class CT>
constexpr T read_signed_from_container(CT c, size_t start_bit, size_t end_bit) {
     CT __mask = mdsd::get_bit_mask<CT>(start_bit, end_bit);
     using UT = typename EnumUnderlyingType<T>::type;
     auto x = static_cast<UT>((c & __mask) >> end_bit);
     if ((x & static_cast<UT>(1<<(start_bit-end_bit))) != static_cast<UT>(0)) {
       return static_cast<T>(x | signed_fill_mask<UT>(start_bit-end_bit));
     }
     else {
       return static_cast<T>(x);
     }
}

template<class T, class CT>
constexpr CT write_to_container(CT c, size_t start_bit, size_t end_bit, T val) {
    CT __mask = mdsd::get_bit_mask<CT>(start_bit, end_bit);
    return static_cast<CT>(
              static_cast<CT>(c & (~__mask)) 
              | static_cast<CT>(static_cast<CT>(static_cast<CT>(val)<<end_bit) & __mask)
          );
}


}}

#endif
