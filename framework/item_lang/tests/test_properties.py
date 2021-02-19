from textx import metamodel_for_language
from textx import get_children_of_type
from textx.exceptions import TextXSemanticError
import os
import pytest
from item_lang.properties import (
    get_property,
    has_property,
    get_all_possible_properties,
    get_all_possible_mandatory_properties,
    get_property_set,
)
from item_lang.properties import get_property_type


def test_property_set1():
    text = r"""
    package example (property_set built_in.default_properties)
    struct X {
        scalar x : built_in.int32
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    items = get_children_of_type("Struct", model)
    assert len(items) == 1
    assert get_property_set(items[0]) is not None
    assert get_property_set(items[0]).name == "default_properties"


def test_property_set2_default_properties():
    text = r"""
    package example
    struct X {
        scalar x : built_in.int32
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    items = get_children_of_type("Struct", model)
    assert len(items) == 1
    assert get_property_set(items[0]) is not None
    assert get_property_set(items[0]).name == "default_properties"


def test_property1():
    text = r"""
    package example
    
    struct Point {
      scalar x : built_in.float (.minValue=0.1, .defaultValue=1, .maxValue=1e5)
      scalar y : built_in.float (.defaultValue=0x0aB, .description="Hello")
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

    Point = items[0]
    assert Point.name == "Point"
    assert len(Point.attributes[0].properties) == 3
    assert len(Point.attributes[1].properties) == 2
    assert Point.attributes[1].properties[0].definition.name == "defaultValue"
    assert Point.attributes[1].properties[0].numberValue.x.compute_formula() == 0xAB
    assert Point.attributes[1].properties[1].textValue.x == "Hello"

    assert get_property(Point.attributes[1], "defaultValue") == 0xAB
    assert get_property(Point.attributes[1], "description") == "Hello"

    assert has_property(Point.attributes[1], "defaultValue")
    assert has_property(Point.attributes[1], "description")
    assert not has_property(Point.attributes[1], "minValue")
    assert not has_property(Point.attributes[1], "maxValue")

    pdefs = get_all_possible_properties(Point, filter_applicable_to_model_object=False)
    assert len(pdefs) >= 6


def test_property2():
    text = r"""
    package example.one (property_set example.one.ProjExt)
    property_set ProjExt {
        property optional myprop1: STRING
        property myprop2: ATTRTYPE
    }
    struct A {
        scalar x: built_in.int32 (.description="a", .myprop2=1)
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    items = get_children_of_type("Struct", model)
    assert len(items) == 1

    pdefs = get_all_possible_properties(items[0].attributes[0])
    assert len(pdefs) >= 7

    assert "minValue" in pdefs
    assert "maxValue" in pdefs
    assert "defaultValue" in pdefs
    assert "description" in pdefs
    assert "myprop1" in pdefs
    assert "myprop2" in pdefs
    pdefs["myprop1"].internaltype == "STRING"
    pdefs["myprop2"].internaltype == "ATTRTYPE"

    pdefs = get_all_possible_mandatory_properties(items[0].attributes[0])
    assert len(pdefs) == 1
    assert "myprop2" in pdefs


def test_props_load_and_import():
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_file(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "model", "props_example.item"
        )
    )
    assert model is not None

    items = get_children_of_type("Struct", model)
    assert len(items) == 1
    i = items[0]
    assert len(i.attributes[0].properties) == 2

    assert has_property(i.attributes[0], "myprop1")
    assert has_property(i.attributes[0], "myprop2")
    assert get_property(i.attributes[0], "myprop1") is True
    assert get_property(i.attributes[0], "myprop2") == "Hello"
    assert not has_property(i.attributes[0], "minValue")
    assert not has_property(i.attributes[0], "maxValue")
    with pytest.raises(TextXSemanticError, match=r".*max.*"):
        has_property(i.attributes[0], "max")


def test_property1_bad_type1():
    text = r"""
    package example

    struct Point {
      scalar x : built_in.uint32 (.minValue=0.1, .defaultValue=1, .maxValue=1e5)
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with pytest.raises(TextXSemanticError, match=r".*error: minValue must be an INT.*"):
        mm.model_from_str(text)


def test_property1_bad_type2():
    text = r"""
    package example

    struct Point {
      scalar x : built_in.uint32 (.description=123)
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with pytest.raises(
        TextXSemanticError, match=r".*error: description must be a STRING.*"
    ):
        mm.model_from_str(text)


def test_property1_bad_type3():
    text = r"""
    package example(property_set X)
    property_set X {
        property test: ATTRTYPE    
    }
    struct Point {
      scalar x : built_in.uint32 (.test=1.2)
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with pytest.raises(TextXSemanticError, match=r".*error: test must be an INT.*"):
        mm.model_from_str(text)


def test_property1_bad_type4():
    text = r"""
    package example(property_set X)
    property_set X {
        property test: ATTRTYPE    
    }
    struct Point {
      scalar x : built_in.uint32 (.test="no str allowed here")
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with pytest.raises(TextXSemanticError, match=r".*error: test must be .*INT.*"):
        mm.model_from_str(text)


def test_property1_no_constexpr():
    text = r"""
    package example

    struct Point {
      scalar z : built_in.uint32 (.description="do not use in formula")
      scalar x : built_in.uint32 (.defaultValue=2+z)
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with pytest.raises(Exception, match=r".*no constexpr.*"):
        mm.model_from_str(text)


def test_property1_get_property_type():
    text = r"""
    package example(property_set X)
    
    property_set X {
        property optional test: INT
        property optional test2: BOOL
        property optional test3: STRING
    }

    struct Point {
      scalar x : built_in.uint64 (.defaultValue=2)
      scalar y : built_in.double (.defaultValue=2.0, .test=3, .test2=1, .test3="hello")
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    m = mm.model_from_str(text)
    assert m.package.items[0].name == "Point"

    x = m.package.items[0].attributes[0]
    y = m.package.items[0].attributes[1]
    assert x.name == "x"
    assert y.name == "y"

    x_defaultValue = x.properties[0]
    y_defaultValue = y.properties[0]
    y_test = y.properties[1]
    y_test2 = y.properties[2]
    y_test3 = y.properties[3]
    assert x_defaultValue.definition.name == "defaultValue"
    assert y_defaultValue.definition.name == "defaultValue"
    assert y_test.definition.name == "test"
    assert y_test2.definition.name == "test2"
    assert y_test3.definition.name == "test3"

    assert get_property_type(x, "defaultValue").name == "uint64"
    assert get_property_type(y, "defaultValue").name == "double"
    assert get_property_type(y, "test").name == "int32"
    assert get_property_type(y, "test2").name == "bool"
    assert get_property_type(y, "test3") is str


def test_property1_defaultStringValue():
    text = r"""
    package example

    struct Point {
      scalar x : built_in.uint32 (.defaultStringValue="xxx")
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with pytest.raises(Exception, match=r".*defaultStringValue.*"):
        mm.model_from_str(text)
