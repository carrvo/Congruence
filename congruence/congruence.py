"""
"""

class Congruence(object):
    """
    """

    def __init__(self, value, modulus):
        self.remainder = value % modulus
        self.modulus = modulus

    def __repr__(self):
        return repr(tuple([self.remainder, self.modulus]))

    def __str__(self):
        return f"{self.remainder} (mod {self.modulus})"

    def value(self, q):
        """
        x = q * m + r
        """
        return q * self.modulus + self.remainder
