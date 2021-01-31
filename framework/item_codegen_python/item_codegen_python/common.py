import click, os
from textx import textx_isinstance, get_metamodel
from item_lang.properties import (get_property_type,
                                  get_property)
from item_lang.common import (get_package_names_of_obj)


def module_name(obj):
    return ".".join(get_package_names_of_obj(obj) + [obj.name])


def output_filename(base_dir,obj,suffix="py"):
    if base_dir is not None:
        base_dir = os.path.join(base_dir, *get_package_names_of_obj(obj))
        output_file = os.path.join(base_dir, "{}.{}".format(obj.name, suffix))
        output_file = os.path.abspath(output_file)
    else:
        base_dir = os.path.join(*get_package_names_of_obj(obj))
        output_file = os.path.join(base_dir, "{}.{}".format(obj.name, suffix))
    return output_file


def create_folder_and_return_output_filename(obj, base_dir, overwrite):
    """
    :param obj: a struct, enum or constants object
    :return: filename or None (if the file already exists and has not be overriden
    """
    concrete_dir = os.path.join(base_dir, *get_package_names_of_obj(obj))
    if not os.path.exists(concrete_dir):
        os.makedirs(concrete_dir)
    output_file = output_filename(base_dir, obj)
    if overwrite or not os.path.exists(output_file):
        click.echo("-> {}".format(output_file))
        return output_file
    else:
        click.echo("-- Skipping: {}".format(output_file))
        return None


_m = {
    "uint1": "bool",
    "float": "np.float32",
    "double": "np.float64"
}
for i in range(1,65):
    i32 = 8
    if i>64:
        i32=128
    elif i>32:
        i32=64
    elif i>16:
        i32=32
    elif i>8:
        i32=16
    _m["uint{}".format(i)] = "np.uint{}".format(i32)
    _m["int{}".format(i)] = "np.int{}".format(i32)


def get_variant_types(a):
    return ",".join(map(lambda m: fqn(m.type), a.mappings))


def get_variant_type_map(a):
    return "{" + ",".join(map(lambda m: '{}:'.format(m.id)+fqn(m.type), a.mappings)) + "}"


def fp(obj):
    """render_formula parameters"""
    return {"const_separator":'.',
            "repeat_type_name_for_enums":True,
            "inhibit_fqn_for_parent":obj}

def get_property_constexpr(a, pname):
    t = get_property_type(a, pname)
    v = get_property(a, pname)
    if t is str:
        return "\"{}\"".format(v)
    else:
        return "{}".format(v)


def fqn(t):
    mm = get_metamodel(t)
    if textx_isinstance(t, mm["RawType"]):
        if t.name in _m:
            return _m[t.name]
        else:
            return t.name
    else:
        return ".".join(get_package_names_of_obj(t)) + "." + t.name + "." + t.name


def get_signed_or_unsigned(t):
    mm = get_metamodel(t)
    if textx_isinstance(t, mm["Enum"]):
        return get_signed_or_unsigned(t.type)
    elif textx_isinstance(t, mm["RawType"]):
        if t.internaltype == 'INT':
            return "signed"
        elif t.internaltype == 'UINT':
            return "unsigned"
        elif t.internaltype == 'BOOL':
            return "unsigned"
        else:
            raise Exception("unexpected")
    else:
        raise Exception("unexpected")


def tf(v):
    if v:
        return "True"
    else:
        return "False"
