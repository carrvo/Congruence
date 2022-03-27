import unittest

import sys
import os
sys.path.append(os.path.abspath(os.curdir))

import test
from test_congruence import CongruenceTests
from test_congruence_class import CongruenceClassTests

unittest.main()
