from textx import metamodel_for_language
from pytest import raises
from textx.exceptions import TextXSemanticError
from item_lang.common import get_bits, get_start_end_bit


def test_embedded1():
    text = r"""
    package example
    struct Point {
      scalar a : built_in.uint32
      scalar c : built_in.uint32
      validation_embedded scalar x : built_in.int20
      validation_embedded scalar y : built_in.int12
      scalar d : built_in.uint32
    }
    struct Other {
      scalar a : built_in.uint32
      scalar c : built_in.uint32
      validation_embedded scalar x : built_in.int20
      validation_embedded array y : built_in.int2[6]
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    assert len(model.package.items) == 2

    assert not model.package.items[0].attributes[0].embedded
    assert not model.package.items[0].attributes[1].embedded
    assert model.package.items[0].attributes[2].embedded
    assert model.package.items[0].attributes[3].embedded
    assert not model.package.items[0].attributes[4].embedded

    assert model.package.items[0].get_next_attr(model.package.items[0].attributes[1]) is model.package.items[0].attributes[2]

    assert not model.package.items[0].attributes[0].is_container()
    assert model.package.items[0].attributes[1].is_container()
    assert not model.package.items[0].attributes[2].is_container()
    assert not model.package.items[0].attributes[3].is_container()
    assert not model.package.items[0].attributes[4].is_container()

    with raises(Exception):
        get_bits( model.package.items[0] )
    assert get_bits(model.package.items[0].attributes[1].type)==32
    assert get_bits(model.package.items[0].attributes[2].type)==20

    assert get_start_end_bit(model.package.items[0].attributes[2]) == (31,12)
    assert get_start_end_bit(model.package.items[0].attributes[3]) == (11,0)

    assert get_start_end_bit(model.package.items[1].attributes[2]) == (31,12)
    assert get_start_end_bit(model.package.items[1].attributes[3]) == (11,0)

    assert len(model.package.items[0].attributes[1].get_container_elements())==2
    with raises(Exception):
        model.package.items[0].attributes[2].get_container_elements()
    with raises(Exception):
        model.package.items[0].attributes[3].get_container_elements()
    with raises(Exception):
        model.package.items[0].attributes[4].get_container_elements()


def test_embedded_error_in_embedded_field1():
    text = r"""
    package example
    struct Point {
      scalar c : built_in.uint64
      validation_embedded scalar x : built_in.float
      validation_embedded scalar y : built_in.int32
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with raises(TextXSemanticError, match=r".*attribute x must be an integral type"):
        mm.model_from_str(text)


def test_embedded_error_in_sum_of_bits1():
    text = r"""
    package example
    struct Point {
      scalar c : built_in.uint32
      validation_embedded scalar x : built_in.int20
      validation_embedded scalar y : built_in.int13
      validation_embedded scalar z : built_in.bool
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with raises(TextXSemanticError, match=r".*validation_embedded elements of container c .34. do not sum up to 32.*"):
        mm.model_from_str(text)


def test_embedded_error_in_type_of_container():
    text = r"""
    package example
    struct Point {
      scalar c : built_in.int32
      validation_embedded scalar x : built_in.int20
      validation_embedded scalar y : built_in.int12
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None
    with raises(TextXSemanticError, match=r".*container c must be an unsigned integral type.*"):
        mm.model_from_str(text)


def test_embedded_badtype1():
    text = r"""
    package example
    struct Point {
      scalar c : built_in.uint33 // error!
      validation_embedded scalar x : built_in.int21
      validation_embedded scalar y : built_in.int12
    }
    """
    mm = metamodel_for_language("item")
    assert mm is not None

    with raises(TextXSemanticError, match=r".*attribute c must have a bit.*power of two.*"):
        mm.model_from_str(text)
