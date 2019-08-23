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
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../conf')
from conf.Wolffia_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.Molecule import Molecule

from lib.chemicalGraph.molecule.polymer.Polymer import Polymer
import math

#-----------------------------------------------------------------------------------
_FORCE_FIELD = ForceField(None, NANOCAD_FORCE_FIELDS + "/PANI.prm")

class  PANI(Polymer):
   DISPL = 5.68
   ANGLE = 0


   MONOMERS_PDBS={	'Rs':'/Polymers/PANI/startPANIred.pdb',\
			'Rb':'/Polymers/PANI/backbonePANIred.pdb',\
			'Re': '/Polymers/PANI/endPANIred.pdb',\
			'Os':'/Polymers/PANI/startPANIoxi.pdb',\
			'Ob':'/Polymers/PANI/backbonePANIoxi.pdb',\
			'Oe':'/Polymers/PANI/endPANIoxi.pdb'}
   MONOMERS_PSFS={	'Rs':'/Polymers/PANI/startPANIred.psf',\
			'Rb':'/Polymers/PANI/backbonePANIred.psf',\
			'Re': '/Polymers/PANI/endPANIred.psf',\
			'Os':'/Polymers/PANI/startPANIoxi.psf',\
			'Ob':'/Polymers/PANI/backbonePANIoxi.psf',\
			'Oe': '/Polymers/PANI/endPANIoxi.psf'}


   def __init__(self,n,m,numMonomers):
	# initialize base class
	assert(n > 0 or m > 0)
	molname = "PANI(" + str(n) + ", " + str(m) + ")"

	baseChain = []
	for i in range(n):
		baseChain.append('Rb')
	for i in range(m):
		baseChain.append('Ob')

	chain = list(baseChain)
	if n > 0:
		chain[0] = 'Rs'
	else:
		chain[0] = 'Os'
	
	for i in range(1,numMonomers):
		chain += baseChain

	if m > 0:
		chain[-1] = 'Oe'
	else:
		chain[-1] = 'Re'

	Polymer.__init__(self, chain, molname)

        
	self.setForceField(_FORCE_FIELD )
	self.copyChargesToForceField()


#==========================================================================
if __name__ == '__main__':
	print("Probando PANI")
	m = PANI(1,1,4)
	print(m)
	m.writePDB("prueba.pdb")
	m.writePSF("prueba.psf")

