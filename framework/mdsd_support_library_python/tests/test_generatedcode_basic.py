from items.Point import *
from items.Polygon import *
from items.Line import *
from items.ColoredTriangle import *
from items.VariantExample import *
from items.Image import *
import pytest


def test_basic():
    p=Point(int(1),2.1)
    assert p.x==pytest.approx(1)
    assert p.y==pytest.approx(2.1)


def test_typecheck():
    l=Line()
    l.p1 = Point()
    l.p1 = None  # "ok"
    with pytest.raises(Exception,match=".*Illegal value of type Polygon for field p1.*"):
        l.p1 = Polygon()


def test_basic_illegal_field():
    p=Point(1,2)
    p.x=3
    with pytest.raises(Exception,match=".*Illegal.*new_field.*"):
        p.new_field=4


def test_basic_typecheck_for_arrays():
    t=ColoredTriangle()
    t.color = [1,2,3]
    assert t.color.dtype.type is np.float32
    t.points = [Point(),Point(),Point()]
    assert t.points.dtype.type is np.object_  # not so good!
    support.check_array_sizes_and_variants(t)
    t.points[1] = Line()
    with pytest.raises(Exception,match=".*unexpected.*Line.*points.*ColoredTriangle.*"):
        support.check_array_sizes_and_variants(t)
    with pytest.raises(Exception,match=".*unexpected.*Line.*points.*ColoredTriangle.*"):
        support.check_array_sizes_and_variants(t)


def test_basic_array():
    m=Polygon();
    m.header.n=10
    support.adjust_array_sizes_and_variants(m)
    assert len(m.points)==10
    assert m.points[0].x==0


def test_basic_variant():
    m=VariantExample();
    m.selector=10
    support.adjust_array_sizes_and_variants(m)
    assert m.payload.__class__ is Point
    m.selector=11
    support.adjust_array_sizes_and_variants(m)
    assert m.payload.__class__ is Line
    m.selector=99
    with pytest.raises(Exception):
        support.check_array_sizes_and_variants(m)

    m.selector=20
    support.adjust_array_sizes_and_variants(m)
    assert m.payload.__class__ is Polygon
    m.payload.header.n=3
    support.adjust_array_sizes_and_variants(m)
    assert len(m.payload.points)==3
    m.payload.header.n=2
    support.adjust_array_sizes_and_variants(m.payload)
    assert len(m.payload.points)==2


def test_arrays():
    i = Image()
    i.w=10
    i.h=3
    with pytest.raises(Exception):
        support.check_array_sizes_and_variants(i)
    support.adjust_array_sizes_and_variants(i)
    assert len(i.pixel)==3*10


def test_arrays2():
    t = ColoredTriangle()
    assert len(t.color)==3
    assert len(t.points)==3
    assert t.color.__class__ is np.ndarray
    assert t.points.__class__ is np.ndarray
