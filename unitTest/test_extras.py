import unittest
import sys
sys.path.append(".")
from cutterDRcovPlugin import extras

class TestExtras(unittest.TestCase):

    def test_hexPad(self):
        self.assertEqual(extras.hexPad(0x123,0), "0x123")
        self.assertEqual(extras.hexPad(0x123,1), "0x123")
        self.assertEqual(extras.hexPad(0x123,2), "0x123")
        self.assertEqual(extras.hexPad(0x123,3), "0x123")
        self.assertEqual(extras.hexPad(0x123,4), "0x0123")
        self.assertEqual(extras.hexPad(0x123,5), "0x00123")
        self.assertEqual(extras.hexPad(0x123,6), "0x000123")
        self.assertEqual(extras.hexPad(0x123,7), "0x0000123")
        self.assertEqual(extras.hexPad(0x123,8), "0x00000123")

    def test_fileName(self):
        self.assertEqual(extras.fileName(r"C:\Windows\notepad.exe"), "notepad.exe")
        self.assertEqual(extras.fileName(r"C:/Windows/notepad.exe"), "notepad.exe")
        self.assertEqual(extras.fileName(r"/bin/ls"), "ls")
        self.assertEqual(extras.fileName(r"./test"), "test")
if __name__ == '__main__':
    unittest.main()
