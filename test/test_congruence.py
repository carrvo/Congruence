import unittest
import math

import congruence
from congruence import Congruence,is_relatively_prime,ChineseRemainderTheorem

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

    def test_exponential(self):
        raw = tuple([3, 7])
        mod = Congruence(*raw)
        p = 5
        self.assertEqual(Congruence(raw[0]**p, raw[1]), mod**p)

    def test_polynomial(self):
        raw = tuple([3, 7])
        mod = Congruence(*raw)
        f = lambda x: x**5 - x**3 + 17
        self.assertEqual(Congruence(f(raw[0]), 7), f(mod))

    def test_constant_multiple(self):
        raw = tuple([3, 7])
        mod = Congruence(*raw)
        c = 5
        self.assertEqual(Congruence(c*raw[0], raw[1]), c*mod)

    @unittest.skip("No practical implementation (as far as proper checks) known.")
    def test_cancellation_law(self):
        raw = tuple([3, 7])
        c = 5
        mod = Congruence(c*raw[0], raw[1])
        self.assertEqual(mod//c, Congruence(*raw))

    def test_relatively_prime(self):
        a = 24
        mod = Congruence(a, 7)
        self.assertTrue(mod.is_relatively_prime_to_modulus)
        self.assertTrue(is_relatively_prime(a, mod.modulus))

    def test_Eulers_Theorem(self):
        raw = tuple([3, 7])
        mod = Congruence(*raw)
        self.assertTrue(mod.is_relatively_prime_to_modulus)
        self.assertEqual(mod**congruence.EulerTotent(mod.modulus),
                         Congruence(1, mod.modulus))

    def test_Linear_Congruence(self):
        a = 24
        b = Congruence(31, 7)
        self.assertTrue(congruence.is_relatively_prime(a, b.modulus))
        linear = b.LinearCongruence(a)
        self.assertEqual(Congruence(a*linear, b.modulus), b)

    def test_multiplicative_inverse(self):
        raw = tuple([3, 7])
        mod = Congruence(*raw)
        self.assertTrue(mod.is_relatively_prime_to_modulus)
        self.assertEqual(mod*mod.multiplicative_inverse, 1)

    def test_Linear_Congruence_when_not_relatively_prime(self):
        a = 33
        b = Congruence(15, 45)
        self.assertFalse(b.is_relatively_prime_to_modulus)
        count = math.gcd(a, b.modulus)
        linear = b.LinearCongruence(a)
        self.assertEqual(len(linear), count)
        self.assertEqual(linear, (10, 25, 40))

    def test_Chinese_Remainder_Theorem(self):
        a1 = Congruence(2, 7)
        a2 = Congruence(4, 11)
        a3 = Congruence(5, 13)
        self.assertEqual(ChineseRemainderTheorem(a1, a2, a3), Congruence(499, 1001))

    def test_order(self):
        raw = tuple([25, 7])
        mod = Congruence(*raw)
        order = mod.order
        self.assertLess(order, congruence.EulerTotent(mod.modulus))
        self.assertEqual(order, 3)
