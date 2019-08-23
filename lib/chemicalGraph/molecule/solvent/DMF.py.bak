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
if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')
from conf.Wolffia_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS

from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes, AtomInfo
#=========================================================================

class DMF(Molecule):
	_FORCE_FIELD = None
	ai1 = AtomInfo("N1", "N", "N1",  0.509, 14.0067, 0.0, 1.0, ' ', "N1  ", "XXX", "A", 1)
	ai2 = AtomInfo("C1", "C", "C1",  0.509, 12.011, 0.0, 1.0, ' ', "C1  ", "XXX", "A", 1)
	ai3 = AtomInfo("O1", "O", "O1", -0.514, 15.9994, 0.0, 1.0, ' ', "O1  ", "XXX", "A", 1)
	ai4 = AtomInfo("C2", "C", "C2",  0.509, 12.011, 0.0, 1.0, ' ', "C2  ", "XXX", "A", 1)
	ai5 = AtomInfo("C3", "C", "C3",  0.509, 12.011, 0.0, 1.0, ' ', "C3  ", "XXX", "A", 1)
	ai6 = AtomInfo("H1", "H", "H1",  1.0, 1.0079, 0.0, 1.0, ' ', "H1  ", "XXX", "A", 1)
	ai7 = AtomInfo("H2", "H", "H2",  1.0, 1.0079, 0.0, 1.0, ' ', "H2  ", "XXX", "A", 1)
	ai8 = AtomInfo("H3", "H", "H3",  1.0, 1.0079, 0.0, 1.0, ' ', "H3  ", "XXX", "A", 1)
	ai9 = AtomInfo("H4", "H", "H4",  1.0, 1.0079, 0.0, 1.0, ' ', "H4  ", "XXX", "A", 1)
	ai10 = AtomInfo("H5", "H", "H5", 1.0, 1.0079, 0.0, 1.0, ' ', "H5  ", "XXX", "A", 1)
	ai11 = AtomInfo("H6", "H", "H6", 1.0, 1.0079, 0.0, 1.0, ' ', "H6  ", "XXX", "A", 1)
	ai12 = AtomInfo("H7", "H", "H7", 1.0, 1.0079, 0.0, 1.0, ' ', "H7  ", "XXX", "A", 1)
   	def __init__(self):
		Molecule.__init__(self, "DMF")
		
		#print NANOCAD_PDB_DIR + "/Solvents/DMF.pdb" , NANOCAD_PDB_DIR + "/Solvents/DMF.psf" 
		#self.load(NANOCAD_PDB_DIR + "/Solvents/DMF.pdb" , NANOCAD_PDB_DIR + "/Solvents/DMF.psf")
		
		atr = AtomAttributes(DMF.ai1, [ 0.045 ,     -0.12800001,  0.038     ])
		self.add_atom(atr,[])
		atr = AtomAttributes(DMF.ai2, [-0.38    ,    1.09099996 ,-0.31900001])
		self.add_atom(atr,[1])
		atr = AtomAttributes(DMF.ai3, [ 0.45500001 , 2.171   ,   -0.19499999])
		self.add_atom(atr,[2])
		atr = AtomAttributes(DMF.ai4, [ 1.38699996, -0.30599999 , 0.55500001])
		self.add_atom(atr,[1])
		atr = AtomAttributes(DMF.ai5, [-0.838      ,-1.26999998, -0.094     ])
		self.add_atom(atr,[1])
		atr = AtomAttributes(DMF.ai6, [-1.38    ,    1.22399998, -0.70499998])
		self.add_atom(atr,[2])
		atr = AtomAttributes(DMF.ai7, [ 1.37600005, -0.192    ,   1.63900006])
		self.add_atom(atr,[4])
		atr = AtomAttributes(DMF.ai8, [ 2.04699993 , 0.442    ,   0.117     ])
		self.add_atom(atr,[4])
		atr = AtomAttributes(DMF.ai9, [ 1.74600005, -1.30299997,  0.29800001])
		self.add_atom(atr,[4])
		atr = AtomAttributes(DMF.ai10, [-1.12800002, -1.38699996, -1.13800001])
		self.add_atom(atr,[5])
		atr = AtomAttributes(DMF.ai11, [-1.72899997 ,-1.11199999 , 0.51499999])
		self.add_atom(atr,[5])
		atr = AtomAttributes(DMF.ai12, [-0.322,      -2.16899991 , 0.243     ])
		self.add_atom(atr,[5])
		
		if DMF._FORCE_FIELD == None: 
			DMF._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/DMF.prm")
		self.setForceField(DMF._FORCE_FIELD )
		self.copyChargesToForceField()

#==========================================================================
if __name__ == '__main__':
	print "Probando DMF"
	m = DMF()
	print m

