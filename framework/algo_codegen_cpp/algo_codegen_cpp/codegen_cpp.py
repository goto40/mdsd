import textx, os, click
from item_lang.common import get_package_names_of_obj
from textx import get_children_of_type, get_model, TextXSemanticError, get_location
from item_lang.common import obj_is_newer_than_file


@textx.generator("algo", "cpp")
def generate_cpp(metamodel, model, output_path, overwrite, debug):
    "Generating c++ code from the algo model"
    input_file = model._tx_filename
    base_dir = output_path if output_path else os.path.dirname(input_file)

    algos = get_children_of_type("Algo", model)

    for algo in algos:
        output_file = create_folder_and_return_output_filename(
            algo, base_dir, overwrite
        )
        generate_cpp_for_algo(algo, output_file)


def fqn(a):
    return "::".join(get_package_names_of_obj(a)) + "::" + a.name


def fqn_funcparam(a, prefix=None):
    t = fqn(a.type)
    if prefix is not None:
        t = prefix + " " + t
    if hasattr(a, "datatype") and a.datatype == "shared_ptr":
        return "std::shared_ptr<{}>".format(t)
    elif hasattr(a, "datatype") and a.datatype is not None:
        raise TextXSemanticError(
            "unexpected: unknown datatype {}".format(a.datatype), **get_location(a)
        )
    else:
        return t + "&"


def _get_open_namespace(model):
    return "namespace " + "::".join(get_package_names_of_obj(model)) + "{\n"


def generate_cpp_for_algo(a, output_file):
    if obj_is_newer_than_file(a, output_file):
        item_models = []
        for p in a.inputs:
            item_models.append(get_model(p.type))
        for p in a.outputs:
            item_models.append(get_model(p.type))
        for p in a.parameters:
            item_models.append(get_model(p.type))
        item_models = set(item_models)
        item_headers = []
        for m in item_models:
            for element in get_children_of_type("Struct", m):
                item_headers.append(output_filename(None, element))
            for element in get_children_of_type("Enum", m):
                item_headers.append(output_filename(None, element))
            for element in get_children_of_type("Consants", m):
                item_headers.append(output_filename(None, element))
        item_headers = list(set(item_headers))
        item_headers.sort()

        with open(output_file, "w") as f:
            f.write(
                "#ifndef __{}_{}_H\n".format(
                    "_".join(get_package_names_of_obj(a)), a.name.upper()
                )
            )
            f.write(
                "#define __{}_{}_H\n".format(
                    "_".join(get_package_names_of_obj(a)), a.name.upper()
                )
            )
            f.write("// ACTIVATE FOR SWIG\n")
            f.write("#include <functional>\n")
            f.write("#include <memory>\n")
            f.write("#include <stdexcept>\n")
            for h in item_headers:
                f.write('#include "{}"\n'.format(h))
            f.write("#ifdef SWIG\n")
            f.write("%shared_ptr({})\n".format(fqn(a)))
            f.write("#endif\n")
            f.write(_get_open_namespace(a))

            f.write("class {} {{\n".format(a.name))
            f.write(
                "    inline static std::function<std::shared_ptr<{}>()> factory = nullptr;\n".format(
                    a.name
                )
            )
            f.write("protected:\n")
            for p in a.parameters:
                f.write("        {} {};\n".format(fqn(p.type), p.name))
            f.write("public:\n")
            f.write("    virtual ~{}() {{}}\n".format(a.name))
            f.write(
                '    static const char* get_classname() {{ return "{}"; }}\n'.format(
                    a.name
                )
            )
            f.write(
                '    static std::shared_ptr<{}> create() {{ if (factory==nullptr) {{ throw std::runtime_error("factory not set."); }} return factory(); }}\n'.format(
                    a.name
                )
            )
            f.write(
                "    template<class F> static void set_factory(F f) {{ factory=f; }}\n".format(
                    a.name
                )
            )
            f.write("    virtual void compute(")
            sep = ""
            for p in a.inputs:
                f.write(
                    "{}\n        {} {}".format(sep, fqn_funcparam(p, "const"), p.name)
                )
                sep = ", "
            for p in a.outputs:
                f.write("{}\n        {} {}".format(sep, fqn_funcparam(p), p.name))
                sep = ", "
            f.write("\n    )=0;\n")
            f.write("}}; // struct {}\n".format(a.name))
            f.write("} // close namespace\n")
            f.write(
                "#endif // __{}_{}_H\n".format(
                    "_".join(get_package_names_of_obj(a)), a.name.upper()
                )
            )


def output_filename(base_dir, obj, suffix="h"):
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
