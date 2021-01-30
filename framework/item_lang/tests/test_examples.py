from textx import metamodel_for_language, generator_for_language_target
import os
import pytest
from textx.exceptions import TextXSemanticError
from textx import get_children_of_type
from item_lang import lang
from item_lang.common import (get_referenced_elements_of_struct)


def test_example0():
    text = r"""
    package P1.P2.P3
    struct Point {
      scalar x : built_in.float
      scalar y : built_in.float
    }
    """
    mm = lang.metamodel()
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None


def test_example0_alt_syntax():
    text = r"""
    package P1 {
        package P2 {
            package P3 {
                struct Point {
                  scalar x : built_in.float
                  scalar y : built_in.float
                }
            }
        }
    }
    """
    mm = lang.metamodel()
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None


def test_example1():
    text = r"""
    package P1.P2.P3
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
    struct ColoredTriangle {
      array color : built_in.float[3]
      array points : Point[3]
    }    
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    items = get_children_of_type("Struct", model)
    assert len(items) == 4


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
    items = get_children_of_type("Struct", model)
    assert len(items) == 4

    refs = get_referenced_elements_of_struct(items[3])
    assert len(refs) == 3


def test_example2_fail_with_nonstruct_variant():
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
            1:  built_in.float         // not allowed
            10: Point
            11: Line
            12: Circle
        }
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with pytest.raises(TextXSemanticError):
        mm.model_from_str(text)


def test_example2_fail_bad_attr_name():
    text = r"""
    package example
    struct Point {
      scalar x : built_in.float
      scalar item_y : built_in.float
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with pytest.raises(TextXSemanticError):
        mm.model_from_str(text)


def test_example3_load_and_import():
    mm = metamodel_for_language("item")
    assert mm is not None
    with pytest.raises(FileNotFoundError):
        mm.model_from_file("unknown.item")


def test_example4_load_and_import():
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_file(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model","a.item"))
    assert model is not None

