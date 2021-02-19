from big_example.Info import Info
from mdsd.item.printto import printto
from mdsd.item_support import adjust_array_sizes_and_variants
from big_example.VersionedData import VersionedData
import io


def test_string_with_print():
    i = Info()
    i.text1_as_str = 'Hello "Test"'
    i.n = 3
    adjust_array_sizes_and_variants(i)
    i.text2_as_str = "ABCDE"

    out = io.StringIO()
    printto(i, out)
    text = out.getvalue()
    assert text.index(r'"Hello \"Test\""') > 0
    assert text.count("\n") == 1 + len(i._meta_order)


def test_versioned_type_with_print():
    v = VersionedData()

    v.version = 1
    adjust_array_sizes_and_variants(v)
    out1 = io.StringIO()
    printto(v, out1)

    v.version = 0
    adjust_array_sizes_and_variants(v)
    out0 = io.StringIO()
    printto(v, out0)

    assert "data0" in out0.getvalue()
    assert "data1" not in out0.getvalue()

    assert "data1" in out1.getvalue()
    assert "data0" not in out1.getvalue()
