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
#print sys.path
from conf.Wolffia_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS

from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes

#=========================================================================
class Carbon(Molecule):
    _FORCE_FIELD = ForceField("Carbon", NANOCAD_FORCE_FIELDS + "/Carbon.prm")
    def __init__(self):
        Molecule.__init__(self, "C")

        atr = AtomAttributes("C", "C", "C", [ 0.0,  0.0, 0.0], 0.0, 39.9500, 0.0, 1.0, ' ', "C  ", "C", "C", 1)
        #print "----------------------->", str(atr)
        self.add_node(1, attrs=[atr])

        self.setForceField(self._FORCE_FIELD )
        self.copyChargesToForceField()
