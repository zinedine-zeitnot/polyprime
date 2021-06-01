import itertools
from typing import Callable, Iterable, TypeVar

import toolz

X = TypeVar("X")


def iterate(f: Callable[[X], X]) -> Callable[[X], Iterable[X]]:
    """
    (curried version of toolz.itertoolz.iterate())

    Takes a function f: X -> X and yields the function that, given an element x from X, returns the
    infinite stream of repeated f-iterations starting from x, i.e. [x, f(x), f(f(x)), ...].

    To be used in conjunction with "take-first-values-and-stop-after-that" methods like
    toolz.itertoolz.take() or toolz.itertoolz.takewhile() or similar methods.

    Example:
        In [1]: iterate(lambda x: x**2)(2)
        Out[1]: <generator object [2, 4, 16, 256, 65536, ...]>

        In [2]: list(toolz.itertoolz.take(4, iterate(lambda x: x ** 2)(2)))
        Out[2]: [2, 4, 16, 256]
    """
    return lambda x: toolz.itertoolz.iterate(f, x)


def takewhile(p: Callable[[X], bool]) -> Callable[[Iterable[X]], Iterable[X]]:
    """
    (curried version of itertools.takewhile())

    Takes a predicate (boolean function) p: X -> bool and yields the function that, given an
    iterable sequence of X-values, returns its longest "p-consecutively-True" initial subsequence.

    Example:
        In [1]: even = lambda x: x % 2 == 0

        In [2]: takewhile(even)([2, 4, 6, 8, 11, 12, 14, 16])
        Out[2]: [2, 4, 6, 8]

        In [3]: takewhile(even)([1, 2, 4, 6, 8, 10])
        Out[3]: []
    """
    return (
        lambda xs: list(itertools.takewhile(p, xs))
        if isinstance(xs, list)
        else itertools.takewhile(p, xs)
    )
