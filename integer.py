"""Represent the mathematical concept of an integer as a Python object."""


def is_prime(z: int) -> bool:
    """Return whether z is prime.

    This particular implementation is from http://stackoverflow.com/a/27946768.

    Args:
    ----
        z (int): Integer the primality of which to ascertain

    Returns:
    -------
        (bool): Whether `z` is prime

    """
    if not isinstance(z, int) or z < 0:
        return False  # One day, extension to negative integers will happen...

    if z <= 1:
        return False

    return all(z % n for n in range(2, int(z**0.5 + 1)))


def decompose(n: int) -> dict:
    """Return the dict of prime factors of n.

    The dict is of the form of "prime: power". Source of the
    implementation: http://stackoverflow.com/a/412942/4747798
    """
    _n = int(n)
    if _n < 2:
        return {}

    factors: list = []
    d: int = 2
    while _n > 1:
        while _n % d == 0:
            factors.append(d)
            _n /= d
        d: int = d + 1
        if d * d > _n:
            if _n > 1:
                factors.append(_n)
            break

    return {int(f): int(factors.count(f)) for f in set(factors)}


def sequence():
    """Generate the following sequence.

    0, 1, -2, 3, -4, 5, -6, 7, -8, ...
    """
    n = 1
    yield 0
    while True:
        yield n
        sign = -1 if n % 2 else 1
        n = sign * (abs(n) + 1)


def fibonacci_sequence():
    """Generate the Fibonacci sequence.

    1, 1, 2, 3, 5, 8, 13, ...
    """
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


def generate_primes():
    """Sieve of Eratosthenes variation to generate primes."""
    found: list = []
    candidate: int = 2
    while True:
        if all(candidate % prime for prime in found):
            yield candidate
            found.append(candidate)
        candidate += 1


