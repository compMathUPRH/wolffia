# Tube.py
# -*- coding: utf-8 -*-
#
# Represents Hexagonal 2D allotropes (Bravais Primitive hexagonal)
#
# Author: José O. Sotero Esteva
#	Department of Mathematics, University of Puerto Rico at Humacao
#	Humacao, Puerto Rico
#	jse@math.uprh.edu
#


import math

from Molecule import *
from Hexagonal2D import Hexagonal2D

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
	def __init__(self,n,m,length, element="C", bondLength=1.4201, mass=12):
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
		tubePerimeter = sheet.getWidth()
		#print tubePerimeter

		radius = tubePerimeter / 2. / math.pi
		xToAngleFactor = 2. * math.pi / tubePerimeter

		atoms = sheet.atoms()
		for atom in atoms:
			attr = sheet.atom_attributes(atom)
			coords = attr.getCoord()
			angle = coords[0] * xToAngleFactor
			attr.setCoord([radius * math.cos(angle), radius * math.sin(angle), coords[2]])
			sheet.setAtomAttributes(atom, attr)

		# close tube

		incomplete = []
		for atom in atoms:
			if sheet.degree(atom) < 3:
				incomplete.append(atom)
		for atom1 in incomplete:
			for atom2 in incomplete:
				if atom1 != atom2 and not sheet.has_edge(atom1, atom2) and sheet.distance(atom1, atom2) < bondLength + self.EPSILON:
					sheet.addBond(atom1, atom2)
					print "sheet.addBond("
					
		# remove redundant atoms and bonds
		#for i in range(len(atoms)):
		#	for j in range(i+1,len(atoms)):
		#		if sheet.distance(atoms[i], atoms[j]) < self.EPSILON:
		#			print "caca",sheet.distance(atoms[i], atoms[j])
		#			sheet.removeAtom(atoms[i])
		#			break

		Molecule.__init__(self, element + "_Tube(" + str(n) + "," + str(n) + ")", sheet)

	#============================================================================
	class Dialog:
		"""
		Class fields: 
			_molecules
			_top
			_length
			_n
			_m
		"""
		def __init__(self, parent, molecules, classname):
			self.parent = parent
			self._top = top = Toplevel(parent)
			self._molecules = molecules
			#self._classname = classname
			
			Label(top, text="Tube specifications: ").grid(row=0,column=0, columnspan=4)
			
			Label(top, text="Length in angstroms: ").grid(row=1,column=0, columnspan=1)
			self._length = Entry(top)
			self._length.grid(row=1,column=1, columnspan=1)

			Label(top, text="Unit vectors indices: (").grid(row=2,column=0, columnspan=1)
			self._n = Entry(top)
			self._n.grid(row=2,column=1, columnspan=1)
			Label(top, text=" , ").grid(row=2,column=2, columnspan=1)
			self._m = Entry(top)
			self._m.grid(row=2,column=3, columnspan=1)
			Label(top, text=")").grid(row=2,column=4, columnspan=1)

			b = Button(top, text="OK", command=self.ok)
			b.grid(row=3,column=1, columnspan=1)
			Button(top, text="Cancel", command=self.cancel).grid(row=3,column=2, columnspan=1)

		def ok(self):
			#print "value is", self.Input.get()
			l = int(self._length.get())
			n = int(self._n.get())
			m = int(self._m.get())
			self._molecules.append(Tube(n,m,l))
			
			#turn on edit options
			#editObject.updateMenuEntires()
			
			self._top.destroy()

		def cancel(self):
			self._top.destroy()
				
if __name__ == "__main__":
	t = Tube(5,10, 50)
	t.writePDB()
