
VPATH = ../../../conf

all: AtomAttributes.py BuildCstruct.py ChemicalGraph.py CLF.py CNT.py DMF.py ForceField.py Graphene.py Hexagonal2D.py Homopolymer.py MDControl_molecules_conf.py Mixture.py Molecule.py PMMA.py PolyCYT.py Polymer.py PSF.py SolventBox.py THF.py Tube.py WATER.py

ChemicalGraph.py: AtomAttributes.py PSF.py

CLF.py: Molecule.py ForceField.py NanoCAD_conf.py

DMF.py: Molecule.py NanoCAD_conf.py

Graphene.py: Hexagonal2D.py

Hexagonal2D.py: Molecule.py

Homopolymer.py: Polymer.py

MDControl_molecules_conf.py: PMMA.py Graphene.py Tube.py

Mixture.py: ChemicalGraph.py AtomAttributes.py Molecule.py PSF.py

Molecule.py: ChemicalGraph.py Mixture.py AtomAttributes.py

PMMA.py: Homopolymer.py

PolyCYT.py: Homopolymer.py

Polymer.py: Molecule.py NanoCAD_conf.py

THF.py: Molecule.py NanoCAD_conf.py

Tube.py: Molecule.py Hexagonal2D.py

WATER.py: Molecule.py ForceField.py NanoCAD_conf.py


clean:
	rm -f *.pyc *.py~ ui_*.py


