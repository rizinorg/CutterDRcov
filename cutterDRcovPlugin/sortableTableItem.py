from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import Qt

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

