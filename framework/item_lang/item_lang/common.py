import textx
from textx import get_location, get_model
from textx.exceptions import TextXSemanticError
from functools import reduce
from os.path import exists, getmtime


def get_package_names_of_obj(obj):
    return list(map(lambda x:x.name, get_packages_of_obj(obj)))


def get_packages_of_obj(obj):
    from textx import textx_isinstance, get_metamodel
    pkgs = []
    p = obj
    while (p is not None):
        if textx_isinstance(p,get_metamodel(p)["AnyPackage"]):
            pkgs.insert(0, p)
        if hasattr(p, "parent"):
            p = p.parent
        else:
            p = None
    return pkgs


def get_referenced_elements_of_struct(i):
    from textx import get_metamodel, textx_isinstance, get_children_of_type
    mm = get_metamodel(i)
    res=[]
    for a in i.attributes:
        if textx_isinstance(a, mm["ScalarAttribute"]):
            res.append(a.type)
        elif textx_isinstance(a, mm["ArrayAttribute"]):
            res.append(a.type)
            for d in a.dims:
                for r in get_children_of_type("AttrRef", d.dim):
                    if textx_isinstance(r.ref, mm["Constant"]):
                        c = r.ref
                        res.append(c.parent)
        elif textx_isinstance(a, mm["VariantAttribute"]):
            for m in a.mappings:
                res.append(m.type)
        else:
            raise Exception("unexpected")

        for p in a.properties:
            if p.numberValue:
                for r in get_children_of_type("AttrRef", p.numberValue.x):
                    if textx_isinstance(r.ref, mm["Constant"]):
                        c = r.ref
                        res.append(c.parent)

    for c in i.constant_entries:
        for r in get_children_of_type("AttrRef", c.value):
            if textx_isinstance(r.ref, mm["Constant"]):
                c = r.ref
                res.append(c.parent)

    res = filter(lambda x: textx_isinstance(x, mm["Enum"]) or textx_isinstance(x, mm["Struct"]) or textx_isinstance(x, mm["Constants"]), res)
    res = filter(lambda x: x != i, res)
    res = list(set(res))
    res = sorted(res, key=lambda x:x.name)
    return res


def get_referenced_elements_of_enum(e):
    from textx import get_metamodel, textx_isinstance, get_children_of_type
    mm = get_metamodel(e)
    res=[]
    for e in e.enum_entries:
        for r in get_children_of_type("AttrRef", e.value):
            if textx_isinstance(r.ref, mm["Constant"]):
                c = r.ref
                res.append(c.parent)

    res = filter(lambda x: textx_isinstance(x, mm["Enum"]) or textx_isinstance(x, mm["Struct"]) or textx_isinstance(x, mm["Constants"]), res)
    res = filter(lambda x: x != e, res)
    res = list(set(res))
    res = sorted(res, key=lambda x:x.name)
    return res


def get_referenced_elements_of_constants(cs):
    from textx import get_metamodel, textx_isinstance, get_children_of_type
    mm = get_metamodel(cs)
    res=[]
    for c in cs.constant_entries:
        for r in get_children_of_type("AttrRef", c.value):
            if textx_isinstance(r.ref, mm["Constant"]):
                c = r.ref
                res.append(c.parent)

    res = filter(lambda x: textx_isinstance(x, mm["Enum"]) or textx_isinstance(x, mm["Struct"]) or textx_isinstance(x, mm["Constants"]), res)
    res = filter(lambda x: x != cs, res)
    res = list(set(res))
    res = sorted(res, key=lambda x:x.name)
    return res


def textx_assert(req_true, o, text):
    if not req_true:
        raise TextXSemanticError(text + " for " + str(o), **get_location(o));


def compute_formula_for_internaltype(f, internaltype, info="formula"):
    """
    :param f: a Formula
    :param internaltype: the internal type
    :param info: prefix for error text
    :return: the computed number
    """
    if internaltype == 'INT':
        textx_assert(type(f.compute_formula()) is int, f, info + " must be an INT")
        return f.compute_formula()
    elif internaltype == 'UINT':
        textx_assert(type(f.compute_formula()) is int, f, info + " must be an INT/UINT")
        textx_assert(f.compute_formula() >= 0, f, info + " must be an UINT")
        return f.compute_formula()
    elif internaltype == 'BOOL':
        textx_assert(type(f.compute_formula()) is int, f, info + " must be an INT/BOOL as int")
        textx_assert(f.compute_formula() == 0 or f.compute_formula() == 1, f,
                     info + " must be an BOOL as int (0 or 1)")
        return f.compute_formula() != 0
    elif internaltype == 'FLOAT':
        return f.compute_formula()
    elif internaltype == 'ENUM':
        return f.compute_formula()
    else:
        return None


