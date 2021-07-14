import textx
import os
from textx import get_children_of_type
from item_codegen_lua_dissector.common import create_folder_and_return_output_filename
from item_codegen_lua_dissector.struct import generate_lua_for_struct
from item_codegen_lua_dissector.dissector import generate_lua_for_dissector


@textx.generator("item", "lua_dissector")
def generate_lua_dissector_itemcode(metamodel, model, output_path, overwrite, debug):
    "Generating dissector code from the item model"
    input_file = model._tx_filename
    base_dir = output_path if output_path else os.path.dirname(input_file)

    structs = get_children_of_type("Struct", model)

    for elem in structs:
        output_file = create_folder_and_return_output_filename(
            elem, base_dir, overwrite
        )
        generate_lua_for_struct(elem, output_file, overwrite)


@textx.generator("dissector", "lua_dissector")
def generate_lua_dissector(metamodel, model, output_path, overwrite, debug):
    "Generating dissector entry/main code"
    input_file = model._tx_filename
    base_dir = output_path if output_path else os.path.dirname(input_file)

    dissectors = get_children_of_type("Dissector", model)

    for elem in dissectors:
        output_file = create_folder_and_return_output_filename(
            elem, base_dir, overwrite
        )
        generate_lua_for_dissector(elem, output_file, overwrite)
