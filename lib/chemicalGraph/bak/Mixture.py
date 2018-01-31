# -*- coding: utf-8 -*-
#
# Authors: José O. Sotero Esteva
#	Department of Mathematics, University of Puerto Rico at Humacao
#	Humacao, Puerto Rico
#	jse@math.uprh.edu

import sys,math

from networkx.classes.multigraph import MultiGraph

from ChemicalGraph import ChemicalGraph
from AtomAttributes import *
import Molecule

class Mixture(MultiGraph):
	"""
	A Mixture is a collection of instances of the Molecule class.
	"""

	def __init__(self, mixture=None):
		super(Mixture, self).__init__(self)
		if mixture != None:
			raise MixtureError("Mixture copy constructor not implemented yet.")

	#-------------------------------------------------------------
	def writePSF(self, psfFile=None):
		if psfFile==None:
			fd = sys.stdout
			print "writePSF imprimiendo stdout"
		else:
			fd = open(psfFile, 'w')
			print "writePSF(",psfFile,")"

		# write ATOM section
		fd.write("PSF\n\n       1 !NTITLE\n REMARKS \n\n%8i !NATOM\n" % self.order())
		count = 1
		for molecule in self:
			mol = self.getMolecule(molecule)
			for atom in mol:
				atr = mol.atom_attributes(atom)
				fd.write(atr.PSFline(count)+"\n")
				count += 1
			
		# write BOND section
		fd.write("\n%8i !NBOND\n" % self.bonds())
		count = 0
		bondCount = 0
		for molecule in self:
			mol = self.getMolecule(molecule)
			bondsT = mol.bonds()
			nbonds = len(bondsT)
			bonds = list()
			for bond in bondsT:
				bonds.append([bond[0]+count, bond[1]+count])
				fd.write("%8d%8d" % (bond[0]+count, bond[1]+count))
				bondCount += 1
				if bondCount % 4 == 0:
					fd.write("\n")
			#for i in range(0, nbonds - nbonds % 4, 4):
				#fd.write("%8d%8d" % (bonds[i][0], bonds[i][1]))
			count += mol.order()

		# write angles
		fd.write("\n\n%8d !NTHETA: angles\n" % (0))

		# write dihedrals
		fd.write("\n\n%8d !NPHI: dihedrals\n" % (0))

		# write other stuff
		fd.write("\n\n%8d !NIMPHI: impropers\n" % (0))
		fd.write("\n\n%8d !NDON: donors\n" % (0))
		fd.write("\n\n%8d !NACC: acceptors\n" % (0))
		fd.write("\n\n%8d !NNB\n" % (0))
		fd.write("\n\n%8d !NGRP\n" % (0))

		fd.close()
			

	#-------------------------------------------------------------
	def writePDB(self, pdbFile=None):
		if pdbFile==None:
			fd = sys.stdout
			#print "writePDB imprimiendo stdout"
		else:
			fd = open(pdbFile, 'w')
			#print "writePDB(",pdbFile,")"
		count = 1

		#print self
		for molecule in self:
			mol = self.getMolecule(molecule)
			print mol
			for atom in mol:
				atr = mol.atom_attributes(atom)
				fd.write(atr.PDBline(count)+"\n")
				count += 1

		#count = 1
		#for molecule in self:
		#	for atom in mol.atoms():
		#		fd.write("CONNECT%5d" % (atom+count))
		#		for neighbor in mol.neighbors(atom):
		#			fd.write("%5d" % (neighbor+count))
		#		fd.write("\n")
		#	count += self.getMolecule(molecule).order()
			
		if pdbFile != None:
			fd.close()



	#-------------------------------------------------------------
	def load(self, pdbFile, psfFile):
		"""
		Loads and parses PDB coordinate file and PSF topology file containing molecules.

		@type  pdbFile: string
		@param pdbFile: PDB filename.

		@type  psfFile: string
		@param psfFile: PDB filename.
		"""
		from Bio.PDB.PDBParser import PDBParser
		from PSF import PSF

		structure = PDBParser(PERMISSIVE=1).get_structure("ChemicalGraph", pdbFile)
		atomsGen=structure.get_atoms()
		atoms = [a for a in atomsGen]
		# residues = [r.get_resname() for r in structure.get_residues()]
		# chains = [c for c in structure.get_chains()]
		psf=PSF(psfFile)
		# print len(atoms), " != ", len(psf.atoms)
		print atoms
		# print psf.atoms
		if len(atoms) != len(psf.atoms):
			raise self.MixtureError("Ammount of atoms in "+pdbFile + " and "+psfFile + " files are different ("+str( len(atoms))+" vs "+str(len(psf.atoms))+").")

		mixed = ChemicalGraph()

		# add nodes
		elements = psf.get_elements()
		charges = psf.get_charges()
		masses = psf.get_masses()
		for n in range(len(atoms)):
			atom=atoms[n]
			# print "llamada a AtomAttributes", [elements[n], atom.get_coord(), charges[n], masses[n]]
			atr = AtomAttributes(	atom.get_name(), atom.element, atom.get_coord(), charges[n], masses[n], 
						atom.get_bfactor(), atom.get_occupancy(), atom.get_altloc(), 
						atom.get_fullname(),atom.get_parent().get_resname())
			mixed.add_node(n+1, attrs=[atr])

		# add edges
		for bond in psf.bonds:
			# if bond[0] < bond[1]:  # avoids adding an edge twice
			try:  # avoids adding an edge twice
				mixed.add_edge(bond)
			except AdditionError:
				pass

		# add everything else
		mixed.add_angles(psf.get_angles())
		mixed.add_dihedrals(psf.get_dihedrals())

		# print "attr prev connectedComponents=", mixed.atoms_attributes()
		molecules = mixed.connectedComponents()
		# print "connectedComponents=", molecules

		# finally, add the molecules to the mixture
		count = self.order() + 1
		for m in molecules:
			#mol = Molecule.Molecule(pdbFile+"("+str(count)+")", molecule=m)
			#mol = Molecule.Molecule("mol_"+str(count), molecule=m)
			mol = Molecule.Molecule("loadedPDB", molecule=m)
			self.add(mol)
			count += 1

	#-------------------------------------------------------------
	def merge(self, mix):
		for mol in mix:
			self.add(mix.getMolecule(mol))
	#-------------------------------------------------------------
	def add(self, mol):
		"""
		Merges mol into self.

		@type  mol: Molecule.
		@param mol: Molecule to be added to the mixture.
		"""

		assert(isinstance(mol, Molecule.Molecule))

		cont = 1
		print "---------add: ",self
		while self.has_node(mol.molname()+"_"+str(cont)):
			cont += 1
		print "-------add: ",mol.molname()+"_"+str(cont)

		self.add_node(mol.molname()+"_"+str(cont), attrs=[mol])

	#-------------------------------------------------------------
	def remove(self, molname):
		"""
		Removes molecule with molname  (first found)

		@type  molname: String.
		@param molname: name of Molecule to be added to the mixture.
		"""

		self.remove_node(molname)

	#-------------------------------------------------------------
	def getMolecule(self, name):
		"""
		Returns molecule with given name.

		@type  name: Mixture.
		@param name: name of the molecule.

		@rtype:  Molecule
		@return: Molecule with given name.
		"""
		return self.node_attributes(name)[0]

	#-------------------------------------------------------------
	def enclosingBox(self):
		#  CUIDADO CON boxmin y boxmax iniciales

		if self.order() == 0:
			boxmin = [0., 0., 0.]
			boxmax = [2.,2.,2.]
		else:
			molecules = self.nodes()
			box = self.getMolecule(molecules[0]).enclosingBox()
			boxmin = [box[0][0], box[0][1], box[0][2]]
			boxmax = [box[1][0], box[1][1], box[1][2]]
			molecules.pop(0)

			for molName in molecules:
				box = self.getMolecule(molName).enclosingBox()
				boxmin = [min(boxmin[0], box[0][0]), min(boxmin[1], box[0][1]), min(boxmin[2], box[0][2])]
				boxmax = [max(boxmax[0], box[1][0]), max(boxmax[1], box[1][1]), max(boxmax[2], box[1][2])]
		return [boxmin, boxmax]

	#-------------------------------------------------------------
	def boundingSphere(self):
		box = self.enclosingBox()
		center = [(box[0][0]+box[1][0])/2., (box[0][1]+box[1][1])/2., (box[0][2]+box[1][2])/2.]
		dx =box[0][0]-box[1][0]
		dy = box[0][1]-box[1][1]
		dz = box[0][2]-box[1][2]
		radius = math.sqrt(dx*dx+dy*dy+dz*dz)
		return [center, radius]

	#-------------------------------------------------------------
	def __str__(self):
		result =  "Mixture(" + str(self.order()) + "):"
		for molid in self:
			result += str(self.getMolecule(molid)) + ", "
		return result

	#-------------------------------------------------------------
	def node_attributes(self, molid):
		return self.node[molid]['attrs']

	#-------------------------------------------------------------
	def order(self):
		res = 0
		for molecule in self:
			res += self.getMolecule(molecule).order()
		return res
	#-------------------------------------------------------------
	def _len(self):
		
		return self.__len__()
			

	#-------------------------------------------------------------
	def bonds(self):
		res = 0
		for molecule in self:
			res += len(self.getMolecule(molecule).bonds())
		return res

	#-------------------------------------------------------------
	class MixtureError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)


if __name__ == '__main__':
	from THF import THF
	from DMF import DMF
	print "Probando Mixture"
	#m1 = Molecule.Molecule("Molecula prueba 1" )
	#m2 = Molecule.Molecule("Molecula prueba 2" )
	m1 = THF("Molecula prueba 1")
	m2 = DMF("Molecula prueba 2")

	mi = Mixture()
	mi.add(m1)
	mi.add(m2)
	
	for molecule in mi:
		print molecule

	mi.writePDB("/tmp/prueba.pdb")
	mi.writePSF("/tmp/prueba.psf")




