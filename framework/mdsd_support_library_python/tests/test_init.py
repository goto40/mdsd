from mdsd.item.init_default_values import init_default_values
from big_example.Info import Info


def test_init_default_values():
    i = Info()
    i.n = 3
    init_default_values(i)
    assert i.n == 16
    assert i.text1_as_str == "This is text1"
