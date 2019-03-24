import unittest
import sys
sys.path.append(".")
from cutterDRcovPlugin import drcov

#class drcovTest(unittest.TestCase):
#    def 
class TestDRcov(unittest.TestCase):
    def test_get_file_size(self):
        f = open("test_files/drcov1.log", "r")
        size = drcov.get_file_size(f)
        f.close()
        self.assertEqual(size, 851)

    #2_4 stands for Version 2 Module version 4
    def test_drcov_2_4_linux(self):
        modules, bbs = drcov.load("test_files/drcov1.log")
        self.assertEqual(len(modules), 1)
        self.assertEqual(modules[0]['start'],0x8048000)
        self.assertEqual(modules[0]['name'], 'test1.bin')
        self.assertEqual(len(bbs), 1)
        self.assertEqual(len(bbs[0]), 3)
        bbs = bbs[0]
        self.assertEqual(bbs[0x60], 20)
        self.assertEqual(bbs[0x74], 7)
        self.assertEqual(bbs[0x8a], 12)
if __name__ == '__main__':
    unittest.main()
