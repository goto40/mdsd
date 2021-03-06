import os
from textx import (
    metamodel_for_language,
    generator_for_language_target,
)
import shutil


def test_codegen_python():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "basic",
        "mean_algo_with_shared_ptr.algo",
    )
    mm = metamodel_for_language("algo")
    assert mm is not None
    model = mm.model_from_file(path)
    assert model is not None

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "src-gen")
    gen = generator_for_language_target("algo", "python")

    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    gen(mm, model, output_path=path, overwrite=True, debug=False)

    py_code = open(os.path.join(path, "P1", "MeanAlgo.py")).read()
    print(py_code)
    assert "class MeanAlgo" in py_code
    assert "i:Items.MeanAlgoInput.MeanAlgoInput" in py_code
