from project_tool import SwigTool, Header
import pytest
import os


def test_create_order1():
    tool = SwigTool(["."])
    a = Header("a.h",".")
    b = Header("b.h",".")
    c = Header("c.h",".")

    tool.headers.append(a)
    tool.headers.append(b)
    tool.headers.append(c)

    a.headers.append(b)
    a.headers.append(c)
    b.headers.append(c)

    h = tool.get_sorted()
    assert h[0] == c
    assert h[1] == b
    assert h[2] == a

def test_create_order2():
    tool = SwigTool(["."])
    a = Header("a.h",".")
    b = Header("b.h",".")
    c = Header("c.h",".")

    tool.headers.append(a)
    tool.headers.append(b)
    tool.headers.append(c)

    c.headers.append(b)
    b.headers.append(a)

    h = tool.get_sorted()
    assert h[0] == a
    assert h[1] == b
    assert h[2] == c

def test_create_order3():
    tool = SwigTool(["."])
    a = Header("a.h",".")
    b = Header("b.h",".")
    c = Header("c.h",".")

    tool.headers.append(a)
    tool.headers.append(b)
    tool.headers.append(c)

    c.headers.append(b)
    b.headers.append(a)
    a.headers.append(c)

    with pytest.raises(Exception):
        tool.get_sorted()


def test_create_lookup1():
    tool = SwigTool(["."])
    a = Header("a.h",".")
    b = Header("b.h",".")
    c = Header("c.h",".")

    tool.headers.append(a)
    tool.headers.append(b)
    tool.headers.append(c)

    assert a==tool.lookup("a.h")
    assert b==tool.lookup("b.h")
    assert c==tool.lookup("c.h")

    with pytest.raises(Exception):
        tool.lookup("unknown.h")
    with pytest.raises(Exception):
        tool.lookup("A.h")
    with pytest.raises(Exception):
        tool.lookup("a")
    with pytest.raises(Exception):
        tool.lookup("a.hpp")


def test_create_lookup2():
    tool = SwigTool(["lib1","lib2"])
    a = Header("a.h","lib1")
    b = Header("x/b.h","lib2")
    c = Header("x/c.h","lib2")
    d = Header("x/d.h","lib1")

    tool.headers.append(a)
    tool.headers.append(b)
    tool.headers.append(c)
    tool.headers.append(d)

    assert a==tool.lookup("a.h")
    assert b==tool.lookup("x/b.h")
    assert c==tool.lookup("x/c.h")
    assert d==tool.lookup("x/d.h")

    with pytest.raises(Exception):
        tool.lookup("b.h")

    assert b==tool.lookup("b.h",c)
    with pytest.raises(Exception):
        tool.lookup("b.h", d)


def test_with_real_files():
    base = os.path.dirname(__file__)
    tool = SwigTool([
        os.path.join(base, "example_ok", "lib1"),
        os.path.join(base, "example_ok", "lib2"),
    ])
    tool.analyze()

    assert len(tool.headers) == 6

    a = tool.lookup("a.h")
    b = tool.lookup("x/b.h",a)
    assert len(b.headers) == 3

    x_a = tool.lookup("x/a.h")
    assert x_a != a

    c = tool.lookup("x/c.h")
    x_a2 = tool.lookup("a.h",c)
    assert x_a2 == x_a
    assert len(c.headers) == 0
    assert a.basedir.endswith("lib1")
    assert len(a.headers) == 1

    s = tool.get_sorted()

    for h in s:
        print(h)
    assert s[0].path == "x/c.h"
    assert s[1].path == "x/e.h"
    assert s[-2].path == "a.h"
    assert s[-1].path == "x/d.h"


def test_with_real_files_require_pattern1():
    base = os.path.dirname(__file__)
    tool = SwigTool([
        os.path.join(base, "example_ok", "lib1"),
        os.path.join(base, "example_ok", "lib2"),
    ], r"^\s*//\s*ACTIVATE FOR SWIG\s*$")
    tool.analyze()

    assert len(list(filter(lambda x:x.relevant, tool.headers))) == 1


def test_with_real_files_require_pattern1():
    base = os.path.dirname(__file__)
    tool = SwigTool([
        os.path.join(base, "example_ok", "lib1"),
        os.path.join(base, "example_ok", "lib2"),
    ], r"^\s*//\s*ACTIVATE FOR SWIG")
    tool.analyze()

    assert len(list(filter(lambda x:x.relevant, tool.headers))) == 2
