from decimal import Decimal
import fractions
import itertools as it
import math
import operator
import string
from functools import reduce

from hypothesis import given, strategies as st
import more_itertools as mit
import pytest as pt

from integer import is_prime, Integer, sequence, generate_primes

# Maybe make a fixture here that takes a given logic, e.g. is_woodall, and a max
# value that Hypothesis takes, and return all the examples up to that number.
# Clearly, it is infeasible to test up to the max of st.integers() for each
# method, but it is more justifiable to make a limit that is passed in, e.g. by
# pytest.ini and adhere to that.


# HELPERS TESTS #
@given(st.integers(min_value=0))
def test_sequence(maximum):
    seq = sequence()
    if maximum == 0:
        assert next(seq) == 0
    elif maximum == 1:
        next(seq)
        assert next(seq) == 1
    else:
        s = mit.spy(seq, maximum)[0]
        for i in range(1, len(s)):
            assert abs(s[i]) == abs(s[i-1]) + 1
            assert s[i] + s[i-1] in (1, -1)


@given(st.integers(min_value=1))
def test_generate_primes(how_many):
    primes = generate_primes()
    for _ in range(how_many):
        assert is_prime(next(primes))


# INIT TEST #
@given(st.integers())
def test_init_integer(z):
    assert Integer(z).num == z


@given(st.floats(allow_nan=False,
                 allow_infinity=False))
def test_init_non_nan_non_inf_float(z):
    assert Integer(z).num == int(z)


@given(st.just(float("nan")))
def test_init_nan_float_raises_value_error(z):
    with pt.raises(ValueError):
        Integer(z)


@given(st.decimals(allow_nan=False,
                   allow_infinity=False))
def test_init_non_nan_non_inf_decimal(z):
    assert Integer(z).num == int(z)


@given(st.just(Decimal("nan")))
def test_init_nan_decimal_raises_value_error(z):
    with pt.raises(ValueError):
        Integer(z)


@given(st.text(alphabet=string.digits,
               min_size=1))
def test_init_numeric_string(z):
    assert Integer(z).num == int(z)


# REPR TEST #
@given(st.integers())
def test_repr(z):
    assert Integer(z).__repr__() == "Integer({!r})".format(z)


# DUNDER METHOD TESTS #
@given(st.integers(max_value=1e4))
def test_bool(z):
    if z == 0:
        assert not Integer(z)
    else:
        assert Integer(z)


@given(st.integers(max_value=1e15),
       st.integers(max_value=1e15))
def test_addition(z1, z2):
    assert z1 + z2 == Integer(z1) + Integer(z2)


@given(st.integers(max_value=1e15),
       st.integers(max_value=1e15))
def test_subtraction(z1, z2):
    assert z1 - z2 == Integer(z1) - Integer(z2)


@given(st.integers(max_value=1e15),
       st.integers(max_value=1e15))
def test_modulo(z1, z2):
    assert z1 % z2 == Integer(z1) % Integer(z2) == \
        z1 % Integer(z2) == Integer(z1) % z2


@given(st.integers(min_value=1))
def test_negative(z):
    assert -z == -Integer(z)


@given(st.integers(max_value=1e15),
       st.integers(max_value=1e15))
def test_multiplication(z1, z2):
    assert z1 * z2 == Integer(z1) * Integer(z2) == \
        z1 * Integer(z2) == z2 * Integer(z1)


@given(st.integers(max_value=1e15),
       st.integers(max_value=1e15))
def test_division(z1, z2):
    if z2 == 0:
        with pt.raises(ZeroDivisionError):
            Integer(z1) / z2
        with pt.raises(ZeroDivisionError):
            z1 / Integer(z2)
    else:
        assert (z1 / z2) == (Integer(z1) / Integer(z2)) == \
            (z1 / Integer(z2)) == (Integer(z1) / z2)


@given(st.integers(max_value=1e15),
       st.integers(max_value=5))
def test_exponentiation(z1, z2):
    assert (z1 ** z2 == Integer(z1) ** Integer(z2))


@given(st.integers(), st.integers())
def test_less_than(z1, z2):
    assert (z1 < z2) == (Integer(z1) < Integer(z2))


@given(st.integers(), st.integers())
def test_less_than_or_equal(z1, z2):
    assert (z1 <= z2) == (Integer(z1) <= Integer(z2))


@given(st.integers(), st.integers())
def test_greater_than(z1, z2):
    assert (z1 > z2) == (Integer(z1) > Integer(z2))


@given(st.integers(), st.integers())
def test_greater_than_or_equal(z1, z2):
    assert (z1 >= z2) == (Integer(z1) >= Integer(z2))


@given(st.integers(), st.integers())
def test_not_equal(z1, z2):
    assert (z1 != z2) == (Integer(z1) != Integer(z2))


# STATIC METHOD TEST #
@given(st.integers(), st.integers())
def test_gcd(a, b):
    assert Integer.gcd(a, b) == math.gcd(a, b)


