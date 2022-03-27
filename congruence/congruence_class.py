"""
"""

from congruence.congruence import Congruence

class CongruenceClass(object):
    """
    """

    def __init__(self, value, modulus):
        self.remainder = value % modulus
        self.modulus = modulus

    def __repr__(self):
        return repr(tuple([self.remainder, self.modulus]))

    def __str__(self):
        return f'{self.remainder}\u0304'

    @staticmethod
    def Set(cls, modulus):
        return set(CongruenceClass(r, modulus) for r in range(0, modulus))
