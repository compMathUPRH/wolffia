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
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes, AtomInfo
#=========================================================================

class THF(Molecule):
	_FORCE_FIELD = None
	atr1  = AtomInfo("C2", "C", "C2",-0.012, 14.0270, 0.0, 1.0, ' ', "CAA", "THF", "A", 1)
	atr2  = AtomInfo("HA", "H", "HA", 0.0,    1.0079, 0.0, 1.0, ' ', "HAA", "THF", "A", 1)
	atr3  = AtomInfo("HB", "H", "HB", 0.0,    1.0079, 0.0, 1.0, ' ', "HAB", "THF", "A", 1)
	atr4  = AtomInfo("C3", "C", "C3", 0.011, 14.0270, 0.0, 1.0, ' ', "CAE", "THF", "A", 1)
	atr5  = AtomInfo("HG", "H", "HG", 0.0,    1.0079, 0.0, 1.0, ' ', "HAG", "THF", "A", 1)
	atr6  = AtomInfo("HH", "H", "HH", 0.0,    1.0079, 0.0, 1.0, ' ', "HAH", "THF", "A", 1)
	atr7  = AtomInfo("C4", "C", "C4", 0.081, 14.0270, 0.0, 1.0, ' ', "CAD", "THF", "A", 1)
	atr8  = AtomInfo("HE", "H", "HE", 0.0,    1.0079, 0.0, 1.0, ' ', "HAE", "THF", "A", 1)
	atr9  = AtomInfo("HF", "H", "HF", 0.0,    1.0079, 0.0, 1.0, ' ', "HAF", "THF", "A", 1)
	atr10 = AtomInfo("O", "O", "O",  -0.139, 15.9994, 0.0, 1.0, ' ', "OAC", "THF", "A", 1)
	atr11 = AtomInfo("C1", "C", "C1", 0.081, 14.0270, 0.0, 1.0, ' ', "CAB", "THF", "A", 1)
	atr12 = AtomInfo("HD", "H", "HD", 0.0,    1.0079, 0.0, 1.0, ' ', "HAD", "THF", "A", 1)
	atr13 = AtomInfo("HC", "H", "HC", 0.0,    1.0079, 0.0, 1.0, ' ', "HAC", "THF", "A", 1)

	def __init__(self):
		Molecule.__init__(self, "THF")

		#print NANOCAD_PDB_DIR + "/Solvents/THF.pdb" , NANOCAD_PDB_DIR + "/Solvents/THF.psf" 
		#self.load(NANOCAD_PDB_DIR + "/Solvents/THF.pdb" , NANOCAD_PDB_DIR + "/Solvents/THF.psf")


		atr = AtomAttributes(THF.atr1, [0.180,  0.300, -2.690])
		self.add_atom(atr,[])
		atr = AtomAttributes(THF.atr2, [1.084,  0.909, -2.675])
		self.add_atom(atr,[1])
		atr = AtomAttributes(THF.atr3, [-0.637,  0.671, -3.309])
		self.add_atom(atr,[1])
		atr = AtomAttributes(THF.atr4, [-0.350,  0.030, -1.310])
		self.add_atom(atr,[1])
		atr = AtomAttributes(THF.atr5,[-1.282, -0.535, -1.328])
		self.add_atom(atr,[4])
		atr = AtomAttributes(THF.atr6, [-0.371,  0.969, -0.757])
		self.add_atom(atr,[4])
		atr = AtomAttributes(THF.atr7, [0.820, -0.800, -0.800])
		self.add_atom(atr,[4])
		atr = AtomAttributes(THF.atr8, [0.539, -1.361,  0.091])
		self.add_atom(atr,[7])
		atr = AtomAttributes(THF.atr9, [1.667, -0.126, -0.669])
		self.add_atom(atr,[7])
		atr = AtomAttributes(THF.atr10, [1.110, -1.690, -1.900])
		self.add_atom(atr,[7])
		atr = AtomAttributes(THF.atr11, [0.460, -1.140, -3.080])
		self.add_atom(atr,[1,10])
		atr = AtomAttributes(THF.atr12, [-0.501, -1.639, -3.207])
		self.add_atom(atr,[11])
		atr = AtomAttributes(THF.atr13, [1.120, -1.188, -3.946])
		self.add_atom(atr,[11])

		'''
		self.addBond(1,2)
		self.addBond(1,3)
		self.addBond(1,4)
		self.addBond(1,11)
		self.addBond(4,5)
		self.addBond(4,6)
		self.addBond(4,7)
		self.addBond(7,8)
		self.addBond(7,9)
		self.addBond(7,10)
		self.addBond(10,11)
		self.addBond(11,12)
		self.addBond(11,13)
		'''


		#self.add_angle()
		#self.add_angle()
		#self.add_angle()
		#self.add_angle()

		#self.add_dihedrals ()
		#self.add_dihedrals ()
		
		if THF._FORCE_FIELD == None: 
			THF._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/THF.prm")
		self.setForceField(THF._FORCE_FIELD )
		self.copyChargesToForceField()

#==========================================================================
if __name__ == '__main__':
	print("Probando THF")
	m = THF()
	print(m)
	m.writePSF("THF.psf")
	m.writePDB("THF.pdb")

