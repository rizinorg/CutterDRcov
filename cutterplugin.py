import cutter
from PySide2 import QtCore
from PySide2.QtWidgets import QAction, QFileDialog
from cutterdrcov.autogen import Ui_DockWidget
from cutterdrcov.drcov import DCov_load
from cutterdrcov.covTable import *

class MyDockWidget(cutter.CutterDockWidget, Ui_DockWidget):
    def __init__(self, parent, action):
        super(MyDockWidget, self).__init__(parent, action)
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.loader.dragEnterEvent = self.loaderDragEnterEvent
        self.loader.dropEvent = self.dropFile
        self.loader.setAcceptDrops(True)
        self.loader.mousePressEvent = self.openFile
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
        self.stackedWidget.setCurrentIndex(1)
        initCovTable(self.covTable, modules, bbs)
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
