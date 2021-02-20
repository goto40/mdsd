import os
import shutil
from textx import (
    metamodel_for_language,
    generator_for_language_target,
    get_children_of_type,
)


def test_attr_formula1():
    text = r"""
    package example
    struct Image {
      scalar w: built_in.uint32
      scalar h: built_in.uint32
      array pixel : built_in.float[w*h]
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    items = get_children_of_type("Struct", model)
    assert len(items) == 1

    model._tx_filename = "example.item"
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "src-gen")
    gen1 = generator_for_language_target("item", "cpp")
    gen2 = generator_for_language_target("item", "python")

    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    gen1(mm, model, output_path=path, overwrite=True, debug=False)
    gen2(mm, model, output_path=path, overwrite=True, debug=False)

    cpp_code = open(os.path.join(path, "example", "Image.h")).read()
    print(cpp_code)
    assert "struct Image" in cpp_code
    assert "s.w*s.h" in cpp_code


def test_constants_with_formulas():
    text = """
    package abc {
        constants MyConstants (.description = "example")
        {
            constant c1: built_in.uint32 = 1 (.description = "constant")
            constant c2: built_in.float = 3.4 (.description = "constant")
            constant c3: built_in.uint32 = MyConstants.c1 (.description = "constant")
            constant c4: built_in.uint32 = c1 (.description = "constant")
        }
        struct A {
            array a: built_in.uint32[2*abc.MyConstants.c1]
            array b: built_in.uint32[3*MyConstants.c1]
            array c: built_in.uint32[4*CONST MyConstants.c1]
        }
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None

    model._tx_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "mymodel.txt"
    )
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "src-gen")
    gen1 = generator_for_language_target("item", "cpp")
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    gen1(mm, model, output_path=path, overwrite=True, debug=False)
    cpp_code = open(os.path.join(path, "abc", "A.h")).read()
    print(cpp_code)
    assert "2*abc::MyConstants::c1" in cpp_code
    assert "3*abc::MyConstants::c1" in cpp_code
    assert "4*abc::MyConstants::c1" in cpp_code


def test_example2():
    text = r"""
    package example
    struct Point {
      scalar x : built_in.float
      scalar y : built_in.float
    }
    struct Line {
      scalar p1 : Point
      scalar p2 : Point
    }
    struct Circle {
      scalar center : Point
      scalar radius : built_in.float
    }
    struct VariantExample {
        scalar selector: built_in.uint32
        variant payload: selector -> {
            10: Point
            11: Line
            12: Circle
        }
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None

    model._tx_filename = "example.item"
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "src-gen")
    gen1 = generator_for_language_target("item", "cpp")
    gen2 = generator_for_language_target("item", "python")

    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    gen1(mm, model, output_path=path, overwrite=True, debug=False)
    gen2(mm, model, output_path=path, overwrite=True, debug=False)

    cpp_code = open(os.path.join(path, "example", "VariantExample.h")).read()
    print(cpp_code)
    assert "switch(s.selector)" in cpp_code
    assert "std::variant" in cpp_code


def test_props_load_and_import():
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_file(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "model", "props_example.item"
        )
    )
    assert model is not None

    model._tx_filename = "example.item"
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "src-gen")
    gen1 = generator_for_language_target("item", "cpp")

    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    gen1(mm, model, output_path=path, overwrite=True, debug=False)

    cpp_code = open(os.path.join(path, "example", "X.h")).read()
    print(cpp_code)
    assert "minValue" in cpp_code
    assert "maxValue" in cpp_code
    assert "myprop1" in cpp_code
    assert "myprop2" in cpp_code
    assert "myprop3" not in cpp_code
