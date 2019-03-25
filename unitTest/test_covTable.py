import unittest
import sys
sys.path.append(".")
class fakeCutter():
    def cmdj(self, command):
        if command == "ij":
            return {'core': {'file': 'test1.bin'},
                    'bin': {'baddr': 0x8048000}}
        if command == "aflj":
            return [{'offset': 134512736, 'name': 'entry0'}]
        if command == "afbj @entry0":
            return [
                    {'addr': 0x8048060, 'size': 20, 'ninstr': 5},
                    {'addr': 0x8048074, 'size': 7,  'ninstr': 2},
                    {'addr': 0x804807b, 'size': 15, 'ninstr': 3},
                    {'addr': 0x804808a, 'size': 12, 'ninstr': 3}
                    ]

        
sys.modules['cutter'] = fakeCutter()

import cutter
from cutterDRcovPlugin import covTable, drcov

sys.modules['cutter'] = fakeCutter()

class TestcovTable(unittest.TestCase):
    def test_analyse_function(self):
        # Here, checking if cutter works as expected is out of scope but rather
        # what I am checking is given that cutter works as expected does my code
        # work as expected as well or not
        modules, bbs = drcov.load("test_files/drcov2.4.log")
        function = cutter.cmdj("aflj")[0]
        base = cutter.cmdj("ij")['bin']['baddr']
        entry, hits = covTable.analyse_function(function, base, bbs[0])
        self.assertEqual(entry, ['76.923%', 'entry0', '0x08048060', '10/13', '3/4'])
        self.assertEqual(hits, {0x8048060, 0x804808a, 0x8048074})
if __name__ == '__main__':
    unittest.main()
