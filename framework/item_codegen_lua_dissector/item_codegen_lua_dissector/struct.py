import textx
from textx import get_metamodel
from item_lang.properties import (
    get_all_possible_properties,
    has_property,
    get_fixpoint_LSB_value,
    get_fixpoint_offset_value,
    has_fixpoint,
)  # TODO: why is the offset value function not used?
from item_lang.common import (
    get_referenced_elements_of_struct,
    get_start_end_bit,
    get_bits,
    get_container,
    obj_is_newer_than_file,
)
from item_lang.attributes import is_dynamic
from item_codegen_lua_dissector.common import (
    get_package_names_of_obj,
    output_filename,
    get_variant_types,
    get_lua_return_type,
    fqn,
    tf,
    get_open_namespace_for_obj,
    define_swig_array,
    define_swig_variant_access,
    define_swig_vector,
    get_property_type,
    get_property_constexpr,
    get_signed_or_unsigned,
)
from os.path import exists


def generate_lua_for_struct(struct_obj, output_file, overwrite):
    if not exists(output_file) or (
        overwrite and obj_is_newer_than_file(struct_obj, output_file)
    ):
        with open(output_file, "w") as f:
            f.write(
                "#ifndef __{}_{}_H\n".format(
                    "_".join(get_package_names_of_obj(struct_obj)),
                    struct_obj.name.upper(),
                )
            )
            f.write(
                "#define __{}_{}_H\n".format(
                    "_".join(get_package_names_of_obj(struct_obj)),
                    struct_obj.name.upper(),
                )
            )
            f.write("// ACTIVATE FOR SWIG\n")
            f.write("#include <cstdint>\n")
            f.write("#include <vector>\n")
            f.write("#include <array>\n")
            f.write("#include <variant>\n")
            f.write("#include <memory>\n")
            f.write("#include <stdexcept>\n")
            f.write("#include <type_traits>\n")
            f.write("\n")
            f.write('#include "mdsd/item_support.h"\n')
            f.write('#include "mdsd/virtual_struct.h"\n')
            f.write('#include "mdsd/item/init_default_values.h"\n')
            f.write("\n")

            for r in get_referenced_elements_of_struct(struct_obj):
                f.write('#include "{}"\n'.format(output_filename(None, r)))
            f.write("\n")

            generate_lua_struct(f, struct_obj)

            f.write(
                "#endif // __{}_{}_H\n".format(
                    "_".join(get_package_names_of_obj(struct_obj)),
                    struct_obj.name.upper(),
                )
            )


def _extra_init_required(i):
    return not is_dynamic(i)


def _get_ctor_param_type(a):
    mm = get_metamodel(a)
    if a.is_embedded():
        if textx.textx_isinstance(a, mm["ScalarAttribute"]):
            return get_lua_return_type(a.type)
        elif textx.textx_isinstance(a, mm["ArrayAttribute"]):
            return f"std::array<{get_lua_return_type(a.type)},{a.compute_formula()}>"
    if textx.textx_isinstance(a, mm["ScalarAttribute"]):
        return fqn(a.type)
    elif textx.textx_isinstance(a, mm["ArrayAttribute"]):
        if a.has_fixed_size():
            return f"std::array<{fqn(a.type)},{a.compute_formula()}>"
        else:
            return f"std::vector<{fqn(a.type)}>"
    elif textx.textx_isinstance(a, mm["VariantAttribute"]):
        return f"std::variant<{get_variant_types(a)}>"
    else:
        raise Exception("unexpected type")


def _get_ctor_params(i):
    res = ""
    comma = ""
    for a in i.attributes:
        if not a.is_container():
            res += comma + f"const {_get_ctor_param_type(a)} &_p_{a.name}"
            comma = ","
    return res


def _get_ctor_body(i):
    res = ""
    for a in i.attributes:
        if a.is_embedded():
            if a.is_array():
                res += f"for(size_t __idx=0;__idx<_p_{a.name}.size();__idx++) "\
                       f"{{ {a.name}(__idx, _p_{a.name}[__idx]); }} "
            else:
                res += f"{a.name}(_p_{a.name}); "
        elif not a.is_container():
            res += f"{a.name} = _p_{a.name}; "
    return res


