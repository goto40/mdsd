from textx import get_metamodel, get_children_of_type, textx_isinstance
from item_codegen_python.common import fqn, fp, module_name
from item_lang.common import (
    obj_is_newer_than_file,
    get_referenced_elements_of_constants,
)


def generate_py_for_constants(constants_obj, output_file):
    mm = get_metamodel(constants_obj)
    if obj_is_newer_than_file(constants_obj, output_file):
        with open(output_file, "w") as f:
            f.write(
                f"""# generated code
# for constants f{constants_obj.name}
import numpy as np
"""
            )
            for r in get_referenced_elements_of_constants(constants_obj):
                f.write("import {}\n".format(module_name(r)))
            f.write("\n")
            for c in constants_obj.constant_entries:
                t = fqn(c.type)
                v = c.value.render_formula(**fp(constants_obj))
                f.write(f"{c.name} = {t}({v})\n")
