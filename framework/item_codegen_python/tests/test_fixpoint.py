from big_example.FixpointExample import *
import pytest


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


def test_fixpoint2_arrays_enblock():
    x = FixpointExample()
    x.au1 = [82, 99]
    complete_array = x.item_fixpoint_au1
    assert complete_array[0] == pytest.approx(8.2)
    assert complete_array[1] == pytest.approx(9.9)

    x.item_fixpoint_au1 = [8.34, 0.16]
    assert x.au1[0] == 83
    assert x.au1[1] == 2