def generate_lua_struct(f, i):
    """
    :param f: output file obj
    :param i: item to be generated (the struct)
    """
    mm = textx.get_metamodel(i)
    f.write("//---------------------------\n")
    f.write("#ifdef SWIG\n")
    f.write("%shared_ptr({});\n".format(fqn(i)))
    f.write(
        "%template(MDSD_StructFunctions_{}) mdsd::StructFunctions<{}>;\n".format(
            i.name, fqn(i)
        )
    )
    f.write("%template(MDSD_Struct_{}) mdsd::Struct<{}>;\n".format(i.name, fqn(i)))
    f.write(
        "%template(MDSD_StructWrapper_{}) mdsd::StructWrapper<{}>;\n".format(
            i.name, fqn(i)
        )
    )
    for a in i.attributes:
        if textx.textx_isinstance(a, mm["ArrayAttribute"]):
            if a.has_fixed_size():
                f.write(define_swig_array(a.type, a.compute_formula(), mm))
            else:
                f.write(define_swig_vector(a.type, mm))
    f.write("#endif\n")
    f.write("//---------------------------\n")
    f.write(get_open_namespace_for_obj(i))
    f.write("struct {} {{\n".format(i.name))

    for c in i.constant_entries:
        f.write(
            "  static constexpr {} {} = {};\n".format(
                fqn(c.type), c.name, c.value.render_formula()
            )
        )

    for a in i.attributes:
        if a.is_embedded():
            value_type = get_lua_return_type(a.type)
            if textx.textx_isinstance(a, mm["ScalarAttribute"]):
                f.write("  inline {} {}() const;\n".format(value_type, a.name))
            else:
                f.write(
                    "  inline {} {}(size_t idx) const;\n".format(value_type, a.name)
                )

            if textx.textx_isinstance(a, mm["ScalarAttribute"]):
                f.write("  inline void {}({} val);\n".format(a.name, value_type))
            else:
                f.write(
                    "  inline void {}(size_t idx, {} val);\n".format(a.name, value_type)
                )
            continue

        if textx.textx_isinstance(a, mm["ScalarAttribute"]):
            f.write("  {} {} = {{}};\n".format(fqn(a.type), a.name))
        elif textx.textx_isinstance(a, mm["ArrayAttribute"]):
            if a.has_fixed_size():
                f.write(
                    "  std::array<{},{}> {} = {{}};\n".format(
                        fqn(a.type), a.compute_formula(), a.name
                    )
                )
            else:
                f.write("  std::vector<{}> {} = {{}};\n".format(fqn(a.type), a.name))
        elif textx.textx_isinstance(a, mm["VariantAttribute"]):
            f.write(
                "  std::variant<{}> {} = {{}};\n".format(get_variant_types(a), a.name)
            )
        else:
            raise Exception("unexpected type")
    f.write(
        "  mdsd::StructWrapper<{0}> _GET_WRAPPER() {{ return mdsd::StructWrapper<{0}>{{this}}; }}\n".format(
            i.name
        )
    )
    f.write("\n#ifndef SWIG\n")
    f.write("  struct META {\n")

    # ----------------------------------------
    f.write(
        "    template<class STRUCT,class VISITOR, class ...T> // enable accept for this struct: \n"
    )
    f.write("    static void __accept_varargs(VISITOR &&v, T&... s) {\n")
    for a in i.attributes:
        f.write("      v.template visit<{}::META::{}>(s...);\n".format(i.name, a.name))
    f.write("    }\n")
    # ----------------------------------------

    f.write("    static constexpr const char* __name() ")
    f.write('{{ return "{}"; }}\n'.format(i.name))
    f.write(f"    static constexpr bool __is_dynamic = {tf(is_dynamic(i))};\n")
    for a in i.attributes:
        f.write("    struct {} {{\n".format(a.name))
        f.write("      using STRUCT={};\n".format(i.name))
        f.write("      static constexpr const char* __name() ")
        f.write('{{ return "{}"; }}\n'.format(a.name))
        if not textx.textx_isinstance(a, mm["VariantAttribute"]):
            f.write(f"      using __type = {fqn(a.type)};")
        f.write(f"      static constexpr bool __is_dynamic = {tf(is_dynamic(a))};\n")

        if hasattr(a, "type") and a.type.name == "char":
            f.write("      static constexpr bool __has_char_content = true;\n")
        else:
            f.write("      static constexpr bool __has_char_content = false;\n")

        if a.if_attr is None:
            f.write("      static constexpr bool __has_if_restriction = false;\n")
            f.write(
                "      static constexpr bool __if_restriction(const STRUCT &) { return true; }\n\n"
            )
        else:
            f.write("      static constexpr bool __has_if_restriction = true;\n")
            f.write(
                "      static constexpr bool __if_restriction(const STRUCT &s) {{ return {}; }}\n\n".format(
                    a.if_attr.predicate.render_formula(prefix="s.")
                )
            )

        if not (a.is_embedded()):
            if (
                textx.textx_isinstance(a, mm["ArrayAttribute"])
                and a.type.name == "char"
            ):
                f.write(
                    "      static constexpr auto __get_ref(STRUCT &s) {{ return mdsd::String(s.{}); }}\n".format(
                        a.name
                    )
                )
                f.write(
                    "      static constexpr const auto __get_ref(const STRUCT &s)"
                    " {{ return mdsd::String(s.{}); }}\n".format(a.name)
                )
            else:
                f.write(
                    "      static constexpr auto& __get_ref(STRUCT &s) {{ return s.{}; }}\n".format(
                        a.name
                    )
                )
                f.write(
                    "      static constexpr const auto& __get_ref(const STRUCT &s) {{ return s.{}; }}\n".format(
                        a.name
                    )
                )
        else:
            f.write(
                "      static constexpr auto& __get_ref_of_container(STRUCT &s) {{ return s.{}; }}\n".format(
                    get_container(a).name
                )
            )
            f.write(
                "      static constexpr const auto& __get_ref_of_container(const STRUCT &s)"
                " {{ return s.{}; }}\n".format(get_container(a).name)
            )
            if textx.textx_isinstance(a, mm["ArrayAttribute"]):
                f.write(
                    "      static constexpr auto __get_ref(STRUCT &s) {{ return mdsd::makeArrayRef<{}>(\n".format(
                        fqn(a.type)
                    )
                )
                f.write(
                    "          [&s](size_t idx){{ return s.{}(idx); }},\n".format(
                        a.name
                    )
                )
                f.write(
                    "          [&s](size_t idx, {} x){{ return s.{}(idx, x); }},\n".format(
                        fqn(a.type), a.name
                    )
                )
                f.write("          {}\n".format(a.compute_formula()))
                f.write("      ); }\n")
                f.write(
                    "      static constexpr auto __get_ref(const STRUCT &s)"
                    " {{ return mdsd::makeCArrayRef<{}>(\n".format(fqn(a.type))
                )
                f.write(
                    "          [&s](size_t idx){{ return s.{}(idx); }},\n".format(
                        a.name
                    )
                )
                f.write("          {}\n".format(a.compute_formula()))
                f.write("      ); }\n")
            else:
                f.write(
                    "      static constexpr auto __get_ref(STRUCT &s) {{ return mdsd::makeRef<{}>(\n".format(
                        fqn(a.type)
                    )
                )
                f.write("          [&s](){{ return s.{}(); }},\n".format(a.name))
                f.write(
                    "          [&s]({} x){{ return s.{}(x); }}\n".format(
                        fqn(a.type), a.name
                    )
                )
                f.write("      ); }\n")
                f.write(
                    "      static constexpr auto __get_ref(const STRUCT &s) {{ return mdsd::makeCRef<{}>(\n".format(
                        fqn(a.type)
                    )
                )
                f.write("          [&s](){{ return s.{}(); }}\n".format(a.name))
                f.write("      ); }\n")

        pdefs = get_all_possible_properties(a)
        pdefs = sorted(pdefs.keys())

        if "fixpointLsbValue" in pdefs:
            if has_fixpoint(a):
                f.write("      static constexpr bool __is_fixpoint = true;\n")
                f.write(
                    f"      static constexpr double __fixpointLsbValue = {get_fixpoint_LSB_value(a)};\n"
                )
                f.write(
                    f"      static constexpr double __fixpointOffsetValue = {get_fixpoint_offset_value(a)};\n"
                )
                f.write(
                    f"      template<class FLOAT=double> static constexpr {fqn(a.type)} __float2integral(FLOAT f) "
                    f"{{ return static_cast<{fqn(a.type)}>(std::llround((f-__fixpointOffsetValue)"
                    f"/__fixpointLsbValue)); }}\n"
                )
                f.write(
                    f"      template<class FLOAT=double> static constexpr FLOAT __integral2float({fqn(a.type)} i) "
                    f"{{ return static_cast<FLOAT>(i)*__fixpointLsbValue+__fixpointOffsetValue; }}\n"
                )
            else:
                f.write("      static constexpr bool __is_fixpoint = false;\n")
        else:
            f.write("      static constexpr bool __is_fixpoint = false;\n")

        for pname in pdefs:
            if has_property(a, pname):
                f.write("      static constexpr bool __has_{} = true;\n".format(pname))
                f.write(
                    "      static constexpr {} {}() {{ return {};}}\n".format(
                        get_lua_return_type(get_property_type(a, pname)),
                        pname,
                        get_property_constexpr(a, pname),
                    )
                )
            else:
                f.write("      static constexpr bool __has_{} = false;\n".format(pname))

        if textx.textx_isinstance(a, mm["VariantAttribute"]):
            f.write("      template<class S, class F> // S may also be const\n")
            f.write(
                "      static void __call_function_on_concrete_variant_type(S &s, F f) {\n"
            )

            f.write(
                "        switch(s.{}) {{\n".format(a.variant_selector.render_formula())
            )
            for m in a.mappings:
                f.write("          case {}: ".format(m.id))
                if textx.textx_isinstance(m.type, mm["RawType"]):
                    f.write(
                        "f(std::get<{}>(s.{})); break;\n".format(fqn(m.type), a.name)
                    )
                else:
                    f.write(
                        "f(std::get<{}>(s.{})); break;\n".format(fqn(m.type), a.name)
                    )
            f.write('          default: throw std::runtime_error("(unexpected id)");\n')
            f.write("        }\n")

            f.write("      }\n")

            f.write("      template<class S> // S may also be const\n")
            f.write(
                "      static void __init_variant_type_if_type_is_not_matching(S &s) {\n"
            )

            f.write(
                "        switch(s.{}) {{\n".format(a.variant_selector.render_formula())
            )
            for m in a.mappings:
                f.write("          case {}: ".format(m.id))
                f.write(
                    "if (not std::holds_alternative<{}>(s.{})) {{ s.{}={}{{}}; }} break;\n".format(
                        fqn(m.type),
                        a.name,
                        a.name,
                        fqn(m.type),
                    )
                )
            f.write('          default: throw std::runtime_error("unexpected id");\n')
            f.write("        }\n")

            f.write("      }\n")
            f.write("      static constexpr bool __is_scalar = true;\n")
            f.write("      static constexpr bool __is_variant = true;\n")
            f.write("      static constexpr bool __is_array = false;\n")
            f.write("      static constexpr bool __is_enumtype = false;\n")
            f.write("      static constexpr bool __is_rawtype = false;\n")
            f.write("      static constexpr bool __is_struct = true;\n")
            f.write(
                "      static constexpr bool __is_container = {};\n".format(
                    tf(a.is_container())
                )
            )
            f.write(
                "      static constexpr bool __is_embedded = {};\n".format(
                    tf(a.is_embedded())
                )
            )
        elif textx.textx_isinstance(a, mm["ScalarAttribute"]):
            f.write("      static constexpr bool __is_scalar = true;\n")
            f.write("      static constexpr bool __is_variant = false;\n")
            f.write("      static constexpr bool __is_array = false;\n")
            if textx.textx_isinstance(a.type, mm["Enum"]):
                f.write("      static constexpr bool __is_enumtype = true;\n")
            else:
                f.write("      static constexpr bool __is_enumtype = false;\n")
            if textx.textx_isinstance(a.type, mm["RawType"]):
                f.write("      static constexpr bool __is_rawtype = true;\n")
            else:
                f.write("      static constexpr bool __is_rawtype = false;\n")
            if textx.textx_isinstance(a.type, mm["Struct"]):
                f.write("      static constexpr bool __is_struct = true;\n")
            else:
                f.write("      static constexpr bool __is_struct = false;\n")
            f.write(
                "      static constexpr bool __is_container = {};\n".format(
                    tf(a.is_container())
                )
            )
            f.write(
                "      static constexpr bool __is_embedded = {};\n".format(
                    tf(a.is_embedded())
                )
            )
            if a.is_embedded():
                start_end_bit = get_start_end_bit(a)
                f.write(
                    "      static constexpr size_t __embedded_bits = {};\n".format(
                        get_bits(a.type)
                    )
                )
                f.write(
                    "      static constexpr size_t __embedded_start_bit = {};\n".format(
                        start_end_bit[0]
                    )
                )
                f.write(
                    "      static constexpr size_t __embedded_end_bit = {};\n".format(
                        start_end_bit[1]
                    )
                )
        elif textx.textx_isinstance(a, mm["ArrayAttribute"]):
            f.write("      static constexpr bool __is_scalar = false;\n")
            f.write("      static constexpr bool __is_variant = false;\n")
            f.write("      static constexpr bool __is_array = true;\n")
            if a.has_fixed_size():
                f.write("      static constexpr bool __is_dynamic_array = false;\n")
            else:
                f.write("      static constexpr bool __is_dynamic_array = true;\n")
            f.write(
                "      static constexpr size_t __get_dim([[maybe_unused]] const {} &{}) {{ return {};}}\n".format(
                    i.name,
                    "s" if not a.has_fixed_size() else "",
                    a.render_formula(prefix="s."),
                )
            )
            txt = f"      static constexpr size_t __get_dim([[maybe_unused]] const {i.name}"
            txt += f"&{'s' if not a.has_fixed_size() else ''}, size_t _idx) {{\n"
            txt += "            switch(_idx) {\n"
            for idx in range(len(a.dims)):
                txt += f"                  case {idx}: return {a.dims[idx].dim.render_formula(prefix='s.')};\n"
            txt += '                 default: throw std::runtime_error("unexpected dimension");\n'
            txt += "            }\n"
            txt += "      }\n"
            f.write(txt)
            if textx.textx_isinstance(a.type, mm["Enum"]):
                f.write("      static constexpr bool __is_enumtype = true;\n")
            else:
                f.write("      static constexpr bool __is_enumtype = false;\n")
            if textx.textx_isinstance(a.type, mm["RawType"]):
                f.write("      static constexpr bool __is_rawtype = true;\n")
            else:
                f.write("      static constexpr bool __is_rawtype = false;\n")
            if textx.textx_isinstance(a.type, mm["Struct"]):
                f.write("      static constexpr bool __is_struct = true;\n")
            else:
                f.write("      static constexpr bool __is_struct = false;\n")
            f.write(
                "      static constexpr bool __is_container = {};\n".format(
                    tf(a.is_container())
                )
            )
            f.write(
                "      static constexpr bool __is_embedded = {};\n".format(
                    tf(a.is_embedded())
                )
            )
            if a.is_embedded():
                start_end_bit = get_start_end_bit(a)
                f.write(
                    "      static constexpr size_t __embedded_bits = {};\n".format(
                        get_bits(a.type)
                    )
                )
                f.write(
                    "      static constexpr size_t __embedded_start_bit = {};\n".format(
                        start_end_bit[0]
                    )
                )
                f.write(
                    "      static constexpr size_t __embedded_end_bit = {};\n".format(
                        start_end_bit[1]
                    )
                )
        else:
            raise Exception("unexpected type constellation")

        f.write("    }}; // meta struct {}\n".format(a.name))
    f.write("  }; //struct META\n\n")

    f.write("#endif // #ifndef SWIG\n\n")

    f.write(f"  {i.name}() {{\n")
    f.write("    mdsd::init_default_values(*this);\n")
    f.write("  }\n")

    if _extra_init_required(i):
        f.write(f"  {i.name}({_get_ctor_params(i)}) {{\n")
        f.write(f"    {_get_ctor_body(i)};\n")
        f.write("  }\n")

    f.write(
        "  static std::shared_ptr<{}> item_create() {{ return std::make_shared<{}>(); }}\n".format(
            i.name, i.name
        )
    )
    f.write("}}; //struct {}\n".format(i.name))

    for a in i.attributes:
        if a.is_embedded():
            value_type = get_lua_return_type(a.type)
            signed_info = get_signed_or_unsigned(a.type)
            container_name = get_container(a).name

            if textx.textx_isinstance(a, mm["ScalarAttribute"]):
                f.write(
                    "  inline {} {}::{}() const {{\n".format(value_type, i.name, a.name)
                )
                f.write(
                    f"     return mdsd::read_{signed_info}_from_container<{value_type}>({container_name},"
                    f" META::{a.name}::__embedded_start_bit, META::{a.name}::__embedded_end_bit);\n"
                )
                f.write("  }\n")
            else:
                f.write(
                    "  inline {} {}::{}(size_t idx) const {{\n".format(
                        value_type, i.name, a.name
                    )
                )
                f.write(
                    f"     return mdsd::read_{signed_info}_from_container<{value_type}>({container_name},"
                    f" META::{a.name}::__embedded_start_bit-idx*META::{a.name}::__embedded_bits,"
                    f" META::{a.name}::__embedded_start_bit+1-(idx+1)*META::{a.name}::__embedded_bits);\n"
                )
                f.write("  }\n")

            if textx.textx_isinstance(a, mm["ScalarAttribute"]):
                f.write(
                    "  inline void {}::{}({} val) {{\n".format(
                        i.name, a.name, value_type
                    )
                )
                f.write(
                    f"     {container_name} = mdsd::write_to_container({container_name},"
                    f" META::{a.name}::__embedded_start_bit, META::{a.name}::__embedded_end_bit, val);\n"
                )
                f.write("  }\n")
            else:
                f.write(
                    "  inline void {}::{}(size_t idx, {} val) {{\n".format(
                        i.name, a.name, value_type
                    )
                )
                f.write(
                    f"     {container_name} = mdsd::write_to_container({container_name},"
                    f" META::{a.name}::__embedded_start_bit-idx*META::{a.name}::__embedded_bits,"
                    f" META::{a.name}::__embedded_start_bit+1-(idx+1)*META::{a.name}::__embedded_bits, val);\n"
                )
                f.write("  }\n")

    f.write("#ifndef SWIG\n")

    # ----------------------------------------
    f.write(
        "template<class VISITOR, class STRUCT> // enable accept for this struct: \n"
    )
    f.write(
        "std::enable_if_t<std::is_same_v<std::remove_const_t<STRUCT>,{}>> accept(VISITOR &&v, STRUCT &s) {{\n".format(
            i.name
        )
    )
    f.write("  STRUCT::META::template __accept_varargs<STRUCT>(v, s);\n")
    f.write("}\n")
    # ----------------------------------------

    f.write("#endif // #ifndef SWIG\n")

    f.write("} // close namespace\n")

    f.write("// swig helper:\n")
    for a in i.attributes:
        if textx.textx_isinstance(a, mm["VariantAttribute"]):
            f.write(define_swig_variant_access(i, a))
