import textx, click, os
from textx import textx_isinstance, get_metamodel
from item_lang.properties import (get_property_type,
                                  get_property)
from item_lang.common import (get_package_names_of_obj)


def output_filename(base_dir,obj,suffix="h"):
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
    "uint1": "bool"
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
    _m["uint{}".format(i)] = "uint{}_t".format(i32)
    _m["int{}".format(i)] = "int{}_t".format(i32)
    _m["sint{}".format(i)] = "int{}_t".format(i32)


def get_variant_types(a):
    return ",".join(map(lambda m: fqn(m.type), a.mappings))


def get_cpp_return_type(t):
    if t is str:
        return "const char*"
    else:
        return fqn(t)


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
        return "::".join(get_package_names_of_obj(t)) + "::" + t.name


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


def get_open_namespace_for_obj(obj):
    return "namespace " +"::".join(get_package_names_of_obj(obj)) + "{\n"


def define_swig_vector(t, mm):
    txt = ""
    txt += "#ifndef __SWIG_HELPER_ITEMCODE__VECTOR_{}\n".format(t.name)
    if textx.textx_isinstance(t, mm["RawType"]):
        txt += '%template(vector_{0}) std::vector<{0}>;\n'.format(fqn(t))
    else:
        txt += '%template(vector_{0}) std::vector<{1}>;\n'.format(t.name,fqn(t))
    txt += "#endif // __SWIG_HELPER_ITEMCODE__VECTOR_{}\n".format(t.name)
    return txt


def define_swig_array(t, s, mm):
    txt = ""
    txt += "#ifndef __SWIG_HELPER_ITEMCODE__ARRAY_{}_{}\n".format(t.name, s)
    if textx.textx_isinstance(t, mm["RawType"]):
        txt += '%template(array_{0}_{1}) std::array<{0},{1}>;\n'.format(fqn(t), s)
    else:
        txt += '%template(array_{0}_{2}) std::array<{1},{2}>;\n'.format(t.name,fqn(t),s)
    txt += "#endif // __SWIG_HELPER_ITEMCODE__ARRAY_{}_{}\n".format(t.name, s)
    return txt


def define_swig_variant_access(i, a):
    types = list(map(lambda m: m.type, a.mappings))
    txt = ""
    for t in types:
        txt += "inline {0}& MDSD_get_{3}_from_{4}_{2}({1}& s) {{ return std::get<{0}>(s.{2}); }}\n".format(fqn(t),fqn(i), a.name, t.name,i.name)
        txt += "#ifndef SWIG\n"
        txt += "inline const {0}& MDSD_get_{3}_from_{4}_{2}(const {1}& s) {{ return std::get<{0}>(s.{2}); }}\n".format(fqn(t),fqn(i), a.name, t.name,i.name)
        txt += "#endif //SWIG\n"
    return txt


def tf(v):
    if v:
        return "true"
    else:
        return "false"
