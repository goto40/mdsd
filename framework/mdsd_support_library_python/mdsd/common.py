import numpy as np


def get_mask(thetype, bfrom, bto):
    return thetype(((thetype(1) << (bfrom-bto+1)) - 1) << bto)


def get_imask(thetype, bfrom, bto):
    return thetype(np.bitwise_not(get_mask(thetype, bfrom, bto)))


class ArrayLike:
    def __init__(self, getter, setter, mytype = bool):
        self.getter = getter
        self.setter = setter
        self.mytype = mytype

    def __getitem__(self, idx):
        return self.getter(idx)

    def __setitem__(self, idx, value):
        assert isinstance(value, self.mytype)
        self.setter(idx, value)

_unsigned2signed={
    np.uint64: np.int64,
    np.uint32: np.int32,
    np.uint16: np.int16,
    np.uint8: np.int8
}

def get_embedded_from_uint(vtype, cvalue, start_end_bit):
    ctype = type(cvalue)
    assert len(start_end_bit) == 2
    assert start_end_bit[0] >= start_end_bit[1]
    assert start_end_bit[1] >= 0
    assert start_end_bit[0] < np.dtype(ctype).itemsize*8
    assert start_end_bit[0]-start_end_bit[1] < np.dtype(vtype).itemsize*8
    assert np.dtype(vtype).itemsize <= np.dtype(ctype).itemsize
    assert np.issubdtype(ctype, np.unsignedinteger)
    assert np.issubdtype(vtype, np.integer)
    assert np.issubdtype(vtype, np.unsignedinteger) or start_end_bit[0] >= start_end_bit[1]
    assert isinstance(cvalue, np.unsignedinteger)
    if np.issubdtype(vtype, np.signedinteger):
        uintvalue = (cvalue & get_mask(ctype, start_end_bit[0], start_end_bit[1])) >> start_end_bit[1]
        if uintvalue >> (start_end_bit[0]-start_end_bit[1]-1) == 0:
            return vtype(uintvalue)
        else:
            uintvalue = uintvalue | get_imask(ctype, start_end_bit[0]-start_end_bit[1],0)
            return vtype(uintvalue)
    else:
        return vtype((cvalue & get_mask(ctype, start_end_bit[0], start_end_bit[1])) >> start_end_bit[1])
