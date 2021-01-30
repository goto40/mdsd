from textx import metamodel_for_language
from pytest import raises
from textx.exceptions import TextXSemanticError
from item_lang.common import (get_referenced_elements_of_constants)


def test_constants1():
    text='''
    package abc
    constants MyConstants (.description = "example")
    {
        constant c1: built_in.uint32 = 1 (.description = "constant")
        constant c2: built_in.float = 3.4 (.description = "constant")
    }
    struct Test1 {
        constant c3: built_in.uint32 = 1 (.description = "constant")
        scalar a: built_in.uint32 (.defaultValue = 3*MyConstants.c1)
        scalar b: built_in.uint32 (.defaultValue = c3)
    }
    constants MyConstants2 (.description = "example")
    {
        constant c1: built_in.uint32 = MyConstants.c1 (.description = "constant")
    }
    struct Test2 {
        scalar a: built_in.uint32 (.defaultValue = 3*Test1.c3)
    }
    '''
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    assert len(model.package.constants) == 2
    assert len(model.package.constants[0].constant_entries) == 2
    assert model.package.constants[0].constant_entries[0].name == 'c1'
    assert model.package.constants[0].constant_entries[1].name == 'c2'

    refs = get_referenced_elements_of_constants(model.package.constants[1])
    assert len(refs) == 1


def test_constants1_type_error_in_struct():
    text='''
    package abc
    constants MyConstants (.description = "example")
    {
        constant c1: built_in.uint32 = 1 (.description = "constant")
        constant c2: built_in.float = 3.4 (.description = "constant")
    }
    struct Test1 {
        scalar a: built_in.uint32 (.defaultValue = 3*MyConstants.c2)
    }
    '''
    mm = metamodel_for_language("item")
    assert mm is not None
    with raises(TextXSemanticError, match=r".*must be an INT/UINT for.*"):
        mm.model_from_str(text)


def test_constants1_type_error1():
    text='''
    package abc
    constants MyConstants (.description = "example")
    {
        constant c2: built_in.float = 3 (.description = "constant") // ok (int -> float)
        constant c1: built_in.uint32 = 1.2 (.description = "constant") // error
    }
    '''
    mm = metamodel_for_language("item")
    assert mm is not None

    with raises(TextXSemanticError, match=r".*c1 must be an INT/UINT for.*"):
        _ = mm.model_from_str(text)


def test_constants1_type_error2():
    text='''
    package abc
    constants MyConstants (.description = "example")
    {
        constant c2: built_in.float = 3 (.description = "constant") // ok (int -> float)
        constant c1: built_in.uint32 = -1 (.description = "constant") // error
    }
    '''
    mm = metamodel_for_language("item")
    assert mm is not None

    with raises(TextXSemanticError, match=r".*c1 must be an UINT for.*"):
        _ = mm.model_from_str(text)


def test_constants_with_formulas_and_wrong_valueClassificator():
    text='''
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
            array c: built_in.uint32[4*ENUM MyConstants.c1]
        }
    }
    '''
    mm = metamodel_for_language("item")
    assert mm is not None
    with raises(TextXSemanticError, match=r".*referenced value is not matching classificator 'ENUM'.*"):
        mm.model_from_str(text)
