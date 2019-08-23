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
#print sys.path
from conf.Wolffia_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS

from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes, AtomInfo

#=========================================================================
class WATER(Molecule):
	_FORCE_FIELD = None
	otObj = AtomInfo("OT", "O", "OT", -0.834, 15.9994, 0.0, 1.0, ' ', "OT  ", "WAT", "A", 1)
	htObj = AtomInfo("HT1", "H", "HT", 0.417, 1.00794, 0.0, 1.0, ' ', "HT ", "WAT", "A", 1)
	def __init__(self):
		Molecule.__init__(self, "WATER")

		# print NANOCAD_PDB_DIR + "/Solvents/WATER.pdb" , NANOCAD_PDB_DIR + "/Solvents/WATER.psf" 
		#self.load(NANOCAD_PDB_DIR + "/Solvents/WATER.pdb" , NANOCAD_PDB_DIR + "/Solvents/WATER.psf")

		# build water molecule
		atr = AtomAttributes(WATER.otObj, [ 4.01300001,  0.83099997, -9.08300018])
		#print "----------------------->", str(atr)
		self.add_atom(atr,[])

		atr = AtomAttributes(WATER.htObj, [ 4.94099998,  0.84399998, -8.83699989])
		#print "----------------------->", str(atr)
		self.add_atom(atr,[1])

		atr = AtomAttributes(WATER.htObj, [ 3.75,       -0.068,      -9.29300022])
		#print "----------------------->", str(atr)
		self.add_atom(atr,[1])

		if WATER._FORCE_FIELD == None: 
			print("WATER generating FF")
			WATER._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/WATER.prm")
		#print "WATER1", WATER._FORCE_FIELD._BONDS
		self.setForceField(WATER._FORCE_FIELD )
		#print "WATER2", self.getForceField()._BONDS
		self.copyChargesToForceField()
		#print "WATER3", self.getForceField()._BONDS


#==========================================================================
if __name__ == '__main__':
	print("Probando WATER")
	m = WATER( )
	print(m)
	for node in m:
		print(m.getAtomAttributes(node))
	m.writePSF("caca.psf")
	m.writePDB("caca.pdb")

