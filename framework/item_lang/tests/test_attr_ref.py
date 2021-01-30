from textx import metamodel_for_language
from textx import get_children_of_type
from textx.exceptions import TextXSemanticError
import pytest


def test_attr_ref1():
    text = r"""
    package example
    struct Point {
      scalar x : built_in.float
      scalar y : built_in.float
    }
    struct Polygon {
      scalar n : built_in.uint32
      array points : Point[n]
    }    
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    items = get_children_of_type("Struct", model)
    assert len(items) == 2

    assert not items[1].attributes[1].has_fixed_size()
    r = get_children_of_type("AttrRef", items[1].attributes[1])
    assert len(r) == 1
    assert r[0].ref == items[1].attributes[0]


def test_attr_ref2():
    text = r"""
    package example
    struct Point {
      scalar x : built_in.float
      scalar y : built_in.float
    }
    struct Header {
      scalar n : built_in.uint32
      scalar nb_bytes: built_in.uint32    
    }
    struct Polygon {
      scalar header: Header
      array points : Point[header.n]
    }    
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    items = get_children_of_type("Struct", model)
    assert len(items) == 3

    assert not items[2].attributes[1].has_fixed_size()
    Header = items[1]
    Polygon = items[2]
    r = get_children_of_type("AttrRef", Polygon.attributes[1])
    assert len(r) == 1
    assert r[0].ref == Header.attributes[0]


def test_attr_ref3():
    text = r"""
    package example
    struct Point {
      scalar x : built_in.float
      scalar y : built_in.float
    }
    struct Header {
      scalar n : built_in.uint32
      scalar nb_bytes: built_in.uint32    
    }
    struct Polygon {
      scalar header: Header
      array points : Point[header.not_existant]
    }    
    """
    mm = metamodel_for_language("item")
    with pytest.raises(TextXSemanticError, match=r".*Unknown object.*not_existant.*"):
        mm.model_from_str(text)
