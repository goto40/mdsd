from textx import metamodel_for_language, generator_for_language_target, get_children_of_type
from os.path import join, abspath, dirname, exists
from os import mkdir
from shutil import rmtree
from codegen_test_support import check_file
from item_codegen_python.struct import get_mask
import numpy as np

this_folder = abspath(dirname(__file__))

def test_get_mask():
    assert get_mask(np.uint32,0,0) == 1
    assert get_mask(np.uint32,31,0) == 0xffffffff
    assert get_mask(np.uint16,15,0) == 0xffff
    assert get_mask(np.uint16,15,8) == 0xff00
    assert get_mask(np.uint16,11,8) == 0x0f00


def test_big_example():
    mm = metamodel_for_language("item")
    assert mm is not None

    inpath = join(this_folder, "model")

    model = mm.model_from_file(join(inpath, "big_example.item"))
    assert model is not None

    outpath = join(this_folder, "src-gen")
    gen = generator_for_language_target("item", "python")

    if exists(outpath):
        rmtree(outpath)
    mkdir(outpath)
    gen(mm, model, output_path=outpath, overwrite=True, debug=False)

    refpath = join(inpath, "ref")

    structs = get_children_of_type("Struct", model)
    enums = get_children_of_type("Enum", model)
    constants = get_children_of_type("Constants", model)

#    for s in structs + enums + constants:
#        check_file(
#            filename=output_filename(outpath, s),
#            regex_reference_filename=output_filename(refpath, s, "regex_ref")
#        )
