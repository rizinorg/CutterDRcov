from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import Qt

class PercentWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        return float(self.text()[:-1]) < float(other.text()[:-1])

class HexWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        return int(self.text(), 16) < int(other.text(), 16)

class RatioWidgetItem(QTableWidgetItem):
    def get_ratio(self):
        splt = self.text().split("/")
        return int(splt[0]) / int(splt[1])
    def __lt__(self, other):
        return self.get_ratio() < other.get_ratio()

def centered_text(txt):
    item = RatioWidgetItem(txt)
    item.setTextAlignment(Qt.AlignCenter)
    return item
