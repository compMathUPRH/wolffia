# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, 

    Computational Science Group, Department of Mathematics, 
    University of Puerto Rico at Humacao 
    <jse@math.uprh.edu>.

    (On last names: Most hispanic people, Puerto Ricans included, use two surnames; 
    one from the father and one from the mother.  We have separated first names from 
    surnames with two spaces.)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 3 as published by
    the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program (gpl.txt).  If not, see <http://www.gnu.org/licenses/>.

    Acknowledgements: The main funding source for this project has been provided
    by the UPR-Penn Partnership for Research and Education in Materials program, 
    USA National Science Foundation grant number DMR-0934195. 
"""
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../conf')
from conf.Wolffia_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS

from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes
#=========================================================================
_FORCE_FIELD = ForceField("H2O2", NANOCAD_FORCE_FIELDS + "/H2O2.prm")
class H2O2(Molecule):
	def __init__(self):
		Molecule.__init__(self, "H2O2")

		# print NANOCAD_PDB_DIR + "/Solvents/WATER.pdb" , NANOCAD_PDB_DIR + "/Solvents/WATER.psf" 
		#self.load(NANOCAD_PDB_DIR + "/Solvents/WATER.pdb" , NANOCAD_PDB_DIR + "/Solvents/WATER.psf")

		# build water H2O2
		atr = AtomAttributes("OT1", "O", "OT", [ -0.077,   0.000,   0.730 ], 0.834, 15.9994, 0.0, 1.0, ' ', "OT  ", "XXX", "A", 1)
		#print "----------------------->", str(atr)
		self.add_node(1, attrs=[atr])

		atr = AtomAttributes("OT2", "O", "OT", [  0.077,   0.000,  -0.730], 0.834, 15.9994, 0.0, 1.0, ' ', "OT  ", "XXX", "A", 1)
		#print "----------------------->", str(atr)
		self.add_node(2, attrs=[atr])

		atr = AtomAttributes("HT1", "H", "HT", [  -1.077,   0.000,   1.730], 0.417, 1.00794, 0.0, 1.0, ' ', "HT ", "XXX", "A", 1)
		#print "----------------------->", str(atr)
		self.add_node(3, attrs=[atr])

		atr = AtomAttributes("HT2", "H", "HT", [   1.077,   0.000,  -1.730], 0.417, 1.00794, 0.0, 1.0, ' ', "HT ", "XXX", "A", 1)
		#print "----------------------->", str(atr)
		self.add_node(4, attrs=[atr])

		self.addBond(1, 2)
		self.addBond(1, 3)
		self.addBond(2, 4)

		#self.add_angle(3,1,2)
		#self.add_angle(1,2,4)

		#self.add_dihedral(1,2,3,4)

		
		self.setForceField(_FORCE_FIELD )
		self.copyChargesToForceField()

#==========================================================================
if __name__ == '__main__':
	print("Probando H2O2")
	m = H2O2("H2O2 prueba" )
	print(m)
	for node in m:
		print(m.getAtomAttributes(node))
	m.writePSF("caca.psf")
	m.writePDB("caca.pdb")

