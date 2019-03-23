# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dock.ui',
# licensing of 'ui/dock.ui' applies.
#
# Created: Sat Mar 23 16:28:22 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(632, 455)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.dockWidgetContents)
        self.stackedWidget.setObjectName("stackedWidget")
        self.LoaderPage = QtWidgets.QWidget()
        self.LoaderPage.setObjectName("LoaderPage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.LoaderPage)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Loader = QtWidgets.QLabel(self.LoaderPage)
        self.Loader.setCursor(QtCore.Qt.PointingHandCursor)
        self.Loader.setStyleSheet("")
        self.Loader.setObjectName("Loader")
        self.gridLayout_2.addWidget(self.Loader, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.LoaderPage)
        self.CovTablePage = QtWidgets.QWidget()
        self.CovTablePage.setObjectName("CovTablePage")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.CovTablePage)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Close = QtWidgets.QToolButton(self.CovTablePage)
        self.Close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icon/x.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Close.setIcon(icon)
        self.Close.setObjectName("Close")
        self.gridLayout_3.addWidget(self.Close, 0, 0, 1, 1)
        self.Reload = QtWidgets.QToolButton(self.CovTablePage)
        self.Reload.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icon/reload.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Reload.setIcon(icon1)
        self.Reload.setObjectName("Reload")
        self.gridLayout_3.addWidget(self.Reload, 0, 1, 1, 1)
        self.SelectColor = QtWidgets.QToolButton(self.CovTablePage)
        self.SelectColor.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icon/brush.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SelectColor.setIcon(icon2)
        self.SelectColor.setObjectName("SelectColor")
        self.gridLayout_3.addWidget(self.SelectColor, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(487, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 3, 1, 1)
        self.CovTable = QtWidgets.QTableWidget(self.CovTablePage)
        self.CovTable.setObjectName("CovTable")
        self.CovTable.setColumnCount(5)
        self.CovTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.CovTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.CovTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.CovTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.CovTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.CovTable.setHorizontalHeaderItem(4, item)
        self.CovTable.horizontalHeader().setDefaultSectionSize(118)
        self.gridLayout_3.addWidget(self.CovTable, 1, 0, 1, 4)
        self.stackedWidget.addWidget(self.CovTablePage)
        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(QtWidgets.QApplication.translate("DockWidget", "Cutter DynamoRIO Coverage", None, -1))
        self.Loader.setText(QtWidgets.QApplication.translate("DockWidget", "<html><head/><body><p align=\"center\"><img src=\":/icons/icon/data-transfer-download.svg\"/></p><p align=\"center\">Click to <span style=\" font-weight:600;\">Open drcov file</span> or drag it here.</p></body></html>", None, -1))
        self.CovTable.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("DockWidget", "Coverage", None, -1))
        self.CovTable.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("DockWidget", "Function Name", None, -1))
        self.CovTable.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("DockWidget", "Address", None, -1))
        self.CovTable.horizontalHeaderItem(3).setText(QtWidgets.QApplication.translate("DockWidget", "Instructions Hits", None, -1))
        self.CovTable.horizontalHeaderItem(4).setText(QtWidgets.QApplication.translate("DockWidget", "Basic Block Hits", None, -1))

from . import icon_rc
