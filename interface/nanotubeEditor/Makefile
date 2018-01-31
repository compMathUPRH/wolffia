
VPATH = ../../conf ../../lib/molecules ../main

nanotubeEditor.py: ui_nanotubeEditor.py ui_nanotubeSaveDialog.py

ui_nanotubeEditor.py: nanotubeEditor.ui
	pyuic4 -o ui_nanotubeEditor.py nanotubeEditor.ui

ui_nanotubeSaveDialog.py: nanotubeSaveDialog.ui
	pyuic4 -o ui_nanotubeSaveDialog.py nanotubeSaveDialog.ui

clean:
	rm -f *.pyc *.py~ ui_*.py
