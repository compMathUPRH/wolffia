
VPATH = ../../conf ../../lib/molecules ../main

diamondEditor.py: ui_diamondEditor.py ui_diamondSaveDialog.py

ui_diamondEditor.py: diamondEditor.ui
	pyuic5 -o ui_diamondEditor.py diamondEditor.ui

ui_diamondSaveDialog.py: diamondSaveDialog.ui
	pyuic5 -o ui_diamondSaveDialog.py diamondSaveDialog.ui

clean:
	rm -f *.pyc *.py~ ui_*.py
