from functools import reduce
import sys, inspect


def get_all_classes():
    res = []
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if obj in [CustomIdlBase, FormulaBase]:
            continue
        if obj is not None and inspect.isclass(obj):
            res.append(obj)
    return res


def render_ref(ref, separator=".", postfix="", prefix="", const_separator='::',
               enum_separator=None, repeat_type_name_for_enums=False,
               inhibit_fqn_for_parent=None):
    from textx import textx_isinstance, get_metamodel
    from item_lang.common import get_package_names_of_obj
    if enum_separator is None:
        enum_separator = const_separator
    mm = get_metamodel(ref)
    if ref.parent is inhibit_fqn_for_parent:
        fqn_parts = []
    else:
        fqn_parts = get_package_names_of_obj(ref) + [ref.parent.name]
    if textx_isinstance(ref, mm["ScalarAttribute"]):
        return prefix + separator.join(
            map(lambda x: x.name, ref._tx_path)) + postfix
    elif textx_isinstance(ref, mm["Constant"]):
        return const_separator.join(
            fqn_parts + [ref.name])
    elif textx_isinstance(ref, mm["EnumEntry"]):
        if repeat_type_name_for_enums:
            return enum_separator.join(
                fqn_parts + [ref.parent.name, ref.name])
        else:
            return enum_separator.join(
                fqn_parts + [ref.name])
    else:
        from textx.exceptions import TextXSemanticError
        raise TextXSemanticError("unexpected type " + ref._tx_obj.__class__.__name__)


class CustomIdlBase(object):
    def __init__(self):
        pass

    def _init_xtextobj(self, **kwargs):
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])


class FormulaBase(CustomIdlBase):
    def __init__(self):
        super(FormulaBase, self).__init__()

    def has_fixed_size(self):
        return reduce(lambda x, y: x and y, map(
            lambda x: x.has_fixed_size(), self.parts), True)

    def render_formula(self, **p):
        if len(self.parts) == 1:
            return self.parts[0].render_formula(**p)
        else:
            return "(" + self.operator.join(map(
                lambda x: x.render_formula(**p), self.parts)) + ")"

    def __repr__(self):
        return self.render_formula()


class Predicate_Or(FormulaBase):
    def __init__(self, **kwargs):
        super(Predicate_Or, self).__init__()
        self._init_xtextobj(**kwargs)
        self.operator = "or"


class Predicate_And(FormulaBase):
    def __init__(self, **kwargs):
        super(Predicate_And, self).__init__()
        self._init_xtextobj(**kwargs)
        self.operator = "and"


class Predicate_Cmp(FormulaBase):
    def __init__(self, **kwargs):
        super(Predicate_Cmp, self).__init__()
        self._init_xtextobj(**kwargs)

    def render_formula(self, **p):
        if len(self.other_parts) == 0:
            raise Exception("unexpected: comparison with at least two elements required.")
        else:
            res0 = self.part0.render_formula(**p)
            return "(" + res0 + "".join(map(
                lambda x: x.cmp_op + x.part.render_formula(**p), self.other_parts)) + ")"


class Sum(FormulaBase):
    def __init__(self, **kwargs):
        super(Sum, self).__init__()
        self._init_xtextobj(**kwargs)
        self.operator = "+"

    def compute_formula(self):
        if len(self.parts) == 1:
            return self.parts[0].compute_formula()
        else:
            return reduce(lambda a,b: a.compute_formula()+b.compute_formula(), self.parts)

    def get_enum(self):
        from textx import textx_isinstance, get_metamodel
        if len(self.parts)!=1:
            return None
        if len(self.parts[0].parts)!=1:
            return None
        if len(self.parts[0].parts[0].parts)!=1:
            return None
        if len(self.parts[0].parts[0].parts[0].parts)!=1:
            return None
        v = self.parts[0].parts[0].parts[0].parts[0]
        mm = get_metamodel(v)
        if v.ref is not None:
            if textx_isinstance(v.ref.ref,mm["EnumEntry"]):
                return v.ref.ref._tx_obj
        return None

    def is_enum(self):
        return self.get_enum() is not None


class Dif(FormulaBase):
    def __init__(self, **kwargs):
        super(Dif, self).__init__()
        self._init_xtextobj(**kwargs)
        self.operator = "-"

    def compute_formula(self):
        if len(self.parts) == 1:
            return self.parts[0].compute_formula()
        else:
            return reduce(lambda a,b: a.compute_formula()-b.compute_formula(), self.parts)


class Mul(FormulaBase):
    def __init__(self, **kwargs):
        super(Mul, self).__init__()
        self._init_xtextobj(**kwargs)
        self.operator = "*"

    def compute_formula(self):
        if len(self.parts) == 1:
            return self.parts[0].compute_formula()
        else:
            return reduce(lambda a,b: a.compute_formula()*b.compute_formula(), self.parts)


def _mydiv(a,b):
    """
    int save divison. Unlike python3 1/5 yields 0 here... (like C)
    :param a:
    :param b:
    :return: a/b
    """
    #return a.compute_formula()/b.compute_formula()
    va = a.compute_formula()
    vb = b.compute_formula()
    if isinstance(va,int) and isinstance(vb,int):
        return va//vb
    else:
        return va/vb

class Div(FormulaBase):
    def __init__(self, **kwargs):
        super(Div, self).__init__()
        self._init_xtextobj(**kwargs)
        self.operator = "/"

    def compute_formula(self):
        if len(self.parts) == 1:
            return self.parts[0].compute_formula()
        else:
            return reduce(_mydiv, self.parts)


class Val(FormulaBase):
    def __init__(self, **kwargs):
        super(Val, self).__init__()
        self._init_xtextobj(**kwargs)

    def render_formula(self, **p):
        if self.ref:
            return self.ref.render_formula(**p)
        elif self.sum:
            return "({})".format(self.sum.render_formula(**p))
        else:
            return "{}".format(self.value)

    def compute_formula(self):
        if self.ref:
            from textx import textx_isinstance, get_metamodel
            if (textx_isinstance(self.ref.ref, get_metamodel(self)["Attribute"])):
                raise Exception("no constexpr")
            return self.ref.ref.value.compute_formula()
        elif self.sum:
            return self.sum.compute_formula()
        else:
            return self.value

    def has_fixed_size(self):
        if self.ref:
            return False
        elif self.sum:
            return self.sum.has_fixed_size()
        else:
            return True


class AttrRef(FormulaBase):
    def __init__(self, **kwargs):
        super(AttrRef, self).__init__()
        self._init_xtextobj(**kwargs)

    def render_formula(self, **p):
        return render_ref(self.ref, **p)
