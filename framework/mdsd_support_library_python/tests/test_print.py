from big_example.Info import Info
from mdsd.item.printto import printto
from mdsd.item_support import adjust_array_sizes_and_variants
import io


def test_string_with_print():
    i = Info()
    i.text1_as_str = 'Hello "Test"'
    i.n=3
    adjust_array_sizes_and_variants(i)
    i.text2_as_str = "ABCDE"

    out = io.StringIO()
    printto(i,out)
    print(out.getvalue())
    assert out.getvalue().index(r'"Hello \"Test\""')>0
    assert out.getvalue().count('\n') == 1+len(i._meta_order)
