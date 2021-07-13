from textx import textx_isinstance, get_metamodel, get_children_of_type


def get_all_attributes_before(a):
    s = a.parent
    idx0 = s.attributes.index(a)
    assert idx0 >= 0
    return filter(lambda x: s.attributes.index(x) < idx0, s.attributes)


def is_attribute_before_other_attribute(a, b):
    return a in get_all_attributes_before(b)


def is_dynamic(a):
    """
    :param a: an attribute or a struct
    :return: True if is dynamic
    """
    mm = get_metamodel(a)
    if textx_isinstance(a, mm["Struct"]):
        for ia in a.attributes:
            if is_dynamic(ia):
                return True
        return False
    if a.if_attr is not None:
        return True
    if textx_isinstance(a, mm["VariantAttribute"]):
        return True
    if textx_isinstance(a, mm["ScalarAttribute"]):
        return False
    if textx_isinstance(a, mm["ArrayAttribute"]):
        attr_refs = a.get_referenceed_dim_attributes()
        if len(attr_refs) > 0:
            return True
        else:
            return False
