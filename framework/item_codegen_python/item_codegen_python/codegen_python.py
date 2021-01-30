import textx
from textx import get_children_of_type
from item_codegen_python.common import *
from item_codegen_python.enum import generate_py_for_enum
from item_codegen_python.constants import generate_py_for_constants
from item_codegen_python.struct import generate_py_for_struct


@textx.generator("item", "python")
def generate_python(metamodel, model, output_path, overwrite, debug):
    "Generating c++ code from the item model"
    input_file = model._tx_filename
    base_dir = output_path if output_path else os.path.dirname(input_file)

    structs = get_children_of_type("Struct", model)
    enums = get_children_of_type("Enum", model)
    constants = get_children_of_type("Constants", model)

    for elem in structs:
        output_file = create_folder_and_return_output_filename(elem, base_dir, overwrite)
        generate_py_for_struct(elem, output_file)

    for elem in enums:
        output_file = create_folder_and_return_output_filename(elem, base_dir, overwrite)
        generate_py_for_enum(elem, output_file)

    for elem in constants:
        output_file = create_folder_and_return_output_filename(elem, base_dir, overwrite)
        generate_py_for_constants(elem, output_file)