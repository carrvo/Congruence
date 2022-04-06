"""
"""

import math

def is_relatively_prime(a, b):
    """
    (a, b) == 1
    """
    return math.gcd(a, b) == 1
