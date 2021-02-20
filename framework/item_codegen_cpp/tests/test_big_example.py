from textx import (
    metamodel_for_language,
    generator_for_language_target,
    get_children_of_type,
)
from os.path import join, abspath, dirname, exists
from os import mkdir
from shutil import rmtree
from codegen_test_support import check_file
from item_codegen_cpp.common import output_filename


this_folder = abspath(dirname(__file__))


def test_big_example():
    mm = metamodel_for_language("item")
    assert mm is not None

    inpath = join(this_folder, "model")

    model = mm.model_from_file(join(inpath, "big_example.item"))
    assert model is not None

    outpath = join(this_folder, "src-gen")
    gen = generator_for_language_target("item", "cpp")

    if exists(outpath):
        rmtree(outpath)
    mkdir(outpath)
    gen(mm, model, output_path=outpath, overwrite=True, debug=False)

    refpath = join(inpath, "ref")

    structs = get_children_of_type("Struct", model)
    enums = get_children_of_type("Enum", model)
    constants = get_children_of_type("Constants", model)

    for s in structs + enums + constants:
        check_file(
            filename=output_filename(outpath, s),
            regex_reference_filename=output_filename(refpath, s, "regex_ref"),
        )
