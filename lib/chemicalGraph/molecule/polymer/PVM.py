# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva
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

from conf.Wolffia_conf import NANOCAD_FORCE_FIELDS
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.molecule.polymer.Homopolymer import Homopolymer
import math

#-----------------------------------------------------------------------------------

_FORCE_FIELD = ForceField("PVP", NANOCAD_FORCE_FIELDS + "/PVP.prm")

class PVP(Homopolymer):
    BACKBONE_MONOMER_PDB = '/Polymers/PVP/backbonePVP.pdb'
    START_MONOMER_PDB    = '/Polymers/PVP/startPVP.pdb'
    END_MONOMER_PDB      = '/Polymers/PVP/endPVP.pdb'
    ONE_MONOMER_PDB      = '/Polymers/PVP/onePVP.pdb'

    BACKBONE_MONOMER_PSF = '/Polymers/PVP/backbonePVP.psf'
    START_MONOMER_PSF    = '/Polymers/PVP/startPVP.psf'
    END_MONOMER_PSF      = '/Polymers/PVP/endPVP.psf'
    ONE_MONOMER_PSF      = '/Polymers/PVP/endPVP.psf'

    NUM_ATOMS_BACKBONE_MONOMER = 15
    NUM_ATOMS_START_MONOMER    = 16
    NUM_ATOMS_LAST_MONOMER     = 4
    STACK_INDEX                = 0
    DISPL                      = 3.7
    ANGLE                      = 3 * math.pi / 4

    def __init__(self,n):
        global _FORCE_FIELD
        # initialize base class
        Homopolymer.__init__(self, n, "PVP(" + str(n) +")")

        self.setForceField(_FORCE_FIELD)
        self.copyChargesToForceField()
