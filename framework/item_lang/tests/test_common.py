from textx import metamodel_for_language
import os
from item_lang.common import get_all_filenames_referenced_by_obj


def test_get_all_files_referenced_by_obj():
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_file(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "model", "props_example.item"
        )
    )
    assert model is not None
    lst = get_all_filenames_referenced_by_obj(model)
    assert len(lst) == 2
