import numpy as np
from functools import reduce


def get_mask(thetype, bfrom, bto):
    return np.left_shift(thetype(np.left_shift(thetype(1) , thetype(bfrom-bto+1)) - 1), thetype(bto))


def get_imask(thetype, bfrom, bto):
    return thetype(np.bitwise_not(get_mask(thetype, bfrom, bto)))


class ArrayLike:
    @property
    def flat(self):
        return self

    def __init__(self, getter, setter, mytype = bool, shape=None):
        self.getter = getter
        self.setter = setter
        self.mytype = mytype
        self.shape = shape

    def _flatten_index(self, idx):
        assert len(idx) == len(self.shape)
        idx0 = 0
        f = 1
        for k in range(len(idx)):
            idx0 += idx[-1 - k] * f
            f *= self.shape[-1 - k]
        return idx0

    def __len__(self):
        return reduce(lambda a,b: a*b, self.shape)

    def __getitem__(self, *idx):
        if len(idx)==1:
            idx0 = idx[0]
        else:
            idx0 = self._flatten_index(idx)
        return self.getter(idx0)

    def __setitem__(self, *args):
        assert len(args) >= 2
        value = args[-1]
        idx = args[0:-1]
        assert isinstance(value, self.mytype)
        if len(idx)==1:
            idx0 = idx[0]
        else:
            idx0 = self._flatten_index(idx)
        self.setter(idx0, value)

    def copy_from(self, a):
        n=reduce(lambda a,b: a*b, self.shape)
        if isinstance(a, list):
            assert len(a) == n
            data = a
        else:
            assert self.shape == a.shape
            data = a.flat
        for i in range(n):
            self.flat[i] = data[i]


_unsigned2signed={
    np.uint64: np.int64,
    np.uint32: np.int32,
    np.uint16: np.int16,
    np.uint8: np.int8
}

def _check_embedded_params(vtype, ctype, start_end_bit):
    assert len(start_end_bit) == 2
    assert start_end_bit[0] >= start_end_bit[1]
    assert start_end_bit[1] >= 0
    assert start_end_bit[0] < np.dtype(ctype).itemsize*8
    assert start_end_bit[0]-start_end_bit[1] < np.dtype(vtype).itemsize*8
    assert np.dtype(vtype).itemsize <= np.dtype(ctype).itemsize
    assert np.issubdtype(ctype, np.unsignedinteger)
    assert np.issubdtype(vtype, np.integer) or vtype == bool
    assert np.issubdtype(vtype, np.unsignedinteger) or start_end_bit[0] >= start_end_bit[1]
    assert np.issubdtype(ctype, np.unsignedinteger)


def get_embedded_from_uint(vtype, cvalue, start_end_bit):
    ctype = type(cvalue)
    _check_embedded_params(vtype,ctype,start_end_bit)
    if np.issubdtype(vtype, np.signedinteger):
        uintvalue = np.right_shift((cvalue & get_mask(ctype, start_end_bit[0], start_end_bit[1])), ctype(start_end_bit[1]))
        if np.right_shift(uintvalue, ctype(start_end_bit[0]-start_end_bit[1])) == 0:
            return vtype(uintvalue)
        else:
            uintvalue = uintvalue | get_imask(ctype, start_end_bit[0]-start_end_bit[1],0)
            return vtype(uintvalue)
    else:
        return vtype(np.right_shift((cvalue & get_mask(ctype, start_end_bit[0], start_end_bit[1])), ctype(start_end_bit[1])))


def set_embedded_in_uint(vvalue, cvalue, start_end_bit):
    ctype = type(cvalue)
    vtype = type(vvalue)
    _check_embedded_params(vtype,ctype,start_end_bit)
    uintvalue = np.left_shift(ctype(ctype(vvalue) & get_mask(ctype, start_end_bit[0]-start_end_bit[1],0)), ctype(start_end_bit[1]))
    return ctype((cvalue & get_imask(ctype, start_end_bit[0], start_end_bit[1])) | uintvalue)
