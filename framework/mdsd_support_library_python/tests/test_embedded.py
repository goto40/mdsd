from mdsd.common import get_mask, get_embedded_from_uint
import numpy as np
from pytest import raises


def test_get_mask():
    assert get_mask(np.uint32,0,0) == 1
    assert get_mask(np.uint32,31,0) == 0xffffffff
    assert get_mask(np.uint16,15,0) == 0xffff
    assert get_mask(np.uint16,15,8) == 0xff00
    assert get_mask(np.uint16,11,8) == 0x0f00


def test_uint_from():
    with raises(Exception):
        assert get_embedded_from_uint(np.uint8, np.uint32(0xffffffff),[31,0]) == np.uint32(0xffffffff);
    assert get_embedded_from_uint(np.uint32, np.uint32(0xffffffff), [31, 0]) == np.uint32(0xffffffff);
    assert isinstance(get_embedded_from_uint(np.uint32, np.uint32(0xffffffff), [31, 0]), np.uint32)
    assert get_embedded_from_uint(np.uint8, np.uint32(0xffffffff),[7,0]) == np.uint8(0xff);
    assert isinstance(get_embedded_from_uint(np.uint8, np.uint32(0xffffffff),[7,0]), np.uint8);
    assert get_embedded_from_uint(np.uint8, np.uint32(0xffffffff),[0,0]) == np.uint8(0x1);
    assert get_embedded_from_uint(np.uint8, np.uint32(0xffffffff),[31,31]) == np.uint8(0x1);
    assert get_embedded_from_uint(np.uint8, np.uint32(0x0fffffff),[31,31]) == np.uint8(0x0);
    assert get_embedded_from_uint(np.uint8, np.uint32(0xf0ffffff),[31-4,31-4]) == np.uint8(0x0);
    assert get_embedded_from_uint(np.uint8, np.uint32(0xf0ffffff),[31-3,31-3]) == np.uint8(0x1);

    assert get_embedded_from_uint(np.int8, np.uint32(0xffffffff),[12,10]) == np.int8(-1);
