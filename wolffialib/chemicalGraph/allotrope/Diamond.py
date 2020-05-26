# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Aixa de Jesús
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

#==========================================================================

import networkx as nx
import matplotlib.pyplot as plt
import sys, os,math
import scipy as sp
import numpy as np
import collections

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')

from math import *
from collections import defaultdict
from wollfialib.chemicalGraph.Mixture import Mixture
from wollfialib.chemicalGraph.Molecule import Molecule
from conf.Wolffia_conf import *
from wollfialib.chemicalGraph.element.Element import Element
from wollfialib.chemicalGraph.ForceField import ForceField, NonBond

TOLERANCE=0.0001

class Diamond(Molecule):
	"""
	
	"""
	

	def __init__(self, m, n, q):

		diamondMix = Mixture()
		diamondMix.loadWFM(WOLFFIA_WFY_DIR + "/diamond.wfm")	
		diamondCell = diamondMix.getMolecule('Diamond_1')
		
		sal = Element("NA")	
		sal.moveBy([-1,-1,-1])  # put it out of the way
		
		#'Crece' el diamante
		tempMixture = Mixture()
		for dm in range(m):
			for dn in range(n):
				for dq in range(q):
					newCell = diamondCell.copy()
					newCell.moveby([dm*5.43, dn*5.43, dq*5.43])
					tempMixture.add(newCell)
		
		tempMixture.add(sal)
		
		G = tempMixture.copy()
		H = tempMixture.copy()
		Coord = []
		overlapAtoms = []
		atomNeighbors = []
		toEliminate =[]
		
		
		#Hace que las moleculas se conecten al atomo de Na y hace de la mezcla una molecula
		for p,mol in enumerate(G):
			molecule = G.getMolecule(mol)
			for idx, atom1 in enumerate(molecule):
				if molecule.getAttributes(atom1).getInfo().getElement() == "NA":
					molSal = mol
					numMolecule = p
					atomSal = molecule.atom(idx)
					
		
		for p,mol in enumerate(G):
			molecule = G.getMolecule(mol)
			if p != numMolecule:
				molC = mol
				atomC = molecule.atom(1)
				H.addBond([molSal, atomSal],[molC, atomC])
				
				
		
		
		#Pone las coordenadas de la mezcla en una lista
		for p,mol in enumerate(H):
			molecule = H.getMolecule(mol)
			for atom in molecule:
				coordinates = molecule.getAttributes(atom).getCoord()
				Coord.append(coordinates)
				
		#Te da los atomos que estan en la misma posicion	
		for a,coord1 in enumerate(Coord):
			#print a,coord1
			for x,coord2 in enumerate(Coord):
				if  a<x and math.fabs(coord1[0]-coord2[0])<TOLERANCE and math.fabs(coord1[1]-coord2[1])<TOLERANCE and math.fabs(coord1[2]-coord2[2])<TOLERANCE:
					overlapAtoms.append(a)
					overlapAtoms.append(x)
					toEliminate.append(x)
					
		#Te dice los vecinos de los atomos
		for mol in H:			
			molecule = H.getMolecule(mol)
			for i in range(len(overlapAtoms)/2):
				vecinos = molecule.neighbors(overlapAtoms[2*i +1]+1)
				#atomNeighbors.append(overlapAtoms[2*i+1]+1)
				atomNeighbors.append(vecinos)
		
		G = H.copy()
		
		for p,mol in enumerate(G):			
			molecule = G.getMolecule(mol)
			for i,j in enumerate(atomNeighbors):
				#print i, len(j), j[0]
							
				mol1 = mol
				atom1 = molecule.atom(overlapAtoms[2*i])
				#print atom1, "atomo 1", i
				if len(j)==1:
					atom2 = molecule.atom(j[0]-1)
					#print j[0]
					#print atom2, atom1
					H.addBond([mol1, atom1],[mol1, atom2])	
				elif len(j)==2:
					atom2A = molecule.atom(j[0]-1)
					atom2B = molecule.atom(j[1]-1)
					H.addBond([mol1, atom1],[mol1, atom2A])	
					H.addBond([mol1, atom1],[mol1, atom2B])	
					
		
		#toEliminate.sort()
		G = H.copy()	
		#print "a Eliminarse", toEliminate
		
		toEliminate = sorted(set(toEliminate))
		
		#Busca el indice del atomo Na
		for p,mol in enumerate(G):
			molecule = G.getMolecule(mol)
			for idx, atom1 in enumerate(molecule):
				if molecule.getAttributes(atom1).getInfo().getElement() == "NA":
					idxNa = idx+1
					
		#Elimina los atomos 'repetidos' y el atomo de Na
		for p,mol in enumerate(G):
			molecule = G.getMolecule(mol)
			for i in reversed(toEliminate):
				#print i+1
				molecule.removeAtom(i+1)
			molecule.removeAtom(idxNa)	
		
		Molecule.__init__(self, "Diamond", G.moleculeGenerator().next())
		
		# Fix atom types
		for atom in self:
			N = len(self.neighbors(atom))
			if N == 4:
				self.getAtomAttributes(atom).getInfo().setType("C")
			if N == 1:
				self.getAtomAttributes(atom).getInfo().setType("C2")
			if N == 2:
				self.getAtomAttributes(atom).getInfo().setType("C3")

		self.getForceField().setBond(('C','C'),  222., NonBond._EPSILON)
		self.getForceField().setBond(('C','C'),  1.512,  NonBond._SIGMA)

