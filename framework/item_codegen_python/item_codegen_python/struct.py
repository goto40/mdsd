from _tracemalloc import start

from textx import (get_metamodel, get_children_of_type,
                   textx_isinstance)
from item_codegen_python.common import (fqn, get_variant_types,
                                        get_variant_type_map,
                                        module_name, fp, tf)
from item_lang.common import (obj_is_new_than_file,
                              get_referenced_elements_of_struct,
                              get_container, get_start_end_bit)
import numpy as np  # used via "eval" (see below, get_mask...)


def generate_py_for_struct(struct_obj, output_file):
    mm = get_metamodel(struct_obj)
    if obj_is_new_than_file(struct_obj, output_file):
        with open(output_file, "w") as f:
            f.write("""# generated code
from dataclasses import dataclass
import numpy as np
import mdsd.item_support as support
from mdsd.common import get_embedded_from_uint, ArrayLike
from mdsd.common import set_embedded_in_uint
from mdsd.common import ArrayLike
from typing import Sequence, Union
""")
            for r in get_referenced_elements_of_struct(struct_obj):
                f.write('import {}\n'.format(module_name(r)))
            f.write("\n")
            i = struct_obj
            f.write("\n@dataclass(eq=False)\n")
            f.write("class {}:\n".format(i.name))
            for a in i.attributes:
                if a.is_embedded():
                    rawtype = a.type
                    if textx_isinstance(a.type, mm["Enum"]):
                        rawtype = a.type.type
                    if textx_isinstance(a, mm["ScalarAttribute"]):
                        # SCALAR EMBEDDED
                        # --------------------------------------------------------------
                        start_end_bit = get_start_end_bit(a)
                        c = get_container(a)
                        f.write(f"    @property\n")
                        f.write(f"    def {a.name}(self):\n")
                        f.write(f"        ret = get_embedded_from_uint({fqn(rawtype)}, self.{c.name},[{start_end_bit[0]},{start_end_bit[1]}])\n")
                        if textx_isinstance(a.type, mm["Enum"]):
                            f.write(f"        v = {fqn(a.type)}(v)\n")
                        f.write(f"        return ret\n")
                        f.write(f"\n")
                        f.write(f"    @{a.name}.setter\n")
                        f.write(f"    def {a.name}(self, v):\n")
                        if textx_isinstance(a.type, mm["Enum"]):
                            f.write(f"        v = v.value\n")
                        f.write(f"        assert isinstance(v, {fqn(rawtype)})\n")
                        f.write(f"        self.{c.name} = set_embedded_in_uint(v, self.{c.name},[{start_end_bit[0]},{start_end_bit[1]}])\n")
                        f.write(f"\n")
                        # --------------------------------------------------------------
                    elif textx_isinstance(a, mm["ArrayAttribute"]):
                        # ARRAY EMBEDDED
                        # --------------------------------------------------------------
                        start_end_bit = get_start_end_bit(a)
                        c = get_container(a)
                        f.write(f"    @property\n")
                        f.write(f"    def {a.name}(self):\n")
                        f.write(f"        def getter(idx):\n")
                        f.write(f"            ret = get_embedded_from_uint({fqn(rawtype)}, self.{c.name},[{start_end_bit[0]}-idx*{rawtype.bits},{start_end_bit[0]}+1-(idx+1)*{rawtype.bits}])\n")
                        if textx_isinstance(a.type, mm["Enum"]):
                            f.write(f"            ret = {fqn(a.type)}(ret)\n")
                        f.write(f"            return ret\n")
                        f.write(f"        def setter(idx, v):\n")
                        f.write(f"            assert isinstance(v, {fqn(a.type)})\n")
                        if textx_isinstance(a.type, mm["Enum"]):
                            f.write(f"            v = v.value\n")
                        f.write(f"            self.{c.name} = set_embedded_in_uint(v, self.{c.name},[{start_end_bit[0]}-idx*{rawtype.bits},{start_end_bit[0]}+1-(idx+1)*{rawtype.bits}])\n")
                        f.write(f"        return ArrayLike( getter=getter, setter=setter, mytype={fqn(rawtype)}, shape={i.name}._meta['{a.name}']['get_dim_nd'](self) )\n")
                        f.write(f"\n")
                        f.write(f"    @{a.name}.setter\n")
                        f.write(f"    def {a.name}(self, v):\n")
                        f.write(f"        self.{a.name}.copy_from(v)\n")
                        f.write(f"\n")
                        # --------------------------------------------------------------
                        pass
                    else:
                        raise Exception("unexpected type")
                else:
                    if textx_isinstance(a, mm["ScalarAttribute"]):
                        if textx_isinstance(a.type, mm["RawType"]):
                            f.write("    {} : {}={}()\n".format(a.name, fqn(a.type), fqn(a.type)))
                        else:
                            f.write("    {} : {}={}()\n".format(a.name, fqn(a.type), fqn(a.type)))
                    elif textx_isinstance(a, mm["ArrayAttribute"]):
                        if textx_isinstance(a.type, mm["RawType"]):
                            f.write(
                                "    {} : np.ndarray=None\n".format(
                                    a.name
                                )
                            )
                        else:
                            f.write(
                                "    {} : Sequence[{}]=None\n".format(
                                    a.name, fqn(a.type)
                                )
                            )
                    elif textx_isinstance(a, mm["VariantAttribute"]):
                        f.write(
                            "    {} : Union[{}]=None\n".format(
                                a.name, get_variant_types(a)
                            )
                        )
                    else:
                        raise Exception("unexpected type")
            f.write("\n    def __post_init__(self):\n")
            f.write("        support.adjust_array_sizes_and_variants(self)\n")
            f.write(f'''    def __setattr__(self, attribute, value):
        if not attribute in self._meta:
            raise Exception("Illegal field {{}} in {{}}".format(attribute,self.__class__.__name__))
        else:
            if self._meta[attribute]["is_embedded"]:
                super({i.name}, self).__setattr__(attribute, value)
            elif value is None:
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_variant"]:
                if isinstance(value, self._meta[attribute]["get_type"]()):
                    self.__dict__[attribute] = value
                else:
                    raise Exception("Illegal value of type {{}} for field {{}}".format(value.__class__.__name__,attribute))
            elif self._meta[attribute]["is_scalar"]:
                if isinstance(value, self._meta[attribute]["get_type"]()):
                    self.__dict__[attribute] = value
                elif self._meta[attribute]["is_rawtype"]:
                    self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
                else:
                    raise Exception("Illegal value of type {{}} for field {{}}".format(value.__class__.__name__,attribute))
            else:
                self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())
''')

            f.write("\n    _meta = {\n")
            for a in i.attributes:
                f.write('        "{}": {{ '.format(a.name))
                f.write('"name":"{}",'.format(a.name))
                if textx_isinstance(a, mm["VariantAttribute"]):
                    f.write('"get_type_for": lambda s: {}[s.{}], '.format(get_variant_type_map(a),a.variant_selector.render_formula(**fp(struct_obj))))
                    f.write('"is_scalar":True,')
                    f.write('"is_variant":True,')
                    f.write('"is_array":False,')
                    f.write('"is_rawtype":False,')
                    f.write('"is_struct":True,')
                    f.write('"is_embedded":False,')
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
                    f.write(f'"is_embedded":{tf(a.is_embedded())},')
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
                    f.write(f'"is_embedded":{tf(a.is_embedded())},')
                    f.write('"get_type": lambda: {}, '.format(fqn(a.type)))
                else:
                    raise Exception("unexpected type constellation")
                f.write("},\n")
            f.write("    } # end of _meta\n")
