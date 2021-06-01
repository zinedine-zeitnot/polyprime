import pytest

from polyprime.prime_field_polynomial import PrimeFieldPolynomial

X = PrimeFieldPolynomial.X(p=17)


@pytest.mark.parametrize(
    "P, n, expected",
    [
        (X + 1, 0, 1),
        (X + 1, 1, X + 1),
        (X + 1, 2, X ** 2 + 2 * X + 1),
        (X + 1, 3, X ** 3 + 3 * X ** 2 + 3 * X + 1),
        (X + 1, 4, X ** 4 + 4 * X ** 3 + 6 * X ** 2 + 4 * X + 1),
        (X + 1, 17, X ** 17 + 1),
    ],
)
def test_exponentiation(P, n, expected):
    assert P ** n == expected


def test_exponentiation_with_invalid_exponent():
    P = X + 1

    with pytest.raises(AssertionError, match="n must be a positive integer"):
        P ** (-1)
