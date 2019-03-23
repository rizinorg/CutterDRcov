import cutter
from PySide2.QtWidgets import QAction, QStackedWidget 
#from PySide2.QtCore import QFile
from cutterdrcov.autogen_ui import Ui_DockWidget
#from PySide2 import QtUiTools

class MyDockWidget(cutter.CutterDockWidget, Ui_DockWidget):
    def __init__(self, parent, action):
        super(MyDockWidget, self).__init__(parent, action)
        #self.setObjectName("MainWindow")
        self.setupUi(self)
        #ui_file = QFile("./cuttercov.ui")
        #ui_file.open(QFile.ReadOnly)
        #loader = QUiLoader()
        #self.window = Ui_Form()#loader.load(ui_file)
        #ui_file.close()
        #self.window.show()
        #layout = QVBoxLayout()
        #layout.addWidget(myWidget)
        #self.setLayout(layout)

        #self.ui = QtUiTools.QUiLoader().load("cuttercov.ui", self)
        
        #self.setObjectName("MyDockWidget")
        #self.setWindowTitle("My cool DockWidget")

        #label = QLabel(self)
        #self.setWidget(label)
        #label.setText("Hello mego")

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
#
