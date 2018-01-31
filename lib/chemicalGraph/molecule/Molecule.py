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
import sys,os, warnings
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../')

if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../')
from lib.chemicalGraph.ChemicalGraph import ChemicalGraph
from ForceField import ForceField, NonBond
from AtomAttributes import AtomAttributes,AtomInfo
from networkx import NetworkXError, isomorphism
import numpy as np

#=========================================================================
class  Molecule(ChemicalGraph):
	"""Represents a single molecule as a connected graph.
	"""
	_EPSILON_ = 0.1

	def __init__(self, ident="Unknown", molecule=None, isSolvent=False):
		"""
		"""

		ChemicalGraph.__init__(self)
		self._name          = ident
		self.forceField     = ForceField()
		self.atomTypesTable = dict()
		
		if isinstance(molecule, Molecule):
			if self._name == "Unknown": self._name = molecule.molname()
			#print "Molecule Init", molecule.molname()
			self.merge(molecule.copy())
		elif isinstance(molecule, ChemicalGraph):  # atoms in ChemicalGraph cannot be assumed to be [1:N]
			# build inverse function
			#print "Molecule Init ChemicalGraph"
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
			self.copyChargesToForceField()
			#print "Molecule Init ChemicalGraph2", self.forceField._NONBONDED
		elif molecule == None:
			self.copyChargesToForceField()
		else:
			raise Molecule.MoleculeError("Molecule initialized with instance variable of a class "+ str(type(molecule)) + " that is not a subclass of ChemicalGraph")

		try: self.solvent = isSolvent
		except: self.solvent = self._name[:8] == "SOLVENT("

	def sameSpeciesAs(self, mol):
		GM = isomorphism.GraphMatcher(self,mol)
		#print "Molecule __eq__ ", self, " isomorphic to ", mol, " ", GM.is_isomorphic()
		if not GM.is_isomorphic(): return False
		for atom in GM.mapping:
			#print "Molecule __eq__ getAtomAttributes =",self.getAtomAttributes(atom).getInfo(), mol.getAtomAttributes(GM.mapping[atom]).getInfo()
			if self.getAtomAttributes(atom) != mol.getAtomAttributes(GM.mapping[atom]): return False
		#print "Molecule __eq__  isomorphic "
		return True
		
	
	#-------------------------------------------------------------	
	def copy(self):	
		"""
		Copy of the molecule.

		@rtype:  
		@return: Copy of the molecule
		"""
		newMol = Molecule("None")
		newMol = ChemicalGraph.copy(self)
		newMol.forceField = self.getForceField().copy()
		
		return newMol


	def copyChargesToForceField(self):
		ff = self.getForceField()
		ff.__addChargeFieldToNonBond__()
		#for atom in self:
			#t = self.atom_attributes(atom).getInfo().getType()
			#print "copyChargesToForceField ", t
			#charge = self.atom_attributes(atom).getInfo().getCharge()
			#if ff.hasType(t) and ff.charge(t) != 0 and not ff.charge(t) == charge:
			#	warnings.warn("Atoms with same types but different charges have been found in molecule \'" + self.molname() + ".  The charge for type " + t + "has been set to " + str(charge) + ".", SyntaxWarning)
				#print "Atoms with same types but different charges have been found in molecule \'" + self.molname() + ".  The charge for type " + t + "has been set to " + str(charge) + ".", SyntaxWarning
			#ff.setCharge(t, charge)

	def charge(self):
		totalCharge = 0
		for atom in self:
			t = self.atom_attributes(atom).getInfo().getType()
			#print "copyChargesToForceField ", t
			#charge = self.atom_attributes(atom).getInfo().getCharge()
			totalCharge += self.atom_attributes(atom).getInfo().getCharge()
			#totalCharge += self.getForceField().charge(t)
		return totalCharge
	
	def load(self, pdbFile, psfFile):
		"""Loads and parses PDB coordinate file and PSF topology file containing a molecule.
		If the files contain more than one molecule, only one of them will be loaded.
		Erases the current molecule.

		@type  pdbFile: string
		@param pdbFile: PDB filename.

		@type  psfFile: string
		@param psfFile: PSF filename.
		"""

		from chemicalGraph.Mixture import Mixture
		# print "Loading "+pdbFile+ " into molecule " + self._name
		mix = Mixture()
		mix.load(pdbFile, psfFile)
		mol = mix.getMolecule(mix.nodes()[0])
		#print "Molecule load ", mol.getForceField()._NONBONDED
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
		from lib.chemicalGraph.Mixture import Mixture

		mix = Mixture()
		mix.add(self)
		mix.writePSF(psfFile)


	#-------------------------------------------------------------
	def __str__(self):
		"""
		"""
		return self._name + ": " + ChemicalGraph.__str__(self)

	def crc32(self, val=0):
		prev = val
		for atom in self.atoms():
			prev = self.atom_attributes(atom).crc32(prev)
		return prev
	#-------------------------------------------------------------
	def node_attributes(self, atom):
		"""
		"""
		try:
			return self.node[atom]['attrs']
		except KeyError:
			print "ERROR: Molecule.node_attributes() failed to obtain attributes for atom ", atom, "."
			raise KeyError
			

	#-------------------------------------------------------------
	def molname(self):
		"""
		"""
		return self._name
        
        
	def isSolvent(self):
		#print "isSolvent ",self._name, "SOLVENT(",self._name[:8] == "SOLVENT("
		try:
			return self.solvent
		except:   # backward compatibility
			return  self._name[:8] == "SOLVENT("
    

	def setAsSolvent(self, isSolvent=True):
		self.solvent = isSolvent

	def isIsomorphicTo(self, mol):
		return ChemicalGraph.is_isomorphic(self, mol)
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

	def atomsGenerator(self):
		for atom in self:
			yield self.getAtomAttributes(atom)

	def bonds(self):
		"""Returns bonds.

		@rtype:  list of integers.
		@return: Atoms of the molecules.

		Checks for an apparent defect in networkx.  Sometimes
		if has non-existent nodes.
		edgesList = self.edges()
		#print "Molecule.bonds() ", self.nodes()
		#print "Molecule.bonds() ", self.atoms()
		atomsList = self.atoms()
		for e in edgesList:
			removeEdge = False
			for a in e:
				if not a in atomsList: 
					try:
						self.remove_node(a)
					except :
						print "Molecule.bonds() tried to remove non-existing atom"
					removeEdge = True
				if removeEdge: self.remove_edge(e)
		#print "Molecule.bonds() ", self.nodes()
		"""
		return self.edges()
		
	def bondsGenerator(self):
		for e in self.bonds():
			try:  #  there seems to be problems with Networkx on removing edges
				yield (self.getAtomAttributes(e[0]), self.getAtomAttributes(e[1]))
			except KeyError:
				print "WARNING: Molecule.bondsGenerator ", e
				pass

	#-------------------------------------------------------------
	def inferBonds(self, element1, element2, bondDistance, atoms=None):
		"""Adds bonds between pairs of elements of the specified types (element1, element2) that
		are at distance bondDistance +/- _EPSILON_

		@type	element1: string
		@param	element1: element name
		@type	element2: string
		@param	element2: element name
		@type	atoms:    list
		@param	atoms:    list of atoms
		"""
		import math
		if atoms == None:
			atoms = self.atoms()
		for i in range(len(atoms)):
			if self.getAtomAttributes(atoms[i]).getElement() == element1:
				for j in range(i+1,len(atoms)):
					if self.getAtomAttributes(atoms[j]).getElement() == element2 and math.fabs(self.distance(atoms[i], atoms[j]) ) < self._EPSILON_:
						print "WARNING: Atoms ",atoms[i], " and ", atoms[j] , " are too close."
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
	def getBondsAnglesFrom(self):
		'''
		Sets bond lengths and angles from the molecule and assigns it to the
		force field.
		'''
		ff = self.getForceField()
		bondTypes = self.bondTypes()
		bonds     = self.bonds()
		#print "on_bondButton_pressed bonds=",bonds
		for bt in bondTypes:
			bondLengths = []
			for b in bonds:
				t0 = self.getAtomAttributes(b[0]).getInfo().getType()
				t1 = self.getAtomAttributes(b[1]).getInfo().getType()
				#print "on_bondButton_pressed ",bt,[t0,t1],bt == (t0,t1)
				if bt == (t0,t1) or bt == (t1,t0):
					bondLengths.append(self.getAtomAttributes(b[0]).distanceTo(self.getAtomAttributes(b[1])))
			#print "on_bondButton_pressed bondLengths=",bt, bondLengths
			ff.setBond(bt,sum(bondLengths)/len(bondLengths), 1)
		
		angleTypes = self.angleTypes()
		angles = self.angles()
		for at in angleTypes:
			angleMeasures = []
			for a in angles:
				t0 = self.getAtomAttributes(a[0]).getInfo().getType()
				t1 = self.getAtomAttributes(a[1]).getInfo().getType()
				t2 = self.getAtomAttributes(a[2]).getInfo().getType()
				#print "getBondsAnglesFrom ", at, (t0,t1,t2), (t2,t1,t0)
				if at == (t0,t1,t2) or at == (t2,t1,t0):
					ba = np.array(self.getAtomAttributes(a[0]).getCoord()) - np.array(self.getAtomAttributes(a[1]).getCoord())
					bc = np.array(self.getAtomAttributes(a[2]).getCoord()) - np.array(self.getAtomAttributes(a[1]).getCoord())
					cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
					if(cosine_angle == 0): angle = 180;
					else: angle = np.arccos(cosine_angle)
					#print "getBondsAnglesFrom = ",angle
					angleMeasures.append(np.degrees(angle))
			ff.setAngle(at,sum(angleMeasures)/len(angleMeasures), 1)
	
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
	def setAtomAttributes(self, atom, attr):
		"""
		"""
		#print "Molecule.setAtomAttributes: ", attr.getType().typeName()
		if attr.getInfo().typeName() in self.atomTypesTable:
			attr.setType(self.atomTypes[attr.getType().typeName()])
		self.node[atom]['attrs'] = [attr]

	#-------------------------------------------------------------
	def rename(self, name):
		"""
		"""
		#import inspect
		#print "Molecule.rename ", self._name, " to  ", name, " by ", inspect.stack()[1][3]
		self._name = name


	def redefineTypes(self):
		"""
		"""

		# redefine types as pair (element, atom).  Every atom has a unique type.
		usedElments     = dict()
		typeAssignments = dict()
		for atom in self:
			attr    = self.getAtomAttributes(atom).getInfo()
			element = attr.getElement()
			if usedElments.has_key(element):
				newType               = element+str(usedElments[element])
				usedElments[element] += 1
			else:
				usedElments[element]  = 0
				newType               = element
			attr.setType(newType)		
			typeAssignments[newType]  = [atom]

		self.forceField = ForceField()
		self.forceField.addZeroParameters(self)
		self.copyChargesToForceField()

		#print "Molecule.redefineTypes typeAssignments", typeAssignments
		return typeAssignments
	#-------------------------------------------------------------

	def redefineTypes1(self):
		"""
		"""

		# redefine types as pair (element, atom).  Every atom has a unique type.
		for atom in self:
			attr = self.getAtomAttributes(atom).getInfo()
			attr.setType((attr.getElement(), atom))
			
		atomClasses = dict()
		atoms       = self.atomTypes()
		bonds       = self.bondTypes()
		angles      = self.angleTypes()
		dihedrals = self.dihedralTypes()
		#print "redefineTypes atomClasses", atoms,bonds,angles,dihedrals
	
		for atomType in atoms:
			atom    = atomType[1]
			#print "redefineTypes atom",atom

			atomBonds = []
			for bond in bonds:
				#print "redefineTypes atomType in bond",atomType , bond,atomType in bond
				if atomType in bond: atomBonds.append(str([bond[0][0],bond[1][0]]))
			atomBonds.sort()
			#print "redefineTypes atomBonds", atomBonds
			
			atomAngles = []
			for angle in angles:
				#print "redefineTypes atomType in angle",atomType , angle,atomType in angle
				if atomType in angle: atomAngles.append(str([angle[0][0],angle[1][0],angle[2][0]]))
			atomAngles.sort()
			#print "redefineTypes atomAngles", atomAngles
			
			atomDihedrals = []
			for dihedral in dihedrals:
				#print "redefineTypes atomType in angle",atomType , angle,atomType in angle
				if atomType in dihedral: atomDihedrals.append(str([dihedral[0][0],dihedral[1][0],dihedral[2][0],dihedral[3][0]]))
			atomDihedrals.sort()
			#print "redefineTypes atomDihedrals", atomDihedrals
			
			atomSignature = str([atomType[0],atomBonds, atomAngles, atomDihedrals])
			#atomSignature = (atomType[0],atomBonds, atomAngles, atomDihedrals)
			#print "redefineTypes atomSignature", atomSignature
			#atomSignature = str(atomType[0]+str(atom)+",")
			#print "redefineTypes atomSignature", atomSignature
			
			if not atomClasses.has_key(atomSignature):
				atomClasses[atomSignature] = list()
			atomClasses[atomSignature].append(atom)

		#print "redefineTypes atomClasses", atomClasses
		#define new type names
		newTypeNames = dict()
		usedElments = dict()
		for aClass in atomClasses.keys():
			element = aClass[2:aClass.find(',')-1] 
			#element = aClass[0] 
			if usedElments.has_key(element):
				usedElments[element] += 1
				newTypeNames[aClass] = element + str(usedElments[element])
				
			else:
				usedElments[element] = 0
				newTypeNames[aClass] = element
		#print "redefineTypes newTypeNames", newTypeNames

		# Finally, change types of atoms
		typeAssignments = dict()
		for aClass in atomClasses:
			#print "redefineTypes atomClasses[aClass]", aClass,atomClasses[aClass]
			typeAssignments[newTypeNames[aClass]] = atomClasses[aClass]
			for atom in atomClasses[aClass]:
				self.getAtomAttributes(atom).getInfo().setType(newTypeNames[aClass])

		self.forceField = ForceField()
		self.forceField.addZeroParameters(self)
		self.copyChargesToForceField()

		print "Molecule.redefineTypes typeAssignments", typeAssignments
		return typeAssignments
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

		for t in self.atomTypes():
			#print "Molecula add_atom ", t.typeName()
			if t == attr.getInfo().getType():
				#print "Molecula add_atom encontrado", t
				attr.getInfo().setType(t)
				break

		atom = self.order() + 1
		self.add_node(atom, attrs=None)
		self.setAtomAttributes(atom, attr)
		for n in neighbors:
			self.add_edge((atom, n))

	#-------------------------------------------------------------
	def add_edge(self, atoms):
		"""
		"""
		assert(atoms[0] != atoms[1] and not self.has_edge(atoms[0], atoms[1]))
		super(Molecule, self).add_edge(atoms)

	#-------------------------------------------------------------
	def addBond(self, atom1, atom2):
		"""
		"""
		self.add_edge([atom1,atom2])

	#-------------------------------------------------------------
	def removeBond(self, edge):
		"""
		"""
		self.remove_edge(edge)

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

	def closestAtoms(self, mol, atomsSubset=None):
		import sys
		mind = sys.float_info.max
		if atomsSubset == None: atomsSubset = self.atoms()
		for atom1 in atomsSubset:
			for atom2 in mol:
				d = self.getAtomAttributes(atom1).distanceTo(mol.getAtomAttributes(atom2))
				if d < mind:
					mind = d
					atomsPair = (atom1,atom2)
		return atomsPair

	def changeResidues(self, res, atomList=None):
		if not atomList:
			atomList = self.nodes()
		for atom in atomList:
			a = self.getAtomAttributes(atom).getInfo()
			a._residue = res
		return self
	
	def distanceTo2(self, mol):
		import sys
		mind = sys.float_info.max
		for atom1 in self:
			for atom2 in mol:
				d = self.getAtomAttributes(atom1).distanceTo(mol.getAtomAttributes(atom2))
				if d < mind:
					mind = d
		return mind

	def distanceTo(self, mol):
		pair = self.closestAtoms(mol)
		return self.getAtomAttributes(pair[0]).distanceTo(mol.getAtomAttributes(pair[1]))

	def removeAtomsFromSphere(self, center, radius):
		"""
		Remove atoms within a sphere.  Removing atoms may split or empty the molecule.
		Thus, the result is a list of molecules.

		@type  center: list of 3 coordinates.
		@param center: Center of the sphere.

		@type  radius: Float.
		@param radius: Radius of the sphere.
		
		@type List
		@return: A list of the molecules that result from removing the atoms.
		"""
		newMol = Molecule(self.molname(), self)
		
		#dummy atom as center of sphere
		centerAt  = AtomAttributes( AtomInfo('', '', '', 0,0), center)

		for atom in newMol.atoms():
			if centerAt.distanceTo(self.getAtomAttributes(atom)) <= radius:
				newMol.removeAtom(atom)
		del centerAt
		return newMol.connectedComponents()
	
	def removeBonds(self, edgesList):
		"""
		Remove bonds.  Removing bonds may split or empty the molecule.
		Thus, the result is a list of molecules.

		@type  edgesList: list of tuples of 2 atoms.
		@param edgesList: list of bonded atoms.

		@type List
		@return: A list of the molecules that result from removing the edge.
		"""
		newMol = Molecule(self.molname(), self)
		
		for edge in edgesList:
			try:
				newMol.remove_edge(edge[0], edge[1])
			except NetworkXError:
				print "WARNING: Tried to remove inexistent bond ", edge, " from molecule ", self, " in Molecule.removeBond()"

		newMolsList = newMol.connectedComponents()
		print "Molecule.removeBonds() produjo ", len(newMolsList), " moleculas"
		return newMolsList
	
	def removeAtoms(self, atomsList):
		"""
		Remove bonds.  Removing bonds may split or empty the molecule.
		Thus, the result is a list of molecules.

		@type  atomsList: list  atoms.
		@param atomsList: list   atoms.

		@type List
		@return: A list of the molecules that result from removing the atoms.
		"""
		newMol = Molecule(self.molname(), self)
		
		for atom in atomsList:
			try:
				newMol.remove_node(atom)
			except NetworkXError:
				print "WARNING: Tried to remove inexistent atom ", atom, " from molecule ", self, " in Molecule.removeBond()"

		newMolsList = newMol.connectedComponents()
		print "Molecule.removeBonds() produjo ", len(newMolsList), " moleculas"
		return newMolsList
	
	#-------------------------------------------------------------
	def merge(self, mol, bonds=[], keepTypes=True):
		"""
		Merges mol into self.  Atom labels of mol are modified to avoid name collisions
		with existing atoms.

		@type  mol: Molecule.
		@param mol: Molecule to be merged into self.

		@type  bonds: list of pairs of integers.
		@param bonds: Bonds to be added between the two molecules to form a new molecule.  It must have at least one pair unless the molecule is empty.  For each pair, the first integer is an atom (int) of the first molecule and the second an atom of the second.
		"""
		#print "Molecule merge", self, mol,bonds
		assert(self.order() == 0 or len(bonds) > 0)
		ChemicalGraph.merge(self, mol, newBonds=bonds)
		#print "Molecule merge", self.getForceField()._NONBONDED, mol.getForceField()._NONBONDED
		self.getForceField().update(mol.getForceField())
		#print "Molecule merge: resulting molecule class:", self.__class__.__name__
		
	#-------------------------------------------------------------
	def writePDB(self, pdbFile=None, count=1):
		"""
		"""
		import sys
		#print "Molecule writePDB", pdbFile, type(pdbFile)
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
			elts.append(self.getAtomAttributes(atom).getInfo().getElement())
		elts.sort()
		for i in range(len(elts)-2, -1, -1):
			if elts[i] == elts[i+1]:
				del elts[i+1]
		return elts

	def getTypes(self):
		"""
		"""
		ts = list()
		for atom in self.atoms():
			ts.append(self.getAtomAttributes(atom).getInfo().getType())
		ts.sort()
		for i in range(len(ts)-2, -1, -1):
			if ts[i] == ts[i+1]:
				del ts[i+1]
		return ts

	#-------------------------------------------------------------
	def enclosingBox(self):
		"""
		"""
		boxmin = boxmax = self.getAtomAttributes(self.atoms()[0]).getCoord()
		for atom in self.atoms():
			coords = self.getAtomAttributes(atom).getCoord()
			boxmin = [min(boxmin[0], coords[0]), min(boxmin[1], coords[1]), min(boxmin[2], coords[2])]
			boxmax = [max(boxmax[0], coords[0]), max(boxmax[1], coords[1]), max(boxmax[2], coords[2])]
		return [boxmin, boxmax]

	#-------------------------------------------------------------
	def diameter(self):
		"""
		Approximate diameter of the molecule.

		Actually, the length of the diagonal of the enclosing box.

		@type: float
		@return: Approximate diameter of the molecule.
		"""
		if len(self) == 1: # return 2 * L-J diameter
			return -4 * self.getForceField().nonBond(
						self.atom_attributes(self.atom(0)).getType()
				   )[NonBond._EPSILON]
		else:
			import math
			[[xmin, ymin, zmin], [xmax, ymax, zmax]] = self.enclosingBox()
			dx = xmax - xmin
			dy = ymax - ymin
			dz = zmax - zmin
			return math.sqrt(dx*dx + dy*dy + dz*dz)


	#-------------------------------------------------------------
	def massCenter(self):
		M = 0.0
		cx = 0.0
		cy = 0.0
		cz = 0.0
		
		for atom in self.atoms():
			attr = self.getAtomAttributes(atom)
			mass = attr.getInfo().getMass()
			coor = attr.getCoord()
			#print "massCenter", atom
			#print "massCenter", coor
			cx += mass * coor[0]
			cy += mass * coor[1]
			cz += mass * coor[2]
			M += mass
		
		cx /= M
		cy /= M
		cz /= M
		
		return [cx, cy, cz]
    
	def center(self):
		cx = 0.0
		cy = 0.0
		cz = 0.0
		count = 0
		
		for atom in self.atoms():
			attr = self.getAtomAttributes(atom)
			coor = attr.getCoord()
			#print "massCenter", atom
			#print "massCenter", coor
			cx += coor[0]
			cy += coor[1]
			cz += coor[2]
			count += 1
		
		cx /= count
		cy /= count
		cz /= count
		
		return [cx, cy, cz]
    
	
	#-------------------------------------------------------------
	def atomTypes(self):
		#from chemicalGraph import Mixture
		print "Molecule atomTypes molecula: '", self.molname(), "'"
		
		return sorted(set([ self.getAttributes(atom).getInfo().getType() for atom in self.atoms()]))
	
	#-------------------------------------------------------------
	def bondTypes(self):
		#from chemicalGraph import Mixture
		#print "molecula: '", molecule, "'"
		
		allBonds = list()
		for atom in self:
			ta = self.getAttributes(atom).getInfo().getType()
			neigh = self.neighbors(atom)
			#print "Neighbours: ", atom, ", ", neigh
			for n1 in neigh:
				tn1 = self.getAttributes(n1).getInfo().getType()
				if tn1 < ta:
					allBonds.append((tn1, ta))
				else:
					allBonds.append((ta, tn1))
		uniqueBonds = list()
		for bond in allBonds:
			if not bond in uniqueBonds:
				uniqueBonds.append(bond)

		return uniqueBonds
	
	#-------------------------------------------------------------
	def angleTypes(self):
		#from chemicalGraph import Mixture
		#print "molecula: '", molecule, "'"
		
		allAngles = list()
		for atom in self:
			ta = self.getAttributes(atom).getInfo().getType()
			neigh = self.neighbors(atom)
			#print "Neighbours: ", atom, ", ", neigh
			for n1 in neigh:
				tn1 = self.getAttributes(n1).getInfo().getType()
				for n2 in neigh:
					if n1 < n2:
						tn2 = self.getAttributes(n2).getInfo().getType()
						self.getForceField()
						if tn1 < tn2:
							allAngles.append((tn1, ta, tn2))
						else:
							allAngles.append((tn2, ta, tn1))
						
		uniqueAngles = list()
		for a in allAngles:
			if not a in uniqueAngles:
				uniqueAngles.append(a)

		return uniqueAngles
	
	
	#-------------------------------------------------------------
	def dihedralTypes(self):
		#from chemicalGraph import Mixture
		#print "molecula: '", molecule, "'"
		
		allDihedrals = list()
		for atom in self:
			ta = self.getAttributes(atom).getInfo().getType()
			neigh = self.neighbors(atom)
			#print "Neighbours: ", atom, ", ", neigh
			for n1 in neigh:
				tn1 = self.getAttributes(n1).getInfo().getType()
				for n2 in neigh:
					if n1 < n2:
						tn2 = self.getAttributes(n2).getInfo().getType()
						neigh1 = self.neighbors(n1)
						for n3 in neigh1:
							if n3 != atom:
								tn3 = self.getAttributes(n3).getInfo().getType()
								self.getForceField()
								if tn2 < tn3:
									allDihedrals.append([tn2, ta, tn1, tn3])
								else:
									allDihedrals.append([tn3, tn1, ta, tn2])
						
		uniqueDihedrals = list()
		for a in allDihedrals:
			if not a in uniqueDihedrals:
				uniqueDihedrals.append(a)

		return uniqueDihedrals
	
	
	
	#-------------------------------------------------------------
	def angles(self):
		#from chemicalGraph import Mixture
		#print "molecula: '", molecule, "'"
		
		allAngles = list()
		for atom in self:
			neigh = self.neighbors(atom)
			#print "Neighbours: ", atom, ", ", neigh
			for n1 in neigh:
				for n2 in neigh:
					if n1 < n2:
						allAngles.append([n1, atom, n2])
						
		return allAngles
	


	def setForceField(self, givenFF, trad=None):
		import lib.chemicalGraph as chemicalGraph
		#print "setForceField ", givenFF._NONBONDED
		#assert(isinstance(ff, (ForceField,chemicalGraph.molecule.ForceField.ForceField)))
		#print " setForceField", givenFF.getTypes(), self.atomTypes(), trad
		
		if trad != None or set(givenFF.getTypes()) != set(self.getTypes()):  # copy the object only if names will be changed
			self.forceField = givenFF.copy()
			self.renameTypes(trad)
		else:  # otherwise molecules share ff object
			self.forceField = givenFF
			
		#check compatibility
		fftypes = self.forceField.getTypes()
		#print "Molecule.setForceField types: ",fftypes
		for atom in self:
			if not self.forceField.hasType(self.getAtomAttributes(atom).getInfo().getType()):
				print "WARNING: Molecule.setForceField found type ", self.getAtomAttributes(atom).getInfo().getType()," not present in FF", self.getAtomAttributes(atom).getInfo().getTypes(), ".  Setting parameters to zero."
				#ff.setNonBond(self.getAtomAttributes(atom).getInfo().getType(),0.,0) # sets both parameters to 0.
				raise Molecule.MoleculeError("Trying to assign incompatible force field to a molecule in Molecule.setForceField()")
		
		#print " setForceField", self.forceField._NONBONDED
		#print " setForceField", self.getForceField()._NONBONDED
		
		self.forceField.clean(self.atomTypes())
		#print " setForceField", self.getForceField()._NONBONDED



	def getForceField(self):
		#print "Molecule getForceField ", self.forceField
		#self.forceField.clean(self.atomTypes())  # moved to self.setForeField()
		return self.forceField
		#raise Molecule.MoleculeError("Molecule class " + self.__class__ + " does not have a force field.")


	def ripElement(self, elt="H"):
		atoms = self.atoms()
		for atom in atoms:
			if self.atom_attributes(atom).getType().startswith(elt):
				self.removeAtom(atom)

	def guessForceField(self, timeLimit=float("inf"), options=None, includeHydrogens=True):
		if options ==None:
			pairing = self.getForceField().guess(self, timeLimit, includeHydrogens)
		else:
			pairing = self.getForceField().guess(self, timeLimit, options, includeHydrogens)
		#self.renameTypes(pairing.getPairing())
		if pairing != None:
			print "guessForceField result", pairing.getForceField()._NONBONDED
			print "guessForceField result", pairing.getForceField()._BONDS
		else:
			print "guessForceField NO result"
		return pairing

	def renameTypes(self, nameTable=None):
		if nameTable != None:
			#print "Mol renameTypes ", nameTable, self.angleTypes()
			for atom in self.atoms():
				a = self.getAtomAttributes(atom).getInfo()
				if a.getType() in nameTable.keys():
					a.setType(nameTable[a.getType()])
			self.forceField.renameTypes(nameTable)
	
	#-------------------------------------------------------------

	#-------------------------------------------------------------
	class MoleculeError(Exception):
		"""
		"""
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)



#==========================================================================
if __name__ == '__main__':
	from solvent.THF import THF
	mol = THF()
	print mol.getForceField()._ANGLES
	#mol.guessForceField(5)
	#print mol.getForceField()._NONBONDED

	for atom in mol.atomsGenerator(): print atom


