
VPATH = ../../conf ../../lib/molecules ../main

CelluloseEditor.py: ui_celluloseEditor.py polymer_images_rc.py

ui_celluloseEditor.py: celluloseEditor.ui
	pyuic4 -o ui_celluloseEditor.py celluloseEditor.ui

polymer_images_rc.py: polymer_images.qrc
	pyrcc4 polymer_images.qrc -o polymer_images_rc.py

clean:
	rm -f *.pyc *.py~ ui_*.py
