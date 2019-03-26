from PySide2.QtWidgets import QAction
import cutter

from .cutterplugin import MyDockWidget

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
    """
    This function is the only api accessed by cutter, it
    would return object of cutter.CutterPlugin for cutter to work with
    """
    return CutterCovPlugin()

