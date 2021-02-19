from textx import metamodel_for_language
from pytest import raises
from item_lang.common import get_referenced_elements_of_enum


def test_enum1():
    text = r"""
    package example
    constants C {
        constant true : built_in.bool = 1
    }
    enum OnOff : built_in.bool {
        value ON = C.true
        value OFF = 0
    }
    enum ABC : built_in.uint2 (.description="test") {
        value A = 0 (.description="test")
        value B = 1 (.description="test")
        value C = 2 (.description="test")
    }
    enum SABC : built_in.int32 (.description="test") {
        value A = 0 (.description="test")
        value B = -1 (.description="test")
        value C = 2 (.description="test")
    }
    struct Test {
      scalar c : built_in.uint32
      embedded scalar spare : built_in.int20
      embedded scalar abc : ABC
      embedded array onoffs : OnOff[10]
      scalar d : SABC
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    assert len(model.package.items) == 4

    onoff = model.package.items[0]
    assert onoff.name == "OnOff"
    refs = get_referenced_elements_of_enum(onoff)
    assert len(refs) == 1


def test_variant_with_enum1():
    text = r"""
    package example
    struct E1 {
        scalar x: built_in.uint32
    }
    struct E2 {
        scalar y: built_in.uint32
    }
    enum ABC8 : built_in.uint8 {
        value A = 1
        value B = 2
        value C = 3
    }
    enum ABC2 : built_in.uint2 (.description="test") {
        value A = 0 (.description="test")
        value B = 1 (.description="test")
        value C = 2 (.description="test")
    }
    struct Test {
      scalar sel8 : ABC8
      scalar c: built_in.uint8
      embedded scalar spare: built_in.uint6
      embedded scalar sel2 : ABC2
      variant data8 : sel8 -> {
        A : E1
        B : E1
        C : E2
      }
      variant data2 : sel2 -> {
        A : E1
        B : E1
        C : E2
      }
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None


def test_variant_with_enum1_bad_selector_value99():
    text = r"""
    package example
    struct E1 {
        scalar x: built_in.uint32
    }
    struct E2 {
        scalar y: built_in.uint32
    }
    enum ABC8 : built_in.uint8 {
        value A = 1
        value B = 2
        value C = 3
    }
    enum ABC2 : built_in.uint2 (.description="test") {
        value A = 0 (.description="test")
        value B = 1 (.description="test")
        value C = 2 (.description="test")
    }
    struct Test {
      scalar sel8 : ABC8
      scalar c: built_in.uint8
      embedded scalar spare: built_in.uint6
      embedded scalar sel2 : ABC2
      variant data8 : sel8 -> {
        A : E1
        B : E1
        99 : E2
      }
      variant data2 : sel2 -> {
        A : E1
        B : E1
        C : E2
      }
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with raises(Exception, match=r".*bad type.*"):
        _ = mm.model_from_str(text)


def test_enum_in_formula_error1():
    text = r"""
    package example
    enum ABC8 : built_in.uint8 {
        value A = 1
        value B = 2
        value C = 3
    }
    struct E {
        scalar x: ABC8 (.defaultValue = 3*ENUM ABC8.A)
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with raises(Exception, match=r".*must not be part of a formula.*"):
        _ = mm.model_from_str(text)


def test_enum_in_formula_error2():
    text = r"""
    package example
    enum ABC8 : built_in.uint8 {
        value A = 1
        value B = 2
        value C = 3
    }
    struct E {
        scalar x: ABC8 (.defaultValue = 3*ABC8.A)
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with raises(Exception, match=r".*must not be part of a formula.*"):
        _ = mm.model_from_str(text)


def test_enum_in_formula_no_error():
    text = r"""
    package example
    enum ABC8 : built_in.uint8 {
        value A = 1
        value B = 2
        value C = 3
    }
    struct E {
        scalar x: ABC8 (.defaultValue = ENUM ABC8.A)
        scalar y: ABC8 (.defaultValue = ABC8.A)
        //scalar z: ABC8 (.defaultValue = A)
        //scalar w: ABC8 (.defaultValue = ENUM A)
        scalar v: ABC8 (.defaultValue = example.ABC8.A)
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    mm.model_from_str(text)
