"""
"""

import sys
import math

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

    def convert(self, modulo):
        """
        First, a note about notation:
        x̄∈Zm =>  x̄ = { x*0+r, x*1+r, x*2+r, ..., x*(m-1)+r }
        x̄ (mod n) <=> { x*0+r (mod n), x*1+r (mod n), x*2+r (mod n), ..., x*(m-1)+r (mod n) }
        That is, just as x̄ is a set with multiple values, so is x̄ (mod n) a set with multiple values.
        And "~" is the negation.

        Thus:
        m<n, m|n, x̄∈Zm, | x̄ (mod n) | = m
        m>n, m|n, x̄∈Zm, | x̄ (mod n) | = 1
        ~m|n, x̄∈Zm, | x̄ (mod n) | = n / (m, n)
        Note that for relatively prime: (m, n) = 1 => n / (m, n) = n
        """
        def iterate_and_convert(size):
            return {
                self.__class__(c, modulo)
                for c
                in range(self.remainder, self.value(size), self.modulus)
            }

        if self.modulus % modulo == 0:
            if self.modulus > modulo:
                return iterate_and_convert(1)
            else:
                return iterate_and_convert(self.modulus)
        else:
            return iterate_and_convert(modulo // math.gcd(self.modulus, modulo))

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
