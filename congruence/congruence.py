"""
"""

class Congruence(tuple):
    """
    """

    def __new__(cls, value, modulus):
        """
        :kudos: to https://stackoverflow.com/a/23878346
        """
        self = super(Congruence, cls).__new__(cls, [value, modulus])
        return self

    def __init__(self, value, modulus):
        self.value = value
        self.modulus = modulus

    def __str__(self):
        return f"{self.value} (mod {self.modulus})"
