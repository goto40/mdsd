from functools import reduce
import sys
import inspect
import item_lang.metamodel_formula as f
from textx import textx_isinstance, get_children_of_type, get_metamodel

def get_all_classes():
    res = []
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if obj is not None and inspect.isclass(obj):
            res.append(obj)
    return res + f.get_all_classes()


def _get_referenceed_if_attributes(self):
    mm = get_metamodel(self)
    return list(
        filter(
            lambda x: textx_isinstance(x.ref, mm["Attribute"]),
            get_children_of_type("AttrRef", self.if_attr),
        )
    )

class RawType(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])
            
    def get_size_in_bytes(self):
        assert self.bits % 8 == 0
        return self.bits//8

    def is_rawtype(self):
        return True

    def is_enum(self):
        return False

    def is_struct(self):
        return False


class Enum(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])
        setattr(self, "internaltype", "ENUM")

    def get_size_in_bytes(self):
        return self.type.get_size_in_bytes()    

    def is_rawtype(self):
        return False

    def is_enum(self):
        return True

    def is_struct(self):
        return False


class Constants(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

    def is_rawtype(self):
        return False

    def is_enum(self):
        return False

    def is_struct(self):
        return False


class VariantAttribute(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])
        setattr(self, "embedded", False)

    def is_container(self):
        return False

    def is_embedded(self):
        return False

    def is_array(self):
        return False

    def is_scalar(self):
        return False

    def is_variant(self):
        return True

    def __str__(self):
        return self.parent.name + "." + self.name

    def has_rawtype(self):
        return False

    def has_enum(self):
        return False

    def has_struct(self):
        return self.type.is_struct()

    def get_referenceed_if_attributes(self):
        return _get_referenceed_if_attributes(self)

    def has_if(self):
        return self.if_attr is not None


class ScalarAttribute(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

    def is_container(self):
        if self.embedded:
            return False
        next = self.parent.get_next_attr(self)
        return next is not None and hasattr(next, "embedded") and next.embedded

    def is_embedded(self):
        return self.embedded

    def get_container_elements(self):
        assert self.is_container()
        next = self.parent.get_next_attr(self)
        result = list()
        while next is not None and next.embedded:
            result.append(next)
            next = self.parent.get_next_attr(next)
        return result

    def is_array(self):
        return False

    def is_scalar(self):
        return True

    def is_variant(self):
        return False

    def __str__(self):
        return self.parent.name + "." + self.name

    def has_rawtype(self):
        return self.type.is_rawtype()

    def has_enum(self):
        return self.type.is_enum()

    def has_struct(self):
        return self.type.is_struct()

    def get_referenceed_if_attributes(self):
        return _get_referenceed_if_attributes(self)

    def has_if(self):
        return self.if_attr is not None


class Struct(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

    def get_next_attr(self, a):
        try:
            lst = list(map(lambda x: id(x), self.attributes))
            idx = lst.index(id(a))
            idx += 1
            if idx < len(self.attributes):
                return self.attributes[idx]
            else:
                return None
        except Exception:
            return None

    def get_prev_attr(self, a):
        try:
            lst = list(map(lambda x: id(x), self.attributes))
            idx = lst.index(id(a))
            idx -= 1
            if idx >= 0:
                return self.attributes[idx]
            else:
                return None
        except Exception:
            return None

    def __str__(self):
        return self.name

    def is_rawtype(self):
        return False

    def is_enum(self):
        return False

    def is_struct(self):
        return True


class Package(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])


class PropertyDefinition(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])


class Property(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

    def __str__(self):
        return f"{self.parent}(.{self.definition.name})"


class ArrayAttribute(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

    def has_fixed_size(self):
        return reduce(
            lambda a, b: a and b, map(lambda x: x.dim.has_fixed_size(), self.dims), True
        )

    def compute_fixed_size_dim(self):
        return reduce(
            lambda a, b: a * b, map(lambda x: x.dim.compute_formula(), self.dims), 1
        )

    def compute_formula(self):
        """
        deprecated. use compute_fixed_size_dim
        """
        return self.compute_fixed_size_dim()

    def get_referenceed_dim_attributes(self):
        mm = get_metamodel(self)
        l = []
        for d in self.dims:
            l = l + list(
                filter(
                    lambda x: textx_isinstance(x.ref, mm["Attribute"]),
                    get_children_of_type("AttrRef", d),
                )
            )
        return l

    def render_formula(self, **kwargs):
        return reduce(
            lambda a, b: "{}*{}".format(a, b),
            map(lambda x: x.dim.render_formula(**kwargs), self.dims),
            "1",
        )

    def render_formula_comma_separated(self, **kwargs):
        dims = list(map(lambda x: x.dim.render_formula(**kwargs), self.dims))
        if len(self.dims) == 1:
            return dims[0]
        else:
            return reduce(lambda a, b: "{},{}".format(a, b), dims)

    def is_container(self):
        return False

    def is_embedded(self):
        return self.embedded

    def is_array(self):
        return True

    def is_scalar(self):
        return False

    def is_variant(self):
        return False

    def __str__(self):
        return self.parent.name + "." + self.name

    def has_rawtype(self):
        return self.type.is_rawtype()

    def has_enum(self):
        return self.type.is_enum()

    def has_struct(self):
        return self.type.is_struct()

    def get_referenceed_if_attributes(self):
        return _get_referenceed_if_attributes(self)

    def has_if(self):
        return self.if_attr is not None
