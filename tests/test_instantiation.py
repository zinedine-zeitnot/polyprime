import pytest

from polyprime.prime_field_polynomial import PrimeFieldPolynomial

X = PrimeFieldPolynomial.X(p=17)


def test_instantiation():
    P = PrimeFieldPolynomial(coefs=[17, 18, 0, 0, 0, 0], p=17)

    assert P == X
    assert P.coefs == [0, 1]


def test_instantiating_polynomial_with_non_integer_coefs():
    with pytest.raises(AssertionError, match="Polynomial coefs must all be integers."):
        PrimeFieldPolynomial(coefs=[1.5, 0, 0, 1], p=17)


def test_instantiating_polynomial_over_non_prime_field():
    with pytest.raises(AssertionError, match="p must be prime."):
        PrimeFieldPolynomial(coefs=[1, 0, 1], p=17.5)

    with pytest.raises(AssertionError, match="p must be prime."):
        PrimeFieldPolynomial(coefs=[1, 0, 1], p=8)
