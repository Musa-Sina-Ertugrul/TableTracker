from abc import ABCMeta
from typing import Any,Self

class Interface(type):
    
    def __new__(mcls: type[Self], name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kwargs: str) -> Self:

        for value in kwargs.values():
            if type(value) is not str:
                raise TypeError("Wrong interface argument")
            elif not namespace.get(value,False) or not callable(namespace.get(value,None)):
                raise NotImplementedError(f"{value} not implemented in {name} class")
        
        return super().__new__(mcls, name, bases, namespace)
