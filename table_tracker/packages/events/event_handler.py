from abc import ABCMeta
from typing import Literal
from types import NotImplementedType
from packages.utils import check_methods


class EventHandler(metaclass=ABCMeta):

    __slots__: tuple = ()

    @classmethod
    def __subclasshook__(cls, subcls) -> NotImplementedType | Literal[True]:
        return check_methods(subcls, "handle")
