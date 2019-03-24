all:
	pyside2-uic ui/dock.ui --from-imports > cutterDRcovPlugin/autogen/dockui.py
	pyside2-rcc resources/icon.qrc > cutterDRcovPlugin/autogen/icon_rc.py