def find_builtin(obj, lookup_list, rrel_tree, obj_cls=None):
    """
    Find a object from the buildin_models
    :param obj: an object of the model to get the metamodel from
    :param lookup_list: search path (FQN)
    :param rrel_tree: search path (in the abstract syntax tree)
    :param obj_cls: class to be searched for (optional)
    :return: the object or None
    """
    from textx.scoping.rrel import find
    from textx import get_metamodel
    res = None
    mm = get_metamodel(obj)
    for m in mm.builtin_models:
        res = find(m, lookup_list, rrel_tree, obj_cls)
        if res is not None:
            break
    return res


def get_fixed_dimension(attr):
    if textx.textx_isinstance(attr, textx.get_metamodel(attr)['ScalarAttribute']):
        return 1
    elif textx.textx_isinstance(attr, textx.get_metamodel(attr)['VariantAttribute']):
        return 1
    elif textx.textx_isinstance(attr, textx.get_metamodel(attr)['ArrayAttribute']):
        if attr.has_fixed_size():
            return attr.compute_formula()
        else:
            raise TextXSemanticError('unexpected: no fixed dimension available for {}'.format(
                attr.name), **get_location(attr))


def _assert_is_embedded(atype):
    if not atype.is_embedded():
        raise TextXSemanticError('unexpected: get_start_end_bit called for an non-embedded attribute {}'.format(
            atype), **get_location(atype))


def get_embedded_elements(container):
    textx_assert( container.is_container(), container, "container expected")
    res = []
    n = container
    n = n.parent.get_next_attr(n)
    while n is not None and n.is_embedded():
        res.append(n)
        n = n.parent.get_next_attr(n)
    return res


def get_container(atype):
    _assert_is_embedded(atype)
    p = atype.parent.get_prev_attr(atype)
    while p is not None and not p.is_container():
        p = atype.parent.get_prev_attr(p)
    if p is None:
        raise TextXSemanticError('unexpected: did not found container of embedded attribute {}'.format(
            atype), **get_location(atype))
    return p


def get_start_end_bit(myattr):
    """
    compute the start and end bit (both included)
    :param myattr: an embedded attribute
    :return: start_bit, end_bit (starting at the MSB)
    """
    _assert_is_embedded(myattr)
    c = get_container(myattr)
    lst = get_embedded_elements(c)
    idx = lst.index(myattr)
    textx_assert(idx >= 0, myattr, "unexpected: element not in list of embedded elements of own conatainer")
    lst = lst[0:idx]
    start_bit = reduce(lambda a,b: a+get_bits(b), lst, 0)
    end_bit = start_bit + get_bits(myattr)

    total_bits = get_bits(c)
    start_bit = total_bits - 1 - start_bit
    end_bit = total_bits - end_bit  # end bit included!

    textx_assert(start_bit >= 0 and start_bit < total_bits, myattr, "plausibility check bits={}..{}".format(start_bit, end_bit))
    textx_assert(end_bit >= 0 and end_bit < total_bits, myattr, "plausibility check bits={}..{}".format(start_bit, end_bit))
    textx_assert(start_bit >= end_bit, myattr, "plausibility check bits={}..{}".format(start_bit, end_bit))
    return start_bit, end_bit


def get_bits(x):
    mm = textx.get_metamodel(x)
    if textx.textx_isinstance(x, mm['RawType']):
        return x.bits
    elif textx.textx_isinstance(x, mm['Enum']):
        return x.type.bits
    elif textx.textx_isinstance(x, mm['ScalarAttribute']):
        return get_bits(x.type)
    elif textx.textx_isinstance(x, mm['ArrayAttribute']):
        textx_assert(x.has_fixed_size(), x, "embedded arrays must have fixed size")
        return get_bits(x.type) * x.compute_formula()
    else:
        raise TextXSemanticError('unexpected: no bits available for {}'.format(
            x.name), **get_location(x))


def get_all_filenames_referenced_by_obj(obj):
    file_names = set()
    if (obj._tx_filename is not None):
        file_names.add(obj._tx_filename)
    if hasattr(obj, "_tx_model_repository"):
        for m in obj._tx_model_repository.all_models:
            if (m._tx_filename is not None):
                file_names.add(m._tx_filename)
    return file_names


def obj_is_new_than_date(obj, date):
    file_names = get_all_filenames_referenced_by_obj(obj)
    if len(file_names)==0:
        return True
    for f in file_names:
        if getmtime(f)>=date:
            return True
    return False


def obj_is_new_than_file(obj, filename):
    if not exists(filename):
        return True
    date = getmtime(filename)
    return obj_is_new_than_date(get_model(obj), date)