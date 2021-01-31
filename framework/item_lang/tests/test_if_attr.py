from item_lang import lang


def test_if_attr_example0():
    text = r"""
    package example
    struct Point {
      scalar dim : built_in.uint32 (.maxValue=2)
      scalar x : built_in.float
      if (dim>1) scalar y : built_in.float
    }
    """
    mm = lang.metamodel()
    assert mm is not None
    model = mm.model_from_str(text)
    assert model is not None
    assert model.package.items[0].attributes[1].if_attr is None
    assert model.package.items[0].attributes[2].if_attr is not None
    if_attr = model.package.items[0].attributes[2].if_attr
    f = if_attr.predicate.render_formula(prefix="THIS:")
    assert f == "(THIS:dim>1)"