from item_lang.common import (get_referenced_elements_of_constants,
                              obj_is_newer_than_file)
from item_codegen_cpp.common import *
from os.path import exists


def generate_cpp_for_constants(constants_obj, output_file, overwrite):
    if not exists(output_file) or (overwrite and obj_is_newer_than_file(constants_obj, output_file)):
        with open(output_file, "w") as f:
            f.write("#ifndef __{}_{}_H\n".format("_".join(get_package_names_of_obj(constants_obj)), constants_obj.name.upper()))
            f.write("#define __{}_{}_H\n".format("_".join(get_package_names_of_obj(constants_obj)), constants_obj.name.upper()))
            f.write("// ACTIVATE FOR SWIG\n")
            f.write("#include <cstdint>\n")
            f.write("\n")

            for r in get_referenced_elements_of_constants(constants_obj):
                f.write('#include "{}"\n'.format(output_filename(None, r)))
            f.write("\n")

            generate_cpp_constants(f, constants_obj)

            f.write("#endif // __{}_{}_H\n".format("_".join(get_package_names_of_obj(constants_obj)), constants_obj.name.upper()))


def generate_cpp_constants(f, cs):
    f.write(get_open_namespace_for_obj(cs))
    f.write("struct {} {{\n".format(cs.name))
    for c in cs.constant_entries:
        f.write("  static constexpr {} {} = {};\n".format(fqn(c.type), c.name, c.value.render_formula()))
    f.write("}}; //{}\n\n".format(cs.name))
    f.write("};\n")
