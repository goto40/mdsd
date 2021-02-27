import click
from project_tool import SwigTool
import os


@click.group()
def swig_tool():
    pass


@swig_tool.command()
@click.option("--require-pattern", nargs=1, type=str, default=None)
@click.argument("module-name", nargs=1)
@click.argument("ouput-path", nargs=1)
@click.argument("header-paths", nargs=-1)
def python_i_file(module_name, ouput_path, header_paths, require_pattern):
    """create i file with imports for python"""
    try:
        if not os.path.exists(ouput_path):
            os.makedirs(ouput_path)
        ouput_i_file = os.path.join(ouput_path, module_name + ".i")
        ouput_setup_file = os.path.join(ouput_path, "setup.py")
        # print(header_paths, ouput_i_file)
        # print('"{}"'.format(require_pattern))
        tool = SwigTool(header_paths, require_pattern)
        tool.analyze()
        h = tool.get_sorted()
        with open(ouput_i_file, "w") as f:
            f.write(create_i_file(h, module_name))
        with open(ouput_setup_file, "w") as f:
            f.write(create_setup_file(module_name, header_paths))
    except Exception as e:
        raise click.ClickException(repr(e))
    except:
        raise click.ClickException("unknown error")


def create_i_file(headers, module_name):
    # ?? #define SWIG_FILE_WITH_INIT
    res = ""
    res += "%include <std_shared_ptr.i>\n"
    res += "%include <stdint.i>\n"
    res += "%include <std_vector.i>\n"
    res += "%include <std_array.i>\n"
    res += "%module {}\n".format(module_name)
    res += """%{
//#define SWIG_PYTHON_STRICT_BYTE_CHAR
#include <stdexcept>
"""
    for h in headers:
        res += '#include "{}"\n'.format(h.path)
    res += "%}\n"
    res += """
%typemap(in) (const std::byte* mem, size_t n) {
    $1 = reinterpret_cast<std::byte*>( PyByteArray_AsString($input) );
    $2 = static_cast<size_t>( PyByteArray_Size($input) );
}
%typemap(in) (std::byte* mem, size_t n) {
    $1 = reinterpret_cast<std::byte*>( PyByteArray_AsString($input) );
    $2 = static_cast<size_t>( PyByteArray_Size($input) );
}

%exception {
        try {
        $action
        }
        catch (std::exception &e) {
                PyErr_SetString(PyExc_Exception,e.what());
                return NULL;
        }
}
"""
    for h in filter(lambda x: x.relevant, headers):
        res += '%include "{}"\n'.format(h.path)
    return res


def create_setup_file(module_name, header_paths):
    includes = ",".join(map(lambda x: "'{}'".format(x), header_paths))
    res = ""
    res += "from setuptools import setup, Extension\n"
    res += "import os\n"
    res += "\n"
    res += 'swig_module_name = "{}"\n'.format(module_name)
    res += """
extra_compile_args = ["-std=c++17"] #, "-Wall", "-Wextra", "-Weffc++"]
swig_module = Extension('_{}'.format(swig_module_name),
                           sources=['wrapper.cpp'.format(swig_module_name)],
"""
    res += "                           include_dirs=[{}],".format(includes)
    res += '''
                           extra_compile_args=extra_compile_args,
                           language='c++17',
                           libraries=['stdc++']
                           )

setup (name = swig_module_name,
       version = '0.0',
       author      = "swig_tool",
       description = """swig wrapper""",
       ext_modules = [swig_module],
       py_modules = [swig_module_name]
       )
'''
    return res


@swig_tool.command()
@click.argument("module-name", nargs=1)
@click.argument("project-path", nargs=1)
def generic_setup_file(module_name, project_path):
    """create a generic setup file"""
    try:
        if not os.path.exists(project_path):
            raise Exception("missing src path {}.".format(project_path))
        ouput_setup_file = os.path.join(project_path, "setup.py")
        with open(ouput_setup_file, "w") as f:
            f.write(create_generic_setup_file(module_name))
    except Exception as e:
        raise click.ClickException(repr(e))
    except:
        raise click.ClickException("unknown error")


def create_generic_setup_file(module_name):
    return '''
from setuptools import setup, find_packages
import os

package_name = "{}"

my_packages = find_packages(where='src-gen/python', exclude=[])

setup (name = package_name,
       version = '0.0',
       author      = "swig_tool",
       description = """generic setup""",
       packages = my_packages,
       package_dir = {{'': '.'}}
       )
'''.format(
        module_name
    )
