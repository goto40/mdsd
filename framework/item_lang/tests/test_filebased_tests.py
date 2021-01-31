from textx import metamodel_for_language, TextXSemanticError
import os, glob
from codegen_test_support import get_expected_error_regex
import pytest


def test_filebased_tests():
    mm = metamodel_for_language("item")
    assert mm is not None

    good_files = glob.glob(
        os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "model","filebased_tests","**","good*.item"),
        recursive=True)

    print(f"good files found: {len(good_files)}")
    assert len(good_files) > 0
    for f in good_files:
        model = mm.model_from_file(f)
        assert model is not None

    bad_files = glob.glob(
        os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "model","filebased_tests","**","bad*.item"),
        recursive=True)

    print(f"bad files found: {len(bad_files)}")
    assert len(bad_files) > 0
    for f in bad_files:
        error_regex = get_expected_error_regex(f)
        with pytest.raises(TextXSemanticError, match=error_regex):
            mm.model_from_file(f)
