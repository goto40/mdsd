# import textx
# from textx import get_metamodel
from item_lang.common import (
    obj_is_newer_than_file,
)
from os.path import exists


def generate_lua_for_struct(struct_obj, output_file, overwrite):
    if not exists(output_file) or (
        overwrite and obj_is_newer_than_file(struct_obj, output_file)
    ):
        with open(output_file, "w") as f:
            generate_lua_struct(f, struct_obj)


def generate_lua_struct(f, i):
    """
    :param f: output file obj
    :param i: item to be generated (the struct)
    """
    f.write(f"-- lua code for {i.name}\n")

    for a in i.attributes:
        f.write(f"-- attr {a.name}\n")
