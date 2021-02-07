from textx import (get_location, textx_isinstance, get_metamodel,
                   textxerror_wrap, get_children_of_type)
from textx.exceptions import TextXSemanticError
from item_lang.common import (get_bits, compute_formula_for_internaltype, get_fixed_dimension,
                              textx_assert)
from item_lang.metamodel_classes import RawType
from item_lang.properties import (get_property, is_applicable,
                                  get_all_possible_mandatory_properties,
                                  get_all_possible_properties,
                                  has_property)
from item_lang.attributes import (is_attribute_before_other_attribute)
from functools import reduce
import sys, inspect


def get_all_checks_as_map():
    res = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if obj is not None and inspect.isfunction(obj) and name.startswith("check_"):
            res[name[6:]] = textxerror_wrap(obj)
    return res


def check_Attribute(a):
    if a.name.startswith("item_"):
        raise TextXSemanticError("attribute may not start with 'item_'"+a.name, **get_location(a))
    if a.name.startswith("_"):
        raise TextXSemanticError("attribute may not start with '_'"+a.name, **get_location(a))

    if hasattr(a,'type'):
        if a.embedded:
            textx_assert(a.type.name != 'char', a, 'char may be be used as embedded field')

    if hasattr(a, 'type'):
        if textx_isinstance(a.type, RawType):
            if a.type.internaltype in ['INT', 'UINT'] and not a.embedded:
                if get_bits(a.type) not in [8,16,32,64,128]:
                    raise TextXSemanticError("attribute {} must have a bit size of a power of two.".format(a.name), **get_location(a))
            if a.type.internaltype not in ['INT', 'UINT'] and a.embedded:
                raise TextXSemanticError("attribute {} must be an integral type.".format(a.name), **get_location(a))
        elif textx_isinstance(a.type, get_metamodel(a)['Enum']):
            if get_bits(a.type) not in [8, 16, 32, 64, 128] and not a.embedded:
                raise TextXSemanticError("attribute {} must have a bit size of a power of two.".format(a.name),
                                         **get_location(a))

    # check mandatory properties in attributes
    mandatory_prop_defs = get_all_possible_mandatory_properties(a)
    attr_prop_defs = list(map(lambda p: p.definition, a.properties))
    for d in mandatory_prop_defs.values():
        textx_assert(d in attr_prop_defs, a, f"missing mandatory property '{d.name}'")

    if a.is_container():
        textx_assert(a.if_attr is None, a, f"restricted attributes may not be used as container (put them into a separate substruct)")

    if a.is_embedded():
        textx_assert(a.if_attr is None, a, f"restricted attributes may not be embedded (put them into a separate substruct)")


def check_Struct(s):
    mm = get_metamodel(s)

    # check mandatory properties in attributes
    mandatory_prop_defs = get_all_possible_mandatory_properties(s)
    attr_prop_defs = map(lambda p: p.definition, s.properties)
    for d in mandatory_prop_defs.values():
        textx_assert(d in attr_prop_defs, s, f"missing mandatory property '{d.name}'")

    # check if max count of properties are not violated ("... to ... times per message)
    def get_all_properties_of_struct(s):
        lst = []
        for a in s.attributes:
            lst = lst + a.properties
            if textx_isinstance(a, mm["ScalarAttribute"]) and textx_isinstance(a.type, mm["Struct"]):
                lst = lst + get_all_properties_of_struct(a.type)
        return lst
    properties = get_all_properties_of_struct(s)
    properties_per_def={}
    for p in properties:
        if p.definition not in properties_per_def:
            properties_per_def[p.definition] = [p]
        else:
            properties_per_def[p.definition].append(p)

    property_defs = get_all_possible_properties(
        s,filter_applicable_to_model_object=False).values()
    for d in property_defs:
        if d.numberOfPropRestriction is not None:
            n = len(properties_per_def.get(d, []))
            textx_assert(n>=d.numberOfPropRestriction.min,s,
                         f'need at least {d.numberOfPropRestriction.min} of property "{d.name}"')
            textx_assert(n<=d.numberOfPropRestriction.max,s,
                         f'not more than {d.numberOfPropRestriction.max} of property "{d.name}" allowed')

    # unique names:
    all_attribute_names = list(map(lambda x:x.name, s.attributes))
    all_attribute_names_unique = set(all_attribute_names)
    if len(all_attribute_names) != len(all_attribute_names_unique):
        idx = 0
        while len(all_attribute_names)>0:
            first = all_attribute_names[0]
            del all_attribute_names[0]
            textx_assert(first in all_attribute_names_unique, s.attributes[idx], f'attribute name {first} is not unique')
            all_attribute_names_unique.remove(first)
            idx += 1


