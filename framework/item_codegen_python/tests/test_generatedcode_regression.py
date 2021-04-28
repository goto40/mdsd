import mdsd.item.io as io
from big_example.Headers1 import *
import numpy as np


def test_regression_instance_check():
    a = Headers1()
    b = Headers1()
    assert id(a.header) != id(a.header_extra)
    assert id(a.header) != id(b.header)  # this can fail, if the "default" value
    # in dataclasses are not created by a factory
