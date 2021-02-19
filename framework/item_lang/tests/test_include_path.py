from textx import metamodel_for_language, generator_for_language_target
import os
import pytest
from item_lang import lang


def test_example_search_path():
    mm = metamodel_for_language("item")
    assert mm is not None
    with pytest.raises(FileNotFoundError, match=".*No such file or directory.*"):
        mm.model_from_file(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "model",
                "search_path",
                "test_a.item",
            )
        )
    os.environ["ITEM_LANG_SEARCH_PATH"] = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "model", "search_path", "a"
    )
    mm2 = lang.metamodel()
    model = mm2.model_from_file(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "model",
            "search_path",
            "test_a.item",
        )
    )
    assert model is not None
