# generated code
from dataclasses import dataclass
import numpy as np
import mdsd_support_library.item_support as support
from typing import Sequence, Union


@dataclass(eq=False)
class Point:
  x : np.float32=0
  y : np.float32=0

  def __post_init__(self):
    support.adjust_array_sizes_and_variants(self)
  def __setattr__(self, attribute, value):
    if not attribute in self._meta:
        raise Exception("Illegal field {} in {}".format(attribute,self.__class__.__name__))
    else:
        if value is None:
            self.__dict__[attribute] = value
        elif self._meta[attribute]["is_variant"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        elif self._meta[attribute]["is_scalar"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_rawtype"]:
                self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        else:
            self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())

  _meta = {
    "x": { "name":"x","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":True,"is_struct":False,"get_type": lambda: np.float32, },
    "y": { "name":"y","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":True,"is_struct":False,"get_type": lambda: np.float32, },
  } # end of _meta


@dataclass(eq=False)
class Line:
  p1 : Point=Point()
  p2 : Point=Point()

  def __post_init__(self):
    support.adjust_array_sizes_and_variants(self)
  def __setattr__(self, attribute, value):
    if not attribute in self._meta:
        raise Exception("Illegal field {} in {}".format(attribute,self.__class__.__name__))
    else:
        if value is None:
            self.__dict__[attribute] = value
        elif self._meta[attribute]["is_variant"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        elif self._meta[attribute]["is_scalar"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_rawtype"]:
                self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        else:
            self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())

  _meta = {
    "p1": { "name":"p1","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":False,"is_struct":True,"get_type": lambda: Point, },
    "p2": { "name":"p2","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":False,"is_struct":True,"get_type": lambda: Point, },
  } # end of _meta


@dataclass(eq=False)
class Circle:
  center : Point=Point()
  radius : np.float32=0

  def __post_init__(self):
    support.adjust_array_sizes_and_variants(self)
  def __setattr__(self, attribute, value):
    if not attribute in self._meta:
        raise Exception("Illegal field {} in {}".format(attribute,self.__class__.__name__))
    else:
        if value is None:
            self.__dict__[attribute] = value
        elif self._meta[attribute]["is_variant"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        elif self._meta[attribute]["is_scalar"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_rawtype"]:
                self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        else:
            self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())

  _meta = {
    "center": { "name":"center","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":False,"is_struct":True,"get_type": lambda: Point, },
    "radius": { "name":"radius","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":True,"is_struct":False,"get_type": lambda: np.float32, },
  } # end of _meta


@dataclass(eq=False)
class ColoredTriangle:
  color : np.ndarray=None
  points : Sequence[Point]=None

  def __post_init__(self):
    support.adjust_array_sizes_and_variants(self)
  def __setattr__(self, attribute, value):
    if not attribute in self._meta:
        raise Exception("Illegal field {} in {}".format(attribute,self.__class__.__name__))
    else:
        if value is None:
            self.__dict__[attribute] = value
        elif self._meta[attribute]["is_variant"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        elif self._meta[attribute]["is_scalar"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_rawtype"]:
                self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        else:
            self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())

  _meta = {
    "color": { "name":"color","is_scalar":False,"is_variant":False,"is_array":True,"is_dynamic_array":False,"get_dim":lambda x:(1*3),"get_dim_nd":lambda x:(3,),"is_rawtype":True,"is_struct":False,"get_type": lambda: np.float32, },
    "points": { "name":"points","is_scalar":False,"is_variant":False,"is_array":True,"is_dynamic_array":False,"get_dim":lambda x:(1*3),"get_dim_nd":lambda x:(3,),"is_rawtype":False,"is_struct":True,"get_type": lambda: Point, },
  } # end of _meta


@dataclass(eq=False)
class Header:
  n : np.uint32=0

  def __post_init__(self):
    support.adjust_array_sizes_and_variants(self)
  def __setattr__(self, attribute, value):
    if not attribute in self._meta:
        raise Exception("Illegal field {} in {}".format(attribute,self.__class__.__name__))
    else:
        if value is None:
            self.__dict__[attribute] = value
        elif self._meta[attribute]["is_variant"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        elif self._meta[attribute]["is_scalar"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_rawtype"]:
                self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        else:
            self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())

  _meta = {
    "n": { "name":"n","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":True,"is_struct":False,"get_type": lambda: np.uint32, },
  } # end of _meta


@dataclass(eq=False)
class Polygon:
  header : Header=Header()
  points : Sequence[Point]=None

  def __post_init__(self):
    support.adjust_array_sizes_and_variants(self)
  def __setattr__(self, attribute, value):
    if not attribute in self._meta:
        raise Exception("Illegal field {} in {}".format(attribute,self.__class__.__name__))
    else:
        if value is None:
            self.__dict__[attribute] = value
        elif self._meta[attribute]["is_variant"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        elif self._meta[attribute]["is_scalar"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_rawtype"]:
                self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        else:
            self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())

  _meta = {
    "header": { "name":"header","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":False,"is_struct":True,"get_type": lambda: Header, },
    "points": { "name":"points","is_scalar":False,"is_variant":False,"is_array":True,"is_dynamic_array":True,"get_dim":lambda x:(1*x.header.n),"get_dim_nd":lambda x:(x.header.n,),"is_rawtype":False,"is_struct":True,"get_type": lambda: Point, },
  } # end of _meta


@dataclass(eq=False)
class VariantExample:
  selector : np.uint32=0
  payload : Union[Point,Line,Circle,Polygon,ColoredTriangle]=None

  def __post_init__(self):
    support.adjust_array_sizes_and_variants(self)
  def __setattr__(self, attribute, value):
    if not attribute in self._meta:
        raise Exception("Illegal field {} in {}".format(attribute,self.__class__.__name__))
    else:
        if value is None:
            self.__dict__[attribute] = value
        elif self._meta[attribute]["is_variant"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        elif self._meta[attribute]["is_scalar"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_rawtype"]:
                self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        else:
            self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())

  _meta = {
    "selector": { "name":"selector","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":True,"is_struct":False,"get_type": lambda: np.uint32, },
    "payload": { "name":"payload","get_type_for": lambda s: {10:Point,11:Line,12:Circle,20:Polygon,0:ColoredTriangle}[s.selector], "is_scalar":True,"is_variant":True,"is_array":False,"is_rawtype":False,"is_struct":True,"get_type": lambda: (Point,Line,Circle,Polygon,ColoredTriangle), },
  } # end of _meta


@dataclass(eq=False)
class Region:
  min : Point=Point()
  max : Point=Point()

  def __post_init__(self):
    support.adjust_array_sizes_and_variants(self)
  def __setattr__(self, attribute, value):
    if not attribute in self._meta:
        raise Exception("Illegal field {} in {}".format(attribute,self.__class__.__name__))
    else:
        if value is None:
            self.__dict__[attribute] = value
        elif self._meta[attribute]["is_variant"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        elif self._meta[attribute]["is_scalar"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_rawtype"]:
                self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        else:
            self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())

  _meta = {
    "min": { "name":"min","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":False,"is_struct":True,"get_type": lambda: Point, },
    "max": { "name":"max","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":False,"is_struct":True,"get_type": lambda: Point, },
  } # end of _meta


@dataclass(eq=False)
class Image:
  w : np.uint32=0
  h : np.uint32=0
  pixel : np.ndarray=None

  def __post_init__(self):
    support.adjust_array_sizes_and_variants(self)
  def __setattr__(self, attribute, value):
    if not attribute in self._meta:
        raise Exception("Illegal field {} in {}".format(attribute,self.__class__.__name__))
    else:
        if value is None:
            self.__dict__[attribute] = value
        elif self._meta[attribute]["is_variant"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        elif self._meta[attribute]["is_scalar"]:
            if isinstance(value, self._meta[attribute]["get_type"]()):
                self.__dict__[attribute] = value
            elif self._meta[attribute]["is_rawtype"]:
                self.__dict__[attribute] = self._meta[attribute]["get_type"]()(value)
            else:
                raise Exception("Illegal value of type {} for field {}".format(value.__class__.__name__,attribute))
        else:
            self.__dict__[attribute] = np.array(value, dtype=self._meta[attribute]["get_type"]())

  _meta = {
    "w": { "name":"w","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":True,"is_struct":False,"get_type": lambda: np.uint32, },
    "h": { "name":"h","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":True,"is_struct":False,"get_type": lambda: np.uint32, },
    "pixel": { "name":"pixel","is_scalar":False,"is_variant":False,"is_array":True,"is_dynamic_array":True,"get_dim":lambda x:(1*(x.w*x.h)),"get_dim_nd":lambda x:((x.w*x.h),),"is_rawtype":True,"is_struct":False,"get_type": lambda: np.float32, },
  } # end of _meta
