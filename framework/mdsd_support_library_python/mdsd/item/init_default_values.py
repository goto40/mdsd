from mdsd.item_support import init_visitor
from mdsd.item_support import accept
import numpy as np


@init_visitor
class init_default_values_visitor:
    def __init__(self,):
        pass

    def visit_scalar(self, struct, attr, meta):
        if meta["_has_defaultValue"]:
            setattr(struct, attr, meta["defaultValue"]())

    def visit_scalar_struct(self, struct, attr, meta):
        accept(getattr(struct,attr), self)

    def visit_array(self, struct, attr, meta):
        if meta["_has_defaultValue"]:
            v = np.fill(getattr(struct, attr).shape, dtype=meta["get_type"]())
            setattr(struct, attr, v)

    def visit_string(self, struct, attr, rawattr, meta):
        if meta["_has_defaultStringValue"]:
            setattr(struct,attr,meta["defaultStringValue"]())
        else:
            self.visit_array(struct, rawattr, meta)

    def visit_array_struct(self, struct, attr, meta):
        for s in getattr(struct, attr):
            accept(s, self)


def init_default_values(s):
    v = init_default_values_visitor()
    accept(s, v)
