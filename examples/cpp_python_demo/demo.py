import swig_firsttest as e0
from items.Point import Point
import pytest
from mdsd.item_support import *
from mdsd.item.io import *

p = e0.MDSD_Struct_Point()
p.data.x=12.34
p.data.y=56.78
mem = bytearray(100)
p.copy_to_mem(mem)
print(mem)
print("--------------")
q = Point()
copy_from_mem(mem,q)
print("q=",q)
print("--------------")

p0 = e0.Point()
print(p0)
print(p0.x)
print(p0.y)
print(p0.__dict__)

p1 = Point()
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

a = copy(Point(10,12), e0.Point.item_create())
b = copy(Point(-4,18.1), e0.Point.item_create())
c = e0.Point.item_create()
algo.compute(a,b,c)
copy(c,p1)
print(p1)
assert p1.x==pytest.approx(6)
assert p1.y==pytest.approx(30.1)

i = e0.MDSD_Struct_Image()
i.data.w=9
i.data.h=4
i.adjust_array_sizes_and_variants()
print(i.data.pixel)
print(i.data.pixel.size())
print(i.data.pixel[0])


tri = e0.MDSD_Struct_ColoredTriangle()
print(tri.data.color)
print(tri.data.points)
print(tri.data.color[0])
print(tri.data.points[0])


poly = e0.MDSD_Struct_Polygon()
poly.data.n=4
poly.adjust_array_sizes_and_variants()
poly.print_to_stream()

vari = e0.MDSD_Struct_VariantExample()
vari.data.selector=11
vari.adjust_array_sizes_and_variants()
vari.print_to_stream()

print(vari.data.payload)

copy(p1,e0.MDSD_get_Line_from_VariantExample_payload(vari.data).p1)
vari.print_to_stream()
