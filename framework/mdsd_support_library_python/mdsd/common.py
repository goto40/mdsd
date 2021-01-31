class ArrayLike:
    def __init__(self, getter, setter, mytype = bool):
        self.getter = getter
        self.setter = setter
        self.mytype = mytype

    def __getitem__(self, idx):
        return self.getter(idx)

    def __setitem__(self, idx, value):
        assert isinstance(value, self.mytype)
        self.setter(idx, value)
