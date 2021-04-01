from big_example.FixpointExample import *
from big_example.FixpointExample2 import *
import pytest
import numpy as np


def test_fixpoint1_scalars():
    x = FixpointExample()
    x.u1 = 99
    assert x.item_fixpoint_u1 == pytest.approx(9.9)
    x.item_fixpoint_u1 = 8.2
    assert x.u1 == 82

    x.item_fixpoint_u1 = 8.16
    assert x.u1 == 82
    x.item_fixpoint_u1 = 8.24
    assert x.u1 == 82

    x.item_fixpoint_u1 = 8.14
    assert x.u1 == 81
    x.item_fixpoint_u1 = 8.26
    assert x.u1 == 83


def test_fixpoint2_arrays():
    x = FixpointExample()
    x.au1 = [82, 99]
    complete_array = x.item_fixpoint_au1
    assert len(complete_array) == 2
    assert complete_array[0] == pytest.approx(8.2)
    assert complete_array[1] == pytest.approx(9.9)

    assert x.item_fixpoint_au1[0] == pytest.approx(8.2)
    assert x.item_fixpoint_au1[1] == pytest.approx(9.9)

    x.item_fixpoint_au1 = [8.34, 0.16]
    assert x.au1[0] == 83
    assert x.au1[1] == 2


def test_fixpoint3_arrays():
    x = FixpointExample2()
    assert x.md.shape == (2,3)
    x.md = np.array([[20,21,22],[30,31,32]])
    complete_array = x.item_fixpoint_md
    assert complete_array[0,0] == pytest.approx(2.0)