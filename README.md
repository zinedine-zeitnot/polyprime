# :teddy_bear: A playground library to get your hands on polynomials with integer coefficients modulo prime numbers

[![codecov](https://codecov.io/gh/zinedine-zeitnot/polyprime/branch/main/graph/badge.svg?token=UPKNOF2OOF)](https://codecov.io/gh/zinedine-zeitnot/polyprime)

Instantiate polynomials either by specifying their coefficients as a list:

```py
In [1]: from polyprime.prime_field_polynomial import PrimeFieldPolynomial

In [2]: P = PrimeFieldPolynomial(coefs=[3, 0, 1], p=17)
   ...: Q = PrimeFieldPolynomial(coefs=[0, 1, 2], p=17)

In [3]: A = P + Q
   ...: M = P * Q
   ...: S = P - Q

In [4]: A
Out[4]: 3X**2 + X + 3

In [5]: M
Out[5]: 2X**4 + X**3 + 6X**2 + 3X

In [6]: S
Out[6]: 16X**2 + 16X + 3  # we said modulo p = 17 so -1 = 16
```

Or by defining them directly in terms of the `X` variable:

```py
In [1]: from polyprime.prime_field_polynomial import PrimeFieldPolynomial

In [2]: X = PrimeFieldPolynomial.X(p=17)

In [3]: P = X**2 + 3
   ...: Q = 2*X**2 + X

In [4]: S = P - Q

In [5]: assert S == -X**2 - X + 3 == 16*X**2 + 16*X + 3
```

And now you can test [Fermat's Little Theorem](https://en.wikipedia.org/wiki/Fermat%27s_little_theorem) via polynomial evaluation :rainbow:

```py
In [1]: from polyprime.prime_field_polynomial import PrimeFieldPolynomial

In [2]: p = 17

In [3]: X = PrimeFieldPolynomial.X(p)

In [4]: P = X**(p-1) - 1

In [5]: assert all(P(a) == 0 for a in range(1, 17))
```
