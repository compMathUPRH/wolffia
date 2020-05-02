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
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')

import numpy as np
from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes

class Solvent(Molecule):
    '''
        Although a subclass of Molecule, Solvent is a container for the coordinates
        of many solvent molecules that can be added at once to a Mixture.
    '''

    def __init__(self, molecule, ident="Unknown"):
        print( "Solvent.__init__(): ", molecule.__class__)
        #super(Solvent, self).__init__(molecule=moleculeClass())
        #self.solventClass = moleculeClass
        super(Solvent, self).__init__(molecule=molecule)
        self.solventClass = molecule.__class__
        self.molecule = molecule.copy()

        self.coordinates = []  #list of matrices of coordinates

    def __len__(self):
        return len(self.coordinates)


    def getAtomAttributes(self, atom):
        solvAtom = atom % super(Solvent, self).order()
        molID    = int(atom / super(Solvent, self).order())
        molAttr = super(Solvent, self).getAtomAttributes(solvAtom+1) # indices in networkx start at 1
        attributes = SolventAtomAttributes(molAttr.getInfo(), self.coordinates, molID, solvAtom)
        #attributes.setCoord(self.coordinates[molID][solvAtom])
        return attributes

    def addCoordinates(self, molecule):
        ''' assumes molecule is the same as base molecule. '''
        #print("Solvent.addCoordinates molecule  {} with {} atoms.... ".format(molecule, len(molecule)))
        self.coordinates.append(np.array([molecule.getAtomAttributes(atom).getCoord() for atom in molecule.atoms()]))

    def atomsGenerator(self):
        #attributes = list(super(Solvent, self).atomsGenerator())
        print( "Solvent.atomsGenerator: ")
        try: # back compatibility
            attributes = list(self.solventClass().atomsGenerator())
        except:
            attributes = list(self.molecule.atomsGenerator())

        atom = 0
        for molCoords in self.coordinates:
            for coords in molCoords:
                attributes[atom].setCoord(coords)
                yield attributes[atom]
                atom = (atom+1) %  len(attributes)
        
    def bondsGenerator(self):
        ''' Redundant (already defined in Molecule).  Speeds-up painting.
        '''
        solvAtoms = super(Solvent, self).order()
        numMols = self.order() / solvAtoms
        edges = super(Solvent, self).edges()
        for molID in range(numMols):
            coordsPos = 0
            for par in edges:
                molAttr0 = super(Solvent, self).getAtomAttributes(par[0]) 
                molAttr1 = super(Solvent, self).getAtomAttributes(par[1]) 
                attributes0 = SolventAtomAttributes(molAttr0.getInfo(), self.coordinates, molID, coordsPos)
                attributes1 = SolventAtomAttributes(molAttr1.getInfo(), self.coordinates, molID, coordsPos)
                yield (attributes0,attributes1)
                coordsPos += 1

    #-------------------------------------------------------------
    def enclosingBox(self):
        """
        """
        boxmin = boxmax = self.coordinates[0][0]
        for molCoords in self.coordinates:
            for coords in molCoords:
                boxmin = [min(boxmin[0], coords[0]), min(boxmin[1], coords[1]), min(boxmin[2], coords[2])]
                boxmax = [max(boxmax[0], coords[0]), max(boxmax[1], coords[1]), max(boxmax[2], coords[2])]
        return [boxmin, boxmax]


    #-------------------------------------------------------------
    def isSolvent(self):  return True

    def molname(self):
        return super(Solvent, self).molname() + "(solvent)"

    def edges(self):
        #import copy

        solvBonds = [(par[0]-1, par[1]-1) for par in super(Solvent, self).edges()]  # indices in networkx start at 1
        bonds = []

        solvAtoms = super(Solvent, self).order()
        numMols = int(self.order() / solvAtoms)
        for molID in range(numMols):
            bonds += [(par[0]+solvAtoms*molID, par[1]+solvAtoms*molID) for par in solvBonds]
        return bonds

    def neighbors(self, atom):
        solvAtoms = super(Solvent, self).order()
        solvAtom = atom % solvAtoms
        baseID    = atom / solvAtoms * solvAtoms - 1
        neigh = super(Solvent, self).neighbors(solvAtom+1) # indices in networkx start at 1
        neigh = [a + baseID for a in neigh]
        return neigh


    def order(self):
        try:
            return len(self.coordinates * self.coordinates[0].shape[0])
        except:
            return 0

    def __iter__(self):
        return iter(range(self.order()))

'''
class SolventAtomIterator:
    def __init__(self, solv):
        self.max = solv.order()

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        self.count += 1
        if self.count <= self.max:
            return self.count - 1
        else:
            raise StopIteration
'''
#==========================================================================

class SolventAtomAttributes(AtomAttributes):
    def __init__(self, atomInfo, coordsTable, molID, coordsPos):
        super(SolventAtomAttributes, self).__init__(atomInfo, None)
        self.coordsPos = coordsPos
        self.coordsTable = coordsTable
        self.molID = molID

    def setCoord(self, coords):
        #if isinstance(coords, list) and isinstance(coords[0], np.ndarray): # detecting solvent, I hope we can get rid of it soon
        #    print "SolventAtomAttributes.setCoord: detecting solvent"
        #    self.coordsTable = coords
        #elif coords != None:
        #    print "SolventAtomAttributes.setCoord: coords != None"
        #    self.coordsTable[self.molID][self.coordsPos,:] = coords    
        #else:
        #    print "SolventAtomAttributes.setCoord: coords == None"

        if coords != None:
            self.coordsTable[self.molID][self.coordsPos,:] = coords    
        

    #-------------------------------------------------------------
    def getCoord(self):
        #print("SolventAtomAttributes.getCoord", self.molID, self.coordsPos)
        return self.coordsTable[self.molID][self.coordsPos,:]

#==========================================================================
if __name__ == '__main__':
    from THF import THF

    solv = Solvent(THF)
    print( type(solv.molname()))
    t = THF()
    print( type(t.molname()))
    solv = Solvent(t.__class__)
    print( solv.molname())
    solv.addCoordinates(t)
    solv.addCoordinates(t)
    print( solv.coordinates)

    print( "atomsGenerator")
    print( map(str,solv.atomsGenerator() ))

    print( "SolventAtomIterator")
    for atom in solv:
        print( atom, ": ", solv.atom_attributes(atom))

    print( "bonds")
    print( solv.bonds())
