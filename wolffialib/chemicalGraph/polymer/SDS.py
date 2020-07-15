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

from wolffialib.chemicalGraph.Molecule import Molecule
from wolffialib.chemicalGraph.ForceField import ForceField
from wolffialib.chemicalGraph.AtomAttributes import AtomAttributes
#=========================================================================
#_FORCE_FIELD = ForceField("THF", NANOCAD_FORCE_FIELDS + "/THF.prm")

class SDS(Molecule):
	def __init__(self):
		Molecule.__init__(self, "SDS")

		#print NANOCAD_PDB_DIR + "/Solvents/THF.pdb" , NANOCAD_PDB_DIR + "/Solvents/THF.psf" 
		self.load(NANOCAD_PDB_DIR + "/Surfactant/SDS.pdb" , NANOCAD_PDB_DIR + "/Surfactant/SDS.psf")


#==========================================================================
if __name__ == '__main__':
	print "Probando SDS"
	m = SDS()
	print m
	m.writePSF("SDS.psf")
	m.writePDB("SDS.pdb")

