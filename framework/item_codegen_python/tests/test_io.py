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

from mdsd.item.io import copy_to_mem, count_bytes
from os.path import join, dirname,exists
import os
import shutil

Types= [
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
    path = join(dirname(__file__), 'output')
    if exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    print(path)

    def init_default(o):
        return o;

    def init_min(o):
        return o;

    def init_max(o):
        return o;

    def create_and_save(t, func, name):
        obj = t()
        obj = func(obj)
        n = count_bytes(obj)
        mem = bytearray(n)
        copy_to_mem(obj,mem)
        name = obj.__class__.__name__
        filename = join(
            dirname(__file__),
            'output',
            name+f"_{name}.bin"
        )
        with open(filename,"wb") as f:
            f.write(mem)

    for t in Types:
        create_and_save(t, init_default, "default")
        create_and_save(t, init_min, "min")
        create_and_save(t, init_max, "max")
