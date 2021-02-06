import mdsd.item_io as io
from big_example.EmbeddedArrayDim2 import *
import numpy as np

def test_embedded1():
    s = EmbeddedArrayDim2()
    s.s2_1 = np.uint8(1)
    s.s2_2 = np.int8(-1)

    s.a3_1 = [np.uint8(a%8) for a in range(16)]
    for k in range(16):
        assert s.a3_1[k] == (k%8)

    x = [np.int8((a%8)-4) for a in range(16)]
    x.reverse()
    print(x)
    s.a3_2 = x
    for k in range(16):
        print(s.a3_2[k])
        assert s.a3_2[k] == x[k]


    assert s.s2_1 == np.uint8(1)
    assert s.s2_2 == np.int8(-1)
