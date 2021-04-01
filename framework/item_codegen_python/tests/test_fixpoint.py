from big_example.FixpointExample import *

def test_fixpoint1():
    x = FixpointExample()
    x.u1 = 99
    assert x.item_fixpoint_u1 == 9.9
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
