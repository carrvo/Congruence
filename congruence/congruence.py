"""
"""

import sys
import math
import functools

import congruence

class Congruence(object):
    """
    """

    def __init__(self, value, modulus):
        modulus = abs(modulus)
        self.remainder = value % modulus
        self.modulus = modulus

    def __repr__(self):
        return repr(tuple([self.remainder, self.modulus]))

    def __str__(self):
        return f'{self.remainder} (mod {self.modulus})'

    def value(self, q):
        """
        x = q * m + r
        """
        return q * self.modulus + self.remainder

    def __sanitize(self, other):
        if not isinstance(other, Congruence):
            return Congruence(other, self.modulus)
        if other.modulus != self.modulus:
            raise ValueError(f"modulus {other.modulus} from {type(other)} "
                             f"differs against {self.modulus} from {type(self)}")
        return other

    def __eq__(self, other):
        other = self.__sanitize(other)
        return (self.modulus == other.modulus and
                self.remainder == other.remainder)

    def __add__(self, other):
        other = self.__sanitize(other)
        return Congruence(self.remainder + other.remainder, self.modulus)

    __radd__ = __add__

    def __sub__(self, other):
        other = self.__sanitize(other)
        return Congruence(self.remainder - other.remainder, self.modulus)

    __rsub__ = __sub__

    def __mul__(self, other):
        other = self.__sanitize(other)
        return Congruence(self.remainder * other.remainder, self.modulus)

    __rmul__ = __mul__

    def __pow__(self, other):
        return Congruence(self.remainder ** other, self.modulus)

    @property
    def is_relatively_prime_to_modulus(self):
        return congruence.is_relatively_prime(self.remainder, self.modulus)

    def LinearCongruence(self, value):
        """
        value * return == str(self)
        """
        if congruence.is_relatively_prime(value, self.modulus):
            return self.remainder * value**(congruence.EulerTotent(self.modulus) - 1)
        else:
            count = math.gcd(value, self.modulus)
            div, mod = divmod(self.remainder, count)
            if mod != 0:
                raise ValueError(f"{value} and {str(self)} do not all divide "
                                 f"{count} ({self.remainder} / {count} = "
                                 f"{self.remainder / count})")
            mod_ratio = self.modulus // count
            x0 = Congruence(div, mod_ratio).LinearCongruence(value // count)
            return tuple(
                Congruence(x0 + mod_ratio*t, self.modulus).remainder
                for t in range(0, count)
            )

    @property
    def multiplicative_inverse(self):
        one = Congruence(1, self.modulus)
        return Congruence(one.LinearCongruence(self.remainder), self.modulus)

    @property
    def order(self):
        for i in range(1, congruence.EulerTotent(self.modulus) + 1):
            if Congruence(self.remainder**i, self.modulus).remainder == 1:
                return i

    @property
    def Reflexive(self):
        return True

    @property
    def Symmetrical(self):
        return True

    @property
    def Transitive(self):
        return True

def ChineseRemainderTheorem(*congruences):
    M = functools.reduce(lambda x, y: x*y, [congruence.modulus for congruence in congruences]) // functools.reduce(math.gcd, [congruence.modulus for congruence in congruences]) # LCM based on https://stackoverflow.com/a/50830937
    congruence_triples = [(congruence, M // congruence.modulus) for congruence in congruences]
    x = sum(triple[0].remainder * triple[1] * Congruence(triple[1], triple[0].modulus).multiplicative_inverse.remainder for triple in congruence_triples)
    return Congruence(x, M)
