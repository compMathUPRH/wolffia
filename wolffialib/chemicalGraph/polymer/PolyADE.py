# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Radamés J.  Vega Alfaro, 
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
from wollfialib.chemicalGraph.ForceField import ForceField
from wollfialib.chemicalGraph.polymer.Homopolymer import Homopolymer
import math

#-----------------------------------------------------------------------------------

#_FORCE_FIELD = ForceField("PolyADE", NANOCAD_FORCE_FIELDS + "/PolyADE.prm") # DONE

class  PolyADE(Homopolymer):
    _FORCE_FIELD = None
    BACKBONE_MONOMER_PDB = '/Polymers/ADE/backbone_ADE.pdb' # DONE
    START_MONOMER_PDB    = '/Polymers/ADE/start_ADE.pdb'    # DONE
    END_MONOMER_PDB      = '/Polymers/ADE/end_ADE.pdb'      # DONE
    ONE_MONOMER_PDB      = '/Polymers/ADE/one_ADE.pdb'      # XXX: ONE_MONOMER_PDB for PolyADE

    BACKBONE_MONOMER_PSF = '/Polymers/ADE/backbone_ADE.psf' # DONE
    START_MONOMER_PSF    = '/Polymers/ADE/start_ADE.psf'    # DONE
    END_MONOMER_PSF      = '/Polymers/ADE/end_ADE.psf'      # DONE
    ONE_MONOMER_PSF      = '/Polymers/ADE/one_ADE.psf'      # XXX: ONE_MONOMER_PSF for PolyADE

    IMAGE                = "/PolyADE.png"

    NUM_ATOMS_BACKBONE_MONOMER = 32
    NUM_ATOMS_START_MONOMER    = 30
    NUM_ATOMS_LAST_MONOMER     = 33
    DISPL                      = 6.0
    ANGLE                      = math.pi / 6.0

    def __init__(self,n):
        # initialize base class
        Homopolymer.__init__(self, n, "PolyADE(" + str(n) +")")

        global _FORCE_FIELD
        #self.setForceField(_FORCE_FIELD)
        #self.copyChargesToForceField()
        if PolyADE._FORCE_FIELD == None: 
            PolyADE._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/PolyADE.prm")
        self.setForceField(PolyADE._FORCE_FIELD )
        self.copyChargesToForceField()

