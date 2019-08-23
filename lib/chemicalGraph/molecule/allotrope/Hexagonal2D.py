# Hexagonal2D.py
# -*- coding: utf-8 -*-
#
# Represents Hexagonal 2D allotropes (Bravais Primitive hexagonal)
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
if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')
from conf.Wolffia_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS

import math

from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes, AtomInfo
from lib.chemicalGraph.molecule.Molecule import Molecule


class  Hexagonal2D(Molecule):
	"""
	Class fields: 
		coords: lists of triples (xyz coordinates)
		_length: positive float (lenth ribbon)
		_n: positive integer (number of unit vectors, n=0 => zigzag)
		_m: positive integer (number of unit vectors, zigzag direction)
		_mass: positive float (defaults to carbon mass)
		_bondLength: positive float (defaults to bond length in graphene)
		_element: string (defaults to "C")
		_ribbonWidth: float (actual width of the ribbon)
	"""

	def __init__(self,n,m,length, element="C", bondLength=1.421, mass=12.011):
		Molecule.__init__(self, element + "_hP4(" + str(n) + "," + str(n) + ")")

		self.coords = []
		self._n = n
		self._m = m
		self._length = length
		self._mass = mass
		self._bondLength = bondLength
		self._element = element
		self._ribbonWidth = 0.
		self.ai  = AtomInfo("C", self._element, "C", 0., self._mass, 'HP4')

		self.generateZigZag()
		self.rotateSheet()
		#self.removeLoneAtoms()
		self.recalculateDimensions()

	# ========================================================================================
	def recalculateDimensions(self):
		[bmin, bmax] = self.enclosingBox()
		self._length = bmax[2] - bmin[2]
		self._ribbonWidth = bmax[0] - bmin[0]

	# ========================================================================================
	def generateZigZag(self):
		unitVectLength = self._bondLength * math.sqrt(2.-2.*math.cos(2.*math.pi/3.))
		by             = math.sqrt(self._bondLength * self._bondLength - unitVectLength*unitVectLength/4)
		bondsArray     = list()
		Cx             = self._m * unitVectLength + math.cos(math.pi/3.) * self._n * unitVectLength
		Cy             = math.sin(math.pi/3.) * self._n * unitVectLength
		Cangle         = math.atan2(Cy, Cx)

		xMin           = -self._length * math.cos(Cangle)
		xMax           = Cx 
		zMax           = self._length + Cx 
		xsteps         = int((xMax - xMin) / unitVectLength) + 1
		zsteps         = int(zMax / unitVectLength) + 1

		# determine gap widths
		 
		# generate coordinates
		z = 0.
		for zi in range(zsteps):
			row1 = list()
			if zi % 2 == 0:
				x = xMin
			else:
				x = xMin + unitVectLength / 2.
			for xi in range(xsteps):
				row1.append([x,0.,z])
				x += unitVectLength

			row2 = list()
 			if zi % 2 == 0:
				x = xMin + unitVectLength / 2.
			else:
				x = xMin
			z += by
			for xi in range(xsteps):
				row2.append([x,0.,z])
				x += unitVectLength
			bondsArray.append([row1,row2])
			z += self._bondLength

		n = 1
		# first two rows
		for row in range(len(bondsArray)):
			coords = bondsArray[row][0]
			rowLength = xsteps
			for coord in coords:
				atr = AtomAttributes(self.ai, coord, 0., [])
				self.add_node(n, attrs=[atr])
				if row > 0:
					self.add_bond([n,n-rowLength])
				n += 1

			coords = bondsArray[row][1]
			rowLength = xsteps

			
			atr = AtomAttributes(self.ai, coords[0], 0., [])
			self.add_node(n, attrs=[atr])
			self.add_bond([n,n-rowLength])
			if row % 2 == 0:
				self.add_bond([n,n-rowLength+1])
			n += 1
			for coord in coords[1:-1]:
				atr = AtomAttributes(self.ai, coord, [])
				self.add_node(n, attrs=[atr])
				self.add_bond([n,n-rowLength])
				if row % 2 == 0:
					self.add_bond([n,n-rowLength+1])
				else:
					self.add_bond([n,n-rowLength-1])
				n += 1
			atr = AtomAttributes(self.ai, coords[-1], 0., [])
			self.add_node(n, attrs=[atr])
			self.add_bond([n,n-rowLength])
			if row % 2 == 1:
				self.add_bond([n,n-rowLength-1])
			n += 1
			
	# ========================================================================================
	def rotateSheet(self):
		unitVectLength = self._bondLength*math.sqrt(2.-2.*math.cos(2.*math.pi/3.))

		Cx = self._m * unitVectLength + math.cos(math.pi/3.) * self._n * unitVectLength
		Cy = math.sin(math.pi/3.) * self._n * unitVectLength
		Cangle = math.atan2(Cy, Cx)
		#print "rotateSheet", unitVectLength, Cx, Cy, Cangle

		self._ribbonWidth = math.sqrt(Cx*Cx+Cy*Cy)
		#print "self._ribbonWidth", self._ribbonWidth

		self.rotateRad(0., Cangle, 0.)

		atoms = list(self.atoms())
		toRemove = list()
		for atom in atoms:
			[x,y,z] = self.getAtomAttributes(atom).getCoord()
			if x < 0 or x > self._ribbonWidth or z < 0 or z > self._length:
				toRemove.append(atom)
		self.remove_nodes_from(toRemove)

	#============================================================================
	def removeLoneAtoms(self):
		atoms = self.atoms()
		for atom in atoms:
			if self.degree(atom) == 1:
				self.removeAtom(atom)

	#============================================================================
	def getWidth(self):
		return self._ribbonWidth


#==========================================================================
if __name__ == '__main__':
	print("Probando Hexagonal2D")
	m = Hexagonal2D(10,10,200)
	print(m)
	m.writePDB("prueba.pdb")
	m.writePSF("prueba.psf")

