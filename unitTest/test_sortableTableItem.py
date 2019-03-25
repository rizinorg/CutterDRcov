import unittest
import sys
sys.path.append(".")
from cutterDRcovPlugin.sortableTableItem import *

class TestSortableTableItem(unittest.TestCase):

    def test_PercentWidgetItem(self):
        a = PercentWidgetItem("50%")
        b = PercentWidgetItem("100%")
        self.assertEqual(a < b, True)
        self.assertEqual(a < a, False)

    def test_HexWidgetItem(self):
        a = HexWidgetItem("0x5")
        b = HexWidgetItem("0X07")
        self.assertEqual(a < b, True)
        self.assertEqual(a < a, False)

    def test_RatioWidgetItem(self):
        a = RatioWidgetItem("1/2")
        b = RatioWidgetItem("3/4")
        self.assertEqual(a < b, True)
        self.assertEqual(a < a, False)

if __name__ == '__main__':
    unittest.main()
