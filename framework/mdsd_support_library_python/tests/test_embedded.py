from mdsd.common import get_mask, get_embedded_from_uint, set_embedded_in_uint
import numpy as np
from pytest import raises


def test_get_mask():
    assert get_mask(np.uint32, 0, 0) == 1
    assert get_mask(np.uint16, 15, 0) == 0xFFFF
    assert get_mask(np.uint32, 31, 0) == 0xFFFFFFFF
    assert get_mask(np.uint16, 15, 8) == 0xFF00
    assert get_mask(np.uint16, 11, 8) == 0x0F00


def test_uint_from():
    with raises(Exception):
        assert get_embedded_from_uint(
            np.uint8, np.uint32(0xFFFFFFFF), [31, 0]
        ) == np.uint32(0xFFFFFFFF)
    assert get_embedded_from_uint(
        np.uint32, np.uint32(0xFFFFFFFF), [31, 0]
    ) == np.uint32(0xFFFFFFFF)
    assert isinstance(
        get_embedded_from_uint(np.uint32, np.uint32(0xFFFFFFFF), [31, 0]), np.uint32
    )
    assert get_embedded_from_uint(np.uint8, np.uint32(0xFFFFFFFF), [7, 0]) == np.uint8(
        0xFF
    )
    assert isinstance(
        get_embedded_from_uint(np.uint8, np.uint32(0xFFFFFFFF), [7, 0]), np.uint8
    )
    assert get_embedded_from_uint(np.uint8, np.uint32(0xFFFFFFFF), [0, 0]) == np.uint8(
        0x1
    )
    assert get_embedded_from_uint(
        np.uint8, np.uint32(0xFFFFFFFF), [31, 31]
    ) == np.uint8(0x1)
    assert get_embedded_from_uint(
        np.uint8, np.uint32(0x0FFFFFFF), [31, 31]
    ) == np.uint8(0x0)
    assert get_embedded_from_uint(
        np.uint8, np.uint32(0xF0FFFFFF), [31 - 4, 31 - 4]
    ) == np.uint8(0x0)
    assert get_embedded_from_uint(
        np.uint8, np.uint32(0xF0FFFFFF), [31 - 3, 31 - 3]
    ) == np.uint8(0x1)

    assert get_embedded_from_uint(bool, np.uint32(0xFFFFFFFF), [31, 31])
    assert not get_embedded_from_uint(bool, np.uint32(0x0FFFFFFF), [31, 31])
    assert isinstance(
        get_embedded_from_uint(bool, np.uint32(0xFFFFFFFF), [31, 31]), bool
    )

    assert get_embedded_from_uint(np.int8, np.uint32(0xFFFFFFFF), [12, 10]) == np.int8(
        -1
    )

    c = set_embedded_in_uint(np.int8(-3), np.uint64(0), [15, 10])
    assert isinstance(c, np.uint64)
    get_embedded_from_uint(np.int8, c, [15, 10]) == np.int8(-3)

    c = set_embedded_in_uint(np.int8(-3), np.uint64(0), [12, 10])
    assert isinstance(c, np.uint64)
    get_embedded_from_uint(np.int8, c, [12, 10]) == np.int8(-3)

    # 3 bits: 0..7
    c = np.bitwise_not(np.uint64(0x0))
    for x in range(0, 8):
        assert x >= 0 and x < 8
        c = set_embedded_in_uint(np.uint8(x), c, [60, 58])
        assert isinstance(c, np.uint64)
        assert get_embedded_from_uint(np.uint8, c, [60, 58]) == np.uint8(x)
    assert isinstance(c, np.uint64)
    assert c == np.bitwise_not(np.uint64(0x0))

    c = set_embedded_in_uint(np.uint8(8), c, [60, 58])
    assert isinstance(c, np.uint64)
    get_embedded_from_uint(np.uint8, c, [60, 58]) != np.uint8(8)

    # 3 bits: -4..3
    c = np.bitwise_not(np.uint64(0x0))
    for x in range(-4, 4):
        assert x >= -4 and x < 4
        c = set_embedded_in_uint(np.int8(x), c, [60, 58])
        assert isinstance(c, np.uint64)
        ret = get_embedded_from_uint(np.int8, c, [60, 58])
        assert ret == np.int8(x)

    c = set_embedded_in_uint(np.int8(-1), c, [60, 58])
    assert c == np.bitwise_not(np.uint64(0x0))

    c = np.uint64(0x0)
    c = set_embedded_in_uint(np.int8(-1), c, [60, 58])
    c = set_embedded_in_uint(np.int8(0), c, [60, 58])
    assert c == np.uint64(0x0)
