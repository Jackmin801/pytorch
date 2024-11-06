# mypy: allow-untyped-defs
from typing import Generator
from contextlib import contextmanager


try:
    from torch._C import _itt
except ImportError:

    class _ITTStub:
        @staticmethod
        def _fail(*args, **kwargs):
            raise RuntimeError(
                "ITT functions not installed. Are you sure you have a ITT build?"
            )

        @staticmethod
        def is_available():
            return False

        rangePush = _fail
        rangePop = _fail
        mark = _fail
        range = _fail

    _itt = _ITTStub()  # type: ignore[assignment]


__all__ = ["is_available", "range_push", "range_pop", "mark", "range"]


def is_available() -> bool:
    """
    Check if ITT feature is available or not
    """
    return _itt.is_available()


def range_push(msg: str) -> None:
    """
    Pushes a range onto a stack of nested range span.  Returns zero-based
    depth of the range that is started.

    Arguments:
        msg (str): ASCII message to associate with range
    """
    return _itt.rangePush(msg)


def range_pop() -> None:
    """
    Pops a range off of a stack of nested range spans. Returns the
    zero-based depth of the range that is ended.
    """
    return _itt.rangePop()


def mark(msg: str) -> None:
    """
    Describe an instantaneous event that occurred at some point.

    Arguments:
        msg (str): ASCII message to associate with the event.
    """
    return _itt.mark(msg)


# TODO: Maybe rename this function to not have name conflict with Python's built-in range
@contextmanager
def range(msg: str, *args, **kwargs) -> Generator[None, None, None]:
    """
    Context manager / decorator that pushes an ITT range at the beginning
    of its scope, and pops it at the end. If extra arguments are given,
    they are passed as arguments to msg.format().

    Args:
        msg (str): message to associate with the range
    """
    range_push(msg.format(*args, **kwargs))
    try:
        yield
    finally:
        range_pop()
