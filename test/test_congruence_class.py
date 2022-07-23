import unittest
import sys
import math

import congruence
from congruence import CongruenceClass,Zm_star,EulerTotent

class CongruenceClassTests(unittest.TestCase):

    def test_user_friendly(self):
        raw = tuple([3, 7])
        mod = CongruenceClass(*raw)
        self.assertEqual(str(mod), '3\u0304')
        self.assertEqual(repr(mod), repr(raw))

    def test_definition(self):
        raw = tuple([3, 7])
        mod = CongruenceClass(*raw)
        #self.assertEqual(len(mod), math.inf)
        self.assertEqual(len(mod), sys.maxsize)
        for i in range(-100*7+3, +100*7+3, 7):
            self.assertIn(i, mod)
        self.assertIn(congruence.Congruence(*raw), mod)

    def test_set_of_classes(self):
        mod = 7
        congruence_set = CongruenceClass.Set(mod)
        self.assertEqual(len(congruence_set), mod)
        self.assertEqual(set(c.remainder for c in congruence_set),
                         set(range(0, mod)))

    def test_negatives(self):
        a = 24
        mod = 7
        positive_positive = CongruenceClass(a, mod)
        positive_negative = CongruenceClass(a, -mod)
        negative_positive = CongruenceClass(-a, mod)
        negative_negative = CongruenceClass(-a, -mod)
        self.assertEqual(positive_positive, positive_negative)
        self.assertEqual(negative_positive, negative_negative)

    def test_addition(self):
        a = 24
        b = CongruenceClass(a, 7)
        c = 31
        d = CongruenceClass(c, 7)
        self.assertEqual(CongruenceClass(a+c, 7), b+d)
        self.assertEqual(CongruenceClass(a+c, 7), b+c)
        self.assertEqual(CongruenceClass(a+c, 7), a+d)

    def test_subtraction(self):
        a = 24
        b = CongruenceClass(a, 7)
        c = 31
        d = CongruenceClass(c, 7)
        self.assertEqual(CongruenceClass(a-c, 7), b-d)
        self.assertEqual(CongruenceClass(a-c, 7), b-c)
        self.assertEqual(CongruenceClass(a-c, 7), a-d)

    def test_multiplication(self):
        a = 24
        b = CongruenceClass(a, 7)
        c = 31
        d = CongruenceClass(c, 7)
        self.assertEqual(CongruenceClass(a*c, 7), b*d)
        self.assertEqual(CongruenceClass(a*c, 7), b*c)
        self.assertEqual(CongruenceClass(a*c, 7), a*d)

    def test_EulerTotent(self):
        self.assertEqual(EulerTotent(12), 4)

    def test_multiplicative_inverse(self):
        raw = tuple([3, 7])
        mod = CongruenceClass(*raw)
        self.assertIn(mod, Zm_star(mod.modulus))
        self.assertTrue(mod.is_relatively_prime_to_modulus)
        self.assertEqual(mod*mod.multiplicative_inverse, 1)

    def test_two_relatively_prime(self):
        a = CongruenceClass(24, 7)
        self.assertTrue(a.is_relatively_prime_to_modulus)
        b = CongruenceClass(31, 7)
        self.assertTrue(b.is_relatively_prime_to_modulus)
        self.assertTrue((a*b).is_relatively_prime_to_modulus)

    def test_modulo_conversion(self):
        """
        My personal theory.
        """
        five = CongruenceClass(0, 5)
        ten = CongruenceClass(0, 10)
        twentyfive = CongruenceClass(0, 25)
        twentysix = CongruenceClass(0, 26)
        self.assertEqual({c.remainder for c in five.convert(modulo=twentyfive.modulus)}, {0, 5, 10, 15, 20})
        self.assertEqual({c.remainder for c in five.convert(modulo=ten.modulus)}, {0, 5})
        self.assertEqual({c.remainder for c in twentyfive.convert(modulo=five.modulus)}, {0})
        self.assertEqual({c.remainder for c in five.convert(modulo=twentysix.modulus)}, {0, 5, 10, 15, 20, 25, 4, 9, 14, 19, 24, 3, 8, 13, 18, 23, 2, 7, 12, 17, 22, 1, 6, 11, 16, 21})
        self.assertEqual({c.remainder for c in ten.convert(modulo=twentysix.modulus)}, {0, 10, 20, 4, 14, 24, 8, 18, 2, 12, 22, 6, 16})
        self.assertEqual({c.remainder for c in twentysix.convert(modulo=five.modulus)}, {0, 1, 2, 3, 4})
        self.assertEqual({c.remainder for c in twentysix.convert(modulo=ten.modulus)}, {6, 2, 8, 4, 0})

    def test_Chinese_Remainder_Theorem(self):
        """
        Usage of CongruenceClass.convert as an alternative to ChineseRemainderTheorem.
        """
        a1 = CongruenceClass(2, 7)
        a2 = CongruenceClass(4, 11)
        a3 = CongruenceClass(5, 13)
        def lcm(a, b):
            """
            kudos: https://stackoverflow.com/a/51716959/7163041
            """
            return abs(a*b) // math.gcd(a, b)
        M = lcm(lcm(a1.modulus, a2.modulus), a3.modulus)
        a1M = a1.convert(M)
        a2M = a2.convert(M)
        a3M = a3.convert(M)
        self.assertEqual(a1M.intersection(a2M, a3M), {congruence.ChineseRemainderTheorem(a1, a2, a3, klass=CongruenceClass)})
