import big_example.Header
import big_example.Point
import big_example.Polygon
import big_example.Color
import big_example.Triangle
import big_example.MultiMessage
import big_example.Info
import big_example.EmbeddedArrayDim
import big_example.EmbeddedArrayDim2
import big_example.NDPoint
import big_example.VersionedData
import big_example.Headers1
import big_example.Headers2
import big_example.Headers3
import big_example.Headers4
import big_example.Headers5_noheader
import big_example.Headers6_noheader
import big_example.FixpointExample
import big_example.FixpointExample2

from mdsd.item.io import copy_to_mem, count_bytes, copy_from_mem
from os.path import join, dirname, exists
from mdsd.item.init_values import init_max_values, init_default_values, init_min_values
import os
import shutil
from io import StringIO
from mdsd.item.printto import printto

Types = [
    big_example.Header.Header,
    big_example.Point.Point,
    big_example.Polygon.Polygon,
    big_example.Color.Color,
    big_example.Triangle.Triangle,
    big_example.MultiMessage.MultiMessage,
    big_example.Info.Info,
    big_example.EmbeddedArrayDim.EmbeddedArrayDim,
    big_example.EmbeddedArrayDim2.EmbeddedArrayDim2,
    big_example.NDPoint.NDPoint,
    big_example.VersionedData.VersionedData,
    big_example.Headers1.Headers1,
    big_example.Headers2.Headers2,
    big_example.Headers3.Headers3,
    big_example.Headers4.Headers4,
    big_example.Headers5_noheader.Headers5_noheader,
    big_example.Headers6_noheader.Headers6_noheader,
    big_example.FixpointExample.FixpointExample,
    big_example.FixpointExample2.FixpointExample2,
]


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
                printto(obj, f2)
                text_version = f2.getvalue()
                read_back_text_version = f2.getvalue()
        with open(filename_txt, "w") as f:
            f.write(text_version)

        assert len(text_version) > 0
        assert text_version == read_back_text_version

    for t in Types:
        create_and_save_and_reload(t, init_default, "default")
        create_and_save_and_reload(t, init_min, "min")
        create_and_save_and_reload(t, init_max, "max")
