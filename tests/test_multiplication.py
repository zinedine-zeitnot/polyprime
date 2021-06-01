import pytest

from polyprime.prime_field_polynomial import PrimeFieldPolynomial

X = PrimeFieldPolynomial.X(p=17)


@pytest.mark.parametrize(
    "P, Q, expected_product",
    [
        (0, X, 0),
        (17, X, 0),
        (1, X, X),
        (X, 2, 2 * X),
        (X, X ** 2, X ** 3),
        (X + 1, X + 2, X ** 2 + 3 * X + 2),
        (X + 1, X + 16, X ** 2 + 16),
        (X + 1, X - 1, X ** 2 + 16),
        (X + 1, X - 1, X ** 2 - 1),
    ],
)
def test_multiplication(P, Q, expected_product):
    assert P * Q == Q * P == expected_product


def test_multiplication_with_incoherent_primes():
    P = PrimeFieldPolynomial(coefs=[1, 0, 1], p=17)
    Q = PrimeFieldPolynomial(coefs=[0, 2, 1], p=13)

    with pytest.raises(
        AssertionError, match="Polynomials must be defined over the same prime field."
    ):
        P * Q
