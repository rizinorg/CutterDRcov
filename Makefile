all:
	pyside2-uic ui/dock.ui --from-imports > autogen/dockui.py
	pyside2-rcc resources/icon.qrc > autogen/icon_rc.py