# METHOD TEST #
@given(st.integers(max_value=1e9), st.integers(max_value=10))
def test_is_perfect_power(z, k):
    if k <= 0:
        with pt.raises(ValueError):
            Integer(z).is_perfect_power(k)
    elif k == 1:
        assert Integer(z).is_perfect_power(k)
    else:
        if (z ** (1/k)).is_integer():
            assert Integer(z).is_perfect_power(k)
        else:
            assert not Integer(z).is_perfect_power(k)


@given(st.integers(max_value=1e4), st.integers())
def test_is_power_of(z, n):
    if z < 0:
        with pt.raises(NotImplementedError):
            Integer(z).is_power_of(n)
    elif z == 0:
        assert not Integer(z).is_power_of(n)
    elif z == 1:
        assert Integer(z).is_power_of(n)
    else:
        if n < 0:
            with pt.raises(ValueError):
                Integer(z).is_power_of(n)
        elif n == 0:
            assert not Integer(z).is_power_of(n)
        elif n == 1:
            assert not Integer(z).is_power_of(n)
        else:
            f = math.log(z, n)
            if f.is_integer():
                assert Integer(z).is_power_of(n)
            else:
                assert not Integer(z).is_power_of(n)


# PRIMALITY TEST #
@given(st.integers(max_value=1e15))
def test_is_prime_false_for_any_integer_not_ending_in_1379(z):
    if z <= 1:
        assert not is_prime(z)
    elif z == 2:
        assert is_prime(z)
    else:
        if str(z)[-1] not in map(str, (1, 3, 7, 9)):
            assert not is_prime(z)


# PROPERTY TEST #
@given(st.integers())
def test_binary(z):
    assert Integer(z).binary == bin(z)


@given(st.integers(max_value=1e8))
def test_decomposition(z):
    assert isinstance(Integer(z).decomposition, dict)
    assert z == reduce(lambda x, y: x * y,
                       (k**v for k, v in Integer(z).decomposition.items()))


