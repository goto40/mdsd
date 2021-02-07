from big_example.Info import Info
from mdsd.item_support import adjust_array_sizes_and_variants


def test_string1():
    i = Info()
    i.text1_as_str = "Hello"
    assert i.text1_as_str == "Hello"
    i.n=3
    adjust_array_sizes_and_variants(i)
    assert len(i.text2) == 3
    i.text2_as_str = "ABCDE"
    assert i.text2_as_str == "ABC"

    i.c_as_str = 'X'
    assert i.c_as_str == 'X'
