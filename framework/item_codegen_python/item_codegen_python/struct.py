from textx import (get_metamodel, get_children_of_type,
                   textx_isinstance)
from item_codegen_python.common import (fqn, get_variant_types,
                                        get_variant_type_map,
                                        module_name, fp)
from item_lang.common import (obj_is_new_than_file,
                              get_referenced_elements_of_struct)


def generate_py_for_struct(struct_obj, output_file):
    mm = get_metamodel(struct_obj)
    if obj_is_new_than_file(struct_obj, output_file):
        with open(output_file, "w") as f:
            f.write("""# generated code
from dataclasses import dataclass
import numpy as np
import mdsd_support_library.item_support as support
from typing import Sequence, Union
""")
            for r in get_referenced_elements_of_struct(struct_obj):
                f.write('import {}\n'.format(module_name(r)))
            f.write("\n")
            items = get_children_of_type("Struct", struct_obj)
            for i in items:
                f.write("\n@dataclass(eq=False)\n")
                f.write("class {}:\n".format(i.name))
                for a in i.attributes:
                    if textx_isinstance(a, mm["ScalarAttribute"]):
                        if textx_isinstance(a.type, mm["RawType"]):
                            f.write("  {} : {}=0\n".format(a.name, fqn(a.type)))
                        else:
                            f.write("  {} : {}={}()\n".format(a.name, fqn(a.type), fqn(a.type)))
                    elif textx_isinstance(a, mm["ArrayAttribute"]):
                        if textx_isinstance(a.type, mm["RawType"]):
                            f.write(
                                "  {} : np.ndarray=None\n".format(
                                    a.name
                                )
                            )
                        else:
                            f.write(
                                "  {} : Sequence[{}]=None\n".format(
                                    a.name, fqn(a.type)
                                )
                            )
                    elif textx_isinstance(a, mm["VariantAttribute"]):
                        f.write(
                            "  {} : Union[{}]=None\n".format(
                                a.name, get_variant_types(a)
                            )
                        )
                    else:
                        raise Exception("unexpected type")
                f.write("\n  def __post_init__(self):\n")
                f.write("    support.adjust_array_sizes_and_variants(self)\n")
                f.write(r'''  def __setattr__(self, attribute, value):
        if not attribute in self._meta:
            raise Exception("Illegal field {} in {}".format(attribute,self.__class__.__name__))
        else:
            if value is None:
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_variant"]:
                if isinstance(value, self._meta[attribute]["get_type"]()):
                    self.__dict__[attribute] = value
                else:
                    raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
            elif self._meta[attribute]["is_scalar"]:
                if isinstance(value, self._meta[attribute]["get_type"]()):
                    self.__dict__[attribute] = value
                elif self._meta[attribute]["is_rawtype"]:
                    self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
                else:
                    raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
            else:
                self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())
    ''')

                f.write("\n  _meta = {\n")
                for a in i.attributes:
                    f.write('    "{}": {{ '.format(a.name))
                    f.write('"name":"{}",'.format(a.name))
                    if textx_isinstance(a, mm["VariantAttribute"]):
                        f.write('"get_type_for": lambda s: {}[s.{}], '.format(get_variant_type_map(a),a.variant_selector.render_formula(**fp(struct_obj))))
                        f.write('"is_scalar":True,')
                        f.write('"is_variant":True,')
                        f.write('"is_array":False,')
                        f.write('"is_rawtype":False,')
                        f.write('"is_struct":True,')
                        f.write('"get_type": lambda: ({}), '.format(get_variant_types(a)))
                    elif textx_isinstance(a, mm["ScalarAttribute"]):
                        f.write('"is_scalar":True,')
                        f.write('"is_variant":False,')
                        f.write('"is_array":False,')
                        if textx_isinstance(a.type, mm["RawType"]):
                            f.write('"is_rawtype":True,')
                            f.write('"is_struct":False,')
                        else:
                            f.write('"is_rawtype":False,')
                            f.write('"is_struct":True,')
                        f.write('"get_type": lambda: {}, '.format(fqn(a.type)))
                    elif textx_isinstance(a, mm["ArrayAttribute"]):
                        f.write('"is_scalar":False,')
                        f.write('"is_variant":False,')
                        f.write('"is_array":True,')
                        if a.has_fixed_size():
                            f.write('"is_dynamic_array":False,')
                        else:
                            f.write('"is_dynamic_array":True,')
                        f.write('"get_dim":lambda x:({}),'.format(a.render_formula(prefix="x.",**fp(struct_obj))))
                        f.write('"get_dim_nd":lambda x:({},),'.format(a.render_formula_comma_separated(prefix="x.", **fp(struct_obj))))
                        if textx_isinstance(a.type, mm["RawType"]):
                            f.write('"is_rawtype":True,')
                            f.write('"is_struct":False,')
                        else:
                            f.write('"is_rawtype":False,')
                            f.write('"is_struct":True,')
                        f.write('"get_type": lambda: {}, '.format(fqn(a.type)))
                    else:
                        raise Exception("unexpected type constellation")
                    f.write("},\n")
                f.write("  } # end of _meta\n")
