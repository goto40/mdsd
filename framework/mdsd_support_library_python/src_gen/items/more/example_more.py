# generated code
from dataclasses import dataclass
import numpy as np
import mdsd_support_library.item_support as support
from typing import Sequence, Union


@dataclass(eq=False)
class Point3D:
  x : np.float32=0
  y : np.float32=0
  z : np.float32=0

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
    "z": { "name":"z","is_scalar":True,"is_variant":False,"is_array":False,"is_rawtype":True,"is_struct":False,"get_type": lambda: np.float32, },
  } # end of _meta
