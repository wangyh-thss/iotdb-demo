from enum import Enum


class EnumWithMeta(Enum):

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # Ignores the first param since it is already set by __new__.
    def __init__(self, _: int, meta):
        self._meta_ = meta

    def __str__(self):
        return self.value
