import unittest

from congruence import Congruence

class CongruenceTests(unittest.TestCase):

    def test_user_friendly(self):
        raw = tuple([3, 7])
        mod = Congruence(3, 7)
        self.assertEqual("3 (mod 7)", str(mod))
        self.assertEqual(repr(raw), repr(mod))
