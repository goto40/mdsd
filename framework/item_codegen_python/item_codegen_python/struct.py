from textx import (get_metamodel,
                   textx_isinstance)
from item_codegen_python.common import (fqn, get_variant_types,
                                        get_variant_type_map,
                                        module_name, fp, tf,
                                        get_property_constexpr)
from item_lang.common import (obj_is_new_than_file,
                              get_referenced_elements_of_struct,
                              get_container, get_start_end_bit)
from item_lang.properties import (get_all_possible_properties, has_property,
                                  get_property_type)


def generate_py_for_struct(struct_obj, output_file):
    mm = get_metamodel(struct_obj)
    if obj_is_new_than_file(struct_obj, output_file):
        with open(output_file, "w") as f:
            f.write("""# generated code
from dataclasses import dataclass
import numpy as np
import mdsd.item_support as support
from mdsd.item.init_default_values import init_default_values
from mdsd.common import get_embedded_from_uint, ArrayLike
from mdsd.common import set_embedded_in_uint
from mdsd.common import ArrayLike, str2array, array2str
from typing import Sequence, Union
from functools import reduce
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
                        f.write(f"            assert idx >= 0\n")
                        f.write(f"            assert idx < reduce(lambda a, b: a * b, {i.name}._meta['{a.name}']['_get_dim_nd'](self))\n")
                        f.write(f"            ret = get_embedded_from_uint({fqn(rawtype)}, self.{c.name},[{start_end_bit[0]}-idx*{rawtype.bits},{start_end_bit[0]}+1-(idx+1)*{rawtype.bits}])\n")
                        if textx_isinstance(a.type, mm["Enum"]):
                            f.write(f"            ret = {fqn(a.type)}(ret)\n")
                        f.write(f"            return ret\n")
                        f.write(f"        def setter(idx, v):\n")
                        f.write(f"            assert idx >= 0\n")
                        f.write(f"            assert idx < reduce(lambda a, b: a * b, {i.name}._meta['{a.name}']['_get_dim_nd'](self))\n")
                        f.write(f"            assert isinstance(v, {fqn(a.type)})\n")
                        if textx_isinstance(a.type, mm["Enum"]):
                            f.write(f"            v = v.value\n")
                        f.write(f"            self.{c.name} = set_embedded_in_uint(v, self.{c.name},[{start_end_bit[0]}-idx*{rawtype.bits},{start_end_bit[0]}+1-(idx+1)*{rawtype.bits}])\n")
                        f.write(f"        return ArrayLike( getter=getter, setter=setter, mytype={fqn(rawtype)}, shape={i.name}._meta['{a.name}']['_get_dim_nd'](self) )\n")
                        f.write(f"\n")
                        f.write(f"    @{a.name}.setter\n")
                        f.write(f"    def {a.name}(self, v):\n")
                        f.write(f"        self.{a.name}.copy_from(v)\n")
                        f.write(f"\n")
                        # --------------------------------------------------------------
                        pass
                    else:
                        raise Exception("unexpected type")
                else:  # not validation_embedded
                    if textx_isinstance(a, mm["ScalarAttribute"]):
                        if textx_isinstance(a.type, mm["RawType"]):
                            f.write("    {} : {}={}()\n".format(a.name, fqn(a.type), fqn(a.type)))
                        else:
                            f.write("    {} : {}={}()\n".format(a.name, fqn(a.type), fqn(a.type)))
                        if hasattr(a, 'type') and a.type.name == 'char':
                            f.write(f"    @property\n")
                            f.write(f"    def {a.name}_as_str(self):\n")
                            f.write(f"        return chr(self.{a.name})\n")
                            f.write(f"\n")
                            f.write(f"    @{a.name}_as_str.setter\n")
                            f.write(f"    def {a.name}_as_str(self, v):\n")
                            f.write(f"        self.{a.name} = np.uint8(ord(v))\n")
                            f.write(f"\n")
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
                        if hasattr(a, 'type') and a.type.name == 'char':
                            f.write(f"    @property\n")
                            f.write(f"    def {a.name}_as_str(self):\n")
                            f.write(f"        return array2str(self.{a.name})\n")
                            f.write(f"\n")
                            f.write(f"    @{a.name}_as_str.setter\n")
                            f.write(f"    def {a.name}_as_str(self, v):\n")
                            f.write(f"        self.{a.name} = str2array(v, len(self.{a.name}))\n")
                            f.write(f"\n")

                    elif textx_isinstance(a, mm["VariantAttribute"]):
                        f.write(
                            "    {} : Union[{}]=None\n".format(
                                a.name, get_variant_types(a)
                            )
                        )
                    else:
                        raise Exception("unexpected type")
            f.write("\n    def __post_init__(self):\n")
            f.write("        init_default_values(self)\n")
            f.write(f'''    def __setattr__(self, attribute, value):
        if not attribute in self._meta:
            raise Exception("Illegal field {{}} in {{}}".format(attribute,self.__class__.__name__))
        else:
            if len(self._meta[attribute])==0:
                super({i.name}, self).__setattr__(attribute, value)
            elif self._meta[attribute]["_is_embedded"]:
                super({i.name}, self).__setattr__(attribute, value)
            elif value is None:
                self.__dict__[attribute] = value
            elif self._meta[attribute]["_is_variant"]:
                if isinstance(value, self._meta[attribute]["_get_type"]()):
                    self.__dict__[attribute] = value
                else:
                    raise Exception("Illegal value of type {{}} for field {{}}".format(value.__class__.__name__,attribute))
            elif self._meta[attribute]["_is_scalar"]:
                if isinstance(value, self._meta[attribute]["_get_type"]()):
                    self.__dict__[attribute] = value
                elif self._meta[attribute]["_is_rawtype"]:
                    self.__dict__[attribute] = self._meta[attribute]["_get_type"]()(value)
                else:
                    raise Exception("Illegal value of type {{}} for field {{}}".format(value.__class__.__name__,attribute))
            else:
                self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["_get_type"]())
''')

            f.write("\n    _meta_order = [\n")
            for a in i.attributes:
                f.write(f"        '{a.name}',\n")
            f.write("\n    ]\n")
            f.write("\n    _meta = {\n")
            for a in i.attributes:
                if hasattr(a, 'type') and a.type.name == 'char':
                    f.write(f'        "{a.name}_as_str": {{}},\n')

                f.write('        "{}": {{ '.format(a.name))
                f.write('"_name":"{}",'.format(a.name))
                if a.if_attr is None:
                    f.write('"_has_if_restriction":False,')
                    f.write('"_if_restriction":lambda _: True,')
                else:
                    f.write('"_has_if_restriction":True,')
                    f.write('"_if_restriction":lambda s:{},'.format(
                        a.if_attr.predicate.render_formula(prefix="s.")
                    ))
                if textx_isinstance(a, mm["VariantAttribute"]):
                    f.write('"_get_type_for": lambda s: {}[s.{}], '.format(get_variant_type_map(a),a.variant_selector.render_formula(**fp(struct_obj))))
                    f.write('"_is_scalar":True,')
                    f.write('"_is_variant":True,')
                    f.write('"_is_array":False,')
                    f.write('"_is_rawtype":False,')
                    f.write('"_is_struct":True,')
                    f.write('"_is_embedded":False,')
                    f.write('"_get_type": lambda: ({}), '.format(get_variant_types(a)))
                elif textx_isinstance(a, mm["ScalarAttribute"]):
                    f.write('"_is_scalar":True,')
                    f.write('"_is_variant":False,')
                    f.write('"_is_array":False,')
                    if textx_isinstance(a.type, mm["RawType"]) or textx_isinstance(a.type, mm["Enum"]):
                        f.write('"_is_rawtype":True,')
                        f.write('"_is_struct":False,')
                    else:
                        f.write('"_is_rawtype":False,')
                        f.write('"_is_struct":True,')
                    f.write(f'"_is_embedded":{tf(a.is_embedded())},')
                    f.write('"_get_type": lambda: {}, '.format(fqn(a.type)))
                    if hasattr(a, 'type') and a.type.name == "char":
                        f.write('"_has_char_content":True,')
                    else:
                        f.write('"_has_char_content":False,')
                elif textx_isinstance(a, mm["ArrayAttribute"]):
                    f.write('"_is_scalar":False,')
                    f.write('"_is_variant":False,')
                    f.write('"_is_array":True,')
                    if a.has_fixed_size():
                        f.write('"_is_dynamic_array":False,')
                    else:
                        f.write('"_is_dynamic_array":True,')
                    f.write('"_get_dim":lambda x:({}),'.format(a.render_formula(prefix="x.",**fp(struct_obj))))
                    f.write('"_get_dim_nd":lambda x:({},),'.format(a.render_formula_comma_separated(prefix="x.", **fp(struct_obj))))
                    if textx_isinstance(a.type, mm["RawType"]) or textx_isinstance(a.type, mm["Enum"]):
                        f.write('"_is_rawtype":True,')
                        f.write('"_is_struct":False,')
                    else:
                        f.write('"_is_rawtype":False,')
                        f.write('"_is_struct":True,')
                    f.write(f'"_is_embedded":{tf(a.is_embedded())},')
                    f.write('"_get_type": lambda: {}, '.format(fqn(a.type)))
                    if hasattr(a, 'type') and a.type.name == "char":
                        f.write('"_has_char_content":True,')
                    else:
                        f.write('"_has_char_content":False,')
                else:
                    raise Exception("unexpected type constellation")

                pdefs = get_all_possible_properties(a)
                pdefs = sorted(pdefs.keys())

                for pname in pdefs:
                    if has_property(a, pname):
                        f.write(f'"__has_{pname}":True,')
                        f.write('"{}":lambda:{}({}),'.format(pname,
                            fqn(get_property_type(a, pname)),
                            get_property_constexpr(a, pname)
                        ))
                    else:
                        f.write(f'"__has_{pname}":False,')

                f.write("},\n")
            f.write("    } # end of _meta\n")
