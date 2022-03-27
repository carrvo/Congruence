import unittest

from congruence import Congruence

class CongruenceTests(unittest.TestCase):

    def test_user_friendly(self):
        raw = tuple([3, 7])
        mod = Congruence(*raw)
        self.assertEqual(str(mod), "3 (mod 7)")
        self.assertEqual(repr(mod), repr(raw))

    def test_keeps_remainder(self):
        """
        0 <= remainder < modulus
        """
        raw = tuple([3+7*5, 7])
        mod = Congruence(*raw)
        self.assertEqual(mod.remainder, 3)
        self.assertGreaterEqual(mod.remainder, 0)
        self.assertLess(mod.remainder, mod.modulus)

    def test_definition(self):
        """
        modulus divides value minus remainder
        """
        raw = tuple([24, 7])
        mod = Congruence(*raw)
        self.assertEqual((raw[0] - mod.remainder) / mod.modulus,
                         raw[0] // mod.modulus)

    def test_recover_value(self):
        q = 5
        raw = tuple([3+7*q, 7])
        mod = Congruence(*raw)
        self.assertEqual(mod.value(q), raw[0])
