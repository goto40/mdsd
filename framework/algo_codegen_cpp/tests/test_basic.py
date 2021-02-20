import os
from textx import (
    metamodel_for_language,
    generator_for_language_target,
)
import shutil


def test_codegen():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "basic", "mean_algo2.algo"
    )
    mm = metamodel_for_language("algo")
    assert mm is not None
    model = mm.model_from_file(path)
    assert model is not None

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "src-gen")
    gen = generator_for_language_target("algo", "cpp")

    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    gen(mm, model, output_path=path, overwrite=True, debug=False)

    cpp_code = open(os.path.join(path, "P1", "P2", "MeanAlgo.h")).read()
    print(cpp_code)
    assert "struct MeanAlgo" in cpp_code
    assert "shared_ptr<const Items::MeanAlgo" not in cpp_code
    assert "shared_ptr<Items::MeanAlgo" not in cpp_code


def test_codegen_cpp():
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
    gen = generator_for_language_target("algo", "cpp")

    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    gen(mm, model, output_path=path, overwrite=True, debug=False)

    cpp_code = open(os.path.join(path, "P1", "MeanAlgo.h")).read()
    print(cpp_code)
    assert "struct MeanAlgo" in cpp_code
    assert "shared_ptr<const Items::MeanAlgo" in cpp_code
    assert "shared_ptr<Items::MeanAlgo" in cpp_code
