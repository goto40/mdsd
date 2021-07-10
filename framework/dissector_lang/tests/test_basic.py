import os
from textx import (
    metamodel_for_language,
)
import pytest
from textx.exceptions import TextXSemanticError


def test_parse1():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "basic", "example.dissector"
    )
    mm = metamodel_for_language("dissector")
    assert mm is not None
    model = mm.model_from_file(path)
    assert model is not None
    assert model.dissector.name == "MyDissector"
    assert model.dissector.item.name == "VariantExample"