class Integer:
    """A Python object to represent a mathematical integer.

    It features a superset of the methods of built-in int, and
    only uses Python 3 built-ins.

    Integer behaves as `int` in regards to arithmetic for numeric
    types e.g.

    >>> Integer("7") + 0 == 7
    True

    >>> Integer(4) * 3 == 12
    True

    >>> Integer(0) - 1 == -1
    True

    >>> Integer(8.4) + 0 == 8
    True

    Integer boasts of other attributes such as primality,
    subtypes of primality (e.g. Mersenne), perfectness, power-of
    checking, factorization, totatives, Goldbach partition, and
    methods such as nearest_prime and factorial.
    Most of the attributes of Integer are properties: just as
    the mathematical concept of an integer has the property
    that it is either prime or not, Integer has the Boolean
    property `primality`.
    """

    def __init__(self, num: int):
        try:
            self.num = int(num)
        except (OverflowError, TypeError, ValueError) as exc:
            raise ValueError("Integer must be finite and numeric") from exc

        # Values to "cache" for property and method calculations
        self._decomposition: dict = decompose(self.num)
        self._whether_prime: bool = is_prime(self.num)
        self._parity: str = "Odd" if self.num % 2 else "Even"
        if self._whether_prime or self.num < 0:
            # account for negative integers' square root problem
            self._divisors: set = {1, self.num}
        else:
            _sqrt: int = int(num**0.5) + 1
            self._divisors: set = {n for n in range(1, _sqrt) if self.num % n == 0} | {
                num // n for n in range(1, _sqrt) if self.num % n == 0
            }
        self._proper_divisors: set = self._divisors - {self.num}
        self._abundance: int = sum(self._proper_divisors) - self.num
        self._deficiency: int = self.num - sum(self._proper_divisors)

    def __repr__(self) -> str:
        return "Integer({!r})".format(self.num)

    def __bool__(self) -> bool:
        return self.num.__bool__()

    def __add__(self, other):
        num = self.num + other
        return Integer(num) if isinstance(num, int) else num

    def __sub__(self, other):
        num = self.num - other
        return Integer(num) if isinstance(num, int) else num

    def __mod__(self, other):
        num = self.num % other
        return Integer(num) if isinstance(num, int) else num

    def __rmod__(self, other):
        num = other % self.num
        return Integer(num) if isinstance(num, int) else num

    def __neg__(self):
        num: int = -self.num
        return Integer(num)

    def __mul__(self, other):
        num = self.num * other
        return Integer(num) if isinstance(num, int) else num

    def __rmul__(self, other):
        num = other * self.num
        return Integer(num) if isinstance(num, int) else num

    def __truediv__(self, other):
        num = self.num / other
        return num

    def __rtruediv__(self, other):
        num = other / self.num
        return num

    def __floordiv__(self, other):
        num = self.num / other
        return num

    def __rfloordiv__(self, other):
        num = other / self.num
        return num

    def __pow__(self, p):
        num: int = self.num**p
        return Integer(num) if isinstance(num, int) else num

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Return the greatest common divisor between a and b.

        The Greatest common divisor of two integers is the integer n that
        satisfies max({n: a%n=0 & b%n=0, n <= a <= b})
        Args:
        ----
            a (int): first integer to compare
            b (int): second integer to compare
        Returns:
        -------
            (int): the largest integer between (inclusive) `a` and `b`
                such that it divides `a` and `b`
        """
        while b:
            a, b = b, a % b
        return a

    def is_perfect_power(self, k: int) -> bool:
        """Return whether the Integer is a perfect k-power.

        I.e., perfect square (k=2), perfect cube (k=3), etc. Is only defined
        for k > 0. E.g. Integer(16).is_perfect_power(2) is True because
        4**2 == 16

        Args:
            k (int): power to check; i.e., is Integer() ** 1/k an integer?
        Returns:
            (bool)
        """
        if k <= 0:
            raise ValueError("Perfect negative power is not defined")
        if k == 1:
            return True  # Trivial
        if self.num == 0:
            return True  # zero to any k is zero

        return all(x % k == 0 for x in self.decomposition.values())

    def is_power_of(self, n: int) -> bool:
        """Return whether self.num is a power of n.

        I.e. z is a power of n if and only if z = n**k for some integers n>0, k.
        For example, 8 is a power of 2 because 8 = 2**3. Only implemented for
        positive integers
        Args:
            n (int): positive integer to be tested whether Integer() is a
                power of
        Returns:
            (bool)
        """
        if self.num < 0:
            raise NotImplementedError
        if self.num < n:
            return False
        if self.num == 0:
            return False  # No exponentiation can result in 0
        if self.num == 1:
            return True  # 1 is the zero-power of any given n
        if self.num == n:
            return True

        if n < 0:
            raise ValueError
        if n == 0:
            # Already know that z != 0 because logic has gotten to this point
            # There is no other such integer that is a zero-power of anything
            return False
        if n == 1:
            # Already know that z != 1 because logic has gotten to this point
            # There is no other integer such that self is a power of 1
            return False

        k: int = 2
        nk: int = n**k
        while nk < self.num:
            k += 1
            nk: int = n**k

        return nk == self.num

    @property
    def abundance(self):
        """Return the abundance of self.num.

        The abundance of an integer, n, is the difference between the sum
        of the proper divisors of n and n itself.
        """
        return Integer(self._abundance)

    @property
    def aliquot_sum(self):
        """Return the aliquot sum of self.num.

        The aliquot sum of an integer, n, is the sum of the proper divisors
        of n. Equivalently; n subtracted from the sum of the divisors of n.
        """
        return Integer(sum(self.proper_divisors))

    @property
    def binary(self, prefix: bool = True) -> str:
        """Return binary string representation of self.

        If prefix=True, the string has prefix '0b' for positive self.num,
        and prefix '-0b' for negative self.num. Otherwise, return a str
        of the binary representation of self.num.
        """
        return f"{self.num:#b}" if prefix else f"{self.num:b}"

    @property
    def decomposition(self) -> dict:
        """Return the dict of prime factors of self.num.

        The dict is of the form of "prime: power". E.g.,
        >>> Integer(192).decomposition
        {2: 6, 3: 1}
        >>> 192 == 2**6 * 3**1
        True
        """
        return {Integer(k): Integer(v) for k, v in self._decomposition.items()}

    @property
    def deficiency(self):
        """Return the deficiency of self.num.

        The deficiency of an integer, n, is the difference between n and
        the sum of the proper divisors of n.
        """
        return Integer(self._deficiency)

    @property
    def divisors(self) -> set:
        """Return the set of divisors of self.num.

        For the integer 'n', a divisor of n, called d, is an integer
        less than d such that n % d is 0. Equivalently, there exists
        some integer, k, such that d * k == n.
        """
        return set(map(Integer, self._divisors))

    @property
    def euler_totient(self):
        """Return the Euler totient function evaluated at self.num.

        Euler's totient function, phi(z), is the count of positive integers
        less than or equal to z that are coprime to z.
        """
        return Integer(len(self.totatives))

    @property
    def factorial(self):
        if self.num < 0:
            raise ValueError("Factorial is not defined for negative integers")
        if self.num == 0:
            return Integer(1)

        def _factorial(n: int) -> int:
            return 1 if n < 1 else n * _factorial(n - 1)

        return Integer(_factorial(self.num))

    @property
    def factorization(self) -> str:
        """Return quasi-human-readable rendering of prime decomposition."""
        return " * ".join(
            (str(k) + "^" + str(v) for k, v in self.decomposition.items()),
        )

    @property
    def goldbach_partitions(self) -> set:
        """Return the Goldbach partitions of self.num.

        I.e., the representation of an even number as a sum of two primes.
        """
        if self.parity == "Odd":
            return set()
        return {
            (Integer(p), Integer(self.num - p))
            for p in range(2, self.num // 2 + 1)
            if is_prime(p) and is_prime(self.num - p)
        }

    @property
    def is_abundant(self) -> bool:
        """Return whether self.num is abundant.

        An integer, n, is abundant if the sum of the divisors of n is
        greater than 2*n.
        """
        return self._abundance > 0

    @property
    def is_balanced_prime(self) -> bool:
        """Return whether self.num is a balanced prime.

        A balanced prime is a prime, p, that is the average of
        the preceding and succeeding primes. Equivalently, if P is
        the previous prime and N is the next prime, then, for p to
        be a balanced prime, |N-p| = |P-p|; i.e., they must be
        equidistant from p
        """
        # the first balanced prime is 5
        if self.primality == "Composite" or self.num < 5:
            return False

        preceding_prime_candidate: int = self.num - 1

        while not is_prime(preceding_prime_candidate):
            preceding_prime_candidate -= 1

        distance_from_z: int = self.num - preceding_prime_candidate
        return is_prime(self.num + distance_from_z)

    @property
    def is_cullen(self) -> bool:
        """Return whether self.num is a Cullen number.

        A Cullen number is a natural number, C, of the form C = k*2**k  + 1,
        where k is an integer
        """
        k: int = 1
        w: int = self.num - 1
        candidate: int = k * 2**k
        while candidate <= w:
            if w == candidate:
                return True
            k += 1
            candidate: int = k * 2**k
            continue
        return False

    @property
    def is_cullen_prime(self) -> bool:
        """Return whether self.num is a Cullen prime.

        A Cullen prime is a prime, p of the form p = k*2**k + 1, where k is
        an integer.
        """
        return is_prime(self.num) and self.is_cullen

    @property
    def is_deficient(self) -> bool:
        """Return whether self.num is deficient.

        An integer, n, is deficient if the sum of the divisors of n is
        less than 2*n.
        """
        return self._deficiency > 0

    @property
    def is_fibonacci(self) -> bool:
        """Return whether self.num is a member of the Fibonacci sequence.

        The Fibonacci sequence is: 1, 1, 2, 3, 5, 8, 13, 21, ...
        """
        _fs = fibonacci_sequence()
        f: int = next(_fs)
        while f < self.num:
            f: int = next(_fs)

        return f == self.num

    @property
    def is_mersenne(self) -> bool:
        """Return whether self.num is a Mersenne number.

        A Mersenne number is an integer, M, such that M = 2^k - 1, for some
        integer k
        """
        return self.num > 0 and Integer(self.num + 1).is_power_of(2)

    @property
    def is_mersenne_prime(self) -> bool:
        """Return whether self.num is a Mersenne prime.

        A Mersenne prime is a prime, p, of the form p = 2^k - 1, where
        k is an integer
        """
        return self.num > 0 and is_prime(self.num) and self.is_mersenne

    @property
    def is_perfect(self) -> bool:
        """Return whether self.num is perfect.

        A positive integer is perfect if it is equal to the sum of its
        proper divisors; for instance, 6 has divisors {1, 2, 3, 6} (of which
        {1, 2, 3} are the proper divisors) and 1 + 2 + 3 = 6
        """
        return self.aliquot_sum == self.num

    @property
    def is_squarefree(self) -> bool:
        """Return whether self.num is squarefree.

        A positive integer is squarefree if it is not divisible by
        a square greater than 1.
        """
        if self.num < 1:
            return False
        if self.num == 1:
            return True
        return all(exponent < 2 for exponent in self.decomposition.values())

    @property
    def is_untouchable(self) -> bool:
        """Return whether self.num is untouchable, or raise NotImplementedError.

        A positive integer, n, is untouchable if it cannot be expressed as the
        sum of the proper divisors of any positive integer.
        """
        # TODO: find a way to calculate this
        _is_untouchable: bool = False
        if self.num > 658:
            raise NotImplementedError
        if self.num in {
            2,
            5,
            52,
            88,
            96,
            120,
            124,
            146,
            162,
            188,
            206,
            210,
            216,
            238,
            246,
            248,
            262,
            268,
            276,
            288,
            290,
            292,
            304,
            306,
            322,
            324,
            326,
            336,
            342,
            372,
            406,
            408,
            426,
            430,
            448,
            472,
            474,
            498,
            516,
            518,
            520,
            530,
            540,
            552,
            556,
            562,
            576,
            584,
            612,
            624,
            626,
            628,
            658,
        }:
            _is_untouchable: bool = True
        return _is_untouchable

    @property
    def is_woodall(self) -> bool:
        """Return whether self.num is a Woodall number.

        A Woodall number is an integer, W, of the form W = k*2**k - 1, where
        k is an integer
        """
        if self.num < 1:
            return False
        w: int = self.num + 1

        def woodall(k: int, w: int = w) -> int:
            return k * 2**k == w

        range_of_k_to_check: range = (
            range(1, 4) if self.num < 64 else range(1, int(pow(w, 1 / 3)) + 1)
        )
        return any(map(woodall, range_of_k_to_check))

    @property
    def is_woodall_prime(self) -> bool:
        """Return whether self.num is a Woodall prime.

        A Woodall prime is a prime, p, of the form p = k*2**k - 1, where
        k is an integer
        """
        return is_prime(self.num) and self.is_woodall

    @property
    def nearest_prime(self) -> tuple:
        """Return the tuple of the nearest prime(s) to self.num.

        If self.num is prime, returns self.num. Otherwise, returns
        either the nearest prime, or the two nearest primes, if equidistant
        Returns:
            (tuple)
        """
        if self.num <= 1:
            return (2,)
        if self.primality == "Prime":
            return (self.num,)
        z, s = self.num, sequence()

        while not is_prime(z):
            z += next(s)
        nearest: int = z - self.num

        # Is there another prime equidistant?
        return (
            (Integer(z),)
            if not is_prime(self.num - nearest)
            else tuple(sorted(Integer(z), Integer(self.num - nearest)))
        )

    @property
    def Omega(self) -> int:
        """Return the total number of prime factors of self.num."""
        return Integer(sum(self.decomposition.values()))

    @property
    def omega(self) -> int:
        """Return the number of distinct prime factors of self.num."""
        return Integer(len(self.decomposition))

    @property
    def parity(self) -> str:
        """Return whether integer is even or odd."""
        return self._parity

    @property
    def pi(self):
        """Return the amount of primes not exceeding self.num.

        This is the output of the Prime Counting Function with self.num
        as the argument.
        """
        return Integer(sum(1 for z in range(2, self.num + 1) if is_prime(z)))

    @property
    def primality(self) -> str:
        """Return "Prime" if prime, "Composite" if not."""
        return "Prime" if self._whether_prime else "Composite"

    @property
    def proper_divisors(self) -> set:
        """Return the set of proper divisors of self.num.

        For the integer 'n', a positive divisor of n that is different from
        n is called a proper divisor or an aliquot part of n.
        """
        return self._proper_divisors

    @property
    def radical(self):
        """Return the product of the distinct primes dividing n."""
        z = self.num
        if self.is_squarefree:
            return Integer(z)
        product = 1
        for prime_factor in self.decomposition:
            product *= prime_factor
        return Integer(product)

    @property
    def sigma(self):
        """Return the sum of the divisors of self.num.

        This function is also called a(n) or sigma_1(n):
        https://oeis.org/A000203.
        """
        return Integer(sum(self.divisors))

    @property
    def tau(self):
        """Return the number of divisors of self.num.

        The Fundamental Theorem of Arithmetic guarantees that every given
        integer is a unique product of powers of primes; i.e. for all z in Z,
        z = (p_1 ^ a_1 )*...*(p_n ^ a_n) for primes p_1, ..., p_n and
        integer powers a_1, ..., a_n. Moreover, the number of factors of a
        given integer is equal to d(Z) = (a_1 + 1)*...*(a_n + 1). This
        function is an implementation of the theorem. More info at
        https://oeis.org/A000005.
        """
        # TODO: can't this just be len(self._divisors)?

        if self.num <= 0:
            return Integer(0)
        if self.num == 1:
            return Integer(1)
        product: int = 1
        for z in self.decomposition.values():
            product *= z + 1
        return Integer(product)

    @property
    def totatives(self) -> set:
        """Return the totatives of self.num.

        The totatives of z are the k in Z, 1<=k<=z, that are coprime to z
        """
        if self.num <= 0:
            return set()
        return {x for x in range(1, self.num + 1) if self.gcd(self.num, x) == 1}


def nth_most_divisors(n: int) -> int:
    """Return the nth highly-composite number.

    I.e., natural number with nth most divisors. E.g. 1 is the 1st HCN
    because no natural number has more factors; 2 is the second HCN because
    it has the most factors of all natural numbers less than or equal to 2.
    More info at https://oeis.org/A002182.

    Args:
    ----
        n (int): The element in Highly Composite Numbers sequence to return
    Returns:
        (int): the integer in position `n` in the Highly Composite Numbers seq
    """
    if n == 1:
        return 1
    record: list = [1]
    z: int = 2

    while z >= 1:
        # Get the number of divisors of the current integer
        dz = Integer(z).tau

        if dz > max(record):
            record.append(dz)
            if len(record) == n:
                break
            z += 1
            continue
        if dz == max(record):
            z += 1
            continue
        z += 1
        continue

    return z
