import unittest
import sys
sys.path.append(".")
from cutterDRcovPlugin import drcov

class TestDRcov(unittest.TestCase):

    def test_get_file_size(self):
        f = open("test_files/drcov2.4.log", "r")
        size = drcov.get_file_size(f)
        f.close()
        self.assertEqual(size, 851)

    def verify_test1_asm(self, covfile):
        modules, bbs = drcov.load(covfile)
        self.assertEqual(len(modules), 1)
        self.assertEqual(modules[0]['start'],0x8048000)
        self.assertEqual(modules[0]['name'], 'test1.bin')
        self.assertEqual(len(bbs), 1)
        self.assertEqual(len(bbs[0]), 3)
        bbs = bbs[0]
        self.assertEqual(bbs[0x60], 20)
        self.assertEqual(bbs[0x74], 7)
        self.assertEqual(bbs[0x8a], 12)

    def test_drcov_2_4_linux(self):
        # DRCOV VERSION: 2
        # Module Table: version 4
        # dynamoRIO 7.1.0-1 linux 32
        # test1.asm
        self.verify_test1_asm("test_files/drcov2.4.log")

    def test_drcov_2_3_linux(self):
        # DRCOV VERSION: 2
        # Module Table: version 3
        # dynamoRIO 7.0.17595-0 linux 32
        # test1.asm
        self.verify_test1_asm("test_files/drcov2.3.log")

    def test_drcov_2_2_linux(self):
        # DRCOV VERSION: 2
        # Module Table: version 2
        #dynamoRIO 7.0.0-RC1 linux 32
        # test1.asm
        self.verify_test1_asm("test_files/drcov2.2.log")

if __name__ == '__main__':
    unittest.main()
