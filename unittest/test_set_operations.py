import unittest
import sys
sys.path.append(".")
from cutterdrcov_plugin import drcov

A = { 1:1, 2:2, 3:3 }
B = { 2:2, 4:4 }
C = { 1:1, 3:3, 5:5 }

class TestSetOperations(unittest.TestCase):

    def test_union(self):
        self.assertEqual(drcov.union_bbs([A]), A)
        self.assertEqual(drcov.union_bbs([A, B]), {1:1, 2:2, 3:3, 4:4})
        self.assertEqual(drcov.union_bbs([A, B, C]), {1:1, 2:2, 3:3, 4:4, 5:5})

    def test_subtract(self):
        self.assertEqual(drcov.subtract_bbs([A]), {1:1, 2:2, 3:3})
        self.assertEqual(drcov.subtract_bbs([A, B]), {1:1, 3:3})
        self.assertEqual(drcov.subtract_bbs([A, B, C]), {})

    def test_intersect(self):
        self.assertEqual(drcov.intersect_bbs([A]), A)
        self.assertEqual(drcov.intersect_bbs([A, B]), {2:2})
        self.assertEqual(drcov.intersect_bbs([A, B, C]), {})

if __name__ == '__main__':
    unittest.main()
