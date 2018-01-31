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

from lib.chemicalGraph.Mixture import Mixture
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes
#=========================================================================

class SDS(Mixture):
	_FORCE_FIELD_SDS = None
	_FORCE_FIELD_NA  = None
	def __init__(self):
		Mixture.__init__(self, "SDS")

		#print NANOCAD_PDB_DIR + "/Solvents/THF.pdb" , NANOCAD_PDB_DIR + "/Solvents/THF.psf" 
		self.load(NANOCAD_PDB_DIR + "/Surfactant/SDS.pdb" , NANOCAD_PDB_DIR + "/Surfactant/SDS.psf")

		#print "SDS ff", _FORCE_FIELD._NONBONDED
		#print "SDS a", NANOCAD_FORCE_FIELDS + "/SDS.prm"
		p1, p2 = [self.getMolecule(p) for p in self.molecules()]
		if p1.order() == 1:
			p1.rename("NA")
			SDS._FORCE_FIELD_NA = ForceField(p1, NANOCAD_FORCE_FIELDS + "/SDS.prm")
			p1.setForceField(SDS._FORCE_FIELD_NA )
			SDS._FORCE_FIELD_SDS = ForceField(p2, NANOCAD_FORCE_FIELDS + "/SDS.prm")
			p2.setForceField(SDS._FORCE_FIELD_SDS )
		else:
			p2.rename("NA")
			SDS._FORCE_FIELD_NA = ForceField(p2, NANOCAD_FORCE_FIELDS + "/SDS.prm")
			p2.setForceField(SDS._FORCE_FIELD_NA )
			SDS._FORCE_FIELD_SDS = ForceField(p1, NANOCAD_FORCE_FIELDS + "/SDS.prm")
			p1.setForceField(SDS._FORCE_FIELD_SDS )
		
		p1.copyChargesToForceField()
		p2.copyChargesToForceField()

#==========================================================================
if __name__ == '__main__':
	print "Probando SDS"
	m = SDS()
	print m
	m.writePSF("SDS.psf")
	m.writePDB("SDS.pdb")

