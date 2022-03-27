"""
>>> MultiplicativeInverse(143, 7)
(5, 7)
>>> MultiplicativeInverse(91, 11)
(4, 11)
>>> MultiplicativeInverse(77, 13)
(12, 13)

>>> ChineseRemainderTheorem(((2, 7), (4, 11), (5, 13)))
(499, 1001)
"""

import math
import functools

def MultiplicativeInverse(value, modulus):
    value = value % modulus
    for multiple in range(1, value+1):
            condition = multiple * modulus + 1
            if condition % value == 0:
                    break
    return (condition // value, modulus)

def ChineseRemainderTheorem(congruences):
    M = functools.reduce(lambda x, y: x*y, [congruence[1] for congruence in congruences]) // functools.reduce(math.gcd, [congruence[1] for congruence in congruences]) # LCM based on https://stackoverflow.com/a/50830937
    congruence_triples = [(congruence[0], congruence[1], M // congruence[1]) for congruence in congruences]
    x = sum(triple[0] * triple[2] * MultiplicativeInverse(triple[2], triple[1])[0] for triple in congruence_triples)
    return (x % M, M)
