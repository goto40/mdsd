from textx import metamodel_for_language, get_children_of_type
import os
from item_lang.attributes import is_dynamic


def test_is_dynamic():
    mm = metamodel_for_language("item")
    assert mm is not None
    model = mm.model_from_file(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "model", "big_example.item"))
    assert model is not None

    Color = next(filter(lambda x:x.name == "Color", get_children_of_type("Struct",model)))
    assert Color.name == "Color"
    assert not is_dynamic(Color.attributes[0])
    assert not is_dynamic(Color)

    MultiMessage = next(filter(lambda x:x.name == "MultiMessage", get_children_of_type("Struct",model)))
    assert MultiMessage.name == "MultiMessage"
    assert is_dynamic(MultiMessage)

    Polygon = next(filter(lambda x:x.name == "Polygon", get_children_of_type("Struct",model)))
    assert Polygon.name == "Polygon"
    assert not is_dynamic(Polygon.attributes[0])
    assert is_dynamic(Polygon.attributes[1])
    assert not is_dynamic(Polygon.attributes[2])
    assert is_dynamic(Polygon)
