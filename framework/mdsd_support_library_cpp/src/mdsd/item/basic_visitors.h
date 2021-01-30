#ifndef MDSD_ITEM_BASIC_VISIORS_H
#define MDSD_ITEM_BASIC_VISIORS_H
#ifndef SWIG

#include "mdsd/item/misc.h"

namespace mdsd {
inline namespace item {
    
/** The basic modifying visitor */
template<class V>
struct InitVisitor {
    V& v;
    InitVisitor(V &&_v) :v(_v){}
    InitVisitor(V &_v) :v(_v){}
    template<class META, class S> void visit(S& s) {
        decltype(META::__get_ref(s)) x = META::__get_ref(s);
        if constexpr (META::__is_scalar) {
            if constexpr (META::__is_variant) {
                META::__init_variant_type_if_type_is_not_matching(s);
                META::__call_function_on_concrete_variant_type(s, [&v=v](auto &a){
                    v.template visit_item_scalar<META>(a);
                });
            }
            else if constexpr (!META::__is_struct) {
                v.template visit_scalar<META>(x);
            }
            else {
                v.template visit_item_scalar<META>(x);
            }
        }
        else if constexpr (META::__is_array) {
            if constexpr (META::__is_dynamic_array) {
                if (x.size()!=META::__get_dim(s)) {
                    x.resize(META::__get_dim(s));
                }
            }
            if constexpr (META::__has_char_content) {
                v.template visit_string<META>(x);
            }
            else if constexpr (!META::__is_struct) {
                v.template visit_array<META>(x);
            }
            else {
                v.template visit_item_array<META>(x);
            }
        }
        else {
            throw std::runtime_error(get_message_with_meta_info<META>("unexpected meta information"));
        }
    }
};

/** The basic non-modifying visitor */
template<class V>
struct ConstVisitor {
    V& v;
    ConstVisitor(V &&_v) :v(_v){}
    ConstVisitor(V &_v) :v(_v){}
    template<class META, class S> void visit(const S&s) {
        decltype(META::__get_ref(s)) x = META::__get_ref(s);
        if constexpr (META::__is_scalar) {
            if constexpr (META::__is_variant) {
                META::__call_function_on_concrete_variant_type(s, [&v=v](const auto &a){
                    v.template visit_item_scalar<META>(a);
                });
            }
            else if constexpr (!META::__is_struct) {
                v.template visit_scalar<META>(x);
            }
            else {
                v.template visit_item_scalar<META>(x);
            }
        }
        else if constexpr (META::__is_array) {
            if constexpr (META::__is_dynamic_array) {
                if (x.size()!=META::__get_dim(s)) {
                    throw std::runtime_error(get_message_with_meta_info<META>("size does not match, is=",x.size()," should be=",META::__get_dim(s)," (hint: call adjust_array_sizes_and_variants)"));
                }
            }
            if constexpr (META::__has_char_content) {
                v.template visit_string<META>(x);
            }
            else if constexpr (!META::__is_struct) {
                v.template visit_array<META>(x);
            }
            else {
                v.template visit_item_array<META>(x);
            }
        }
        else {
            throw std::runtime_error(get_message_with_meta_info<META>("unexpected meta information"));
        }
    }
};

/** The basic non-modifying and non-checking visitor
 * TODO: untested!
 * can be used to make raw action on struct types, one single 
 * structs (like the InitVisitor or ConstVisitor) or even on
 * multiple structs (e.g. to compare or copy). */
template<class V>
struct BasicVisitor {
    V& v;
    BasicVisitor(V &&_v) :v(_v){}
    BasicVisitor(V &_v) :v(_v){}
    template<class META, class ...S> void visit(S&  ...s) {
        if constexpr (META::__is_scalar) {
            if constexpr (META::__is_variant) {
                v.template visit_variant<META>(s...);
            }
            else if constexpr (!META::__is_struct) {
                v.template visit_scalar<META>(s...);
            }
            else {
                v.template visit_item_scalar<META>(s...);
            }
        }
        else if constexpr (META::__is_array) {
            if constexpr (META::__has_char_content) {
                v.template visit_string<META>(s...);
            }
            else if constexpr (!META::__is_struct) {
                v.template visit_array<META>(s...);
            }
            else {
                v.template visit_item_array<META>(s...);
            }
        }
        else {
            throw std::runtime_error(get_message_with_meta_info<META>("unexpected meta information"));
        }
    }
};

}}
#endif
#endif