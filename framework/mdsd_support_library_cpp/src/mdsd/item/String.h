#ifndef MDSD_ITEM_STRING_H
#define MDSD_ITEM_STRING_H
#ifndef SWIG

#include <iostream>
#include <iomanip>

namespace mdsd {
inline namespace item {

template<class C>
struct String {
  C &container;
  constexpr String(C &_container) : container(_container) {}

  String& operator=(const std::string &x) {
    size_t n = std::min(container.size(), x.size());
    std::copy(x.begin(), x.end(), container.data());
    if (n<container.size()) {
      container[n]='\0';
    }
    return *this;
  }

  constexpr operator std::string_view() const {
    return {container.data(), string_size()};
  }
  auto str() {
    return std::string(*this);
  }
  auto strv() {
    return std::string_view(*this);
  }

  friend std::ostream& operator<<(std::ostream& o, const String &s) {
    o << std::quoted(static_cast<std::string_view>(s));
    return o;
  }
  friend std::istream& operator>>(std::istream& i, String &s) {
    std::string x;
    i >> std::quoted(x);
    s = x;
    return i;
  }
  size_t constexpr string_size() const {
    auto it = std::find(container.data(), container.data()+container.size(), '\0');
    return it - container.data();
  }
  size_t constexpr max_size() const {
    return container.size();
  }
  size_t constexpr size() const {
    return max_size();
  }
  void resize(size_t n) { container.resize(n); }
};

}}

#endif
#endif
