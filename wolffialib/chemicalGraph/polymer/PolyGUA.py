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
from wolffialib.chemicalGraph.ForceField import ForceField
from wolffialib.chemicalGraph.polymer.Homopolymer import Homopolymer
import math

#-------------------------------------------------------------------------------

#_FORCE_FIELD = ForceField("PolyGUA", NANOCAD_FORCE_FIELDS + "/PolyGUA.prm") # DONE

class  PolyGUA(Homopolymer):
    _FORCE_FIELD = None
    BACKBONE_MONOMER_PDB = '/Polymers/GUA/backbone_GUA.pdb' # DONE
    START_MONOMER_PDB    = '/Polymers/GUA/start_GUA.pdb'    # DONE
    END_MONOMER_PDB      = '/Polymers/GUA/end_GUA.pdb'      # DONE
    ONE_MONOMER_PDB      = '/Polymers/GUA/one_GUA.pdb'      # XXX: ONE_MONOMER_PDB for PolyGUA

    BACKBONE_MONOMER_PSF = '/Polymers/GUA/backbone_GUA.psf' # DONE
    START_MONOMER_PSF    = '/Polymers/GUA/start_GUA.psf'    # DONE
    END_MONOMER_PSF      = '/Polymers/GUA/end_GUA.psf'      # DONE
    ONE_MONOMER_PSF      = '/Polymers/GUA/one_GUA.psf'      # XXX: ONE_MONOMER_PSF for PolyGUA
	
    IMAGE                = "/PolyGUA.png"

    NUM_ATOMS_BACKBONE_MONOMER = 30
    NUM_ATOMS_START_MONOMER    = 32
    NUM_ATOMS_LAST_MONOMER     = 33
    DISPL                      = 6.0
    ANGLE                      = math.pi / 6.0

    def __init__(self,n):
        # initialize base class
        Homopolymer.__init__(self, n, "PolyGUA(" + str(n) +")")

        global _FORCE_FIELD
        #self.setForceField(_FORCE_FIELD)
        #self.copyChargesToForceField()
        if PolyGUA._FORCE_FIELD == None: 
           PolyGUA._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/PolyGUA.prm")
        self.setForceField(PolyGUA._FORCE_FIELD )
        self.copyChargesToForceField()

