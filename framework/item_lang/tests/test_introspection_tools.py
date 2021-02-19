import item_lang.metamodel_classes as mmc
import item_lang.metamodel_formula as fc
import item_lang.validation as v


def test_metamodel_classes():
    classes = mmc.get_all_classes()
    print(classes)

    fpos = [fc.Sum, fc.Dif, fc.Mul, fc.Div, fc.Val, fc.AttrRef]
    fneg = [fc.CustomIdlBase, fc.FormulaBase]

    for c in fpos:
        assert c in classes

    for c in fneg:
        assert c not in classes

    fpos = [
        mmc.Package,
        mmc.ScalarAttribute,
        mmc.VariantAttribute,
        mmc.Struct,
        mmc.RawType,
        mmc.ArrayAttribute,
        mmc.Enum,
        mmc.PropertyDefinition,
    ]
    fneg = []

    for c in fpos:
        assert c in classes

    for c in fneg:
        assert c not in classes


def test_validation_checks():
    vm = v.get_all_checks_as_map()
    assert "Sum" in vm
    assert vm["Sum"] is not None
    assert "Unknown" not in vm
    assert len(vm) > 4
