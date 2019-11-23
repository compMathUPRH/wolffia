
VPATH = ../../conf ../../lib/molecules ../main

#grapheneEditor.py: ui_grapheneEditor.py ui_grapheneSaveDialog.py
coralsEditor.py: ui_coralsEditor.py ui_coralsSaveDialog.py

#ui_grapheneEditor.py: grapheneEditor.ui
#	pyuic4 -o ui_grapheneEditor.py grapheneEditor.ui
ui_coralsEditor.py: coralsEditor.ui
	pyuic4 -o ui_coralsEditor.py coralsEditor.ui

#ui_grapheneSaveDialog.py: grapheneSaveDialog.ui
#	pyuic4 -o ui_grapheneSaveDialog.py grapheneSaveDialog.ui
ui_coralsSaveDialog.py: coralsSaveDialog.ui
	pyuic4 -o ui_coralsSaveDialog.py coralsSaveDialog.ui

clean:
	rm -f *.pyc *.py~ ui_*.py
