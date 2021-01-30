import numpy as np


def get_type(struct, attr, meta):
    if meta["is_scalar"]:
        if meta["is_variant"]:
            return meta["get_type_for"](struct)
        else:
            return struct.__dataclass_fields__[attr].type()
    elif meta["is_array"]:
        return meta["get_type"]()
    else:
        raise Error("unexpected: not a scalar and not an array.")


def init_visitor(c):
    class _init_visitor(c):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
        def visit(self,struct,attr,meta):
            if meta["is_scalar"]:
                if meta["is_struct"]:
                    if meta["is_variant"] and getattr(struct,attr).__class__ is not get_type(struct,attr, meta):
                        setattr(struct,attr,get_type(struct,attr, meta)())
                    self.visit_scalar_struct(struct,attr,meta)
                else: 
                    self.visit_scalar(struct,attr,meta)
            elif meta["is_array"]:
                if meta["is_struct"]: 
                    if getattr(struct, attr) is None or len(getattr(struct, attr))!=meta["get_dim"](struct):
                        setattr(struct,attr,[get_type(struct,attr, meta)()]*meta["get_dim"](struct))
                else: 
                    if getattr(struct, attr) is None or getattr(struct, attr).shape!=meta["get_dim_nd"](struct):
                        setattr(struct,attr,np.zeros(meta["get_dim_nd"](struct), dtype=get_type(struct,attr, meta)))
                if meta["is_struct"]: 
                    for x in getattr(struct,attr):
                        if x is not None and not isinstance(x,meta["get_type"]()):
                            raise Exception("unexpected type {} found in field {} of {}".format(
                                str(type(x)), attr, str(type(struct))
                            ))
                    self.visit_array_struct(struct,attr,meta)
                else: 
                    self.visit_array(struct,attr,meta)
            else:
                raise Error("unexpected: not a scalar and not an array.")
    def f(*args, **kwargs):
        return _init_visitor(*args, **kwargs)
    return f


def const_visitor(c):
    class _const_visitor(c):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
        def visit(self,struct,attr,meta):
            if meta["is_scalar"]:
                if meta["is_struct"]: 
                    if meta["is_variant"] and getattr(struct,attr).__class__ is not get_type(struct,attr, meta):
                        raise Exception("variant {} has wrong type. expected {}, got{}.".format(attr, get_type(struct,attr, meta), getattr(struct,attr).__class__))
                    self.visit_scalar_struct(struct,attr,meta)
                else: 
                    self.visit_scalar(struct,attr,meta)
            elif meta["is_array"]:
                if getattr(struct, attr) is None:
                    raise Exception("array {} is None.".format(attr))
                if meta["is_struct"]: 
                    if len(getattr(struct, attr))!=meta["get_dim"](struct):
                        raise Exception("array {} is has wrong length. Expected {} got {}.".format(attr,meta["get_dim"](struct),len(getattr(struct, attr))))
                else: 
                    if getattr(struct, attr).shape!=meta["get_dim_nd"](struct):
                        raise Exception("array {} is has wrong length. Expected {} got {}.".format(attr,meta["get_dim_nd"](struct),getattr(struct, attr).shape))
                if meta["is_struct"]: 
                    for x in getattr(struct,attr):
                        if x is not None and not isinstance(x,meta["get_type"]()):
                            raise Exception("unexpected type {} found in field {} of {}".format(
                                str(type(x)), attr, str(type(struct))
                            ))
                    self.visit_array_struct(struct,attr,meta)
                else: 
                    self.visit_array(struct,attr,meta)
            else:
                raise Exception("unexpected: not a scalar and not an array.")
    def f(*args, **kwargs):
        return _const_visitor(*args, **kwargs)
    return f


def accept(struct,v):
    for k in struct._meta:
        v.visit(struct,k,struct._meta[k])


@init_visitor
class empty_init_visitor:
    def __init__(self):
        pass
    def visit_scalar(self,struct,attr,meta):
        pass
    def visit_scalar_struct(self,struct,attr,meta):
        print(attr)
        accept(getattr(struct,attr), self)
    def visit_array(self,struct,attr,meta):
        pass
    def visit_array_struct(self,struct,attr,meta):
        for s in getattr(struct,attr):
            accept(s, self)


@const_visitor
class empty_const_visitor:
    def __init__(self):
        pass
    def visit_scalar(self,struct,attr,meta):
        pass
    def visit_scalar_struct(self,struct,attr,meta):
        accept(getattr(struct,attr), self)
    def visit_array(self,struct,attr,meta):
        pass
    def visit_array_struct(self,struct,attr,meta):
        for s in getattr(struct,attr):
            accept(s, self)


def adjust_array_sizes_and_variants(s):
    accept(s,empty_init_visitor())

def check_array_sizes_and_variants(s):
    accept(s,empty_const_visitor())
