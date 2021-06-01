import pytest

from polyprime.prime_field_polynomial import PrimeFieldPolynomial

X = PrimeFieldPolynomial.X(p=17)


@pytest.mark.parametrize(
    "P, Q, expected_subtraction",
    [
        (0, X, -X),
        (0 * X, X, -X),
        (2, 0 * X, 2),
        (0 * X, 1, -1),
        (X, 0, X),
        (X, 0 * X, X),
        (2, X, 2 - X),
        (X, 2, X - 2),
        (X + 1, X + 2, 16),
        (X, -16 * X, 0),
        (
            X ** 5 + X ** 3 + X,
            X ** 4 + X ** 2 + 1,
            X ** 5 + 16 * X ** 4 + X ** 3 + 16 * X ** 2 + X + 16,
        ),
    ],
)
def test_subtraction(P, Q, expected_subtraction):
    assert P - Q == expected_subtraction


def test_subtraction_with_incoherent_primes():
    P = PrimeFieldPolynomial(coefs=[1, 0, 1], p=17)
    Q = PrimeFieldPolynomial(coefs=[0, 2, 1], p=13)

    with pytest.raises(
        AssertionError, match="Polynomials must be defined over the same prime field."
    ):
        P - Q
