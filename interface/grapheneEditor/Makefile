
VPATH = ../../conf ../../lib/molecules ../main

grapheneEditor.py: ui_grapheneEditor.py ui_grapheneSaveDialog.py

ui_grapheneEditor.py: grapheneEditor.ui
	pyuic4 -o ui_grapheneEditor.py grapheneEditor.ui

ui_grapheneSaveDialog.py: grapheneSaveDialog.ui
	pyuic4 -o ui_grapheneSaveDialog.py grapheneSaveDialog.ui

clean:
	rm -f *.pyc *.py~ ui_*.py
