import click
import os
from textx import textx_isinstance, get_metamodel
from item_lang.common import get_package_names_of_obj


def modname(i):
    return fqn(i).replace(".","_")


def output_filename(base_dir, obj, suffix="lua"):
    if obj.__class__.__name__ == "Dissector":
        if base_dir is not None:
            base_dir = os.path.join(base_dir)
            output_file = os.path.join(base_dir, "{}.{}".format(obj.name, suffix))
            output_file = os.path.abspath(output_file)
        else:
            base_dir = "."
            output_file = os.path.join(base_dir, "{}.{}".format(obj.name, suffix))
        return output_file
    else:
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
    if obj.__class__.__name__=="Dissector":
        concrete_dir = base_dir
    else:
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
    "uint1": "uint8",
    "bool": "uint8",
    "char": "uint8",
}
for i in range(1, 65):
    i32 = 8
    if i > 64:
        i32 = 128
    elif i > 32:
        i32 = 64
    elif i > 16:
        i32 = 32
    elif i > 8:
        i32 = 16
    _m["uint{}".format(i)] = "uint{}".format(i32)
    _m["int{}".format(i)] = "int{}".format(i32)
    _m["sint{}".format(i)] = "int{}".format(i32)


def fqn(t):
    mm = get_metamodel(t)
    if t.is_enum():
        t = t.type
    if t.is_rawtype():
        if t.name in _m:
            return _m[t.name]
        else:
            return t.name
    else:
        return ".".join(get_package_names_of_obj(t)) + "." + t.name
