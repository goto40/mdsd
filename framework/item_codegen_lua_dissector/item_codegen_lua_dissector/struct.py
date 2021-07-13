# import textx
from textx import (
    get_metamodel,
    textx_isinstance,
)
from item_lang.common import (
    get_referenced_elements_of_struct,
    obj_is_newer_than_file,
)
from item_codegen_lua_dissector.common import (
    output_filename,
    fqn
)
from os.path import exists


def generate_lua_for_struct(struct_obj, output_file, overwrite):
    if not exists(output_file) or (
        overwrite and obj_is_newer_than_file(struct_obj, output_file)
    ):
        with open(output_file, "w") as f:
            generate_lua_struct(f, struct_obj)


def modname(i):
    return fqn(i).replace(".","_")


def generate_lua_struct(f, i):
    """
    :param f: output file obj
    :param i: item to be generated (the struct)
    """
    f.write(f"-- lua code for {i.name}\n")

    for r in get_referenced_elements_of_struct(i):
        f.write(f'local {modname(r)} = require("{fqn(r)}")\n')
    f.write("\n")

    mm = get_metamodel(i)
    fields = []
    for a in i.attributes:
        if not a.is_embedded() and not textx_isinstance(a, mm["VariantAttribute"]) and textx_isinstance(a.type, mm["RawType"]):
            fields.append(a)
    for a in fields:
        f.write(f"local field_{a.name} = Protofield.{fqn(a.type)}(\"{a.name}\",\"{a.name}\", base.DEC)\n")

    f.write("m = {}\n")
    f.write("m.fields = {")
    comma=""
    for a in fields:
        f.write(f"{comma}field_{a.name}")
        comma=","
    f.write("}\n")
    f.write("\n")

    f.write("function m.dissector_data(proto, buffer, pos, tree)\n")
    f.write("  length = buffer:len()\n")
    f.write("  if length == 0 then return end\n")
    f.write("  if length == pos then return end\n")
    f.write(f"  local subtree = tree:add(proto, buffer(), \"{i.name}\"\n")
    for a in i.attributes:
        if a in fields:
            f.write(f"  subtree:add_le(field_{a.name}, buffer(pos,{a.type.get_size_in_bytes()}))\n")
            f.write(f"  pos = pos+{a.type.get_size_in_bytes()}\n")
        else:
            f.write(f"  todo {a.name}")
    
    f.write("  return pos\n")
    f.write("end\n")
