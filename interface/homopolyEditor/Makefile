
VPATH = ../../conf ../../lib/molecules ../main

HomopolyEditor.py: ui_homopolyEditor.py polymer_images_rc.py

ui_homopolyEditor.py: homopolyEditor.ui
	pyuic5 -o ui_homopolyEditor.py homopolyEditor.ui

polymer_images_rc.py: polymer_images.qrc
	pyrcc4 polymer_images.qrc -o polymer_images_rc.py

clean:
	rm -f *.pyc *.py~ ui_*.py
