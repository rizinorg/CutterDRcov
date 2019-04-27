from PySide2 import QtCore
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QFileDialog, QColorDialog
import cutter
from .autogen import Ui_DockWidget
from . import drcov
from .covtable import analyse
from . import sortable_table_item as sit

class MyDockWidget(cutter.CutterDockWidget, Ui_DockWidget):
    def __init__(self, parent, action):
        super(MyDockWidget, self).__init__(parent, action)
        self.setupUi(self)
        self.new_config()
        self.stackedWidget.setCurrentIndex(0)
        self.loader.dragEnterEvent = self.loader_drag_event
        self.loader.dropEvent = self.drop_file
        self.loader.mousePressEvent = self.open_file
        self.colorize.clicked.connect(self.toggle_colorize)
        self.selectColor.clicked.connect(self.set_color)
        self.close.clicked.connect(self.close_callback)
        self.reload.clicked.connect(self.reload_callback)
        self.covtable.doubleClicked.connect(self.seek)

    def seek(self, idx):
        row = idx.row()
        addr = int(self.covtable.item(row, 2).text(), 16)
        cutter.core().seek(addr)

    def toggle_colorize(self):
        self.config['colorize'] = not self.config['colorize']
        self.paint()

    def close_callback(self):
        self.clear_highlight()
        self.new_config()
        self.stackedWidget.setCurrentIndex(0)

    def reload_callback(self):
        self.clear_highlight()
        analyse(self.config)
        self.paint()

    def new_config(self):
        self.config = {
            'color': 0x800000,
            'colorize' : self.colorize.isChecked()
            }

    def loader_drag_event(self, event):
        if event.mimeData().hasUrls():
            self.loader.setCursor(QtCore.Qt.DragMoveCursor)
            event.acceptProposedAction()

    def drop_file(self, event):
        self.loader.setCursor(QtCore.Qt.PointingHandCursor)
        files = event.mimeData().urls()
        file_name = files[0].toLocalFile()
        self.loadcov(file_name)

    def open_file(self, _):
        file_name = QFileDialog.getOpenFileName(self)
        if not file_name[0]:
            return
        self.loadcov(file_name[0])

    def loadcov(self, file_name):
        try:
            modules, bbs = drcov.load(file_name)
        except Exception:
            self.parent().messageBoxWarning("", "Invalid Coverage File")
            return
        self.config['modules'] = modules
        self.config['bbs'] = bbs
        self.stackedWidget.setCurrentIndex(1)
        analyse(self.config)
        self.display()
        self.paint()

    def display(self):
        """
        This function displays analysed coverage entires (1 entry per function)
        """
        covtable = self.covtable
        covtable.clearContents()
        covtable.setRowCount(0)
        for entry in self.config['table']:
            row_position = covtable.rowCount()
            covtable.insertRow(row_position)
            covtable.setItem(row_position, 0, sit.PercentWidgetItem(entry[0]))
            covtable.setItem(row_position, 1, sit.QTableWidgetItem(entry[1]))
            covtable.setItem(row_position, 2, sit.HexWidgetItem(entry[2]))
            covtable.setItem(row_position, 3, sit.RatioWidgetItem(entry[3]))
            covtable.setItem(row_position, 4, sit.centered_text(entry[4]))

    def set_color(self):
        """
        This function changes color of drcoved bbs and reflects
        the change to gui.
        """
        new_color = QColorDialog.getColor(QColor(self.config['color']))
        if not new_color.isValid():
            return
        self.config['color'] = new_color.rgb()
        self.paint()

    def paint(self):
        """
        This function checks if we are allowed to highlight basic block,
        if yes it will highlight all drcov-ed basic blocks, otherwise it
        will clear remove highlights from all drcov-ed bbs.
        """
        if self.config['colorize']:
            self.highlight()
        else:
            self.clear_highlight()

    def highlight(self):
        """
        This function highlights all drcov-ed basic blocks
        """
        core = cutter.core()
        highlighter = core.getBBHighlighter()
        for bblock in self.config['bb_hits']:
            highlighter.highlight(bblock, self.config['color'])

    def clear_highlight(self):
        """
        This function removes highlights from all drcov-ed basic blocks
        """
        core = cutter.core()
        highlighter = core.getBBHighlighter()
        for bblock in self.config['bb_hits']:
            highlighter.clear(bblock)