def check_Property(p):
    mm = get_metamodel(p)
    textx_assert( is_applicable(p), p, f"{p.parent.name}.{p.definition.name} not applicable" )

    prop_value = get_property(p.parent,p.definition.name)  # throws on error

    if p.definition.name == "defaultStringValue":
        textx_assert(not has_property(p.parent, 'defaultValue'), p.parent,
                     "only one default is allowed")
        if textx_isinstance(p.parent, mm["ScalarAttribute"]):
            textx_assert(len(prop_value) == 1, p,
                         "only exactly one char is allowed as default")


def check_ScalarAttribute(a):
    if a.is_container():
        if not textx_isinstance(a.type, RawType):
            raise TextXSemanticError("container {} must be an unsigned integral type.".format(a.name), **get_location(a))
        elif a.type.internaltype != 'UINT':
            raise TextXSemanticError("container {} must be an unsigned integral type.".format(a.name), **get_location(a))
        num_bits = reduce(
            lambda a,b:a+b,
            map(lambda a:get_bits(a.type)*get_fixed_dimension(a), a.get_container_elements()))
        if num_bits != get_bits(a.type):
            raise TextXSemanticError("embedded elements of container {} ({}) do not sum up to {}.".format(
                a.name,num_bits,get_bits(a.type)), **get_location(a))


def check_ArrayAttribute(a):
    if a.type.name == 'char':
        textx_assert( len(a.dims) == 1, a, "no multidimensional strings allowed")


def check_VariantMapping(mapping):
    mm = get_metamodel(mapping)
    selector_type = mapping.parent.variant_selector.ref.type
    if textx_isinstance(selector_type, mm["Enum"]):
        if not mapping.id.is_enum():
            raise TextXSemanticError("bad type (enum of type {} is expected)".format(
                selector_type.name
            ), **get_location(mapping))


def check_Sum(sum):
    from textx import get_children_of_type, textx_isinstance, get_metamodel
    mm = get_metamodel(sum)
    enum_entries = list(filter(
        lambda x: (x.ref is not None) and textx_isinstance(
            x.ref.ref, mm["EnumEntry"]),
        get_children_of_type("Val", sum)
    ))
    if len(enum_entries)>0:
        if not sum.is_enum():
            raise TextXSemanticError("enum must not be part of a formula", **get_location(sum))


def check_Constant(constant):
    compute_formula_for_internaltype(constant.value,constant.type.internaltype, constant.name)  # throws on error


def check_Val(val_object):
    mm = get_metamodel(val_object)
    if val_object.valueClassificator is None:
        return
    elif val_object.valueClassificator == "ENUM":
        textx_assert(textx_isinstance(val_object.ref.ref, mm['EnumEntry']),
                     val_object,
                     "referenced value is not matching classificator '{}'".format(
                         val_object.valueClassificator))
    elif val_object.valueClassificator == "CONST":
        textx_assert(textx_isinstance(val_object.ref.ref, mm['Constant']),
                     val_object,
                     "referenced value is not matching classificator '{}'".format(
                         val_object.valueClassificator))
    else:
        textx_assert(False,
                     val_object,
                     "unexpected classificator '{}'".format(val_object.valueClassificator))


def _assert_attr_defined_before_beeing_used_in_formula(a,f,d):
    mm = get_metamodel(d)
    # only the first element of a reference path has to be checked
    all_refs = map(lambda x: x.ref._tx_path[0], get_children_of_type("AttrRef", f))
    all_refs = filter( lambda x: textx_isinstance(x, mm["ScalarAttribute"] ), all_refs)
    for r in all_refs:
        textx_assert(is_attribute_before_other_attribute(r,a), d, f"{r.name} must be defined before {a.name}")


def _assert_restricted_attr_may_not_be_used_in_formula(f, d, info_where="dimension"):
    mm = get_metamodel(d)
    all_refs = list(map(lambda x: x.ref._tx_path, get_children_of_type("AttrRef", f)))
    if len(all_refs)>0:
        all_refs = reduce(lambda a,b: a+b, all_refs)
    all_refs = filter( lambda x: textx_isinstance(x, mm["ScalarAttribute"] ), all_refs)
    for r in all_refs:
        textx_assert(r.if_attr is None, d, f"restricted attribute {r.name} may not be used in {info_where}")


def check_Dim(d):
    a = d.parent
    _assert_attr_defined_before_beeing_used_in_formula(a, d.dim, d)
    _assert_restricted_attr_may_not_be_used_in_formula(d.dim, d)


def check_IfAttribute(i):
    a = i.parent
    _assert_attr_defined_before_beeing_used_in_formula(a, i.predicate, i)
    _assert_restricted_attr_may_not_be_used_in_formula(i.predicate, i, "predicate")
