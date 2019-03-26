import unittest
import sys
sys.path.append(".")
import cutterdrcov_plugin.sortable_table_item as sti

class TestSortableTableItem(unittest.TestCase):

    def check_lt(self, objs):
        self.assertEqual(objs[0] < objs[1], True)
        self.assertEqual(objs[1] < objs[2], False)
        self.assertEqual(objs[2] < objs[0], False)

    def test_percent_widget_item(self):
        objs = [
            sti.PercentWidgetItem("50%"),
            sti.PercentWidgetItem("100%"),
            sti.PercentWidgetItem("50%")
            ]
        self.check_lt(objs)

    def test_hex_widget_item(self):
        objs = [
            sti.HexWidgetItem("0x5"),
            sti.HexWidgetItem("0X07"),
            sti.HexWidgetItem("0x5")
            ]
        self.check_lt(objs)

    def test_ratio_widget_item(self):
        objs = [
            sti.RatioWidgetItem("1/2"),
            sti.RatioWidgetItem("3/4"),
            sti.RatioWidgetItem("1/2")
            ]
        self.check_lt(objs)

if __name__ == '__main__':
    unittest.main()
