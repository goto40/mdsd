import os
from textx import metamodel_for_language, get_children_of_type
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

    cpp_code = open(os.path.join(path, "P1", "P2", "mean_algo2.h")).read()
    print(cpp_code)
    assert "struct MeanAlgo" in cpp_code
    assert "shared_ptr<const Items::MeanAlgo" not in cpp_code
    assert "shared_ptr<Items::MeanAlgo" not in cpp_code


def test_bad_datatype():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "basic", "mean_algo_bad_datatype.algo"
    )
    mm = metamodel_for_language("algo")
    assert mm is not None
    with pytest.raises(TextXSemanticError):
        mm.model_from_file(path)


def test_codegen_cpp():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "basic", "mean_algo_with_shared_ptr.algo"
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

    cpp_code = open(os.path.join(path, "P1", "mean_algo_with_shared_ptr.h")).read()
    print(cpp_code)
    assert "struct MeanAlgo" in cpp_code
    assert "shared_ptr<const Items::MeanAlgo" in cpp_code
    assert "shared_ptr<Items::MeanAlgo" in cpp_code

def test_codegen_python():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "basic", "mean_algo_with_shared_ptr.algo"
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

    py_code = open(os.path.join(path, "P1", "mean_algo_with_shared_ptr.py")).read()
    print(py_code)
    assert "class MeanAlgo" in py_code
    assert "Items.data.MeanAlgo" in py_code
