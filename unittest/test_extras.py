import unittest
import sys
sys.path.append(".")
from cutterdrcov_plugin import extras

class TestExtras(unittest.TestCase):

    def test_hex_pad(self):
        self.assertEqual(extras.hex_pad(0x123, 0), "0x123")
        self.assertEqual(extras.hex_pad(0x123, 1), "0x123")
        self.assertEqual(extras.hex_pad(0x123, 2), "0x123")
        self.assertEqual(extras.hex_pad(0x123, 3), "0x123")
        self.assertEqual(extras.hex_pad(0x123, 4), "0x0123")
        self.assertEqual(extras.hex_pad(0x123, 5), "0x00123")
        self.assertEqual(extras.hex_pad(0x123, 6), "0x000123")
        self.assertEqual(extras.hex_pad(0x123, 7), "0x0000123")
        self.assertEqual(extras.hex_pad(0x123, 8), "0x00000123")

    def test_file_name(self):
        self.assertEqual(extras.file_name(r"C:\Windows\notepad.exe"), "notepad.exe")
        self.assertEqual(extras.file_name(r"C:/Windows/notepad.exe"), "notepad.exe")
        self.assertEqual(extras.file_name(r"/bin/ls"), "ls")
        self.assertEqual(extras.file_name(r"./test"), "test")
if __name__ == '__main__':
    unittest.main()
