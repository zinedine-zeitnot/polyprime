import pytest

from polyprime.prime_field_polynomial import PrimeFieldPolynomial

X = PrimeFieldPolynomial.X(p=17)


@pytest.mark.parametrize(
    "polynomial, expected_representation",
    [
        (PrimeFieldPolynomial(coefs=[0, 1, 1], p=17), "X**2 + X"),
        (PrimeFieldPolynomial(coefs=[17, 18], p=17), "X"),
        (PrimeFieldPolynomial(coefs=[1, 2, 3, 4], p=17), "4X**3 + 3X**2 + 2X + 1"),
        (1 + X ** 2, "X**2 + 1"),
        (0 * X, "0"),
    ],
)
def test_representation(polynomial, expected_representation):
    assert str(polynomial) == expected_representation
