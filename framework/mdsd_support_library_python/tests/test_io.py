import mdsd_support_library.item_support as support
import mdsd_support_library.item_io as io
from items.Point import *
import numpy as np
import pytest


def test_basic():
    p=Point(1,2)
    assert p.x==1
    assert p.y==2
    mem = bytearray(1000)
    n = io.copy_to_mem(p, mem)
    assert n == 2*np.dtype(np.float32).itemsize
    print(mem[0:n])

    assert n == io.count_bytes(p)

    q=Point(3,4)
    assert q.x != p.x
    assert q.y != p.y

    print(q)
    m = io.copy_from_mem(mem[0:n],q)
    assert m==n
    print(q)

    assert q.x == p.x
    assert q.y == p.y


def test_copy():
    p=Point(1,2)
    q=Point(3,4)
    assert q.x != p.x
    assert q.y != p.y
    io.copy(p,q) is q
    assert q.x == p.x
    assert q.y == p.y
