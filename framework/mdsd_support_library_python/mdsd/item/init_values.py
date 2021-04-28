from mdsd.item_support import init_visitor
from mdsd.item_support import accept
import numpy as np


@init_visitor
class init_default_values_visitor:
    def __init__(
        self,
    ):
        pass

    def visit_scalar(self, struct, attr, meta):
        if meta["_has_char_content"] and meta["__has_defaultStringValue"]:
            setattr(struct, attr + "_as_str", meta["defaultStringValue"]())
        elif meta["__has_defaultValue"]:
            setattr(struct, attr, meta["defaultValue"]())

    def visit_scalar_struct(self, struct, attr, meta):
        accept(getattr(struct, attr), self)

    def visit_array(self, struct, attr, meta):
        if meta["__has_defaultValue"]:
            v = np.fill(getattr(struct, attr).shape, dtype=meta["_get_type"](meta["defaultValue"]()))
            setattr(struct, attr, v)

    def visit_string(self, struct, attr, rawattr, meta):
        if meta["__has_defaultStringValue"]:
            setattr(struct, attr, meta["defaultStringValue"]())
        else:
            self.visit_array(struct, rawattr, meta)

    def visit_array_struct(self, struct, attr, meta):
        for s in getattr(struct, attr):
            accept(s, self)


def init_default_values(s):
    v = init_default_values_visitor()
    accept(s, v)


@init_visitor
class set_max_values_visitor:
    def __init__(
        self,
    ):
        pass

    def visit_scalar(self, struct, attr, meta):
        if "__has_maxValue" in meta and meta["__has_maxValue"]:
            setattr(struct, attr, meta["maxValue"]())

    def visit_scalar_struct(self, struct, attr, meta):
        accept(getattr(struct, attr), self)

    def visit_array(self, struct, attr, meta):
        if "__has_maxValue" in meta and meta["__has_maxValue"]:
            v = np.fill(getattr(struct, attr).shape, dtype=meta["_get_type"](meta["maxValue"]()))
            setattr(struct, attr, v)

    def visit_string(self, struct, attr, rawattr, meta):
        pass

    def visit_array_struct(self, struct, attr, meta):
        for s in getattr(struct, attr):
            accept(s, self)


def init_max_values(s):
    init_default_values(s)
    v = set_max_values_visitor()
    accept(s, v)


@init_visitor
class set_min_values_visitor:
    def __init__(
        self,
    ):
        pass

    def visit_scalar(self, struct, attr, meta):
        if "__has_minValue" in meta and meta["__has_minValue"]:
            setattr(struct, attr, meta["minValue"]())

    def visit_scalar_struct(self, struct, attr, meta):
        accept(getattr(struct, attr), self)

    def visit_array(self, struct, attr, meta):
        if "__has_minValue" in meta and meta["__has_minValue"]:
            v = np.fill(getattr(struct, attr).shape, dtype=meta["_get_type"](meta["minValue"]()))
            setattr(struct, attr, v)

    def visit_string(self, struct, attr, rawattr, meta):
        pass

    def visit_array_struct(self, struct, attr, meta):
        for s in getattr(struct, attr):
            accept(s, self)


def init_min_values(s):
    init_default_values(s)
    v = set_min_values_visitor()
    accept(s, v)
