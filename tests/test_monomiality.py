import pytest

from polyprime.prime_field_polynomial import PrimeFieldPolynomial

X = PrimeFieldPolynomial.X(p=17)


@pytest.mark.parametrize(
    "polynomial", [X, X ** 2, X ** 100, 3 * X ** 5, 5 * X ** 10 + 17]
)
def test_polynomial_is_monomial(polynomial):
    assert polynomial.is_monomial


@pytest.mark.parametrize(
    "polynomial", [0 * X ** 2, 17 * X ** 100, 3 + 0 * X, X + 1, X ** 5 + 1]
)
def test_polynomial_is_not_monomial(polynomial):
    assert not polynomial.is_monomial
