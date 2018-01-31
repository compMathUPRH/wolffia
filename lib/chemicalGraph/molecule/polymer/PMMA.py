# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, Carlos J.  Cortés Martínez, Frances  Martínez Miranda, 
    Radamés J.  Vega Alfaro, 
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
if __name__ == '__main__':
	sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')

from conf.Wolffia_conf import NANOCAD_FORCE_FIELDS
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.molecule.polymer.Homopolymer import Homopolymer
import math

#-----------------------------------------------------------------------------------


class PMMA(Homopolymer):
    BACKBONE_MONOMER_PDB = '/Polymers/PMMA/backbonePMMA.pdb'
    START_MONOMER_PDB    = '/Polymers/PMMA/startPMMA.pdb'
    END_MONOMER_PDB      = '/Polymers/PMMA/endPMMA.pdb'
    ONE_MONOMER_PDB      = '/Polymers/PMMA/onePMMA.pdb'

    BACKBONE_MONOMER_PSF = '/Polymers/PMMA/backbonePMMA.psf'
    START_MONOMER_PSF    = '/Polymers/PMMA/startPMMA.psf'
    END_MONOMER_PSF      = '/Polymers/PMMA/endPMMA.psf'
    ONE_MONOMER_PSF      = '/Polymers/PMMA/endPMMA.psf'

    IMAGE                = "/PMMA-chain.png"

    NUM_ATOMS_BACKBONE_MONOMER = 15
    NUM_ATOMS_START_MONOMER    = 16
    NUM_ATOMS_LAST_MONOMER     = 4
    DISPL                      = 3.7
    ANGLE                      = 3 * math.pi / 4

    def __init__(self,n):
		# initialize base class
		Homopolymer.__init__(self, n, "PMMA(" + str(n) +")")
		
		PMMA._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/PMMA.prm")
		
		self.setForceField(PMMA._FORCE_FIELD)
		self.copyChargesToForceField()
		
#==========================================================================
if __name__ == '__main__':
    print "Probando PMMA"
    m = PMMA(6)
    print m
    #m.writePDB("/home/wensy/invewstigacion/prueba/chito.pdb")
    #m.writePSF("/home/wensy/invewstigacion/prueba/chito.psf")

