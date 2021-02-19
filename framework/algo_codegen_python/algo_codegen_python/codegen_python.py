import textx, os, click
from algo_lang.codegen_common import get_package_names
from textx import get_children_of_type, get_model
from item_codegen_python.common import module_name


@textx.generator("algo", "python")
def generate_python(metamodel, model, output_path, overwrite, debug):
    "Generating c++ code from the algo model"
    input_file = model._tx_filename
    base_dir = output_path if output_path else os.path.dirname(input_file)
    base_dir = os.path.join(base_dir, *get_package_names(model))
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    output_file = os.path.abspath(
        os.path.join(base_dir, "{}.{}".format(base_name, "py"))
    )
    if overwrite or not os.path.exists(output_file):
        click.echo("-> {}".format(output_file))
        generate_python_from_model(model, base_name, output_file)
    else:
        click.echo("-- Skipping: {}".format(output_file))


def fqn(a):
    from os.path import basename, splitext

    file_package, _ = splitext(basename(get_model(a)._tx_filename))
    return (
        ".".join(get_package_names(get_model(a)))
        + "."
        + file_package
        + "."
        + a.name
        + "="
        + str(a)
    )


def generate_python_from_model(model, base_name, output_file):
    _ = textx.get_metamodel(model)
    item_models = []
    algos = get_children_of_type("Algo", model)
    for a in algos:
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
        f.write('todo: problem with "base"-package... encoded in output path.\n')
        for h in required_mdoules:
            f.write("import {}\n".format(h))
        for a in algos:
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
