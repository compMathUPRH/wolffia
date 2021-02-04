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

from conf.Wolffia_conf import WOLFFIA_WFY_DIR
from wolffialib.chemicalGraph.Mixture import Mixture
from wolffialib.chemicalGraph.polymer.Polymer import Polymer

#-----------------------------------------------------------------------------------


class Cellulose(Polymer):
	ALL_MONOMERS = Mixture()
	ALL_MONOMERS.loadWFM(WOLFFIA_WFY_DIR + "/Cellulose.wfm")
	#print ALL_MONOMERS.molecules()
	#ALL_MONOMERS.writeFiles("celuloseTest")
    
    
	IMAGE                = "/Cellulose.png"
	
	MONOMERS_MOLS={	'Cs':ALL_MONOMERS.getMolecule('Cellulose_s_1'),\
			'C_a_b':ALL_MONOMERS.getMolecule('Cellulose_b_1'),\
			'C_a_e':ALL_MONOMERS.getMolecule('Cellulose_e_1'),\
			'C_a_1':ALL_MONOMERS.getMolecule('Cellulose_1_1'),\
			'C_a_s':ALL_MONOMERS.getMolecule('Cellulose_s_1'),\
			'C_b_s':ALL_MONOMERS.getMolecule('CelluloseB_s_1'),\
			'C_b_b':ALL_MONOMERS.getMolecule('CelluloseB_b_1'),\
			'C_b_e':ALL_MONOMERS.getMolecule('CelluloseB_e_1'),\
			'C_b_1':ALL_MONOMERS.getMolecule('CelluloseB_1_1')}
	
	#NUM_ATOMS_BACKBONE_MONOMER = MONOMERS_MOLS['C_a_b'].order()
	
	END_ATOM                   = 2  #!!!
	START_ATOM                 = 0
	DISPL                      = 10.4
	ANGLE                      = 0.
	
	def __init__(self,numMonomers,structure='b'):
		# initialize base class
		assert(numMonomers > 0)
		molname = "Cellulose_"+structure+"(" + str(numMonomers) + ")"
		
		if numMonomers == 1: # only one monomer
			#print "Cellulose ", self.MONOMERS_MOLS['P1'].bonds()
			chain = ['C_'+structure+'_1']
		else:
			chain = ['C_'+structure+'_s']
			for i in range(numMonomers-2):
				chain.append('C_'+structure+'_b')
			chain.append('C_'+structure+'_e')
			
		#print "Cellulose ", chain
		Polymer.__init__(self, chain, molname)
		self.structure = structure

		# add FF parameters for monomer junctions
		#self.getForceField().setAngle(('C','C','C'), 60., 0)
		#self.getForceField().setAngle(('C','C','C'), 109.47, 1)
		self.getForceField().setDihedral(('C100','O400','C400','C300'), 0.6, 0)
		self.getForceField().setDihedral(('C100','O400','C400','C300'), 1, 1)
		self.getForceField().setDihedral(('C100','O400','C400','C300'), 3.14, 2)
		
		for atom in self:
			self.getAtomAttributes(atom).getInfo().setResidue('CEL')


#==========================================================================
class CelluloseCrystal(Mixture):
	DISPL_100 = [8.0,0.0,4.0,3.0] # dx, dy, dz, dxz
	DISPL_010 = [7.3,0.0,4.0]
	DISPL_110 = [6.5,0.0,7.0]
    
	def __init__(self, n, nx, nz, chirality='100', structure='a'):
		"""
		Arguments:
		n:  number of monomers per chain
		nx: number of chains per plane
		nz: number of stacked planes
        chirality: one of '100', '110', '010'
        structure: one of 'a', 'b' for alpha and beta respectively
		"""
		super().__init__()


		#n = self.ui.nSpinBox.value()
		#nx = self.ui.horizontalSpinBox.value()
		#nz = self.ui.layersSpinBox.value()

		assert(chirality in ['100', '110', '010'])
		assert(structure in ['a', 'b'])
		#self.homopol = Mixture()
		from wolffialib.chemicalGraph.polymer.Cellulose import Cellulose
		
		if chirality == '100':
			for i in range(nx):
				for j in range(nz):
					# alpha or betha structure
					poly = Cellulose(n, structure)
					# locate the polymer chain			
					#self.poly.moveby([DISPL_100[0] * (i+(j%2)/2.), DISPL_100[1] * ((i+j)%2), DISPL_100[2] * j])
					poly.moveby([self.DISPL_100[0] * i + self.DISPL_100[3] * (j%2), self.DISPL_100[1] * (i%2), self.DISPL_100[2] * j])
					self.add(poly)
					
		if chirality == '110':
			for i in range(nx):
				for j in range(nz):
					# alpha or betha structure
					poly = Cellulose(n, structure)
					# locate the polymer chain	
					poly.rotateDeg(0., 45.0, 0.)	
					poly.moveby([self.DISPL_110[0] * i, self.DISPL_110[1] * ((i+j)%2), self.DISPL_110[2] * j])
					self.add(poly)	
					
		if chirality == '010': 
			for i in range(nx):
				for j in range(nz):
					# alpha or betha structure
					poly = Cellulose(n, structure)
					# locate the polymer chain	
					poly.rotateDeg(0., 0., 90.)	
					poly.moveby([self.DISPL_010[0] * (i+(j%2)/2.), self.DISPL_010[1] * ((i+j)%2), self.DISPL_010[2] * j])
					self.add(poly)

		#self.history.currentState().reset()
		#self.history.currentState().addMixture(self.homopol)
		#self.homopolPreview.update()


#==========================================================================
if __name__ == '__main__':
    #print "Probando Cellulose"
    m = Cellulose(7)
    #m = Cellulose.MONOMERS_MOLS['Oe']
    #print [m.getAtomAttributes(a) for a in m.atoms()]
    #m.writePDB("/home/wensy/invewstigacion/prueba/chito.pdb")
    #m.writePSF("/home/wensy/invewstigacion/prueba/chito.psf")
    
    mix = CelluloseCrystal(6,2,3)
