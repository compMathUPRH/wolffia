# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, Carlos J.  Cortés Martínez, Frances  Martínez Miranda, 
    Radamés J.  Vega Alfaro, Wensy Cuadrado
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


sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')
from conf.Wolffia_conf import NANOCAD_FORCE_FIELDS
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.molecule.polymer.Homopolymer import Homopolymer
import math

#-----------------------------------------------------------------------------------

class Chitosan(Homopolymer):
	_FORCE_FIELD = None
	BACKBONE_MONOMER_PDB = '/Polymers/Chitosan/backboneChitosan.pdb'
	START_MONOMER_PDB    = '/Polymers/Chitosan/backboneChitosan.pdb'
	END_MONOMER_PDB      = '/Polymers/Chitosan/backboneChitosan.pdb'
	ONE_MONOMER_PDB      = '/Polymers/Chitosan/oneChitosan.pdb'
	
	BACKBONE_MONOMER_PSF = '/Polymers/Chitosan/backboneChitosan.psf'
	START_MONOMER_PSF    = '/Polymers/Chitosan/backboneChitosan.psf'
	END_MONOMER_PSF      = '/Polymers/Chitosan/backboneChitosan.psf'
	ONE_MONOMER_PSF      = '/Polymers/Chitosan/endChitosan.psf'
	
	IMAGE                = "/Chitosan.png"
	
	NUM_ATOMS_BACKBONE_MONOMER = 22
	NUM_ATOMS_START_MONOMER    = 22
	NUM_ATOMS_LAST_MONOMER     = 22
	END_ATOM                   = 10
	START_ATOM                 = 22
	DISPL                      = 6
	ANGLE                      = 0
	
	
	def __init__(self,n):
		global _FORCE_FIELD
		# initialize base class
		Homopolymer.__init__(self, n, "Chitosan(" + str(n) +")")
		
		if Chitosan._FORCE_FIELD == None: 
			Chitosan._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/Chitosan.prm")
		self.setForceField(Chitosan._FORCE_FIELD )
		self.copyChargesToForceField()


#==========================================================================
if __name__ == '__main__':
    print "Probando Chitosan"
    m = Chitosan(6)
    print m
    #m.writePDB("/home/wensy/invewstigacion/prueba/chito.pdb")
    #m.writePSF("/home/wensy/invewstigacion/prueba/chito.psf")

