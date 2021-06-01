import pytest

from polyprime.miller_rabin import prime


@pytest.mark.parametrize(
    "n",
    [5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607],
)
def test_prime(n):
    """
    Tests the primality of some Mersenne primes.

    See https://en.wikipedia.org/wiki/Mersenne_prime#List_of_known_Mersenne_primes.
    """
    assert prime(2 ** n - 1)


@pytest.mark.parametrize(
    "n", [11, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71, 73, 79, 83, 97, 101, 103]
)
def test_non_prime(n):
    """
    Tests the compositeness of some non-prime Mersenne numbers.

    See https://en.wikipedia.org/wiki/Mersenne_prime#Factorization_of_composite_Mersenne_numbers.
    """
    assert not prime(2 ** n - 1)
