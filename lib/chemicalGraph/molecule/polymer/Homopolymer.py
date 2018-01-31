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
from lib.chemicalGraph.molecule.polymer.Polymer import Polymer


from networkx import draw
import math


class Homopolymer(Polymer):
	"""
	"""
	def __init__(self, numMonomers, molname=None):
		if type(self) == Homopolymer:
			raise Molecule.MoleculeError("Homopolymer is an abstract class.  Should not be directly instantiated.")

		try:
			self.MONOMERS_PDBS={'Ps':self.START_MONOMER_PDB,'P':self.BACKBONE_MONOMER_PDB,'Pe':self.END_MONOMER_PDB,'P1':self.ONE_MONOMER_PDB}
			self.MONOMERS_PSFS={'Ps':self.START_MONOMER_PSF, 'P':self.BACKBONE_MONOMER_PSF, 'Pe':self.END_MONOMER_PSF, 'P1':self.ONE_MONOMER_PSF}
		except AttributeError:  # if old style fails then try new style
			self.MONOMERS_MOLS={'Ps':self.START_MONOMER_MOL,'P':self.BACKBONE_MONOMER_MOL,'Pe':self.END_MONOMER_MOL,'P1':self.ONE_MONOMER_MOL}
	
		chain = ['Ps']
		for i in range(1,numMonomers-1):
			chain.append('P')
		chain.append('Pe')

		Polymer.__init__(self, chain, molname)
		if molname == None:
			self.rename(str( self.__class__)+str(numMonomers))

		return
	#============================================================================

