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
from lib.chemicalGraph.molecule.ForceField import ForceField, NonBond
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes,AtomInfo
#=========================================================================

class Na(Molecule):
	_FORCE_FIELD = None
	ai = AtomInfo("NA", "NA", "NA",    1., 22.9898,  0.0, 1.0, ' ', "NA ", "NA", "A", 1)
	
	def __init__(self):
		Molecule.__init__(self, "Na")

		atr = AtomAttributes(Na.ai, [ 0.0 , 0.0, 0.0])
		self.add_atom(atr,[])

		#print NANOCAD_PDB_DIR + "/Solvents/THF.pdb" , NANOCAD_PDB_DIR + "/Solvents/THF.psf" 
		self.load(NANOCAD_PDB_DIR + "/Ions/Na.pdb" , NANOCAD_PDB_DIR + "/Ions/Na.psf")

		if Na._FORCE_FIELD == None: 
			Na._FORCE_FIELD = ForceField(self)
			Na._FORCE_FIELD.setNonBond("Na", -0.1153, NonBond._EPSILON)
			Na._FORCE_FIELD.setNonBond("Na", 2.275, NonBond._SIGMA)
			Na._FORCE_FIELD.setNonBond("Na", 1., NonBond._CHARGE)
		self.setForceField(Na._FORCE_FIELD )
		self.copyChargesToForceField()

#==========================================================================
if __name__ == '__main__':
	print("Probando Na")
	m = Na()
	print(m)
	m.writePSF("Na.psf")
	m.writePDB("Na.pdb")

