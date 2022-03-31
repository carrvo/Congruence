import unittest

from congruence import CongruenceClass

class CongruenceClassTests(unittest.TestCase):

    def test_user_friendly(self):
        raw = tuple([3, 7])
        mod = CongruenceClass(*raw)
        self.assertEqual(str(mod), '3\u0304')
        self.assertEqual(repr(mod), repr(raw))

    def test_set_of_classes(self):
        mod = 5
        congruence_set = CongruenceClass.Set(mod)
        self.assertEqual(len(congruence_set), mod)
        self.assertEqual(set(c.remainder for c in congruence_set),
                         set(range(0, 5)))
