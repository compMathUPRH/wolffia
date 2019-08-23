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
from lib.chemicalGraph.molecule.ForceField import ForceField, NonBond
from lib.chemicalGraph.Mixture import Mixture
from lib.chemicalGraph.molecule.polymer.Polymer import Polymer
import math

#-----------------------------------------------------------------------------------


class PEDOT(Polymer):
	ALL_MONOMERS = Mixture()
	ALL_MONOMERS.loadWFM(WOLFFIA_WFY_DIR + "/PEDOT.wfm")
	#print allMonomers.molecules()
	
	BACKBONE_MONOMER_MOL = ALL_MONOMERS.getMolecule('PEDOT_1')
	START_MONOMER_MOL    = ALL_MONOMERS.getMolecule('PEDOT0_1')
	END_MONOMER_MOL      = ALL_MONOMERS.getMolecule('PEDOTF_1')
	ONE_MONOMER_MOL      = ALL_MONOMERS.getMolecule('PEDOT1_1')
	
	IMAGE                = "/PEDOT.png"
	
	NUM_ATOMS_BACKBONE_MONOMER = BACKBONE_MONOMER_MOL.order()
	NUM_ATOMS_START_MONOMER    = START_MONOMER_MOL.order()
	NUM_ATOMS_LAST_MONOMER     = END_MONOMER_MOL.order()
	
	END_ATOM                   = 2  #!!!
	START_ATOM                 = 21
	DISPL                      = 3
	ANGLE                      = 3.14
	
	MONOMERS_MOLS={	'Rs':ALL_MONOMERS.getMolecule('PEDOT0_1'),\
			'Rb':ALL_MONOMERS.getMolecule('PEDOT_1'),\
			'Re':ALL_MONOMERS.getMolecule('PEDOTF_1'),\
			'Os':ALL_MONOMERS.getMolecule('PEDOTp0_1'),\
			'Ob':ALL_MONOMERS.getMolecule('PEDOTp_1'),\
			'Oe':ALL_MONOMERS.getMolecule('PEDOTpF_1'),\
			'P1':ALL_MONOMERS.getMolecule('PEDOT1_1')}
	
	def __init__(self,n,m,numMonomers):
		# initialize base class
		assert(n > 0 or m > 0)
		molname = "PEDOT(" + str(n) + ", " + str(m) + ", " + str(numMonomers) + ")"
		
		baseChain = []
		for i in range(n):
			baseChain.append('Rb')
		for i in range(m):
			baseChain.append('Ob')
		#for i in range(n):
		#	baseChain.append('Rb')
		
		chain = []
		for i in range(numMonomers):
			chain += baseChain
		if n > 0:
			chain[0] = 'Rs'
			chain[-1] = 'Re'
		else:
			chain[0] = 'Os'
			chain[-1] = 'Oe'
		
		Polymer.__init__(self, chain, molname)

		# add FF parameters for monomer junctions
		self.getForceField().setBond(('C','C'),  305., NonBond._EPSILON)
		self.getForceField().setBond(('C','C'),  1.3750,  NonBond._SIGMA)
		self.getForceField().setBond(('C','C3'),  222.500, NonBond._EPSILON)
		self.getForceField().setBond(('C','C3'),  1.5300,  NonBond._SIGMA)
		self.getForceField().setBond(('C3','C3'), 305.000, NonBond._EPSILON)
		self.getForceField().setBond(('C3','C3'), 1.3750,  NonBond._SIGMA)

		self.getForceField().setAngle(('C','C3','S1'),  40.,  0)
		self.getForceField().setAngle(('C','C3','S1'), 120.,  1)
		self.getForceField().setAngle(('C','C3','C4'),  45.8, 0)
		self.getForceField().setAngle(('C','C3','C4'), 120.,  1)

		self.getForceField().setAngle(('C3','C4','C4'),  51.8, 0)
		self.getForceField().setAngle(('C3','C4','C4'), 107.5, 1)
		self.getForceField().setAngle(('C3','C3','S1'),  40.,  0)
		self.getForceField().setAngle(('C3','C3','S1'), 120.,  1)
		self.getForceField().setAngle(('C3','C3','C4'),  45.8, 0)
		self.getForceField().setAngle(('C3','C3','C4'), 120.,  1)

		self.getForceField().setDihedral(('C','C3','S1','C3'), 1.75, 0)
		self.getForceField().setDihedral(('C','C3','S1','C3'), 2,    1)
		self.getForceField().setDihedral(('C','C3','S1','C3'), 180,  2)
		self.getForceField().setDihedral(('C3','S1','C3','C'), 1.75, 0)
		self.getForceField().setDihedral(('C3','S1','C3','C'), 2,    1)
		self.getForceField().setDihedral(('C3','S1','C3','C'), 180,  2)

		self.getForceField().setDihedral(('C3','C3','S1','C3'), 1.75, 0)
		self.getForceField().setDihedral(('C3','C3','S1','C3'), 2,    1)
		self.getForceField().setDihedral(('C3','C3','S1','C3'), 180,  2)
		self.getForceField().setDihedral(('C3','S1','C3','C3'), 1.75, 0)
		self.getForceField().setDihedral(('C3','S1','C3','C3'), 2,    1)
		self.getForceField().setDihedral(('C3','S1','C3','C3'), 180,  2)


#==========================================================================
if __name__ == '__main__':
    print("Probando PEDOT")
    m = PEDOT(2,2,2)
    print(m)
    #m.writePDB("/home/wensy/invewstigacion/prueba/chito.pdb")
    #m.writePSF("/home/wensy/invewstigacion/prueba/chito.psf")

