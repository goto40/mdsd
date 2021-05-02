import numpy as np
from mdsd.item_support import init_visitor, const_visitor, accept


@init_visitor
class copy_from_mem_visitor:
    def __init__(self, mem: bytearray):
        self.mem = mem
        self.pos = 0

    def visit_scalar(self, struct, attr, meta):
        if meta["_is_embedded"]:
            return
        t = meta["_get_type"]()
        real_t = meta["_get_type"]()
        if meta["_is_enum"]:
            t = meta["_get_underlying_type"]()
        else:
            t = real_t
        n = np.dtype(t).itemsize
        if self.pos + n > len(self.mem):
            raise Exception("out of mem")
        value = np.frombuffer(self.mem, t, 1, self.pos)[0]
        setattr(struct, attr, real_t(value))
        self.pos += n

    def visit_scalar_struct(self, struct, attr, meta):
        accept(getattr(struct, attr), self)

    def visit_array(self, struct, attr, meta):
        if meta["_is_embedded"]:
            return
        real_t = meta["_get_type"]()
        if meta["_is_enum"]:
            t = meta["_get_underlying_type"]()
        else:
            t = real_t
        d = meta["_get_dim"](struct)
        n = np.dtype(t).itemsize
        if self.pos + d * n > len(self.mem):
            raise Exception("out of mem")
        value = np.reshape(
            np.frombuffer(self.mem, t, d, self.pos), meta["_get_dim_nd"](struct)
        )
        setattr(struct, attr, np.array(value, dtype=real_t))
        self.pos += d * n

    def visit_array_struct(self, struct, attr, meta):
        for s in getattr(struct, attr):
            accept(s, self)


@const_visitor
class copy_to_mem_visitor:
    def __init__(self, mem: bytearray):
        self.mem = mem
        self.pos = 0

    def visit_scalar(self, struct, attr, meta):
        if meta["_is_embedded"]:
            return
        t = meta["_get_type"]()
        n = np.dtype(t).itemsize
        if meta["_is_enum"]:
            n = np.dtype(meta["_get_underlying_type"]()).itemsize
        if self.pos + n > len(self.mem):
            raise Exception("out of mem")
        value = getattr(struct, attr)  # , dtype=meta['_get_type']()
        if meta["_is_enum"]:
            value = value.value
        b = value.tobytes()
        assert len(b) == n
        self.mem[self.pos : self.pos + n] = b
        self.pos += n

    def visit_scalar_struct(self, struct, attr, meta):
        accept(getattr(struct, attr), self)

    def visit_array(self, struct, attr, meta):
        if meta["_is_embedded"]:
            return
        t = meta["_get_type"]()
        d = meta["_get_dim"](struct)
        n = np.dtype(t).itemsize
        if meta["_is_enum"]:
            n = np.dtype(meta["_get_underlying_type"]()).itemsize
        if self.pos + d * n > len(self.mem):
            raise Exception("out of mem")
        value = getattr(struct, attr)
        if meta["_is_enum"]:
            value = np.array(value, dtype=meta["_get_underlying_type"]())
        b = value.tobytes()
        assert len(b) == d * n
        self.mem[self.pos : self.pos + d * n] = b
        self.pos += d * n

    def visit_array_struct(self, struct, attr, meta):
        for s in getattr(struct, attr):
            accept(s, self)


def copy_to_mem(s, mem):
    v = copy_to_mem_visitor(mem)
    accept(s, v)
    return v.pos


def copy_from_mem(mem, s):
    v = copy_from_mem_visitor(mem)
    accept(s, v)
    return v.pos


@const_visitor
class count_bytes_visitor:
    def __init__(self):
        self.count = 0

    def visit_scalar(self, struct, attr, meta):
        t = meta["_get_type"]()
        n = np.dtype(t).itemsize
        self.count += n

    def visit_scalar_struct(self, struct, attr, meta):
        accept(getattr(struct, attr), self)

    def visit_array(self, struct, attr, meta):
        t = meta["_get_type"]()
        d = meta["_get_dim"](struct)
        n = np.dtype(t).itemsize
        self.count += d * n

    def visit_array_struct(self, struct, attr, meta):
        for s in getattr(struct, attr):
            accept(s, self)


def count_bytes(s):
    v = count_bytes_visitor()
    accept(s, v)
    return v.count


def compute_length(s):
    # todo: use unit of length
    return count_bytes(s)


def set_length_field(obj):
    if 'item_get_unique_is_message_length_field' in obj._meta_struct:
        obj._meta_struct['item_set_unique_is_message_length_field'](obj,compute_length(obj))


def copy(a, b):
    """
    copies a to b and returns b
    """
    #    # this is used by swig objects...
    #    a_relevant_fields = list(filter(lambda x:not x.startswith("_") and not x.startswith("item_") and x!="this", dir(a)))
    #    b_relevant_fields = list(filter(lambda x:not x.startswith("_") and not x.startswith("item_") and x!="this", dir(b)))
    #    # check if we have same fields...
    #    if len(set(a_relevant_fields) & set(b_relevant_fields)) != len(a_relevant_fields):
    #        p = set(a_relevant_fields) - (set(a_relevant_fields) & set(b_relevant_fields))
    #        raise Exception("fields do not match (assigning {} to {}, missing fields in second arg.: {})".format(str(a.__class__),str(b.__class__),str(p)))
    #    for f in a_relevant_fields:
    #        setattr(b, f, getattr(a, f))
    mem = None

    if "__swig_destroy__" in dir(a.__class__):
        if "_GET_WRAPPER" in dir(a):
            mya = a._GET_WRAPPER()
        else:
            mya = a
        n = mya.count_bytes()
        mem = bytearray(n)
        mya.copy_to_mem(mem)
    else:
        n = count_bytes(a)
        mem = bytearray(n)
        copy_to_mem(a, mem)

    if "__swig_destroy__" in dir(b.__class__):
        if "_GET_WRAPPER" in dir(b):
            myb = b._GET_WRAPPER()
        else:
            myb = b
        myb.copy_from_mem(mem)
    else:
        copy_from_mem(mem, b)
    return b
