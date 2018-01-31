# -*- coding: utf-8 -*-
"""
"""


#
# Authors: 
#	José O. Sotero Esteva
#	Frances Martínez
#
#	Department of Mathematics, University of Puerto Rico at Humacao
#	Humacao, Puerto Rico
#	jse@math.uprh.edu
#
#  Acknowledgements: The main funding source for this project has been provided
#  by the UPR-Penn Partnership for Research and Education in Materials program, 
#  USA National Science Foundation grant number DMR-0934195. 
#---------------------------------------------------------------------------

import sys

from ChemicalGraph import ChemicalGraph
import Mixture
from AtomAttributes import *


#=========================================================================
class  Molecule(ChemicalGraph):
	"""Represents a single molecule as a connected graph.
	"""
	_EPSILON_ = 0.001
	_FORCE_FIELD = None

	def __init__(self, ident, molecule=None):
		"""
		"""
		ChemicalGraph.__init__(self)
		self._name = ident
		
		if isinstance(molecule, Molecule):
			self.merge(molecule)
		elif isinstance(molecule, ChemicalGraph):  # atoms in ChemicalGraph cannot be assumed to be [1:N]
			# build inverse function
			nodes = molecule.nodes()
			newIndex = dict()
			for n in range(1,len(nodes)+1):
				newIndex[nodes[n-1]] = n
				self.add_node(n, molecule.node[nodes[n-1]])
			for edge in molecule.edges():
				try:  # avoids adding an edge twice
					self.add_edge([newIndex[edge[0]], newIndex[edge[1]]])
				except AdditionError:
					pass
		elif molecule != None:
			raise Molecule.MoleculeError("Molecule initialized with instance variable of a class "+ str(type(molecule)) + " that is not a subclass of ChemicalGraph")


	#-------------------------------------------------------------
	def load(self, pdbFile, psfFile):
		"""Loads and parses PDB coordinate file and PSF topology file containing a molecule.
		If the files contain more than one molecule, only one of them will be loaded.
		Erases the current molecule.

		@type  pdbFile: string
		@param pdbFile: PDB filename.

		@type  psfFile: string
		@param psfFile: PSF filename.
		"""

		# print "Loading "+pdbFile+ " into molecule " + self._name
		mix = Mixture.Mixture()
		mix.load(pdbFile, psfFile)
		mol = mix.getMolecule(mix.nodes()[0])
		print "    Loaded ====>",mol.node_attributes(mol.nodes()[0])
		for atom in mol.nodes():
			self.add_node(atom,attrs=mol.node_attributes(atom))

		for edge in mol.edges():
			self.add_edge(edge)

		if len(mix) > 1:
			raise self.MoleculeError('WARNING: Attempt to load more than one molecule into a Molecule instance from file "' + pdbFile + '".\n')
	#-------------------------------------------------------------
	def writePSF(self, psfFile=None, count=1):
		"""
		"""
		if psfFile==None:
			fd = sys.stdout
		else:
			if type(psfFile) == str:
				fd = open(psfFile, 'w')

		fd.write("PSF\n\n")
		fd.write("      01 !NTITLE\n")
		fd.write(" REMARKS Produced by MDControl\n\n")

		# write atoms list
		fd.write("%8d !NATOM\n" % (len(self.atoms())))
		for atom in self.atoms():
			atr = self.atom_attributes(atom)
			fd.write(atr.PSFline(count)+"\n")

		# write bonds
		bonds = self.bonds()
		nbonds = len(bonds)
		fd.write("\n%8d !NBOND: bonds\n" % (nbonds))
		for i in range(0, nbonds - nbonds % 4, 4):
			 fd.write("%8d%8d" % (bonds[i][0], bonds[i][1]))
			 fd.write("%8d%8d" % (bonds[i+1][0], bonds[i+1][1]))
			 fd.write("%8d%8d" % (bonds[i+2][0], bonds[i+2][1]))
			 fd.write("%8d%8d\n" % (bonds[i+3][0], bonds[i+3][1]))
		for i in range(nbonds - nbonds % 4, nbonds):
			fd.write("%8d%8d" % (bonds[i][0], bonds[i][1]))

		# write angles
		angles = self.angles()
		nangles = len(angles)
		fd.write("\n\n%8d !NTHETA: angles\n" % (nangles))
		for i in range(0, nangles - nangles % 3, 3):
			fd.write("%8d%8d%8d" % (angles[i][0], angles[i][1], angles[i][2]))
			fd.write("%8d%8d%8d" % (angles[i+1][0], angles[i+1][1], angles[i+1][2]))
			fd.write("%8d%8d%8d\n" % (angles[i+2][0], angles[i+2][1], angles[i+2][2]))
		for i in range(nangles - nangles % 3, nangles):
			fd.write("%8d%8d%8d\n" % (angles[i][0], angles[i][1], angles[i][2]))

		# write dihedrals
		ndihedrals = len(self._dihedrals)
		fd.write("\n\n%8d !NPHI: dihedrals\n" % (ndihedrals))
		for i in range(0, ndihedrals - ndihedrals % 2, 2):
			fd.write("%8d%8d%8d%8d" % (self._dihedrals[i][0], self._dihedrals[i][1], self._dihedrals[i][2], self._dihedrals[i][3]))
			fd.write("%8d%8d%8d%8d\n" % (self._dihedrals[i+1][0], self._dihedrals[i+1][1], self._dihedrals[i+1][2], self._dihedrals[i+1][3]))
		for i in range(ndihedrals - ndihedrals % 2, ndihedrals):
			fd.write("%8d%8d%8d%8d\n" % (self._dihedrals[i][0], self._dihedrals[i][1], self._dihedrals[i][2], self._dihedrals[i][3]))

		# write other stuff
		fd.write("\n\n%8d !NIMPHI: impropers\n" % (0))
		fd.write("\n\n%8d !NDON: donors\n" % (0))
		fd.write("\n\n%8d !NACC: acceptors\n" % (0))
		fd.write("\n\n%8d !NNB\n" % (0))
		fd.write("\n\n%8d !NGRP\n" % (0))

		if psfFile != None:
			fd.close()

	#-------------------------------------------------------------
	def __str__(self):
		"""
		"""
		return self._name + ": " + ChemicalGraph.__str__(self)


	#-------------------------------------------------------------
	def node_attributes(self, molname):
		"""
		"""
		return self.node[molname]['attrs']

	#-------------------------------------------------------------
	def molname(self):
		"""
		"""
		return self._name

	#-------------------------------------------------------------
	#def name(self):  ESTO PRODUCE ERRORES!!!!!!!!!!!!!!
	#	return self._name

	#-------------------------------------------------------------
	def atoms(self):
		"""Returns atoms.

		@rtype:  list of integers.
		@return: Atoms of the molecules.
		"""
		return self.nodes()

	#-------------------------------------------------------------
	def bonds(self):
		"""Returns bonds.

		@rtype:  list of integers.
		@return: Atoms of the molecules.
		"""
		return self.edges()

	#-------------------------------------------------------------
	def inferBonds(self, element1, element2, bondDistance):
		"""Adds bonds between pairs of elements of the specified types (element1, element2) that
		are at distance bondDistance +/- _EPSILON_

		@type	element1: string
		@param	element1: element name
		@type	element2: string
		@param	element2: element name
		"""
		atoms = self.atoms()
		for i in range(len(atoms)):
			if self.getAtomAttributes(atoms[i]).getElement() == element1:
				for j in range(i+1,len(atoms)):
					if self.getAtomAttributes(atoms[j]).getElement() == element2 and math.fabs(self.distance(atoms[i], atoms[j]) - bondDistance) < self._EPSILON_:
						self.addBond(atoms[i], atoms[j])
			if element1 != element2 and self.getAtomAttributes(atoms[i]).getElement() == element2:
				for j in range(i+1,len(atoms)):
					if self.getAtomAttributes(atoms[j]).getElement() == element1 and math.fabs(self.distance(atoms[i], atoms[j]) - bondDistance) < self._EPSILON_:
						self.addBond(atoms[i], atoms[j])

	#-------------------------------------------------------------
	def atom(self, i):
		"""
		"""
		return self.atoms()[i]

	#-------------------------------------------------------------
	def getForceField(self):
		"""
		"""
		return self.__class__._FORCE_FIELD

	#-------------------------------------------------------------
	def getAtomAttributes(self, atom):
		"""
		"""
		return self.node_attributes(atom)[0]

	#-------------------------------------------------------------
	def atom_attributes(self, atom):
		"""
		"""
		return self.node_attributes(atom)[0]

	#-------------------------------------------------------------
	def setAtomAttributes(self, atom,attr):
		"""
		"""
		self.node[atom]['attrs'] = [attr]

	#-------------------------------------------------------------
	def rename(self, name):
		"""
		"""
		self._name = name

	#-------------------------------------------------------------
	def add_atom(self, attr, neighbors):
		"""
		Adds a new atom.

		@type  attr: AtomAttributes.
		@param attr: Attributes os the atom.

		@type  neighbors: list of integers.
		@param neighbors: Neighbors to be added to atom.  The list must contain valid atoms in the existing molecule.
		"""
		assert(self.order() == 0 or len(neighbors) > 0)

		atom = self.order() + 1
		self.add_node(atom, [attr])
		for n in neighbors:
			self.add_edge((atom, n))

	#-------------------------------------------------------------
	def addBond(self, atom1, atom2):
		"""
		"""
		self.add_edge([atom1,atom2])

	#-------------------------------------------------------------
	def removeAtom(self, atom):
		"""
		"""
		self.remove_node(atom)

	#-------------------------------------------------------------
	def distance(self, atom1, atom2):
		"""
		"""
		return self.getAtomAttributes(atom1).distanceTo(self.getAtomAttributes(atom2))

	#-------------------------------------------------------------
	def merge(self, mol, bonds=[]):
		"""
		Merges mol into self.  Atom labels of mol are modified to avoid name collisions
		with existing atoms.

		@type  mol: Molecule.
		@param mol: Molecule to be merged into self.

		@type  bonds: list of pairs of integers.
		@param bonds: Bonds to be added between the two molecules to form a new molecule.  It must have at least one pair unless the molecule is empty.  For each pair, the first integer is an atom (int) of the first molecule and the second an atom of the second.
		"""
		assert(self.order() == 0 or len(bonds) > 0)
		ChemicalGraph.merge(self, mol, newBonds=bonds)
		
	#-------------------------------------------------------------
	def writePDB(self, pdbFile=None, count=1):
		"""
		"""
		if pdbFile==None:
			fd = sys.stdout
		else:
			if type(pdbFile) == str:
				fd = open(pdbFile, 'w')

		for atom in self.atoms():
			atr = self.atom_attributes(atom)
			fd.write(atr.PDBline(count)+"\n")
			count += 1

		for atom in self.atoms():
			fd.write("CONNECT%5d" % (atom))
			for neighbor in self.neighbors(atom):
				fd.write("%5d" % (neighbor))
			fd.write("\n")
			
		if pdbFile != None:
			fd.close()

		
	#-------------------------------------------------------------
	def getElements(self):
		"""
		"""
		elts = list()
		for atom in self.atoms():
			elts.append(self.getAtomAttributes(atom).getElement())
		elts.sort()
		for i in range(len(elts)-2, -1, -1):
			if elts[i] == elts[i+1]:
				del elts[i+1]
		return elts

	#-------------------------------------------------------------
	def enclosingBox(self):
		"""
		"""
		boxmin = [0., 0., 0.]
		boxmax = [1.,1.,1.]
		for atom in self.atoms():
			coords = self.getAtomAttributes(atom).getCoord()
			boxmin = [min(boxmin[0], coords[0]), min(boxmin[1], coords[1]), min(boxmin[2], coords[2])]
			boxmax = [max(boxmax[0], coords[0]), max(boxmax[1], coords[1]), max(boxmax[2], coords[2])]
		return [boxmin, boxmax]

	#-------------------------------------------------------------
	class MoleculeError(Exception):
		"""
		"""
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)



if __name__ == '__main__':
	print "Probando Molecule"
	m = Molecule("Molecula prueba" )
	print "Leyendo Molecule"
	m.load("/home_inv/jse/inv/Cuchifritos/networkx/MDControl/data/pdb/Homopolymers/PMMA/backbonePMMA.pdb", "/home_inv/jse/inv/Cuchifritos/networkx/MDControl/data/pdb/Homopolymers/PMMA/backbonePMMA.psf")

