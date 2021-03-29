from textx.scoping.rrel import find
from textx import (
    get_metamodel,
    TextXSemanticError,
    textx_isinstance,
    get_location,
)
from item_lang.common import (
    textx_assert,
    compute_formula_for_internaltype,
    find_builtin,
)
from functools import reduce


def get_property(attr, prop_name):
    def get_value(res, internaltype):
        if internaltype == "STRING":
            textx_assert(
                res.textValue is not None, attr, prop_name + " must be a STRING"
            )
            return res.textValue.x
        elif internaltype == "INT":
            textx_assert(
                res.numberValue is not None, attr, prop_name + " must be an NUMBER/INT"
            )
        elif internaltype == "UINT":
            textx_assert(
                res.numberValue is not None, attr, prop_name + " must be an NUMBER/UINT"
            )
        elif internaltype == "BOOL":
            textx_assert(
                res.numberValue is not None,
                attr,
                prop_name + " must be an NUMBER/BOOL as int",
            )
        elif internaltype == "FLOAT":
            textx_assert(
                res.numberValue is not None, attr, prop_name + " must be an NUMBER"
            )
            assert res.numberValue is not None
        elif internaltype == "ENUM":
            textx_assert(
                res.numberValue is not None, attr, prop_name + " must be an ENUM"
            )
            assert res.numberValue is not None
        else:
            return None
        return compute_formula_for_internaltype(
            res.numberValue.x, internaltype, prop_name
        )

    res = list(filter(lambda x: x.definition.name == prop_name, attr.properties))
    if len(res) == 0:
        return None
    else:
        mm = get_metamodel(attr)
        textx_assert(len(res) == 1, attr, prop_name + " must be unique")
        res = res[0]
        internaltype = res.definition.internaltype
        if internaltype == "ATTRTYPE":
            textx_assert(
                not textx_isinstance(attr, mm["VariantAttribute"]),
                attr,
                prop_name + " not supported for variants",
            )
            correct_instance = textx_isinstance(
                attr.type, mm["RawType"]
            ) or textx_isinstance(attr.type, mm["Enum"])
            textx_assert(
                correct_instance,
                attr,
                prop_name + " only applicable for rawtypes/enums",
            )
            internaltype = attr.type.internaltype
        value = get_value(res, internaltype)
        textx_assert(
            value is not None,
            attr,
            prop_name + " could not be interpreted (unexpected)",
        )
        return value


def get_default_property_set(mm):
    res = None
    for m in mm.builtin_models:
        res = find(
            m,
            "built_in.default_properties",
            "+m:package.property_sets",
            obj_cls=mm["PropertySet"],
        )
        if res is not None:
            break
    assert res is not None
    return res


def get_property_set(model_obj):
    res = find(
        model_obj,
        "",
        "+m:^~property_set",
        obj_cls=get_metamodel(model_obj)["PropertySet"],
    )
    if res is None:
        res = get_default_property_set(get_metamodel(model_obj))
    return res


def get_all_possible_properties(model_obj, filter_applicable_to_model_object=True):
    ps = get_property_set(model_obj)

    def get(ps):
        res = set(ps.property_definitions)
        if ps.extends is not None:
            res = res | get(ps.extends)
        else:
            res = res | set(
                get_default_property_set(get_metamodel(model_obj)).property_definitions
            )
        return res

    res = get(ps)
    for d in res:
        if len(list(filter(lambda x: x.name == d.name, res))) != 1:
            raise Exception("unexpected, double definition of " + d.name)

    if filter_applicable_to_model_object:
        res = filter(lambda d: is_applicable_for(model_obj, d), res)

    return dict(map(lambda x: (x.name, x), res))


def get_all_possible_mandatory_properties(model_obj):
    res = get_all_possible_properties(model_obj)
    for name in list(res.keys()):
        if res[name].optional:
            del res[name]
    return res


