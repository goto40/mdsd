# import textx
from textx import (
    get_metamodel,
    get_children_of_type,
    textx_isinstance,
)
from item_lang.common import (
    obj_is_newer_than_file,
)
from item_codegen_lua_dissector.common import (
    modname,
    fqn,
)
from os.path import exists


def generate_lua_for_dissector(struct_obj, output_file, overwrite):
    if not exists(output_file) or (
        overwrite and obj_is_newer_than_file(struct_obj, output_file)
    ):
        with open(output_file, "w") as f:
            generate_lua_dissector(f, struct_obj)


def get_all_referenced_structs(s):
    mm = get_metamodel(s)
    l = set()
    l.add(s)
    n = 0
    while n!=len(l):
        n = len(l)
        c = get_children_of_type('ScalarAttribute', s)
        for a in c:
            if textx_isinstance(a.type, mm['Struct']):
                l.add(a.type)
        c = get_children_of_type('ArrayAttribute', s)
        for a in c:
            if textx_isinstance(a.type, mm['Struct']):
                l.add(a.type)
        c = get_children_of_type('VariantMapping', s)
        for m in c:
            if textx_isinstance(m.type, mm['Struct']):
                l.add(m.type)
    return l


def generate_lua_dissector(f, d):
    """
    :param f: output file obj
    :param d: item to be generated (the dissector)
    """
    refs = get_all_referenced_structs(d.item)
    f.write(f"-- lua code for {d.name}\n")
    f.write("\n")
    f.write(f'{d.name}_protocol = Proto("{d.name}",  "Dissector {d.name}")\n')
    for i in refs:
        f.write(f'local {modname(i)} = require("{fqn(i)}")\n')

    f.write(f'{d.name}_protocol.fields = {{}}\n')
    for i in refs:
        f.write(f'for _,f in ipairs({modname(i)}.fields) do table.insert({d.name}_protocol.fields, f) end\n')
    
    f.write(f'function {d.name}_protocol.dissector(buffer, pinfo, tree)\n')
    f.write(f'  pinfo.cols.protocol = {d.name}_protocol.name\n')
    f.write(f'  {modname(d.item)}.dissector_data({d.name}_protocol, buffer, 0, tree,{{}})\n')
    f.write('end\n')

    for c in d.channels:
        if c.udp:
            f.write('local udp_port = DissectorTable.get("udp.port")\n')
            f.write(f'udp_port:add({c.port}, {d.name}_protocol)\n')
        if c.tcp:
            f.write('local tcp_port = DissectorTable.get("tcp.port")\n')
            f.write(f'tcp_port:add({c.port}, {d.name}_protocol)\n')
