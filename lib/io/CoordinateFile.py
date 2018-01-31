# -*- coding: utf-8 -*-
"""
	CoordinateFile.py
	Represents a coordinate file that may have many frames of the simulation.
	
    Copyright 2011, 2012: José O.  Sotero Esteva
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

import openbabel, pybel, os, sys
sys.path.append("/home/jse/inv/Cuchifritos/bazaar/Wolffia")
from lib.chemicalGraph.Mixture import Mixture, MixtureError
from lib.chemicalGraph.ChemicalGraph import ChemicalGraph
from lib.chemicalGraph.io.PSF import PSF
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes, AtomInfo
from lib.chemicalGraph.molecule.Molecule import Molecule

class CoordinateFile:
	def __init__(self, mixtureFile, fileType=None, psfFile=None, mixtureName=None):
		'''
		Prepares file for reading molecules.
		
		Raises MixtureError or whichever exception that pybel raises.
		'''
		if fileType == None:
			fileType = os.path.splitext(mixtureFile)[1][1:].strip()  # get filename extension
		if mixtureName == None:
			mixtureName = os.path.basename(mixtureFile)
			
		self.fileType = fileType
		self.fileName = mixtureFile
		self.mixtureName = mixtureName
		print "CoordinateFile ", fileType

		if psfFile == None: self.psf = None
		else: self.psf = PSF(psfFile)
		
		self.__iter__()
		
	def __iter__(self):
		if self.fileType == "cc1":
			import cc1
			self.molIterator = cc1.readfile(self.fileName)
		else:
			self.molIterator = pybel.readfile(self.fileType, self.fileName)
		self.currentMolecule = None 
		self.firstMolecule = True
		return self


	def _processFirstFrame(self):
		"""
		Gets the first pybel Molecule and puts its Wolffia equivalent Mixture in self.currentMolecule.
		Returns the first frame.
		Raises whichever exception that pybel throws (probably StopIteration).
		"""
		
		mol = self.molIterator.next()
		chemicalGraphMixed = ChemicalGraph()
		etable			 = openbabel.OBElementTable()

		
		n = 0
		for atom in mol.atoms:
			atomType = atom.OBAtom.GetResidue().GetAtomID(atom.OBAtom)
			symbol = etable.GetSymbol(atom.atomicnum)
			coords = list(atom.coords)
			name	 = etable.GetName(atom.atomicnum) 
			residue = atom.OBAtom.GetResidue().GetName()
			psfType = atom.OBAtom.GetResidue().GetAtomID(atom.OBAtom).strip()
			print "'" + psfType + "'"
			charge = atom.partialcharge
			mass	 = atom.atomicmass	
			if self.psf <> None:
				psfType = self.psf.getType(n)
				charge = self.psf.getCharge(n)
				mass	 = self.psf.getMass(n)
		
		
			ai  = AtomInfo(atomType, symbol, psfType, charge, mass, 1, 1, 1, name, residue)
			atr = AtomAttributes(ai, coords, [])
			chemicalGraphMixed.add_node(n + 1, attrs=[atr])
			n += 1
		
		# add edges
		
		if self.psf <> None:
			for b in self.psf.bonds:
				try:  # avoids adding an edge twice
					chemicalGraphMixed.add_edge(b)
				except AdditionError:
					pass			
			if len(mol.atoms) != len(self.psf.atoms):
				raise MixtureError("Amount of atoms in " + self.fileName + " and psf File files are different (" + str(len(self.atoms)) + " vs " + str(len(self.psf.atoms)) + ").")
		else:			
			for bond in openbabel.OBMolBondIter(mol.OBMol):   
				chemicalGraphMixed.add_edge([bond.GetBeginAtom().GetIdx(), bond.GetEndAtom().GetIdx()])	   
					
		molecules = chemicalGraphMixed.connectedComponents()	  
		self.currentMolecule = Mixture()
		
		if len(molecules) == 1:
			self.currentMolecule.add(Molecule(self.mixtureName, molecule=molecules[0]))
		else:
			n = 0
			for m in molecules:
				self.currentMolecule.add(
							Molecule(self.mixtureName + "(" + str(n) + ")", molecule=m),
							checkForInconsistentNames=False)
				n += 1

		return self.currentMolecule
	
	
	def _processNextFrame(self):
		"""
		Gets next pybel Molecule and puts its Wolffia equivalent Mixture in self.currentMolecule.
		Returns the next frame.
		Assumes that _processFirstFrame() has been called earlier.
		Raises whichever exception that pybel throws (probably StopIteration).
		"""
		self.currentMolecule = Mixture(self.currentMolecule)  # copy mixture
		mol = self.molIterator.next()
		print "_processNextFrame", mol
		coordinates = []
		for atom in mol.atoms:
			coordinates.append(atom.coords)
		self.currentMolecule.updateCoordinatesFromArray(coordinates)
		return self.currentMolecule

		
	def next(self):
		"""
		Returns next frame if present.
		Raises whichever exception that pybel throws (probably StopIteration).
		"""
		if self.firstMolecule:
			self.firstMolecule = False
			return self._processFirstFrame()
		else: return self._processNextFrame()
	
			

class CoordinateString(CoordinateFile):
	def __init__(self, mixtureString, mixtureName, fileType="pdb"):
		'''
		Prepares String for reading mixtures.
		
		Raises MixtureError or whichever exception that pybel raises.
		'''
		self.mixtureString = mixtureString
		CoordinateFile.__init__(self, "No file", fileType, None, mixtureName)

	def __iter__(self):
		self.molIterator = iter([pybel.readstring(self.fileType, self.mixtureString)])
		self.currentMolecule = None  # serves to know if a frame has been read
		self.psf = None
		self.firstMolecule = True
		return self

class CoordinatesUpdateFile:
	def __init__(self, mixtureFile, mixture):
		self.mixFile = open(mixtureFile, "r")
		self.mixture = mixture
		
	def next(self):
		"""
		Update the coordinates of the mixture.  It is meant to load results from simumations.

		"""
		num = 0
		line = self.mixFile.readline()
		while line <> "" and line[:3] <> "END":
			if line[:4] == "ATOM":
				try:
					# print "updateCoordinates ", num
					x = float(line[30:38])
					y = float(line[38:46])
					z = float(line[46:54])
					self.mixture.atomOrder[num].setCoord([x, y, z])
					num += 1
				except (IndexError, ValueError):
					print "CoordinatesUpdateFile.updateCoordinates failed to update atom ", num
					break
			line = self.mixFile.readline()
		return len(line) > 0
	
	def close(self): self.mixFile.close()
	

import unittest
class TestCoordinateFile(unittest.TestCase):
	def setUp(self):
		self.pdbFile = "../../data/coordinates/Surfactant/SDBS.pdb"
		self.psfFile = "../../data/coordinates/Surfactant/SDBS.psf"
		
	def test_onlyPDB(self):
		cf1 = CoordinateFile(self.pdbFile)
		self.assertEqual(cf1.next().order(), 52)
		
	def test_PDBandPSF(self):
		cf2 = CoordinateFile(self.pdbFile, psfFile=self.psfFile)
		self.assertEqual(cf2.next().order(), 52)


class TestCoordinateString(unittest.TestCase):
	def setUp(self):
		self.pdbString = "ATOM     1  OH1  WTR A   1       4.013   0.831  -9.083  1.00  0.00           O   \
ATOM     2  HH1  WTR A   1       4.941   0.844  -8.837  1.00  0.00           H     \
ATOM     3  HH2  WTR A   1       3.750  -0.068  -9.293  1.00  0.00           H     \
TER"

	def test_onlyPDB(self):
		cf1 = CoordinateString(self.pdbString, "agua", "pdb")
		self.assertEqual(cf1.next().order(), 3)
		

		
#=====================================================================
if __name__ == '__main__':
	unittest.main()