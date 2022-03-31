import unittest
import sys

from congruence import CongruenceClass

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
