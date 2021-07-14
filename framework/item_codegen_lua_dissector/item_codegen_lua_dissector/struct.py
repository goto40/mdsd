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
    modname,
    fqn,
)
from os.path import exists


def generate_lua_for_struct(struct_obj, output_file, overwrite):
    if not exists(output_file) or (
        overwrite and obj_is_newer_than_file(struct_obj, output_file)
    ):
        with open(output_file, "w") as f:
            generate_lua_struct(f, struct_obj)


def lua_int_getter(t):
    if t.is_enum():
        t = t.type
    assert t.is_rawtype()
    if t.internaltype == 'UINT':
        return "uint"
    elif t.internaltype == 'INT':
        return "int"
    elif t.internaltype == 'BOOL':
        return "uint"
    elif t.internaltype == 'FLOAT':
        return "float"
    else:
        raise Exception(f"unexpected internaltype {t.internaltype} in lua_int_getter")


def generate_lua_struct(f, i):
    """
    :param f: output file obj
    :param i: item to be generated (the struct)
    """
    f.write(f"-- lua code for {i.name}\n")

    for r in get_referenced_elements_of_struct(i):
        if r.is_struct():
            f.write(f'local {modname(r)} = require("{fqn(r)}")\n')
    f.write("\n")


    concrete_variables = []
    for a in i.attributes:
        l = a.get_referenceed_if_attributes()
        concrete_variables = concrete_variables + l
        if a.is_array():
            l = a.get_referenceed_dim_attributes()
            concrete_variables = concrete_variables + l
        if a.is_variant():
            l = [a.variant_selector]
            concrete_variables = concrete_variables + l
    concrete_variable_names = list(map(lambda x: '.'.join(map(lambda x:x.name, x.ref._tx_path)), concrete_variables))
    concrete_variable_names = set(concrete_variable_names)

    fields = []
    for a in i.attributes:
        if not a.is_embedded() and (a.has_enum() or a.has_rawtype()):
            fields.append(a)
    for a in fields:
        f.write(f"local field_{a.name} = ProtoField.{fqn(a.type)}(\"{a.name}\",\"{a.name}\", base.DEC)\n")

    f.write("local m = {}\n")
    f.write("m.fields = {")
    comma=""
    for a in fields:
        f.write(f"{comma}field_{a.name}")
        comma=","
    f.write("}\n")
    f.write("\n")

    f.write("function m.create_relevant_sub_map(fieldname, m1)\n")
    f.write("  local m2={}\n")
    f.write("  for key, _ in pairs(m1) do\n")
    f.write("    if key:find(fieldname .. \".\", 1, true) == 1 then\n")
    f.write("      m2[key:sub(fieldname:len()+2)] = m1[key]\n")
    f.write("      -- print(\"CREATE: \"..key .. \"-->\" .. key:sub(fieldname:len()+2))\n")
    f.write("    end\n")
    f.write("  end\n")
    f.write("  return m2\n")
    f.write("end\n")

    f.write("function m.dissector_data(proto, buffer, pos, tree, var_of_interrest)\n")
    f.write("  local concrete_vars = {}\n")
    for n in concrete_variable_names:
        f.write(f"  concrete_vars[\"{n}\"] = \"none\"\n")
    f.write('  for key, value in pairs(var_of_interrest) do')
    f.write("    concrete_vars[key] = value\n")
    f.write('    -- print("INIT:" .. key.."= init:"..value)\n')
    f.write("  end\n")
    f.write("  local newvars = {}\n")
    f.write("  local length = buffer:len()\n")
    f.write("  if length == 0 then return end\n")
    f.write("  if length == pos then return end\n")
    f.write(f"  local subtree = tree:add(proto, buffer(), \"{i.name}\")\n")
    prefix="concrete_vars[\""
    postfix="\"]"
    for a in i.attributes:
        f.write(f"  -- {a.name}\n")

        if a.has_if():
            f.write(f"  if {a.if_attr.predicate.render_formula(compute_constants=True,prefix=prefix,postfix=postfix)} then\n")

        if a in fields:
            if a.is_array():
                if a.type.name=="char":
                    f.write(f"  local subtree_array = subtree:add(proto, buffer(), \"{a.name} : \" .. buffer(pos,1):stringz())\n")
                else:
                    f.write(f"  local subtree_array = subtree:add(proto, buffer(), \"{a.name} : {a.type.name}-array\")\n")
                f.write(f"  for k = 1, {a.render_formula(compute_constants=True,prefix=prefix,postfix=postfix)} do\n")
                f.write(f"    subtree_array:add_le(field_{a.name}, buffer(pos,{a.type.get_size_in_bytes()}))\n")
                f.write(f"    pos = pos+{a.type.get_size_in_bytes()}\n")
                f.write("  end\n")
            else:
                f.write(f"  subtree:add_le(field_{a.name}, buffer(pos,{a.type.get_size_in_bytes()}))\n")
                f.write(f"  if concrete_vars[\"{a.name}\"] ~= nil then\n")
                f.write(f"    concrete_vars[\"{a.name}\"] = buffer:range(pos,{a.type.get_size_in_bytes()}):le_{lua_int_getter(a.type)}()\n")
                f.write(f'    -- print("SET: {a.name}".."= set:"..concrete_vars[\"{a.name}\"])\n')
                f.write("  end\n")
                f.write(f"  pos = pos+{a.type.get_size_in_bytes()}\n")
        elif a.is_variant():
            f.write(f"  sel = concrete_vars[\"{'.'.join(map(lambda x:x.name, a.variant_selector.ref._tx_path))}\"]\n")
            if_text="if"
            for m in a.mappings:
                f.write(f"  {if_text} sel=={m.id.compute_formula()} then\n")
                f.write(f"    pos, _ = {modname(m.type)}.dissector_data(proto, buffer, pos, subtree,{{}})\n")
                if_text="elseif"
            f.write(f"  else\n")
            f.write(f"    local subtree_error = subtree:add(proto, buffer(), \"{a.name} : ERROR, unknown id\")\n")
            f.write(f"  end\n")
        elif a.has_struct():
            if a.is_array():
                f.write(f"  local subtree_array = subtree:add(proto, buffer(), \"{a.name} : {a.type.name}-array\")\n")
                f.write(f"  for k = 1, {a.render_formula(compute_constants=True,prefix=prefix,postfix=postfix)} do\n")
                f.write(f"    pos, _ = {modname(a.type)}.dissector_data(proto, buffer, pos, subtree_array,{{}})\n")
                f.write("  end\n")
            else:
                f.write(f" pos, newvars = {modname(a.type)}.dissector_data(proto, buffer, pos, subtree,m.create_relevant_sub_map(\"{a.name}\",concrete_vars))\n")
                f.write('  for key, value in pairs(newvars) do')
                f.write(f'    concrete_vars["{a.name}."..key] = value\n')
                f.write(f'    -- print("UPDATE {a.name}."..key.."="..value)\n')
                f.write("  end\n")

        if a.has_if():
            f.write("  end\n")
    f.write("  return pos, concrete_vars\n")
    f.write("end\n")
    f.write("\nreturn m\n")