#==========================================================================
'''		
import sys, os

if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')
from wollfialib.chemicalGraph.molecule.Molecule import Molecule
from wollfialib.chemicalGraph.Mixture import Mixture
from conf.Wolffia_conf import WOLFFIA_WFY_DIR

#-----------------------------------------------------------------------------------
def addAndJoin(mol, cell):
	newBonds = list()
	newCell = cell.copy()
	#print "addAndJoin joining ",mol.edges() , " to ", cell.edges()
	for molAtom in mol.atoms():
		for cellAtom in newCell.atoms():
			if mol.getAtomAttributes(molAtom).distanceTo(newCell.getAtomAttributes(cellAtom)) < 0.5:
				for bondAtom in newCell.neighbors(cellAtom):
					newBonds.append([molAtom,bondAtom])
				newCell.removeAtom(cellAtom)
				
	mol.merge(newCell,bonds=newBonds)
	
	
class DiamondJSE(Molecule):
	_CELL_WIDTH_ = 3.55
	
	def __init__(self,n,m,q):
		super(Diamond,self).__init__(ident="Diamond")
		
		allCells = Mixture()
		allCells.loadWFM(WOLFFIA_WFY_DIR + "/diamond.wfm")
		#print allCells.moleculeNames()
		#print allCells.nodes()
		cell = allCells.getMolecule(allCells.nodes()[0])

		line = Molecule()
		for z in range(q):
			newCell = cell.copy()
			newCell.moveBy([0.,0.,z*self._CELL_WIDTH_])
			addAndJoin(line, newCell)

		plane = Molecule()
		for y in range(m):
			newCell = line.copy()
			newCell.moveBy([0.,y*self._CELL_WIDTH_,0.])
			addAndJoin(plane, newCell)

		for x in range(n):
			newCell = plane.copy()
			newCell.moveBy([x*self._CELL_WIDTH_,0.,0.])
			addAndJoin(self, newCell)
			print "Diamond __init__ plane",x
		#addAndJoin(self, line)
		#print allCells.enclosingBox()
		
	def __init2__(self,n,m,q):
		super(Diamond,self).__init__(ident="Diamond")
		
		allCells = Mixture()
		allCells.loadWFM(WOLFFIA_WFY_DIR + "/diamond.wfm")
		#print allCells.moleculeNames()
		#print allCells.nodes()
		cell = allCells.getMolecule(allCells.nodes()[0])

		for x in range(n):
			for y in range(m):
				line = Molecule()
				for z in range(q):
					newCell = cell.copy()
					newCell.moveBy([x*self._CELL_WIDTH_,y*self._CELL_WIDTH_,z*self._CELL_WIDTH_])
					addAndJoin(line, newCell)
				print "Diamond __init__",x,y
				addAndJoin(self, line)
		#print allCells.enclosingBox()
'''		
#==========================================================================
#==========================================================================
if __name__ == '__main__':
	d = Diamond(3,3,3)
	print d.edges()
	d.writePDB("/home/jse/Desktop/Diamantito.pdb")
	
	m = Mixture()
	m.add(d)
	m.save("/home/jse/Desktop/Diamantito.wfm")