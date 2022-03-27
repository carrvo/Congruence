import unittest

from congruence import Congruence

class CongruenceTests(unittest.TestCase):

    def test_user_friendly(self):
        raw = tuple([3, 7])
        mod = Congruence(*raw)
        self.assertEqual("3 (mod 7)", str(mod))
        self.assertEqual(repr(raw), repr(mod))

    def test_keeps_remainder(self):
        raw = tuple([3+7*5, 7])
        mod = Congruence(*raw)
        self.assertEqual(3, mod.remainder)
