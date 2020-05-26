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
if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')

from wolffialib.chemicalGraph.Molecule import Molecule
from wolffialib.chemicalGraph.allotrope.Hexagonal2D import Hexagonal2D
from conf.Wolffia_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS
from wolffialib.chemicalGraph.ForceField import ForceField
from wolffialib.chemicalGraph.Molecule import Molecule
from wolffialib.chemicalGraph.AtomAttributes import AtomAttributes
import math
#==========================================================================================

class  Tube(Molecule):
	"""
	Class fields: 
		coords: lists of triples (xyz coordinates)
		_length: positive float (lenth ribbon)
		_n: positive integer (number of unit vectors, n=0 => zigzag)
		_m: positive integer (number of unit vectors, zigzag direction)
		_mass: positive float (defaults to carbon mass)
		_bondLength: positive float (defaults to bond length in graphene)
		_element: string (defaults to "C")
	"""
	_FORCE_FIELD = None
	def __init__(self,n,m,length, element="C", bondLength=1.421, mass=12.011):
		self.coords = []
		self._n = n
		self._m = m
		self._length = length
		self._mass = mass
		self._bondLength = bondLength
		self._element = element
		self.EPSILON = bondLength / 2.


		sheet = Hexagonal2D(n,m,length, element, bondLength, mass)
		unitVectLength = self._bondLength*math.sqrt(2.-2.*math.cos(2.*math.pi/3.))
		#tubePerimeter = unitVectLength * math.sqrt(n*n+m*m)
		tubePerimeter = sheet.getWidth() + self._bondLength
		#print tubePerimeter

		radius = tubePerimeter / 2. / math.pi
		xToAngleFactor = 2. * math.pi / tubePerimeter

		atoms = sheet.atoms()
		for atom in atoms:
			attr = sheet.getAtomAttributes(atom)
			coords = attr.getCoord()
			angle = coords[0] * xToAngleFactor
			attr.setCoord([radius * math.cos(angle), radius * math.sin(angle), coords[2]])
			sheet.setAtomAttributes(atom, attr)

		# close tube

		incomplete = []
		#print "degree:", 
		for atom in atoms:
			#print sheet.degree(atom),
			if sheet.degree(atom) < 3:
				incomplete.append(atom)
		for atom1 in incomplete:
			for atom2 in incomplete:
				if atom1 != atom2 and not sheet.has_edge(atom1, atom2) and sheet.distance(atom1, atom2) < bondLength + self.EPSILON:
					sheet.addBond(atom1, atom2)
					#print "sheet.addBond(",atom1,", ",atom2
					
		# remove redundant atoms and bonds
		#for i in range(len(atoms)):
		#	for j in range(i+1,len(atoms)):
		#		if sheet.distance(atoms[i], atoms[j]) < self.EPSILON:
		#			print "caca",sheet.distance(atoms[i], atoms[j])
		#			sheet.removeAtom(atoms[i])
		#			break
		molname = element + "_Tube(" + str(m) + "," + str(n) + ")"

		Molecule.__init__(self, molname, sheet)

		if Tube._FORCE_FIELD == None: 
			Tube._FORCE_FIELD = ForceField(self, NANOCAD_FORCE_FIELDS + "/CNT.prm")
		self.setForceField(Tube._FORCE_FIELD )


	#============================================================================
#==========================================================================
print(__name__)
if __name__ == '__main__':
	print("Probando Tube")
	m = Tube(10,10,20)
	print(m)
	m.writePDB("prueba.pdb")
	m.writePSF("prueba.psf")

