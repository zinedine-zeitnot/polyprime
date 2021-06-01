import pytest

from polyprime.prime_field_polynomial import PrimeFieldPolynomial

X = PrimeFieldPolynomial.X(p=17)


@pytest.mark.parametrize(
    "P, x, expected_value",
    [
        (X, 3, 3),
        (3 + 0 * X, 16, 3),
        (0 * X, 5, 0),
        (X ** 17, 3, 3),  # X**p = X thanks to Fermat's Little Theorem
        (
            X ** 16
            + X ** 15
            + X ** 14
            + X ** 13
            + X ** 12
            + X ** 11
            + X ** 10
            + X ** 9
            + X ** 8
            + X ** 7
            + X ** 6
            + X ** 5
            + X ** 4
            + X ** 3
            + X ** 2
            + X
            + 1,
            1,
            0,
        ),
    ],
)
def test_evaluation(P, x, expected_value):
    assert P(x) == expected_value
