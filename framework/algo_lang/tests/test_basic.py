import os
from textx import (metamodel_for_language, get_children_of_type,
                   generator_for_language_target)
import shutil
import pytest
from textx.exceptions import TextXSemanticError


def test_parse1():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "basic", "mean_algo.algo"
    )
    mm = metamodel_for_language("algo")
    assert mm is not None
    model = mm.model_from_file(path)
    assert model is not None
    algos = get_children_of_type(mm["Algo"], model)
    assert len(algos) == 1
    assert len(algos[0].parameters) == 1
    assert len(algos[0].inputs) == 1
    assert len(algos[0].outputs) == 1


def test_parse2():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "basic", "mean_algo2.algo"
    )
    mm = metamodel_for_language("algo")
    assert mm is not None
    model = mm.model_from_file(path)
    assert model is not None
    algos = get_children_of_type(mm["Algo"], model)
    assert len(algos) == 1
    assert len(algos[0].parameters) == 1
    assert len(algos[0].inputs) == 1
    assert len(algos[0].outputs) == 1


def test_bad_datatype():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "basic", "mean_algo_bad_datatype.algo"
    )
    mm = metamodel_for_language("algo")
    assert mm is not None
    with pytest.raises(TextXSemanticError):
        mm.model_from_file(path)
