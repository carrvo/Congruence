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
            raise ValueError(f"{other} from {type(other)} is not of"
                             f"int for which to compare (mod {self.modulus})")
        return other % self.modulus == self.remainder

    def __sanitize(self, other):
        if not isinstance(other, CongruenceClass):
            return CongruenceClass(other, self.modulus)
        if other.modulus != self.modulus:
            raise ValueError(f"modulus {other.modulus} from {type(other)}" +
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