def get_property_type(attr, prop_name):
    def get_type(internaltype):
        if internaltype == "STRING":
            return str
        elif internaltype == "INT":
            return find_builtin(
                attr, "built_in.int32", "+m:^package.items"
            )  # +m ist not required..
        elif internaltype == "UINT":
            return find_builtin(attr, "built_in.uint32", "+m:^package.items")
        elif internaltype == "BOOL":
            ret = find_builtin(attr, "built_in.bool", "+m:^package.items")
            return ret
        elif internaltype == "FLOAT":
            return find_builtin(attr, "built_in.double", "+m:^package.items")
        else:
            raise Exception("unknown internal type {}".format(internaltype))

    res = list(filter(lambda x: x.definition.name == prop_name, attr.properties))
    if len(res) == 0:
        raise Exception("property {} not found".format(prop_name))
    else:
        mm = get_metamodel(attr)
        textx_assert(len(res) == 1, attr, prop_name + " must be unique")
        res = res[0]
        internaltype = res.definition.internaltype
        if internaltype == "ATTRTYPE":
            textx_assert(
                not textx_isinstance(attr, mm["VariantAttribute"]),
                attr,
                prop_name + " not supported for variants",
            )
            textx_assert(
                textx_isinstance(attr.type, mm["RawType"])
                or textx_isinstance(attr.type, mm["Enum"]),
                attr,
                prop_name + " only applicable for rawtypes/enums",
            )
            return attr.type
        else:
            return get_type(internaltype)


def has_property(attr, prop_name):
    res = list(filter(lambda x: x.definition.name == prop_name, attr.properties))
    if len(res) == 0:
        if prop_name not in get_all_possible_properties(attr):
            raise TextXSemanticError(
                "{} not a possible property".format(prop_name), **get_location(attr)
            )
        return False
    else:
        assert len(res) == 1
        return True


def is_applicable(prop):
    return is_applicable_for(prop.parent, prop.definition)


def is_applicable_for(parent, definition):
    mm = get_metamodel(parent)
    appl = definition.applicable_for

    if len(appl) == 0:
        #  for not apply ATTRTYPE properties for structs
        if (
            textx_isinstance(parent, mm["Struct"])
            and definition.internaltype == "ATTRTYPE"
        ):
            return False
        return True

    if textx_isinstance(parent, mm["Struct"]):
        if "struct_definition" in appl:
            return True
        else:
            return False

    attr = parent
    assert textx_isinstance(attr, mm["Attribute"])
    if "array" in appl or "scalar" in appl:
        if "array" not in appl and textx_isinstance(attr, mm["ArrayAttribute"]):
            return False
        elif "scalar" not in appl and textx_isinstance(attr, mm["ScalarAttribute"]):
            return False
    appl = list(filter(lambda x: x not in ["scalar", "array"], appl))
    if len(appl) == 0:
        return True
    if textx_isinstance(attr, mm["VariantAttribute"]) and "variant" in appl:
        return True
    if textx_isinstance(attr, mm["ArrayAttribute"]) or textx_isinstance(
        attr, mm["ScalarAttribute"]
    ):
        if textx_isinstance(attr.type, mm["Enum"]) and "enum" in appl:
            return True
        if textx_isinstance(attr.type, mm["Struct"]) and "struct" in appl:
            return True
        if textx_isinstance(attr.type, mm["RawType"]):
            rt_appl = list(
                filter(lambda x: textx_isinstance(x, mm["ApplicableForRawType"]), appl)
            )
            allowed = list(
                reduce(
                    lambda x, y: x.extend(y), map(lambda x: x.concrete_types, rt_appl)
                )
            )
            if len(allowed) == 0 and len(rt_appl):
                return True  # all rawtypes allowed
            elif attr.type in allowed:
                return True
    return False


def has_fixpoint(a):
    return has_property(a, "fixpointLsbValue") or has_property(a, "fixpointMsbValue")


def get_fixpoint_LSB_value(a):
    assert has_fixpoint(a), f"expected fixpoint infos for {a.name}"
    if has_property(a, "fixpointLsbValue"):
        return get_property(a, "fixpointLsbValue")
    elif has_property(a, "fixpointMsbValue"):
        return get_property(a, "fixpointMsbValue")/(2**(a.type.bits-1))  # TBC


def get_fixpoint_offset_value(a):
    assert has_fixpoint(a), f"expected fixpoint infos for {a.name}"
    if has_property(a, "fixpointOffsetValue"):
        return get_property(a, "fixpointOffsetValue")
    else:
        return 0.0
