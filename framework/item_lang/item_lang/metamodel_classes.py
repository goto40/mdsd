from functools import reduce
import sys
import inspect
import item_lang.metamodel_formula as f


def get_all_classes():
    res = []
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if obj is not None and inspect.isclass(obj):
            res.append(obj)
    return res + f.get_all_classes()


class RawType(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])


class Enum(object):
    def __init__(self, **kwargs):
        setattr(self, "parent", None)
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])
        setattr(self, "internaltype", "ENUM")


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

    def __str__(self):
        return self.parent.name + "." + self.name


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

    def __str__(self):
        return self.parent.name + "." + self.name


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

    def compute_formula(self):
        return reduce(
            lambda a, b: a * b, map(lambda x: x.dim.compute_formula(), self.dims), 1
        )

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

    def __str__(self):
        return self.parent.name + "." + self.name
