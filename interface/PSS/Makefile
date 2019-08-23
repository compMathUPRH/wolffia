
VPATH = ../../conf ../../lib/molecules ../main

pssEditor.py: ui_pssEditor.py 

ui_pssEditor.py: pssEditor.ui
	pyuic5 -o ui_pssEditor.py pssEditor.ui

ui_pssSaveDialog.py: pssSaveDialog.ui
	pyuic5 -o ui_pssSaveDialog.py pssSaveDialog.ui

clean:
	rm -f *.pyc *.py~ ui_*.py
