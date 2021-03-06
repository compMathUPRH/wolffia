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
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS

from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes, AtomInfo
#=========================================================================

class CLF4(Molecule):
	_FORCE_FIELD = None
	ai1 = AtomInfo("CH", "C", "CH",    0.42, 12.0107,  0.0, 1.0, ' ', "C24 ", "CLF", "A", 1)
	#ai1 = AtomInfo("CH", "C", "CH",    0.2659, 12.0107,  0.0, 1.0, ' ', "C24 ", "CLF", "A", 1)
	ai2 = AtomInfo("CL1", "CL", "CL", -0.14, 35.453,   0.0, 1.0, ' ', "CL1 ", "CLF", "A", 1)
	ai3 = AtomInfo("CL2", "CL", "CL", -0.14, 35.453,   0.0, 1.0, ' ', "CL2 ", "CLF", "A", 1)
	ai4 = AtomInfo("CL3", "CL", "CL", -0.14, 35.453,   0.0, 1.0, ' ', "CL3 ", "CLF", "A", 1)
	#ai4 = AtomInfo("CL3", "CL", "CL", 0.0396, 35.453,   0.0, 1.0, ' ', "CL3 ", "CLF", "A", 1)

	def __init__(self):
		Molecule.__init__(self, "CLF4")


		atr = AtomAttributes(CLF4.ai1, [ 0.,  0.,  0.])
		self.add_atom(atr,[])
		atr = AtomAttributes(CLF4.ai2, [ 0.58099997, -1.07599998, -1.27499998])
		self.add_atom(atr,[1])
		atr = AtomAttributes(CLF4.ai3, [ 1.29900002,  0.29100001,  1.16199994])
		self.add_atom(atr,[1])
		atr = AtomAttributes(CLF4.ai4, [-0.509,       1.53499997, -0.71100003])
		self.add_atom(atr,[1])


		
		if CLF4._FORCE_FIELD == None: 
			CLF4._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/CLF4.prm")
		self.setForceField(CLF4._FORCE_FIELD )
		self.copyChargesToForceField()

