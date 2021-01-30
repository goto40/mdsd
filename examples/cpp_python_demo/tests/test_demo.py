import swig_firsttest as e0
import items.example as e1
import pytest
from mdsd_support_library.item_support import *
from mdsd_support_library.item_io import *

def test_1():
    p = e0.MDSD_Struct_Point()
    p.data.x=12.34
    p.data.y=56.78
    mem = bytearray(100)
    p.copy_to_mem(mem)
    print(mem)
    print("--------------")
    q = e1.Point()
    copy_from_mem(mem,q)
    print("q=",q)
    print("--------------")
    
    assert p.data.x == pytest.approx(q.x)
    assert p.data.y == pytest.approx(q.y)
    
def test_2():
    p0 = e0.Point()
    print(p0)
    print(p0.x)
    print(p0.y)
    print(p0.__dict__)

    p1 = e1.Point()
    print(p1.__dict__)

    p0.x=9
    p0.y=-1.2
    copy(p0,p1)
    print(p1)

    print(e0.VectorAdd.get_classname())
    algo = e0.VectorAdd.create()

    n = algo.get_classname()
    print(n)
    print(n.__class__)

    a = copy(e1.Point(10,12), e0.Point.item_create())
    b = copy(e1.Point(-4,18.1), e0.Point.item_create())
    c = e0.Point.item_create()
    algo.compute(a,b,c)
    copy(c,p1)
    print(p1)
    assert p1.x==pytest.approx(6)
    assert p1.y==pytest.approx(30.1)


def test_2_as_it_is_intended_to_be_used():
    algo = e0.VectorAdd.create()
    p0 = e1.Point(11.11,22.22)
    p1 = e1.Point(33.33,44.44)

    a = copy(p0, e0.Point.item_create())
    b = copy(p1, e0.Point.item_create())
    c = e0.Point.item_create()
    algo.compute(a,b,c)
    
    res = copy(c,e1.Point())

    assert res.x==pytest.approx(p0.x+p1.x)
    assert res.y==pytest.approx(p0.y+p1.y)


def test_3():
    i = e0.MDSD_Struct_Image()
    i.data.w=9
    i.data.h=4
    i.adjust_array_sizes_and_variants()
    assert i.data.pixel.size() == 9*4

    tri = e0.MDSD_Struct_ColoredTriangle()
    assert tri.data.color.size() == 3
    assert tri.data.points.size() == 3

    poly = e0.MDSD_Struct_Polygon()
    poly.data.header.n=4
    poly.adjust_array_sizes_and_variants()
    #poly.print_to_stream()
    assert poly.data.points.size() == 4

    vari = e0.MDSD_Struct_VariantExample()
    vari.data.selector=11
    vari.adjust_array_sizes_and_variants()
    #vari.print_to_stream()

    print(vari.data.payload)

    p1 = e1.Point()
    p1.x = 11

    copy(p1,e0.MDSD_get_Line_from_VariantExample_payload(vari.data).p1)
    #vari.print_to_stream()

    assert e0.MDSD_get_Line_from_VariantExample_payload(vari.data).p1.x == pytest.approx(p1.x)
    
    p1.x = 10
    copy(p1,e0.MDSD_get_Line_from_VariantExample_payload(vari.data).p1)
    assert e0.MDSD_get_Line_from_VariantExample_payload(vari.data).p1.x == pytest.approx(p1.x)
