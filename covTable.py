import cutter
from pathlib import Path
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import Qt

def getmodule_idx(modules, module):
    for i in range(len(modules)):
        if modules[i]['name'] == module:
            return i

class PercentWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        return float(self.text()[:-1]) < float(other.text()[:-1])

class HexWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        return int(self.text(),16) < int(other.text(),16)

class RatioWidgetItem(QTableWidgetItem):
    def get_ratio(self):
        s = self.text().split("/")
        return int(s[0])/int(s[1])
    def __lt__(self, other):
        
        return self.get_ratio() < other.get_ratio()

def centered_text(x):
    w = RatioWidgetItem(x)
    w.setTextAlignment(Qt.AlignCenter)
    return w

def hexpad(num, pad):
    return "{0:#0{1}x}".format(num,pad + 2)

def analyse(config):
    functions = cutter.cmdj("aflj")
    module = Path(cutter.cmdj("ij")['core']['file']).name
    idx = getmodule_idx(config['modules'], module)
    # [coverage, name, address, instruction hits, basic block hits]
    config['bb_hits'] = set()
    config['table'] = []
    for function in functions:
        entry = ["","","","",""]
        entry[1] = function['name']
        entry[2] = hexpad(function['offset'], 8)
        bbs = cutter.cmdj("afbj @" + function['name'])
        inst_count = 0
        inst_hits = 0
        bbs_count = 0
        bbs_hits = 0
        for bb in bbs:
            bbs_count += 1
            inst_count += bb['ninstr']
            if bb['addr'] in config['bbs'][idx]:
                bbs_hits += 1
                inst_hits += bb['ninstr']
                config['bb_hits'].add(bb['addr'])
        if bbs_hits == 0:
            continue; # skip functions with zero coverage
        entry[3] = str(inst_hits) + "/" + str(inst_count)
        entry[4] = str(bbs_hits) + "/" + str(bbs_count)
        entry[0] = str(round(inst_hits*100/inst_count,3)) + "%"
        config['table'].append(entry)
