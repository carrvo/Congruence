"""
"""

import sys

import congruence

class CongruenceClass(congruence.Congruence):
    """
    """

    def __init__(self, value, modulus):
        super().__init__(value, modulus)

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

def Zm(m, klass=CongruenceClass):
    if not issubclass(klass, CongruenceClass):
        raise TypeError(f"Type {type(klass)} is not a subtype of {CongruenceClass}")
    return klass.Set(m)

def Zm_star(m, klass=CongruenceClass):
    return set(
        r
        for r in Zm(m, klass)
        if r.is_relatively_prime_to_modulus
    )

def EulerTotent(m, klass=CongruenceClass):
    return len(Zm_star(m, klass))
