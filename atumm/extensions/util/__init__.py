import warnings
from typing import Callable


def deprecated(msg: str) -> Callable:
    """This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            warnings.warn(f"{msg}", category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator
