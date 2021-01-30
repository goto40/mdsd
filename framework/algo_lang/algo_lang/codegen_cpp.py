import textx, os, click
from .codegen_common import get_package_names
from textx import get_children_of_type, get_model


@textx.generator("algo", "cpp")
def generate_cpp(metamodel, model, output_path, overwrite, debug):
    "Generating c++ code from the item model"
    input_file = model._tx_filename
    base_dir = output_path if output_path else os.path.dirname(input_file)
    base_dir = os.path.join(base_dir,*get_package_names(model))
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    output_file = os.path.abspath(
        os.path.join(base_dir, "{}.{}".format(base_name, "h"))
    )
    if overwrite or not os.path.exists(output_file):
        click.echo("-> {}".format(output_file))
        generate_cpp_from_model(model, base_name, output_file)
    else:
        click.echo("-- Skipping: {}".format(output_file))


def fqn(a):
    return "::".join(get_package_names(get_model(a))) + "::" + a.name

def fqn_funcparam(a,prefix = None):
    t = fqn(a.type)
    if prefix is not None:
        t = prefix+" "+t
    if (hasattr(a,"datatype") and a.datatype=="shared_ptr"):
        return "std::shared_ptr<{}>".format(t)
    elif (hasattr(a,"datatype") and a.datatype is not None):
        raise TextXSemanticError("unexpected: unknown datatype {}".format(a.datatype), **get_location(a))
    else:
        return t+"&"
    

def _get_open_namespace(model):
    return "namespace "+"::".join(get_package_names(model))+"{\n"


def generate_cpp_from_model(model, base_name, output_file):
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
    item_headers =[]
    for i in item_models:
        base_name, _ = os.path.splitext(os.path.basename(i._tx_filename))
        item_headers.append("{}/{}.{}".format("/".join(get_package_names(i)), base_name, "h"))

    with open(output_file, "w") as f:
        f.write("#ifndef __{}_{}_H\n".format("_".join(get_package_names(model)), base_name.upper()))
        f.write("#define __{}_{}_H\n".format("_".join(get_package_names(model)), base_name.upper()))
        f.write("// ACTIVATE FOR SWIG\n")
        f.write("#include <functional>\n")
        f.write("#include <memory>\n")
        f.write("#include <stdexcept>\n")
        for h in item_headers:
            f.write('#include "{}"\n'.format(h))
        f.write("#ifdef SWIG\n")
        for a in algos:
            f.write("%shared_ptr({})\n".format(fqn(a)))
        f.write("#endif\n")
        f.write(_get_open_namespace(model))
        for a in algos:
            f.write("class {} {{\n".format(a.name))
            f.write('    inline static std::function<std::shared_ptr<{}>()> factory = nullptr;\n'.format(a.name))
            f.write('protected:\n')
            for p in a.parameters:
                f.write('        {} {};\n'.format(fqn(p.type), p.name))
            f.write('public:\n')
            f.write('    virtual ~{}() {{}}\n'.format(a.name))
            f.write('    static const char* get_classname() {{ return "{}"; }}\n'.format(a.name))
            f.write('    static std::shared_ptr<{}> create() {{ if (factory==nullptr) {{ throw std::runtime_error("factory not set."); }} return factory(); }}\n'.format(a.name))
            f.write('    template<class F> static void set_factory(F f) {{ factory=f; }}\n'.format(a.name))
            f.write('    virtual void compute(')
            sep = ""
            for p in a.inputs:
                f.write('{}\n        {} {}'.format(sep, fqn_funcparam(p, "const"), p.name))
                sep=", "
            for p in a.outputs:
                f.write('{}\n        {} {}'.format(sep, fqn_funcparam(p), p.name))
                sep=", "
            f.write('\n    )=0;\n')
            f.write("}}; // struct {}\n".format(a.name))
        f.write("} // close namespace\n")
        f.write("#endif // __{}_{}_H\n".format("_".join(get_package_names(model)),base_name.upper()))