@given(st.integers(max_value=1e4))
def test_divisors(z):
    # Using itertools, take Integer.decomposition and get every
    # combination of key ** value for every key and every 0, ..., value
    # THIS IS A SUFFICIENCY PROOF, BUT NOT NECESSESITY PROOF
    assert all(z % f == 0 for f in Integer(z).divisors)

    # THIS IS A COPOUT: COPYING THE LOGIC OF THE PROPERTY
    assert Integer(z).divisors == {x for x in range(1, z//2 + 1)
                                   if z % x == 0}


@given(st.integers(max_value=1e4))
def test_euler_totient(z):
    # Euler's product formula
    if z < 0:
        assert not Integer(z).euler_totient
    else:
        assert Integer(z).euler_totient == \
            int(reduce(operator.mul,
                       ((1 - 1. / k) for k in Integer(z).decomposition.keys()),
                       z))


@given(st.integers(max_value=1e2))
def test_factorial(z):
    if z < 0:
        with pt.raises(ValueError):
            Integer(z).factorial
    elif z == 0:
        assert Integer(z).factorial == 1
    else:
        assert Integer(z).factorial == math.factorial(z)


@given(st.integers(max_value=1e4))
def test_factorization(z):
    assert Integer(z).factorization == \
        ' * '.join((''.join((str(k), '^', str(v)))
                    for k, v in Integer(z).decomposition.items()))


@given(st.integers(max_value=1e3))
def test_goldbach_partitions(z):
    expected = set()
    if z % 2:
        assert Integer(z).goldbach_partitions == expected
    else:
        expected = set(filter(lambda x: is_prime(x[0]) and is_prime(x[1]),
                              zip(range(z//2+1),
                                  (z - x for x in range(z//2+1)))))
        assert Integer(z).goldbach_partitions == expected


@given(st.integers(max_value=1e4))
def test_is_mersenne(z):
    if z <= 0:
        assert not Integer(z).is_mersenne
        # this breaks due to is_power_of not being implemented for negatives
        # with pt.raises(NotImplementedError):
        #     Integer(z).is_mersenne
    else:
        if math.log(z+1, 2).is_integer():
            assert Integer(z).is_mersenne
        else:
            assert not Integer(z).is_mersenne


@given(st.integers(max_value=1e4))
def test_is_mersenne_prime(z):
    if z <= 0:
        assert not Integer(z).is_mersenne_prime
    else:
        if math.log(z+1, 2).is_integer() and is_prime(z):
            assert Integer(z).is_mersenne_prime
        else:
            assert not Integer(z).is_mersenne_prime


@given(st.integers(max_value=1e4))
def test_is_perfect(z):
    Z = Integer(z)
    if sum(Z.divisors) == Z.num:
        assert Z.is_perfect
    else:
        assert not Z.is_perfect


@given(st.integers(max_value=1e4))
def test_is_squarefree(z):
    Z = Integer(z)
    if z < 1:
        assert not Z.is_squarefree
    elif z == 1:
        assert Z.is_squarefree
    else:
        squares_up_to_z = (i for i in range(2, z+1)
                           if Integer(i).is_perfect_power(2))
        if any(z % i == 0 for i in squares_up_to_z):
            assert not Z.is_squarefree
        else:
            assert Z.is_squarefree


@given(st.integers(max_value=1e4))
def test_is_woodall(z):
    if z in {1, 7, 23, 63, 159, 383, 895, 2047, 4607}:
        assert Integer(z).is_woodall
    else:
        assert not Integer(z).is_woodall


@given(st.integers(max_value=1e4))
def test_is_woodall_prime(z):
    if z in {7, 23, 383}:
        assert Integer(z).is_woodall_prime
    else:
        assert not Integer(z).is_woodall_prime

@given(st.integers(max_value=1e4))
def test_is_balanced_prime(z):
    def generate_primes_before_n(n):
        p = generate_primes()
        largest_so_far = next(p)
        while largest_so_far < n:
            yield largest_so_far
            largest_so_far = next(p)

    def generate_primes_after_n(n):
        p = generate_primes()
        largest_so_far = next(p)
        while largest_so_far < n:
            largest_so_far = next(p)

        yield largest_so_far
        while True:
            yield next(p)

    preceding_prime = max(generate_primes_before_n(z))
    succeeding_prime = next(generate_primes_after_n(z))
    if z - closest_before_z == closest_after_z - z:
        if is_prime(z):
            assert Integer(z).is_balanced_prime
        else:
            assert not Integer(z).is_balanced_prime
    else:
        assert not Integer(z).is_balanced_prime

@given(st.integers(max_value=1e4))
def test_is_cullen(z):
    if z in {1, 3, 9, 25, 65, 161, 385, 897, 2049, 4609}:
        assert Integer(z).is_cullen
    else:
        assert not Integer(z).is_cullen


@given(st.integers(max_value=1e4))
def test_is_cullen_prime(z):
    if z == 3:  # Only Cullen prime less than 10,000
        assert Integer(z).is_cullen_prime
    else:
        assert not Integer(z).is_cullen_prime


@given(st.integers(max_value=1e4))
def test_nearest_prime(z):
    def generate_primes_before_n(n):
        p = generate_primes()
        largest_so_far = next(p)
        while largest_so_far < n:
            yield largest_so_far
            largest_so_far = next(p)

    def generate_primes_after_n(n):
        p = generate_primes()
        largest_so_far = next(p)
        while largest_so_far < n:
            largest_so_far = next(p)

        yield largest_so_far
        while True:
            yield next(p)

    np = Integer(z).nearest_prime
    if z <= 0:
        assert np == (2,)
    elif is_prime(z):
        assert np == (z,)
    else:
        closest_before_z = max(generate_primes_before_n(z))
        closest_after_z = next(generate_primes_after_n(z))
        if abs(z - closest_before_z) == abs(z - closest_after_z):
            assert np == (closest_before_z, closest_after_z)
        else:
            assert np == (min(closest_after_z, closest_before_z,
                              key=lambda n, z=z: abs(z-n)),)


@given(st.integers(max_value=1e4))
def test_Omega(z):
    assert Integer(z).Omega == sum(Integer(z).decomposition.values())


@given(st.integers(max_value=1e4))
def test_omega(z):
    Z = Integer(z)
    assert Z.omega == sum(1 for _ in
                          filter(lambda x: is_prime(x) and not z % x,
                                 range(0, z+1)))


@given(st.integers(max_value=1e4))
def test_parity(z):
    if z % 2:
        assert Integer(z).parity == 'Odd'
    else:
        assert Integer(z).parity == 'Even'


@given(st.integers(max_value=1e4))
def test_pi(z):
    assert Integer(z).pi == sum(1 for x in range(2, z + 1) if is_prime(x))


@given(st.integers(max_value=1e4))
def test_primality(z):
    if is_prime(z):
        assert Integer(z).primality == "Prime"
    else:
        assert Integer(z).primality == "Composite"


@given(st.integers(max_value=1e4))
def test_sigma(z):
    Z = Integer(z)
    assert Z.sigma == sum(it.filterfalse(lambda x: z % x,
                                         range(1, z//2 + 1)))


@given(st.integers(max_value=1e4))
def test_tau(z):
    if z <= 0:
        assert Integer(z).tau == 0
    elif z == 1:
        assert Integer(z).tau == 1
    else:
        Z = Integer(z)
        assert Z.tau == reduce(operator.mul,
                               (z + 1 for z in Z.decomposition.values()))


@given(st.integers(max_value=1e4))
def test_totatives(z):
    assert isinstance(Integer(z).totatives, set)
    if z <= 0:
        assert not Integer(z).totatives
    else:
        assert Integer(z).totatives == {x for x in range(1, z + 1)
                                        if Integer.gcd(z, x) == 1}
