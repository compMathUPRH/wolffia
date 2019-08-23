# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, Carlos J.  Cortés Martínez, Frances  Martínez Miranda, 
    Radamés J.  Vega Alfaro, Wensy
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

class Polystyrene(Homopolymer):
	_FORCE_FIELD = None
	BACKBONE_MONOMER_PDB = '/Polymers/Polystyrene/backbonePolystyrene.pdb'
	START_MONOMER_PDB    = '/Polymers/Polystyrene/startPolystyrene.pdb'
	END_MONOMER_PDB      = '/Polymers/Polystyrene/endPolystyrene.pdb'
	ONE_MONOMER_PDB      = '/Polymers/Polystyrene/onePolystyrene.pdb'
	
	BACKBONE_MONOMER_PSF = '/Polymers/Polystyrene/backbonePolystyrene.psf'
	START_MONOMER_PSF    = '/Polymers/Polystyrene/startPolystyrene.psf'
	END_MONOMER_PSF      = '/Polymers/Polystyrene/endPolystyrene.psf'
	ONE_MONOMER_PSF      = '/Polymers/Polystyrene/onePolystyrene.psf'
	
	IMAGE                = "/Polystyrene.png"
	
	NUM_ATOMS_BACKBONE_MONOMER = 16
	NUM_ATOMS_START_MONOMER    = 17
	NUM_ATOMS_LAST_MONOMER     = 17
	END_ATOM                   = 8
	START_ATOM                 = 7
	DISPL                      = 6
	ANGLE                      = 0
	
	
	def __init__(self,n):
		global _FORCE_FIELD
		# initialize base class
		Homopolymer.__init__(self, n, "Polystyrene(" + str(n) +")")
		
		if Polystyrene._FORCE_FIELD == None: 
			Polystyrene._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/Polystyrene.prm")
		self.setForceField(Polystyrene._FORCE_FIELD )
		self.copyChargesToForceField()


#==========================================================================
if __name__ == '__main__':
    print("Probando Polystyrene")
    m = Polystyrene(6)
    print(m)
    m.writePDB("/home/jse/Desktop/Polystyrene.pdb")
    m.writePSF("/home/jse/Desktop/Polystyrene.psf")

