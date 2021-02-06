from dataclasses import dataclass
import numpy as np
import pytest
from typing import Sequence, Union
from enum import Enum
from mdsd.common import ArrayLike


class Season(Enum):
    SPRING = 1
    SUMMER = 2
    AUTUMN = 3
    WINTER = 4


@dataclass(eq=False)
class Point:
    x: np.float32 = 0
    y: np.float32 = 0
    flags: np.uint32 = 0

    @property
    def myflag(self):
        return (self.flags & 2) !=0

    @myflag.setter
    def myflag(self, v):
        assert isinstance(v, bool)
        if v:
            self.flags = self.flags | 2
        else:
            self.flags = self.flags & (~np.uint32(2))

    @property
    def allflags(self):
        def getter(idx):
            (self.flags & (1 << idx)) != 0,
        def setter(idx, val):
            self.flags = (self.flags & (~(1 << idx))) | ((val & 1) << idx)
        return ArrayLike( getter, setter )

    @property
    def mySeason(self):
        return Season(self.flags&7)

    @mySeason.setter
    def mySeason(self, v):
        assert isinstance(v, Season)
        self.flags = (self.flags & (~np.uint32(7))) | v.value


def test_property_demo():
    p = Point()
    p.x = 1
    p.y = 2

    assert p.flags == 0
    p.myflag = True
    assert p.flags == 2
    assert p.myflag
    p.flags = 3
    p.myflag = False
    assert not p.myflag
    assert p.flags == 1

    p.flags = 0
    p.allflags[0] = True
    assert p.flags == 1
    p.allflags[1] = True
    assert p.flags == 3
    p.allflags[2] = True
    assert p.flags == 7
    p.allflags[0] = False
    assert p.flags == 6

    with pytest.raises(Exception):
        p.allflags[0] = 6 # not a bool

    with pytest.raises(Exception):
        p.myflag = 6

    p.flags = 0
    p.mySeason = Season.WINTER
    assert p.mySeason == Season.WINTER
    p.mySeason = Season(2)
    assert p.mySeason == Season.SUMMER
    p.flags = 4

    with pytest.raises(Exception):
        p.mySeason = 4
