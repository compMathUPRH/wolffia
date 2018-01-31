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

import sys,os
if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')
from conf.Wolffia_conf import *

from lib.chemicalGraph.molecule.allotrope.Hexagonal2D import Hexagonal2D
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes
#==========================================================================================
class  Graphene(Hexagonal2D):
	_FORCE_FIELD = None
	def __init__(self,n,m,length):
		Hexagonal2D.__init__(self,n,m,length, element="C", bondLength=1.3350, mass=12.011)

		molname = "Graphene(" + str(n) + "," + str(n) + ")"

		if Graphene._FORCE_FIELD == None: 
			Graphene._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/CNT.prm")
		self.setForceField(Graphene._FORCE_FIELD )


#==========================================================================
if __name__ == '__main__':
	g = Graphene(20,20,40)
	g.writePDB()

