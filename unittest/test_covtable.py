import unittest
import sys
from mock import patch
sys.path.append(".")

class FakeCutter():
    def cmdj(self, _):
        return ""

sys.modules['cutter'] = FakeCutter()

import cutter
from cutterdrcov_plugin import covtable, drcov

def test_1_cmdj(cmd):
    if cmd == "ij":
        return {
            'core': {'file': 'test1.bin'},
            'bin': {'baddr': 0x8048000}
        }
    if cmd == "aflj":
        return [{'offset': 0x8048060, 'name': 'entry0'}]
    if cmd == "afbj @entry0":
        return [
            {'addr': 0x8048060, 'size': 20, 'ninstr': 5},
            {'addr': 0x8048074, 'size': 7, 'ninstr': 2},
            {'addr': 0x804807b, 'size': 15, 'ninstr': 3},
            {'addr': 0x804808a, 'size': 12, 'ninstr': 3}
        ]
    return None

def test_2_cmdj(cmd):
    if cmd == "ij":
        return {
            'core': {'file': 'test2.bin'},
            'bin': {'baddr': 0x8048000}
        }
    if cmd == "aflj":
        return [
            {'offset': 0x8048060, 'name': 'loc.uncalled'},
            {'offset': 0x804806a, 'name': 'entry0'}
            ]
    if cmd == "afbj @entry0":
        return [
            {'addr': 0x804806a, 'size': 20, 'ninstr': 5},
            {'addr': 0x804807e, 'size': 7, 'ninstr': 2},
            {'addr': 0x8048085, 'size': 15, 'ninstr': 3},
            {'addr': 0x8048094, 'size': 17, 'ninstr': 4}
        ]
    if cmd == "afbj @loc.uncalled":
        return [
            {"addr": 0x8048060, "size": 10, "ninstr": 5}
        ]
    return None



class TestcovTable(unittest.TestCase):

    @patch("cutter.cmdj", side_effect=test_1_cmdj)
    def test_analyse_function(self, _):
        # Here, checking if cutter works as expected is out of scope but rather
        # what I am checking is given that cutter works as expected does my code
        # work as expected as well or not
        _, bbs = drcov.load("test_files/drcov2.4.log")
        function = cutter.cmdj("aflj")[0]
        base = cutter.cmdj("ij")['bin']['baddr']
        entry, hits = covtable.analyse_function(function, base, bbs[0])
        hardcoded_entry = ['76.923%', 'entry0', '0x08048060', '10/13', '3/4']
        self.assertEqual(entry, hardcoded_entry)
        self.assertEqual(hits, {0x8048060, 0x804808a, 0x8048074})

    def do_analyse(self, modules, bbs, table, hits):
        config = {}
        config['modules'] = modules
        config['bbs'] = bbs
        covtable.analyse(config)
        self.assertEqual(config['table'], table)
        self.assertEqual(config['bb_hits'], hits)

    @patch("cutter.cmdj", side_effect=test_1_cmdj)
    def test_analyse1(self, _):
        modules, bbs = drcov.load("test_files/drcov2.4.log")
        table = [['76.923%', 'entry0', '0x08048060', '10/13', '3/4']]
        hits = {0x8048060, 0x804808a, 0x8048074}
        self.do_analyse(modules, bbs, table, hits)

    @patch("cutter.cmdj", side_effect=test_2_cmdj)
    def test_analyse2(self, _):
        """
        This test case where not all functions gets covered,
        so they needed be reported
        """
        modules, bbs = drcov.load("test_files/drcov.test2.log")
        # technically speaking only 10 instructions can get executed but what
        # can I do ... any way it wouldn't matter
        table = [["78.571%", "entry0", "0x0804806a", "11/14", "3/4"]]
        hits = {0x0804806a, 0x0804807e, 0x08048094}
        self.do_analyse(modules, bbs, table, hits)

    @patch("cutter.cmdj", side_effect=test_1_cmdj)
    def test_bad_analysis(self, _):
        """
        I found this by mistake, it triggered exception while it shouldn't
        """
        modules, bbs = drcov.load("test_files/drcov.test2.log")
        self.do_analyse(modules, bbs, [], set())

if __name__ == '__main__':
    unittest.main()
