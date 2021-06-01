import math
import random
from typing import Callable

import toolz

from polyprime.list_utils import iterate, takewhile


def highest_power_of(k: int) -> Callable[[int], int]:
    """
    Returns the function yielding the highest power of k dividing a given integer (also called the
    k-adic order or k-adic valuation when k is prime).

    Example:
        In [1]: highest_power_of(2)(5 * 2**1023)
        Out[1]: 1023
    """
    return lambda n: toolz.functoolz.pipe(
        n,
        iterate(lambda n: n // k),
        takewhile(lambda n: n % k == 0 and n != 1),
        list,
        len,
    )


def miller_rabin_witness(n: int, a: int) -> bool:
    """
    Tests whether the integer a is a Miller-Rabin witness for (the compositeness of) n.

    Reference: cf. Definition 2.3 (page 2) in miller-rabin.pdf.
    """
    if math.gcd(a, n) > 1:
        return True

    # n-1 = k * 2**e with k odd:
    e = highest_power_of(2)(n - 1)
    k = (n - 1) // 2 ** e

    return all(
        [pow(a, k, mod=n) != 1] + [pow(a, k * 2 ** i, mod=n) != n - 1 for i in range(e)]
    )


def prime(n: int, t: int = 10) -> bool:
    """
    Tests the primality of the integer n according to Miller-Rabin's test.

    Returns:
        - False if n is composite
        - True if n is probably prime with probability at least 1-4**(-t)

    Reference: cf. the description of the Miller-Rabin test right below Example 2.10 (page 4) in
    miller-rabin.pdf.
    """
    witness_candidates = [random.randint(2, n - 2) for _ in range(t + 1)]
    return not any([miller_rabin_witness(n, a) for a in witness_candidates])
