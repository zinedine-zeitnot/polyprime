import pytest

from polyprime.prime_field_polynomial import PrimeFieldPolynomial

X = PrimeFieldPolynomial.X(p=17)


@pytest.mark.parametrize(
    "polynomial, expected_degree",
    [
        (X, 1),
        (X ** 2, 2),
        (X ** 500, 500),
        ((X + 1) ** 5, 5),
        (2 + 0 * X, 0),
        (0 * X, -1),
        (17 * X, -1),
    ],
)
def test_degree(polynomial, expected_degree):
    assert polynomial.degree == expected_degree
