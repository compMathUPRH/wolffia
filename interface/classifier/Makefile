
VPATH = ../../conf: ../../lib/chemicalGraph ../main

Load.py: Wolffia_conf.py ChemicalGraph.py MixtureViewer.py ui_Load.py History.py ImportMolecules.py AboutLoad.py

ui_Load.py: Load.ui
	pyuic5 Load.ui -o ui_Load.py

ImportMolecules.py: Wolffia_conf.py ui_ImportMolecules.py 

ui_ImportMolecules.py: ImportMolecules.ui
	pyuic5 ImportMolecules.ui -o ui_ImportMolecules.py

AboutLoad.py: Wolffia_conf.py ui_AboutLoad.py 

ui_AboutLoad.py: AboutLoad.ui
	pyuic5 AboutLoad.ui -o ui_AboutLoad.py


	
clean:
	rm -f *.pyc *.py~ ui_*.py


