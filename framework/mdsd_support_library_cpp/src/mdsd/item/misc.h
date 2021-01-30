#ifndef MDSD_ITEM_MISC_H
#define MDSD_ITEM_MISC_H
#ifndef SWIG

#include <string>
#include <sstream>

namespace mdsd {
inline namespace item {

/** returns the parameters as string with the struct name and the attribute name before */
template<class META, class ...P>
std::string get_message_with_meta_info(P... p) {
    std::ostringstream s;
    s << META::STRUCT::META::__name() << "::" << META::__name()
      << ": ";
    (s << ... << p);
    return s.str();
}


/** constexpr function to detect if a type is a mdsd-'STRUCT' */
constexpr bool is_struct(...) { return false; }

/** constexpr function to detect if a type is a mdsd-'STRUCT' */
template<class T, class CHECK=typename T::META>
constexpr bool is_struct(T*) { return true; }


}}

#endif
#endif
