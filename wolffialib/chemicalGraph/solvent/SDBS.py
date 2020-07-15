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

from wolffialib.chemicalGraph.Mixture import Mixture
from wolffialib.chemicalGraph.ForceField import ForceField
#=========================================================================

class SDBS(Mixture):
	_FORCE_FIELD_SDBS = None
	_FORCE_FIELD_NA  = None
	def __init__(self):
		Mixture.__init__(self, "SDBS")

		#print NANOCAD_PDB_DIR + "/Solvents/THF.pdb" , NANOCAD_PDB_DIR + "/Solvents/THF.psf" 
		self.load(NANOCAD_PDB_DIR + "/Surfactant/SDBS.pdb" , NANOCAD_PDB_DIR + "/Surfactant/SDBS.psf")

		#print "SDBS ff", _FORCE_FIELD._NONBONDED
		#print "SDBS a", NANOCAD_FORCE_FIELDS + "/SDBS.prm"
		p1, p2 = [self.getMolecule(p) for p in self.molecules()]
		if p1.order() == 1:
			p1.rename("NA")
			SDBS._FORCE_FIELD_NA = ForceField(p1, NANOCAD_FORCE_FIELDS + "/SDBS.prm")
			p1.setForceField(SDBS._FORCE_FIELD_NA )
			SDBS._FORCE_FIELD_SDBS = ForceField(p2, NANOCAD_FORCE_FIELDS + "/SDBS.prm")
			p2.setForceField(SDBS._FORCE_FIELD_SDBS )
		else:
			p2.rename("NA")
			SDBS._FORCE_FIELD_NA = ForceField(p2, NANOCAD_FORCE_FIELDS + "/SDBS.prm")
			p2.setForceField(SDBS._FORCE_FIELD_NA )
			SDBS._FORCE_FIELD_SDBS = ForceField(p1, NANOCAD_FORCE_FIELDS + "/SDBS.prm")
			p1.setForceField(SDBS._FORCE_FIELD_SDBS )
		
		p1.copyChargesToForceField()
		p2.copyChargesToForceField()

#==========================================================================
if __name__ == '__main__':
    print "Probando SBDS"
    m = SDBS()
    print m
    m.writePSF("SBDS.psf")
    m.writePDB("SBDS.pdb")