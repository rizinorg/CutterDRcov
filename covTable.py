import cutter
from pathlib import Path
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import Qt
def initCovTable(covTable, modules, bbs):
    covTable.bbs = bbs
    covTable.modules = modules
    refresh(covTable)

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

def refresh(covTable):
    functions = cutter.cmdj("aflj")
    module = Path(cutter.cmdj("ij")['core']['file']).name
    idx = getmodule_idx(covTable.modules, module)
    # [coverage, name, address, instruction hits, basic block hits]
    for function in functions:
        entry = {}
        entry['name'] = function['name']
        entry['address'] = function['offset']
        bbs = cutter.cmdj("afbj @" + entry['name'])
        ins_count = 0
        ins_hits = 0
        bbs_count = 0
        bbs_hits = 0
        for bb in bbs:
            bbs_count += 1
            ins_count += bb['ninstr']
            if bb['addr'] in covTable.bbs[idx]:
                bbs_hits += 1
                ins_hits += bb['ninstr']
        entry['ins_hits'] = str(ins_hits) + "/" + str(ins_count)
        entry['bbs_hits'] = str(bbs_hits) + "/" + str(bbs_count)
        entry['coverage'] = str(round(ins_hits*100/ins_count,1)) + "%"
        rowPosition = covTable.rowCount()
        covTable.insertRow(rowPosition)
        covTable.setItem(rowPosition , 0, PercentWidgetItem(entry['coverage']))
        covTable.setItem(rowPosition , 1, QTableWidgetItem(entry['name']))
        covTable.setItem(rowPosition , 2, HexWidgetItem(hexpad(entry['address'],8)))
        covTable.setItem(rowPosition , 3, RatioWidgetItem(entry['ins_hits']))
        covTable.setItem(rowPosition , 4, centered_text(entry['bbs_hits']))
