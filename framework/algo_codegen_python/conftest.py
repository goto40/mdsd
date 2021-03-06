from textx import metamodel_for_language, generator_for_language_target
from os.path import abspath, join, dirname, exists
from shutil import rmtree
from os import mkdir
from glob import glob
import sys


def pytest_configure(config):
    this_folder = abspath(dirname(__file__))

    mm = metamodel_for_language("item")
    assert mm is not None
    inpath = join(this_folder, "tests/model/*.item")

    outpath = join(this_folder, "src-gen")
    sys.path.append(outpath)  # add generated code to python path

    mm2 = metamodel_for_language("algo")
    assert mm2 is not None
    inpath2 = join(this_folder, "tests/model/*.algo")

    if exists(outpath):
        rmtree(outpath)
    mkdir(outpath)

    for f in glob(inpath, recursive=True):
        model = mm.model_from_file(f)
        assert model is not None
        gen = generator_for_language_target("item", "python")
        gen(mm, model, output_path=outpath, overwrite=True, debug=False)

    for f in glob(inpath2, recursive=True):
        model = mm2.model_from_file(f)
        assert model is not None
        gen = generator_for_language_target("algo", "python")
        gen(mm2, model, output_path=outpath, overwrite=True, debug=False)
