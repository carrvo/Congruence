"""
"""

import sys

import congruence

class CongruenceClass(object):
    """
    """

    def __init__(self, value, modulus):
        modulus = abs(modulus)
        self.remainder = value % modulus
        self.modulus = modulus

    def __repr__(self):
        return repr(tuple([self.remainder, self.modulus]))

    def __str__(self):
        return f'{self.remainder}\u0304'

    def __hash__(self):
        """
        :kudos: to https://stackoverflow.com/a/10254636/7163041
        """
        return hash(tuple([self.remainder, self.modulus]))

    @classmethod
    def Set(cls, modulus):
        return set(cls(r, modulus) for r in range(0, modulus))

    def __len__(self):
        """
        Theoretically should be math.inf, but implementation
        restricts to sys.maxsize

        :ref: https://docs.python.org/3/reference/datamodel.html#object.__len__
        """
        return sys.maxsize

    def __contains__(self, other):
        if isinstance(other, congruence.Congruence):
            return other == congruence.Congruence(self.remainder, self.modulus)
        if not isinstance(other, int):
            raise ValueError(f"{other} from {type(other)} is not of "
                             f"int for which to compare (mod {self.modulus})")
        return other % self.modulus == self.remainder

    def __sanitize(self, other):
        if not isinstance(other, CongruenceClass):
            return CongruenceClass(other, self.modulus)
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
        return CongruenceClass(self.remainder + other.remainder, self.modulus)

    __radd__ = __add__

    def __sub__(self, other):
        other = self.__sanitize(other)
        return CongruenceClass(self.remainder - other.remainder, self.modulus)

    __rsub__ = __sub__

    def __mul__(self, other):
        other = self.__sanitize(other)
        return CongruenceClass(self.remainder * other.remainder, self.modulus)

    __rmul__ = __mul__

    @property
    def is_relatively_prime_to_modulus(self):
        return congruence.is_relatively_prime(self.remainder, self.modulus)

    @property
    def multiplicative_inverse(self):
        if not self.is_relatively_prime_to_modulus:
            raise ValueError(f"{str(self)} must be relatively prime"
                             f" to {self.modulus}")
        # brute force but limited to the range it must exist within
        for multiple in range(1, self.remainder+1):
            condition = multiple * self.modulus + 1
            value, mod = divmod(condition, self.remainder)
            if mod == 0:
                return CongruenceClass(value, self.modulus)
        else:
            raise ValueError(f"No multiplicative inverse for {str(self)}")

def Zm(m):
    return CongruenceClass.Set(m)

def Zm_star(m):
    return set(
        r
        for r in Zm(m)
        if congruence.is_relatively_prime(r.remainder, m)
    )

def EulerTotent(m):
    return len(Zm_star(m))
