def get_all_attributes_before(a):
    s = a.parent
    idx0 = s.attributes.index(a)
    assert idx0>=0
    return filter(lambda x: s.attributes.index(x)<idx0, s.attributes)

def is_attribute_before_other_attribute(a,b):
    return a in get_all_attributes_before(b)