from collections import deque
from decimal import Decimal
from fractions import Fraction
from functools import cache, partial
from itertools import count, groupby, islice, takewhile
from math import floor, inf, isqrt
from numbers import Number
from operator import gt
from typing import Callable, Iterator, Optional

# From https://en.wikipedia.org/wiki/List_of_prime_numbers#The_first_1,000_prime_numbers
PRIMES: set[int] = {
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
    127,
    131,
    137,
    139,
    149,
    151,
    157,
    163,
    167,
    173,
    179,
    181,
    191,
    193,
    197,
    199,
    211,
    223,
    227,
    229,
    233,
    239,
    241,
    251,
    257,
    263,
    269,
    271,
    277,
    281,
    283,
    293,
    307,
    311,
    313,
    317,
    331,
    337,
    347,
    349,
    353,
    359,
    367,
    373,
    379,
    383,
    389,
    397,
    401,
    409,
    419,
    421,
    431,
    433,
    439,
    443,
    449,
    457,
    461,
    463,
    467,
    479,
    487,
    491,
    499,
    503,
    509,
    521,
    523,
    541,
    547,
    557,
    563,
    569,
    571,
    577,
    587,
    593,
    599,
    601,
    607,
    613,
    617,
    619,
    631,
    641,
    643,
    647,
    653,
    659,
    661,
    673,
    677,
    683,
    691,
    701,
    709,
    719,
    727,
    733,
    739,
    743,
    751,
    757,
    761,
    769,
    773,
    787,
    797,
    809,
    811,
    821,
    823,
    827,
    829,
    839,
    853,
    857,
    859,
    863,
    877,
    881,
    883,
    887,
    907,
    911,
    919,
    929,
    937,
    941,
    947,
    953,
    967,
    971,
    977,
    983,
    991,
    997,
}

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
def canonical_representation(n: Number) -> str:
    """The Unicode string of an integer's "canonical representation" or "standard form".

    The Fundamental Theorem of Arithmetic guarantees unique output for every integer input > 1.
    """
    prime_power_pairs: tuple[tuple[()]] | tuple[tuple[int, int], ...] = decompose(n)
    # is less than 2; there is no bona fide canonical representation...
    if len(prime_power_pairs[0]) == 0:
        return f"{n:_}"

    # don't have a symbol for the exponent: use plain caret to mean exponentiation
    if max((e for (_, e) in prime_power_pairs)) > max(superscript_map):
        return " * ".join(f"{p:_}^{e}" for (p, e) in prime_power_pairs)

    # otherwise, use fancy superscript for the canonical form
    return " * ".join(f"{p:_}{superscript_map[e]}" for (p, e) in prime_power_pairs)


def six_k_minus_plus_1() -> Iterator[int]:
    """Yield 6 * k - 1 then 6 * k + 1 for k = 1, 2, 3, ....

    This is useful because every prime > 3 is of the form 6k-1 or 6k+1 for some k.
    """
    for z in count(start=6, step=6):
        yield z - 1
        yield z + 1


def generate_prime_factors(z: int) -> Iterator[int]:
    """Yield the (repeated) prime factors of `z`."""
    while z & 1 == 0:
        yield 2
        z //= 2

    while not z % 3:
        yield 3
        z //= 3

    # all primes greater than 3 are of the form 6k+1 or 6k-1 for some positive int k
    # but, any candidate is strictly less than sqrt(z) + 1 (equivalently; the "roof"
    # is strictly greater than any candidate), so only generate those integers that
    # are of the correct form AND less than the "roof" (ceiling plus 1)
    roof: int = isqrt(z) + 1
    roof_greater_than: Callable[[int], bool] = partial(gt, roof)
    candidates: Iterator[int] = takewhile(roof_greater_than, six_k_minus_plus_1())

    for candidate in candidates:
        # if z modulo candidate is 0, then candidate is a divisor of z
        while not z % candidate:
            yield candidate
            # proceed with z having divided out candidate
            z //= candidate

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

    prime_factors: Iterator[int] = generate_prime_factors(z=z)

    # from itertools recipes, use a `deque` to "consume iterator at C speed".
    return tuple((p, len(deque(g))) for p, g in groupby(prime_factors))


@cache
def is_prime(n: Number, registry: Optional[set[int]] = None) -> bool:
    """Whether `n` has only 1 and itself as divisors.

    Non-integer `n` will be cast to int if possible.
    If `registry` is passed, it must be a subset of the primes, for fast membership testing.

    Returns:
        Whether `n` is a prime.
    Raises:
        TypeError: if `n` is a numeric that cannot be considered Integral.
    """
    if isinstance(n, float):
        if not n.is_integer():
            raise TypeError("Only a Integral > 1 can be prime.")
        z: int = int(n)
    elif isinstance(n, Decimal):
        num, denom = n.as_integer_ratio()
        if denom > 1:
            raise TypeError("Only a Integral > 1 can be prime.")
        else:
            del denom
        z = num
    elif isinstance(n, complex):
        if not n.real.is_integer():
            raise TypeError("Only a Integral > 1 can be prime.")
        z = int(n.real)
    elif isinstance(n, Fraction):
        if not n.denominator == 1:
            raise TypeError("Only a Integral > 1 can be prime.")
        z = n.numerator
    elif isinstance(n, int):
        z = n

    # negatives, 0, 1
    if z < 2:
        return False
    # 2 and 3
    if z < 4:
        return True
    # even
    if z & 1 == 0:
        return False

    # 5 and 7
    if z < 9:
        return True

    # divisible by 3
    if z % 3 == 0:
        return False

    if registry is not None and z in registry:
        return True

    # if generate_prime_factors(z) yields more than 1 element, `z` is composite
    # NOTE islice(iterable, 1, None) returns JUST the 1th element of iterable
    # then, next(..., default) swallows StopIteration, returning default
    # so, if `z` is prime, it will hit that StopIteration and return not False
    # otherwise, it will return not <some int> and all non-zero int are truthy
    prime_factors: Iterator[int] = generate_prime_factors(z)
    # NOTE from https://docs.python.org/3.10/library/itertools.html#itertools-recipes
    return not next(islice(prime_factors, 1, None), False)


def fibonacci_sequence() -> Iterator[int]:
    """Generate the Fibonacci sequence.

    Yields:
        1, 1, 2, 3, 5, 8, 13, ...
    """
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


def prime_counting(x: Number) -> int:
    """Return pi(`x`), the quantity of primes less than or equal to `x`."""
    return len(set(generate_prime_factors(floor(x))))


def prime_counting_complement(x: Number) -> float:
    """Return the complement of pi(`x`); amount of primes greater than `x`."""
    return inf
