import cutter
from PySide2 import QtCore
from PySide2.QtWidgets import QAction, QFileDialog, QColorDialog
from .autogen import Ui_DockWidget
from .drcov import DCov_load
from .covTable import analyse
from .extras import *

class MyDockWidget(cutter.CutterDockWidget, Ui_DockWidget):
    def __init__(self, parent, action):
        super(MyDockWidget, self).__init__(parent, action)
        self.newConfig()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.loader.dragEnterEvent = self.loaderDragEnterEvent
        self.loader.dropEvent = self.dropFile
        self.loader.mousePressEvent = self.openFile
        self.colorize.clicked.connect(self.switchColorize)
        self.selectColor.clicked.connect(self.setColor)
        self.close.clicked.connect(self.closeCallBack)
        self.reload.clicked.connect(self.reloadCallBack)
        self.covTable.doubleClicked.connect(self.seek)

    def seek(self, idx):
        row = idx.row()
        addr = int(self.covTable.item(row, 2).text(),16)
        cutter.core().seek(addr)

    def switchColorize(self):
        self.config['colorize'] = not self.config['colorize']
        self.paint()

    def closeCallBack(self):
        self.config['colorize'] = False
        self.paint()
        self.newConfig()
        self.stackedWidget.setCurrentIndex(0)
    def reloadCallBack(self):
        self.config['colorize'] = False
        self.paint()
        analyse(self.config)
        self.config['colorize'] = True
        self.paint()

    def newConfig(self):
        self.config = {'color': 0x800000, 'colorize' : True}

    def loaderDragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            self.loader.setCursor(QtCore.Qt.DragMoveCursor)
            e.acceptProposedAction()

    def dropFile(self, e):
        self.loader.setCursor(QtCore.Qt.PointingHandCursor)
        files = e.mimeData().urls()
        fileName = files[0].toLocalFile()
        self.loadcov(fileName)

    def openFile(self, e):
        fileName = QFileDialog.getOpenFileName(self)
        if len(fileName[0]) == 0:
            return
        self.loadcov(fileName[0])

    def loadcov(self, file_name):
        try:
            modules, bbs = DCov_load(file_name)
        except:
            self.parent().messageBoxWarning("", "Invalid Coverage File")
            return
        self.config['modules'] = modules
        self.config['bbs'] = bbs
        self.stackedWidget.setCurrentIndex(1)
        analyse(self.config)
        self.display()
        self.paint()

    def display(self):
        covTable = self.covTable
        covTable.clearContents()
        covTable.setRowCount(0)
        for entry in self.config['table']:
            rowPosition = covTable.rowCount()
            covTable.insertRow(rowPosition)
            covTable.setItem(rowPosition , 0, PercentWidgetItem(entry[0]))
            covTable.setItem(rowPosition , 1, QTableWidgetItem(entry[1]))
            covTable.setItem(rowPosition , 2, HexWidgetItem(entry[2]))
            covTable.setItem(rowPosition , 3, RatioWidgetItem(entry[3]))
            covTable.setItem(rowPosition , 4, centered_text(entry[4]))

    def setColor(self):
        self.config['color'] = QColorDialog.getColor().rgb()
        self.paint()

    def paint(self):
        core = cutter.core()
        highlighter = core.getBBHighlighter()
        if self.config['colorize']:
            for bb in self.config['bb_hits']:
                highlighter.highlight(bb, self.config['color'])
        else:
            for bb in self.config['bb_hits']:
                highlighter.clear(bb)

class CutterCovPlugin(cutter.CutterPlugin):
    name = "CutterCov"
    description = "Visualize DynamoRIOCov data into Cutter"
    version = "0.0.1"
    author = "oddcoder"

    def setupPlugin(self):
        pass

    def setupInterface(self, main):
        action = QAction("CutterCov", main)
        action.setCheckable(True)
        widget = MyDockWidget(main, action)
        main.addPluginDockWidget(widget, action)

def create_cutter_plugin():
    return CutterCovPlugin()
