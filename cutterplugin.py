import cutter
from PySide2 import QtCore
from PySide2.QtWidgets import QAction, QFileDialog, QColorDialog
from cutterdrcov.autogen import Ui_DockWidget
from cutterdrcov.drcov import DCov_load
from cutterdrcov.covTable import *

class MyDockWidget(cutter.CutterDockWidget, Ui_DockWidget):
    def __init__(self, parent, action):
        super(MyDockWidget, self).__init__(parent, action)
        self.config = {'color': 0x800000}
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.loader.dragEnterEvent = self.loaderDragEnterEvent
        self.loader.dropEvent = self.dropFile
        self.loader.mousePressEvent = self.openFile
        self.selectColor.clicked.connect(self.setColor)
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
        self.loadcov(fileName[0])

    def loadcov(self, file_name):
        modules, bbs = DCov_load(file_name)
        self.config['modules'] = modules
        self.config['bbs'] = bbs
        self.stackedWidget.setCurrentIndex(1)
        analyse(self.config)
        self.display()

    def display(self):
        covTable = self.covTable
        covTable.clear()
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
