from abc import ABCMeta
from typing import Any,Self

class Interface(type):
    
    def __new__(mcls: type[Self], name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kwargs: str) -> Self:
        
        for value in kwargs.values():
            
            if type(value) is not str:
                raise TypeError("Wrong interface arfument")
            elif not hasattr(bases,value) and not callable(getattr(bases,value)):
                raise NotImplementedError(f"{value} not implemented in {name.__class__.__name__} class")
        
        return super().__new__(mcls, name, bases, namespace)
