
VPATH = ../../conf ../../lib/molecules ../main

paniEditor.py: ui_paniEditor.py ui_paniSaveDialog.py

ui_paniEditor.py: paniEditor.ui
	pyuic4 -o ui_paniEditor.py paniEditor.ui

ui_paniSaveDialog.py: paniSaveDialog.ui
	pyuic4 -o ui_paniSaveDialog.py paniSaveDialog.ui

clean:
	rm -f *.pyc *.py~ ui_*.py
