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


def dropwhile(p: Callable[[X], bool]) -> Callable[[Iterable[X]], Iterable[X]]:
    """
    (curried version of itertools.takewhile())

    Takes a predicate (boolean function) p: X -> bool and yields the complement of the takewhile(p)
    function (i.e. yields the function that, given an iterable sequence of X-values, drops every
    element of the sequence while p is True and stops when p first becomes False).

    Example:
        In [1]: even = lambda x: x % 2 == 0

        In [2]: dropwhile(even)([2, 4, 6, 8, 11, 12, 14, 16])
        Out[2]: [11, 12, 14, 16]

        In [3]: dropwhile(even)([1, 2, 4, 6, 8, 10])
        Out[3]: [1, 2, 4, 6, 8, 10]
    """
    return (
        lambda x: list(itertools.dropwhile(p, x))
        if isinstance(x, list)
        else itertools.dropwhile(p, x)
    )


def reverse(x: list) -> list:
    return x[::-1]


def trim_trailing_zeroes(x: list) -> list:
    """
    Trim the trailing zeroes of a list.

    Example:
        In [1]: trim_trailing_zeroes([1, 2, 3, 0, 0, 0])
        Out[1]: [1, 2, 3]

        In [2]: trim_trailing_zeroes([0, 0, 0])
        Out[2]: []
    """

    def zero(y):
        return y == 0

    return toolz.functoolz.pipe(x, reverse, dropwhile(zero), reverse)


def long_zip_with(operation, fill_missings_with):
    """
    Returns the function zipping a pair of lists based on the longest one
    (while filling the missing values of the shortest with the supplied filler value) and
    subsequently applying the provided binary operation onto each pair of the zipped list.

    Example:
        In [1]: pair = ([1, 2], [100, 200, 300, 400])  # a list with two sublists would work too

        In [2]: long_zip_with(sum, fill_missings_with=0)(pair)
        Out[2]: [101, 202, 300, 400]
    """
    return lambda x: list(
        map(operation, itertools.zip_longest(x[0], x[1], fillvalue=fill_missings_with))
    )
