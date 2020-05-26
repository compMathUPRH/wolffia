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


if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')
from conf.Wolffia_conf import WOLFFIA_WFY_DIR
from wollfialib.chemicalGraph.ForceField import ForceField
from wollfialib.chemicalGraph.Mixture import Mixture
from wollfialib.chemicalGraph.polymer.Polymer import Polymer
import math

#-----------------------------------------------------------------------------------


class PSS(Polymer):
	ALL_MONOMERS = Mixture()
	ALL_MONOMERS.loadWFM(WOLFFIA_WFY_DIR + "/PSS.wfm")
	
	'''
	BACKBONE_MONOMER_MOL = ALL_MONOMERS.getMolecule('PSS_1')
	START_MONOMER_MOL    = ALL_MONOMERS.getMolecule('PSS0_1')
	END_MONOMER_MOL      = ALL_MONOMERS.getMolecule('PSSF_1')
	ONE_MONOMER_MOL      = ALL_MONOMERS.getMolecule('PSS1_1')
	'''
	
	IMAGE                = "/PSS.png"
	
	MONOMERS_MOLS={	'Rs':ALL_MONOMERS.getMolecule('PSSs_1'),\
			'Rb':ALL_MONOMERS.getMolecule('PSS_1'),\
			'Re':ALL_MONOMERS.getMolecule('PSSe_1'),\
			'Os':ALL_MONOMERS.getMolecule('PSSns_1'),\
			'Ob':ALL_MONOMERS.getMolecule('PSSn_1'),\
			'Oe':ALL_MONOMERS.getMolecule('PSSne_1'),\
			'P1':ALL_MONOMERS.getMolecule('PSS1_1')}
	
	NUM_ATOMS_BACKBONE_MONOMER = MONOMERS_MOLS['Rb'].order()
	'''
	NUM_ATOMS_START_MONOMER    = MONOMERS_MOLS[].order()
	NUM_ATOMS_LAST_MONOMER     = MONOMERS_MOLS[].order()
	'''
	
	END_ATOM                   = 2  #!!!
	START_ATOM                 = 21
	DISPL                      = 1.0
	ANGLE                      = 3.14
	
	def __init__(self,n,m,numMonomers):
		# initialize base class
		assert(n >= 0 or m >= 0 or numMonomers > 0)
		molname = "PSS(" + str(n) + ", " + str(m) + ", " + str(numMonomers) + ")"
		
		if n == 0 and m == 0 and numMonomers == 1: # only one monomer
			#print "PSS ", self.MONOMERS_MOLS['P1'].bonds()
			chain = ['P1']
		else:
			baseChain = []
			for i in range(n):
				baseChain.append('Rb')
			for i in range(m):
				baseChain.append('Ob')
			for i in range(n):
				baseChain.append('Rb')
			
			chain = []
			for i in range(numMonomers):
				chain += baseChain
			if n > 0:
				chain[0] = 'Rs'
				chain[-1] = 'Re'
			else:
				chain[0] = 'Os'
				chain[-1] = 'Oe'
			
		#print "PSS ", chain
		Polymer.__init__(self, chain, molname)

		# add FF parameters for monomer junctions
		self.getForceField().setAngle(('C','C','C'), 60., 0)
		self.getForceField().setAngle(('C','C','C'), 109.47, 1)
		self.getForceField().setDihedral(('C','C','C','C'), 1.4, 0)
		self.getForceField().setDihedral(('C','C','C','C'), 3, 2)


#==========================================================================
if __name__ == '__main__':
    print "Probando PSS"
    m = PSS(2,2,3)
    #m = PSS.MONOMERS_MOLS['Oe']
    #print [m.getAtomAttributes(a) for a in m.atoms()]
    #m.writePDB("/home/wensy/invewstigacion/prueba/chito.pdb")
    #m.writePSF("/home/wensy/invewstigacion/prueba/chito.psf")

