from textx import get_metamodel
from item_codegen_python.common import fqn, module_name, fp
from item_lang.common import obj_is_newer_than_file, get_referenced_elements_of_enum


def generate_py_for_enum(enum_obj, output_file):
    mm = get_metamodel(enum_obj)
    if obj_is_newer_than_file(enum_obj, output_file):
        with open(output_file, "w") as f:
            f.write(
                f"""# generated code
# for enum f{enum_obj.name}
import numpy as np
from enum import Enum
"""
            )
            for r in get_referenced_elements_of_enum(enum_obj):
                f.write("import {}\n".format(module_name(r)))
            f.write("\n")
            f.write(f"class {enum_obj.name}(Enum):\n")
            t = fqn(enum_obj.type)
            for ev in enum_obj.enum_entries:
                v = ev.value.render_formula(**fp(enum_obj))
                f.write(f"    {ev.name} = {t}({v})\n")
            f.write("    def __repr__(self):\n")
            f.write("        return self.name\n")
            f.write("    def __str__(self):\n")
            f.write("        return self.name\n")
