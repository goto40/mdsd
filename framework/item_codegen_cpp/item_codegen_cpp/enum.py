from item_lang.common import get_referenced_elements_of_enum, obj_is_newer_than_file
from item_codegen_cpp.common import (
    get_open_namespace_for_obj,
    get_package_names_of_obj,
    output_filename,
    fqn,
)
from os.path import exists


def generate_cpp_enum(f, e):
    """
    :param f: outut file obj
    :param e: enum obj
    """
    f.write(get_open_namespace_for_obj(e))
    f.write("enum class {} : {} {{\n".format(e.name, fqn(e.type)))
    for ee in e.enum_entries:
        comma = "" if ee == e.enum_entries[-1] else ","
        f.write("  {} = {}{}\n".format(ee.name, ee.value.render_formula(), comma))
    f.write("};\n")

    f.write(f"std::ostream& operator<<(std::ostream& o, const {e.name}& v) {{\n")
    f.write("  switch(v) {\n")
    for ee in e.enum_entries:
        f.write(f'    case {e.name}::{ee.name}: o << "{ee.name}"; break;\n')
    f.write('    default: o << "???";\n')
    f.write("  }\n")
    f.write("  return o;\n")
    f.write("}\n")

    f.write("} // close namespace\n")


def generate_cpp_for_enum(enum_obj, output_file, overwrite):
    if not exists(output_file) or (
        overwrite and obj_is_newer_than_file(enum_obj, output_file)
    ):
        with open(output_file, "w") as f:
            f.write(
                "#ifndef __{}_{}_H\n".format(
                    "_".join(get_package_names_of_obj(enum_obj)), enum_obj.name.upper()
                )
            )
            f.write(
                "#define __{}_{}_H\n".format(
                    "_".join(get_package_names_of_obj(enum_obj)), enum_obj.name.upper()
                )
            )
            f.write("// ACTIVATE FOR SWIG\n")
            f.write("#include <cstdint>\n")
            f.write("#include <iostream>\n")
            f.write("\n")

            for r in get_referenced_elements_of_enum(enum_obj):
                f.write('#include "{}"\n'.format(output_filename(None, r)))
            f.write("\n")

            generate_cpp_enum(f, enum_obj)

            f.write(
                "#endif // __{}_{}_H\n".format(
                    "_".join(get_package_names_of_obj(enum_obj)), enum_obj.name.upper()
                )
            )
