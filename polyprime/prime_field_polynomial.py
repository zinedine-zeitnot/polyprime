from typing import Union

from polyprime.list_utils import dropwhile, long_zip_with, reverse, trim_trailing_zeroes
from polyprime.miller_rabin import prime


class PrimeFieldPolynomial:
    """
    Class for instantiating polynomials over the field of integers modulo a prime number p
    (i.e. over the field Z/pZ = {0, 1, 2, ..., p-1} with p prime).

    Example:
        In [1]: P = PrimeFieldPolynomial(coefs=[-1, 2, 1], p=17)

        In [2]: P
        Out[2]: X**2 + 2X + 16  # because -1 = 16 modulo 17

        In [3]: X = PrimeFieldPolynomial.X(p=17)

        In [4]: Q = -1 + 2*X + X**2

        In [5]: Q
        Out[5]: X**2 + 2X + 16
    """

    def __init__(self, coefs: list, p: int):
        assert all(
            isinstance(x, int) for x in coefs
        ), "Polynomial coefs must all be integers."
        assert isinstance(p, int) and prime(p), "p must be prime."

        self.coefs = trim_trailing_zeroes([c_i % p for c_i in coefs])
        self.p = p

    @classmethod
    def X(cls, p: int) -> "PrimeFieldPolynomial":
        return cls(coefs=[0, 1], p=p)

    @property
    def degree(self) -> int:
        """
        Implements the degree of a PrimeFieldPolynomial (-1 for the zero polynomial instead of the
        usual mathematical convention of minus infinity but that's okay for our purposes).
        """
        return len(self.coefs) - 1

    @property
    def is_monomial(self) -> bool:
        """
        Tests the monomiality of a PrimeFieldPolynomial (i.e. tests whether the polynomial at hand
        is of the form: coef * X**n with 1 <= n).
        """
        return 1 <= self.degree and len(dropwhile(lambda x: x == 0)(self.coefs)) == 1

    def __eq__(self, other: Union["PrimeFieldPolynomial", int]) -> bool:
        """
        Implements equality between two PrimeFieldPolynomials or between a PrimeFieldPolynomial
        and an integer.
        """
        if isinstance(other, int):
            if other == 0:
                return len(self.coefs) == 0
            else:
                return len(self.coefs) == 1 and self.coefs[0] == other % self.p

        assert isinstance(other, PrimeFieldPolynomial)
        assert (
            self.p == other.p
        ), "Polynomials must be defined over the same prime field to be compared for equality."

        return self.coefs == other.coefs

    def __radd__(self, other: int) -> "PrimeFieldPolynomial":
        """
        Implements the addition of an integer with a PrimeFieldPolynomial as right operand
        (e.g. 3 + P).
        """
        assert isinstance(other, int)

        if self == 0:
            return PrimeFieldPolynomial(coefs=[other], p=self.p)

        return PrimeFieldPolynomial(
            coefs=[self.coefs[0] + other] + self.coefs[1:], p=self.p
        )

    def __rsub__(self, other: int) -> "PrimeFieldPolynomial":
        """
        Implements the subraction of an integer with a PrimeFieldPolynomial as right operand
        (e.g. 3 - P).
        """
        assert isinstance(other, int)

        if self == 0:
            return PrimeFieldPolynomial(coefs=[other], p=self.p)

        return PrimeFieldPolynomial(
            coefs=[other - self.coefs[0]] + [-c_i for c_i in self.coefs[1:]], p=self.p
        )

    def __rmul__(self, n: int) -> "PrimeFieldPolynomial":
        """
        Implements the multiplication of an integer with a PrimeFieldPolynomial as right operand
        (e.g. 3 * P).
        """
        assert isinstance(n, int)

        if n == 0:
            return PrimeFieldPolynomial(coefs=[], p=self.p)

        return PrimeFieldPolynomial(coefs=[n * c_i for c_i in self.coefs], p=self.p)

    def __add__(
        self, other: Union["PrimeFieldPolynomial", int]
    ) -> "PrimeFieldPolynomial":
        """
        Implements the addition of a PrimeFieldPolynomial with another PrimeFieldPolynomial
        or an integer.
        """
        if isinstance(other, int):
            return other + self

        assert isinstance(other, PrimeFieldPolynomial)
        assert (
            other.p == self.p
        ), "Polynomials must be defined over the same prime field to be added."

        def addition(x):
            return x[0] + x[1]

        sum_coefs = long_zip_with(addition, fill_missings_with=0)(
            [self.coefs, other.coefs]
        )

        return PrimeFieldPolynomial(coefs=sum_coefs, p=self.p)

    def __sub__(
        self, other: Union["PrimeFieldPolynomial", int]
    ) -> "PrimeFieldPolynomial":
        """
        Implements the subtraction of a PrimeFieldPolynomial with another PrimeFieldPolynomial
        or an integer.
        """
        if self == 0:
            if isinstance(other, PrimeFieldPolynomial):
                return -other
            else:
                assert isinstance(other, int)
                return PrimeFieldPolynomial(coefs=[-other], p=self.p)

        if isinstance(other, int):
            return PrimeFieldPolynomial(
                coefs=[self.coefs[0] - other] + self.coefs[1:], p=self.p
            )

        assert isinstance(other, PrimeFieldPolynomial)
        assert (
            other.p == self.p
        ), "Polynomials must be defined over the same prime field to be subtracted."

        def subtraction(x):
            return x[0] - x[1]

        sub_coefs = long_zip_with(subtraction, fill_missings_with=0)(
            [self.coefs, other.coefs]
        )

        return PrimeFieldPolynomial(coefs=sub_coefs, p=self.p)

    def __mul__(
        self, other: Union["PrimeFieldPolynomial", int]
    ) -> "PrimeFieldPolynomial":
        """
        Implements the multiplication of a PrimeFieldPolynomial with another PrimeFieldPolynomial
        or an integer.
        """
        if isinstance(other, int):
            return other * self

        assert isinstance(other, PrimeFieldPolynomial)
        assert (
            other.p == self.p
        ), "Polynomials must be defined over the same prime field to be multiplied."

        mul_coefs = [0] * (self.degree + other.degree + 1)

        for i, a_i in enumerate(self.coefs):
            for j, b_j in enumerate(other.coefs):
                mul_coefs[i + j] += a_i * b_j

        return PrimeFieldPolynomial(coefs=mul_coefs, p=self.p)

    def __pow__(self, n: int) -> "PrimeFieldPolynomial":
        """
        Returns the n-th power of a PrimeFieldPolynomial P (i.e. P**n).
        """
        assert isinstance(n, int) and 0 <= n, "n must be a positive integer"

        if n == 0:
            return PrimeFieldPolynomial([1], p=self.p)

        return self ** (n - 1) * self

    def __neg__(self) -> "PrimeFieldPolynomial":
        """
        Returns the negation of a PrimeFieldPolynomial P (i.e. -P).
        """
        return 0 - self

    def __repr__(self) -> str:
        """
        Returns a user-friendly representation of PrimeFieldPolynomials.

        Example:
            In [1]: P = PrimeFieldPolynomial(coefs=[3, 0, 0, 2], p=17)

            In [2]: P
            Out[2]: 2X**3 + 3
        """
        if self == 0:
            return "0"

        if self.degree == 0:
            return str(self.coefs[0])

        if self.is_monomial:
            coef = self.coefs[self.degree]

            if self.degree == 1:
                return "X" if coef == 1 else f"{coef}X"
            else:
                return f"X**{self.degree}" if coef == 1 else f"{coef}X**{self.degree}"

        X = self.X(p=self.p)

        return " + ".join(
            reverse([str(c_i * X ** i) for i, c_i in enumerate(self.coefs) if c_i != 0])
        )

    def __call__(self, x: int) -> int:
        """
        Evaluates a PrimeFieldPolynomial P on the integer x (i.e. returns P(x)).
        """
        if self == 0:
            return 0

        if self.degree == 0:
            return self.coefs[0]

        return sum([c_i * x ** i for i, c_i in enumerate(self.coefs)]) % self.p
