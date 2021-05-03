import numpy as np


def get_type(struct, attr, meta):
    if meta["_is_scalar"]:
        if meta["_is_variant"]:
            return meta["_get_type_for"](struct)
        else:
            return struct.__dataclass_fields__[attr].type()
    elif meta["_is_array"]:
        return meta["_get_type"]()
    else:
        raise Error("unexpected: not a scalar and not an array.")


def init_visitor(c):
    class _init_visitor(c):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def visit(self, struct, attr, meta):
            if meta["_has_if_restriction"] and not meta["_if_restriction"](struct):
                return
            if meta["_is_scalar"]:
                if meta["_is_struct"]:
                    if meta["_is_variant"] and getattr(
                        struct, attr
                    ).__class__ is not get_type(struct, attr, meta):
                        setattr(struct, attr, get_type(struct, attr, meta)())
                    self.visit_scalar_struct(struct, attr, meta)
                else:
                    self.visit_scalar(struct, attr, meta)
            elif meta["_is_array"]:
                if meta["_is_struct"]:
                    if getattr(struct, attr) is None or len(
                        getattr(struct, attr).flat
                    ) != meta["_get_dim"](struct):
                        setattr(
                            struct,
                            attr,
                            [get_type(struct, attr, meta)() for k in range(meta["_get_dim"](struct))]
                        )
                else:
                    if getattr(struct, attr) is None or getattr(
                        struct, attr
                    ).shape != meta["_get_dim_nd"](struct):
                        setattr(
                            struct,
                            attr,
                            np.zeros(
                                meta["_get_dim_nd"](struct),
                                dtype=get_type(struct, attr, meta),
                            ),
                        )
                if meta["_is_struct"]:
                    for x in getattr(struct, attr):
                        if x is not None and not isinstance(x, meta["_get_type"]()):
                            raise Exception(
                                "unexpected type {} found in field {} of {}".format(
                                    str(type(x)), attr, str(type(struct))
                                )
                            )
                    self.visit_array_struct(struct, attr, meta)
                elif meta["_has_char_content"] and hasattr(self, "visit_string"):
                    self.visit_string(struct, attr + "_as_str", attr, meta)
                else:
                    self.visit_array(struct, attr, meta)
            else:
                raise Error("unexpected: not a scalar and not an array.")

    def f(*args, **kwargs):
        return _init_visitor(*args, **kwargs)

    return f


def const_visitor(c):
    class _const_visitor(c):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def visit(self, struct, attr, meta):
            if meta["_has_if_restriction"] and not meta["_if_restriction"](struct):
                return
            if meta["_is_scalar"]:
                if meta["_is_struct"]:
                    if meta["_is_variant"] and getattr(
                        struct, attr
                    ).__class__ is not get_type(struct, attr, meta):
                        raise Exception(
                            "variant {} has wrong type. expected {}, got{}.".format(
                                attr,
                                get_type(struct, attr, meta),
                                getattr(struct, attr).__class__,
                            )
                        )
                    self.visit_scalar_struct(struct, attr, meta)
                else:
                    self.visit_scalar(struct, attr, meta)
            elif meta["_is_array"]:
                if getattr(struct, attr) is None:
                    raise Exception("array {} is None.".format(attr))
                if meta["_is_struct"]:
                    if len(getattr(struct, attr)) != meta["_get_dim"](struct):
                        raise Exception(
                            "array {} is has wrong length. Expected {} got {}.".format(
                                attr,
                                meta["_get_dim"](struct),
                                len(getattr(struct, attr)),
                            )
                        )
                else:
                    if getattr(struct, attr).shape != meta["_get_dim_nd"](struct):
                        raise Exception(
                            "array {} is has wrong length. Expected {} got {}.".format(
                                attr,
                                meta["_get_dim_nd"](struct),
                                getattr(struct, attr).shape,
                            )
                        )
                if meta["_is_struct"]:
                    for x in getattr(struct, attr):
                        if x is not None and not isinstance(x, meta["_get_type"]()):
                            raise Exception(
                                "unexpected type {} found in field {} of {}".format(
                                    str(type(x)), attr, str(type(struct))
                                )
                            )
                    self.visit_array_struct(struct, attr, meta)
                elif meta["_has_char_content"] and hasattr(self, "visit_string"):
                    self.visit_string(struct, attr + "_as_str", attr, meta)
                else:
                    self.visit_array(struct, attr, meta)
            else:
                raise Exception("unexpected: not a scalar and not an array.")

    def f(*args, **kwargs):
        return _const_visitor(*args, **kwargs)

    return f


def accept(struct, v):
    for k in struct._meta_order:
        v.visit(struct, k, struct._meta[k])


@init_visitor
class empty_init_visitor:
    def __init__(self):
        pass

    def visit_scalar(self, struct, attr, meta):
        pass

    def visit_scalar_struct(self, struct, attr, meta):
        print(attr)
        accept(getattr(struct, attr), self)

    def visit_array(self, struct, attr, meta):
        pass

    def visit_array_struct(self, struct, attr, meta):
        for s in getattr(struct, attr):
            accept(s, self)


@const_visitor
class empty_const_visitor:
    def __init__(self):
        pass

    def visit_scalar(self, struct, attr, meta):
        pass

    def visit_scalar_struct(self, struct, attr, meta):
        accept(getattr(struct, attr), self)

    def visit_array(self, struct, attr, meta):
        pass

    def visit_array_struct(self, struct, attr, meta):
        for s in getattr(struct, attr):
            accept(s, self)


def compute_length(s):
    from mdsd.item.io import count_bytes
    # todo: use unit of length
    return count_bytes(s)


def set_length_field(obj):
    """
    Set the length field of a telegram if such a field is defined (.is_message_length_field=true)
    :param obj: message
    """
    if 'item_get_unique_is_message_length_field' in obj._meta_struct:
        obj._meta_struct['item_set_unique_is_message_length_field'](obj,compute_length(obj))


def adjust_array_sizes_and_variants(s):
    accept(s, empty_init_visitor())
    set_length_field(s)


def check_array_sizes_and_variants(s):
    accept(s, empty_const_visitor())
