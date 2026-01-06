from decimal import Decimal
from fractions import Fraction
from functools import cache
from itertools import groupby
from math import isqrt
from numbers import Number
from typing import Iterator

superscript_map: dict[int, str] = {
    0: "⁰",
    1: "¹",
    2: "²",
    3: "³",
    4: "⁴",
    5: "⁵",
    6: "⁶",
    7: "⁷",
    8: "⁸",
    9: "⁹",
    10: "¹⁰",
    11: "¹¹",
    12: "¹²",
    13: "¹³",
    14: "¹⁴",
    15: "¹⁵",
    16: "¹⁶",
    17: "¹⁷",
    18: "¹⁸",
    19: "¹⁹",
    20: "²⁰",
}


@cache
def canonical_form(n: Number) -> str:
    """The Unicode string of an integer's Fundamental Theorem of Arithmetic representation."""
    prime_power_pairs: tuple[tuple[()], ...] | tuple[tuple[int, int], ...] = decompose(
        n
    )
    # is less than 2; there is no bona fide canonical representation...
    if len(prime_power_pairs[0]) == 0:
        return f"{n}"

    # don't have a symbol for the exponent: use plain caret to mean exponentiation
    if max((e for (_, e) in prime_power_pairs)) > max(superscript_map):
        return " * ".join(f"{p}^{e}" for (p, e) in prime_power_pairs)

    # otherwise, use fancy superscript for the canonical form
    return " * ".join(f"{p}{superscript_map[e]}" for (p, e) in prime_power_pairs)


def generate_prime_factors(z: int) -> Iterator[int]:
    """Give back the (maybe repeated) prime factors of `z` as generator."""
    while z & 1 == 0:
        yield 2
        z //= 2

    # odd numbers from 3 to sqrt(z) because prime factors are <= sqrt(z)
    odds: Iterator[int] = (n for n in range(3, isqrt(z) + 1, 2))
    for o in odds:
        # call z/o the name q (quotient). If q is an integer, then o is a divisor of z
        while (q := z / o).is_integer():
            yield o
            # proceed with q as the new z
            z = int(q)

    if z > 1:
        yield z


@cache
def decompose(n: Number) -> tuple[tuple[()], ...] | tuple[tuple[int, int], ...]:
    """Decompose an integer into the product of its prime powers."""
    if isinstance(n, float):
        if not n.is_integer():
            raise TypeError("Only an Integral has a prime decomposition.")
        z: int = int(n)
    elif isinstance(n, Decimal):
        num, denom = n.as_integer_ratio()
        if denom > 1:
            raise TypeError("Only an Integral has a prime decomposition.")
        else:
            del denom
        z = num
    elif isinstance(n, complex):
        if not n.real.is_integer():
            raise TypeError("Only an Integral has a prime decomposition.")
        z = int(n.real)
    elif isinstance(n, Fraction):
        if not n.denominator == 1:
            raise TypeError("Only an Integral has a prime decomposition.")
        z = n.numerator
    elif isinstance(n, int):
        z = n

    # now, working with integers
    if z < 2:
        return ((),)
    if z == 2:
        return ((2, 1),)

    return tuple(
        (p, sum(1 for _ in group)) for p, group in groupby(generate_prime_factors(z))
    )
