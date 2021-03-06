import numpy as np
from functools import reduce


def array2str(a):
    idx = np.where(a == np.uint8(0))
    idx = idx[0]
    if len(idx) > 0:
        return a[0 : idx[0]].tobytes().decode("utf-8")
    else:
        return a.tobytes().decode("utf-8")


def str2array(t, n):
    x = np.frombuffer(t.encode("utf-8"), dtype=np.uint8)
    if len(x) > n:
        return x[0:n]
    elif len(x < n):
        return np.concatenate((x, np.zeros((n - len(x)))))
    else:
        return x


def get_mask(thetype, bfrom, bto):
    return np.left_shift(
        thetype(np.left_shift(thetype(1), thetype(bfrom - bto + 1)) - 1), thetype(bto)
    )


def get_imask(thetype, bfrom, bto):
    return thetype(np.bitwise_not(get_mask(thetype, bfrom, bto)))


class ArrayLike:
    @property
    def flat(self):
        return self

    @property
    def shape(self):
        return self._shape

    def __init__(self, getter, setter, mytype=bool, shape=None):
        self.getter = getter
        self.setter = setter
        self.mytype = mytype
        self._shape = shape

    def _flatten_index(self, idx):
        assert len(idx) == len(self.shape)
        idx0 = 0
        f = 1
        for k in range(len(idx)):
            idx0 += idx[-1 - k] * f
            f *= self.shape[-1 - k]
        return idx0

    def __len__(self):
        return reduce(lambda a, b: a * b, self.shape)

    def item(self, *idx):
        return self.__getitem__(*idx)

    def setitem(self, *args):
        return self.__setitem__(*args)

    def __getitem__(self, *idx):
        if len(idx) == 1:
            idx0 = idx[0]
        else:
            idx0 = self._flatten_index(idx)
        return self.getter(idx0)

    def __setitem__(self, *args):
        assert len(args) >= 2
        value = args[-1]
        idx = args[0:-1]
        mytype = self.mytype
        assert isinstance(value, mytype)
        if len(idx) == 1:
            idx0 = idx[0]
        else:
            idx0 = self._flatten_index(idx)
        self.setter(idx0, value)

    def copy_from(self, a):
        n = reduce(lambda a, b: a * b, self.shape)
        if isinstance(a, list):
            assert len(a) == n
            data = a
        else:
            assert self._shape == a.shape
            data = a.flat
        for i in range(n):
            self.flat[i] = data[i]

    def __repr__(self):
        res="["
        for idx in range(len(self)):
            res+= " " + str(self.flat[idx])
        res+=" ]"
        return res


class FixpointArrayLike:
    
    def __init__(self, item, attrname):
        self.item = item
        self.attrname = attrname
        self.data = getattr(item, attrname)

    @property
    def shape(self):
        return self.data.shape

    def __len__(self):
        return len(self.data)

    def __getitem__(self, *idx):
        return int2float_fixpoint_value(self.item, self.attrname, self.data.item(*idx))

    def __setitem__(self, *args):
        self.data.itemset(*(args[:-1]), float2int_fixpoint_value(self.item, self.attrname, args[-1]))

    def __repr__(self):
        res="["
        for idx in range(len(self)):
            res+= " " + str(self[idx])
        res+=" ]"
        return res


_unsigned2signed = {
    np.uint64: np.int64,
    np.uint32: np.int32,
    np.uint16: np.int16,
    np.uint8: np.int8,
}


def _check_embedded_params(vtype, ctype, start_end_bit):
    assert len(start_end_bit) == 2
    assert start_end_bit[0] >= start_end_bit[1]
    assert start_end_bit[1] >= 0
    assert start_end_bit[0] < np.dtype(ctype).itemsize * 8
    assert start_end_bit[0] - start_end_bit[1] < np.dtype(vtype).itemsize * 8
    assert np.dtype(vtype).itemsize <= np.dtype(ctype).itemsize
    assert np.issubdtype(ctype, np.unsignedinteger)
    assert np.issubdtype(vtype, np.integer) or vtype == bool
    assert (
        np.issubdtype(vtype, np.unsignedinteger) or start_end_bit[0] >= start_end_bit[1]
    )
    assert np.issubdtype(ctype, np.unsignedinteger)


def get_embedded_from_uint(vtype, cvalue, start_end_bit):
    ctype = type(cvalue)
    _check_embedded_params(vtype, ctype, start_end_bit)
    if np.issubdtype(vtype, np.signedinteger):
        uintvalue = np.right_shift(
            (cvalue & get_mask(ctype, start_end_bit[0], start_end_bit[1])),
            ctype(start_end_bit[1]),
        )
        if np.right_shift(uintvalue, ctype(start_end_bit[0] - start_end_bit[1])) == 0:
            return vtype(uintvalue)
        else:
            uintvalue = uintvalue | get_imask(
                ctype, start_end_bit[0] - start_end_bit[1], 0
            )
            return vtype(uintvalue)
    else:
        return vtype(
            np.right_shift(
                (cvalue & get_mask(ctype, start_end_bit[0], start_end_bit[1])),
                ctype(start_end_bit[1]),
            )
        )


def set_embedded_in_uint(vvalue, cvalue, start_end_bit):
    ctype = type(cvalue)
    vtype = type(vvalue)
    _check_embedded_params(vtype, ctype, start_end_bit)
    uintvalue = np.left_shift(
        ctype(ctype(vvalue) & get_mask(ctype, start_end_bit[0] - start_end_bit[1], 0)),
        ctype(start_end_bit[1]),
    )
    return ctype(
        (cvalue & get_imask(ctype, start_end_bit[0], start_end_bit[1])) | uintvalue
    )


def is_fixpoint(item, attrname):
    assert attrname in item._meta, f"{item.__class__.__name__}.{attrname} is not existing"
    my_meta = item._meta[attrname]
    return my_meta["_is_fixpoint"]


def get_fixpoint_config(item, attrname):
    assert is_fixpoint(item, attrname), f"{item.__class__.__name__}.{attrname} is not a fixpoint value"
    my_meta = item._meta[attrname]
    fixpointLsbValue = my_meta["_fixpointLsbValue"]
    fixpointOffsetValue = 0
    if my_meta["__has_fixpointOffsetValue"]:
        fixpointOffsetValue = my_meta["fixpointOffsetValue"]()
    return fixpointLsbValue, fixpointOffsetValue


def int2float_fixpoint_value(item, attrname, intvalue):
    fixpointLsbValue, fixpointOffsetValue = get_fixpoint_config(item, attrname)
    if isinstance(intvalue, list):
        floatvalue = np.array(intvalue)
    return intvalue * fixpointLsbValue + fixpointOffsetValue


def float2int_fixpoint_value(item, attrname, floatvalue):
    fixpointLsbValue, fixpointOffsetValue = get_fixpoint_config(item, attrname)
    if isinstance(floatvalue, list):
        floatvalue = np.array(floatvalue)
    return np.round((floatvalue - fixpointOffsetValue) / fixpointLsbValue)
