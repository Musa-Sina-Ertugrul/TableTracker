
def check_methods(subcls, *methods):
    mro = subcls.__mro__
    for method in methods:
        for cls in mro:
            if method in cls.__dict__:
                if cls.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented
    return True