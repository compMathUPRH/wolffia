
VPATH = ../../conf ../../lib/molecules ../main

pedotEditor.py: ui_pedotEditor.py ui_pedotSaveDialog.py

ui_pedotEditor.py: pedotEditor.ui
	pyuic5 -o ui_pedotEditor.py pedotEditor.ui

ui_pedotSaveDialog.py: pedotSaveDialog.ui
	pyuic5 -o ui_pedotSaveDialog.py pedotSaveDialog.ui

clean:
	rm -f *.pyc *.py~ ui_*.py
