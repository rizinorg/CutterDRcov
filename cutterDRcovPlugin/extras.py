from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import Qt
import ntpath

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

def hexPad(num, pad):
    return "{0:#0{1}x}".format(num,pad + 2)


# https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
# cuz windows sucks :( .. hard
def file_name(path):
   # There's one caveat: Linux filenames may contain backslashes. So on linux,
    # r'a/b\c' always refers to the file b\c in the a folder, while on Windows,
    # it always refers to the c file in the b subfolder of the a folder. So when
    # both forward and backward slashes are used in a path, you need to know the
    # associated platform to be able to interpret it correctly. In practice it's
    # usually safe to assume it's a windows path since backslashes are seldom
    # used in Linux filenames, but keep this in mind when you code so you don't
    # create accidental security holes.

    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

