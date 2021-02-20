import textx
import os
import click
from item_lang.common import get_package_names_of_obj
from textx import get_children_of_type, get_model
from item_codegen_python.common import module_name
from item_lang.common import obj_is_newer_than_file


@textx.generator("algo", "python")
def generate_python(metamodel, model, output_path, overwrite, debug):
    "Generating python code from the algo model"
    input_file = model._tx_filename
    base_dir = output_path if output_path else os.path.dirname(input_file)

    algos = get_children_of_type("Algo", model)

    for algo in algos:
        output_file = create_folder_and_return_output_filename(
            algo, base_dir, overwrite
        )
        generate_py_for_algo(algo, output_file)


def output_filename(base_dir, obj, suffix="py"):
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
    :param obj: an algo object
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


def fqn(a):
    return ".".join(get_package_names_of_obj(a)) + "." + a.name + "." + a.name


def generate_py_for_algo(a, output_file):
    #mm = get_metamodel(a)
    if obj_is_newer_than_file(a, output_file):
        item_models = []
        for p in a.inputs:
            item_models.append(get_model(p.type))
        for p in a.outputs:
            item_models.append(get_model(p.type))
        for p in a.parameters:
            item_models.append(get_model(p.type))
        item_models = set(item_models)
        required_mdoules = []
        for m in item_models:
            for element in get_children_of_type("Struct", m):
                required_mdoules.append(module_name(element))
            for element in get_children_of_type("Enum", m):
                required_mdoules.append(module_name(element))
            for element in get_children_of_type("Consants", m):
                required_mdoules.append(module_name(element))
        required_mdoules = list(set(required_mdoules))
        required_mdoules.sort()

        with open(output_file, "w") as f:
            f.write("from abc import ABC, abstractmethod\n")
            for h in required_mdoules:
                f.write("import {}\n".format(h))
            f.write("class {}(ABC):\n".format(a.name))
            f.write("    def __init__(self):\n")
            for p in a.parameters:
                f.write("        self.{}={}();\n".format(p.name, fqn(p.type)))
            f.write("\n")
            f.write("    @abstractmethod\n")
            f.write("    def compute(")
            sep = ""
            for p in a.inputs:
                f.write("{}\n                {}:{}".format(sep, p.name, fqn(p.type)))
                sep = ", "
            for p in a.outputs:
                f.write("{}\n                {}:{}".format(sep, p.name, fqn(p.type)))
                sep = ", "
            f.write("\n            ):\n")
            f.write("        pass")
            f.write("\n")
