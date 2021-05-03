from mdsd.item.io import copy_to_mem, count_bytes, copy_from_mem
from mdsd.item_support import compute_length
from os.path import join, dirname, exists
from mdsd.item.init_values import init_max_values, init_default_values, init_min_values
import os
import shutil
from io import StringIO
from mdsd.item.printto import printto
import pytest


def get_all_test_structs():
    import big_example.AllInOne
    return [big_example.AllInOne.AllInOne]


def test_io_bin_output():
    path = join(dirname(__file__), "output")
    if exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    print(path)

    def init_default(o):
        init_default_values(o)
        return o

    def init_min(o):
        init_min_values(o)
        return o

    def init_max(o):
        init_max_values(o)
        return o

    def create_and_save_and_reload(t, func, fname):
        obj = t()
        obj = func(obj)
        n = count_bytes(obj)
        mem = bytearray(n)
        copy_to_mem(obj, mem)
        name = obj.__class__.__name__
        filename = join(dirname(__file__), "output", name + f"_{fname}.bin")
        filename_txt = join(dirname(__file__), "output", name + f"_{fname}.txt")
        with StringIO() as f:
            printto(obj, f)
            text_version = f.getvalue()

        with open(filename, "wb") as f:
            f.write(mem)
        with open(filename, "rb") as f:
            read_back_data = bytearray(f.read())
            read_back_obj = t()
            copy_from_mem(read_back_data, read_back_obj)
            with StringIO() as f2:
                printto(read_back_obj, f2)
                read_back_text_version = f2.getvalue()
        with open(filename_txt, "w") as f:
            f.write(text_version)

        assert len(text_version) > 0
        assert text_version == read_back_text_version
        return text_version

    for t in get_all_test_structs():
        create_and_save_and_reload(t, init_default, "default")
        create_and_save_and_reload(t, init_min, "min")
        create_and_save_and_reload(t, init_max, "max")

    # individual test
    from big_example.AllInOne import AllInOne
    from big_example.OnOff import OnOff
    from big_example.Point import Point
    from mdsd.item_support import adjust_array_sizes_and_variants
    demo = AllInOne()
    for k in range(len(demo.embedded_enum_array)):
        demo.embedded_enum_array[k] = OnOff.ON if k%2==0 else OnOff.OFF
    demo.payload.n = 4
    adjust_array_sizes_and_variants(demo)

    for k in range(len(demo.payload.p)):
        if k<2:
            demo.payload.p[k] = Point(80 + k / 2, 20 + k)
        else:
            demo.payload.p[k].x = 80+k/2
            demo.payload.p[k].y = 20+k
    assert demo.payload.p[0].y == pytest.approx(20)
    assert demo.payload.p[1].y == pytest.approx(21)
    assert demo.payload.p[2].y == pytest.approx(22)
    assert demo.payload.p[3].y == pytest.approx(23)
    n = count_bytes(demo)
    mem = bytearray(n)
    copy_to_mem(demo, mem)
    filename = join(dirname(__file__), "output", "AllInOne_demo.bin")
    with open(filename, "wb") as f:
        f.write(mem)
    with StringIO() as f2:
        printto(demo, f2)
        text_version = f2.getvalue()

    with open(filename, "rb") as f:
        read_back_data = bytearray(f.read())
        read_back_obj = AllInOne()
        copy_from_mem(read_back_data, read_back_obj)
        with StringIO() as f2:
            printto(read_back_obj, f2)
            read_back_text_version = f2.getvalue()
    assert read_back_obj.header.length > 0
    assert read_back_obj.header.length == len(read_back_data)
    # next line is for bugfixing (if the model change, the value changes...)
    # assert read_back_obj.header.length == 342
    assert read_back_obj.header.length == compute_length(read_back_obj)
    assert "ON" in read_back_text_version
    assert text_version == read_back_text_version

    filename_txt = join(dirname(__file__), "output", "AllInOne_demo.txt")
    with open(filename_txt, "w") as f:
        f.write(read_back_text_version)
