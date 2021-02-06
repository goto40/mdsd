import mdsd.item_io as io
from big_example.EmbeddedArrayDim2 import *
import numpy as np

def test_embedded1():
    s = EmbeddedArrayDim2()
    s.s2_1 = np.uint8(1)
    s.s2_2 = np.int8(-1)

    assert s.s2_1 == np.uint8(1)
    assert s.s2_2 == np.int8(-1)
