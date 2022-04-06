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

    def test_reflexivity(self):
        a = 24
        raw = tuple([a, 7])
        mod = Congruence(*raw)
        self.assertEqual(mod, Congruence(*raw))
        self.assertEqual(mod, a)
        self.assertTrue(mod.Reflexive)

    def test_symmetry(self):
        a = 24
        b = 31
        raw = tuple([a, 7])
        mod = Congruence(*raw)
        self.assertEqual(mod, b)
        self.assertEqual(b, mod)
        self.assertTrue(mod.Symmetrical)

    def test_transitivity(self):
        a = Congruence(24, 7)
        b = Congruence(31, 7)
        c = Congruence(17, 7)
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(a, c)
        self.assertTrue(a.Transitive)

    def test_negatives(self):
        a = 24
        mod = 7
        positive_positive = Congruence(a, mod)
        positive_negative = Congruence(a, -mod)
        negative_positive = Congruence(-a, mod)
        negative_negative = Congruence(-a, -mod)
        self.assertEqual(positive_positive, positive_negative)
        self.assertEqual(negative_positive, negative_negative)

    def test_addition(self):
        a = 24
        b = Congruence(a, 7)
        c = 31
        d = Congruence(c, 7)
        self.assertEqual(Congruence(a+c, 7), b+d)
        self.assertEqual(Congruence(a+c, 7), b+c)
        self.assertEqual(Congruence(a+c, 7), a+d)

    def test_subtraction(self):
        a = 24
        b = Congruence(a, 7)
        c = 31
        d = Congruence(c, 7)
        self.assertEqual(Congruence(a-c, 7), b-d)
        self.assertEqual(Congruence(a-c, 7), b-c)
        self.assertEqual(Congruence(a-c, 7), a-d)

    def test_multiplication(self):
        a = 24
        b = Congruence(a, 7)
        c = 31
        d = Congruence(c, 7)
        self.assertEqual(Congruence(a*c, 7), b*d)
        self.assertEqual(Congruence(a*c, 7), b*c)
        self.assertEqual(Congruence(a*c, 7), a*d)

    def test_linear(self):
        a = 24
        b = Congruence(a, 7)
        c = 31
        d = Congruence(c, 7)
        x = 5
        y = 10
        self.assertEqual(Congruence(a*x + c*y, 7), b*x + d*y)
