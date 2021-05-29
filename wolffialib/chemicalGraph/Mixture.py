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


from networkx.classes.multigraph import Graph
import math, time, os, sys, numpy
import warnings
import logging

#from Bio.PDB.PDBParser import PDBParser
#import Bio.PDB
#import chemicalGraph.io.xpdb as xpdb 
#import pybel
#import openbabel
if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../')
from wolffialib.chemicalGraph.Molecule import Molecule
#from pybel import *
#from openbabel import *
from wolffialib.chemicalGraph.ChemicalGraph import ChemicalGraph
from wolffialib.chemicalGraph.AtomAttributes import AtomAttributes, AtomInfo
from wolffialib.chemicalGraph.io.PSF import PSF
from wolffialib.chemicalGraph.io.PRM import PRM


#=========================================================================
# funciones de Jordan

#------X--------------------------------------------------------------------------------------------------------
def posicion(Atomo, box,cantidad,setInBox=True):
    dx  = (box[1][0]-box[0][0])/cantidad
    dy  = (box[1][1]-box[0][1])/cantidad
    dz  = (box[1][2]-box[0][2])/cantidad
    d   = [dx,dy,dz]
    pos = []
    for i in range(3):
        if setInBox: pos.append(int((Atomo[i]-box[0][i]) / d[i])%cantidad )
        else: pos.append(math.floor((Atomo[i]-box[0][i]) / d[i]))
    return tuple(pos)

def applyPCB(Atomo, box,cantidad):
    #if Atomo[1] < box[0][1]: print "applyPCB Atomo=", Atomo, box,cantidad
    posN = posicion(Atomo, box,cantidad,setInBox=False)
    posM = posicion(Atomo, box,cantidad,setInBox=True)
    dx  = (box[1][0]-box[0][0])/cantidad
    dy  = (box[1][1]-box[0][1])/cantidad
    dz  = (box[1][2]-box[0][2])/cantidad
    d   = [dx,dy,dz]
    newCoords = []
    for i in range(3):
        difC = Atomo[i]-box[0][i]
        newCoords.append(Atomo[i]-(posN[i]-posM[i])*d[i])
        #if Atomo[i] < box[0][i] or Atomo[i] > box[1][i]: 
            #print "applyPCB final ",box
            #print "applyPCB final ", Atomo, newCoords,i, posN[i],posM[i],cantidad,(posN[i]-posM[i])*d[i]
    #if Atomo[2] < box[0][2]: print "applyPCB final ", Atomo, newCoords
    return tuple(newCoords)
    
#------X--------------------------------------------------------------------------------------------------------
def diccionario(box, listaCoordenadas, cantidad,VDW,applyPBCs=True):
        diccionario = {(a,b,c):set() for a in range(cantidad) for b in range(cantidad) for c in range(cantidad)}
        #VDW = 1.5
        dx  = (box[1][0]-box[0][0])/cantidad
        dy  = (box[1][1]-box[0][1])/cantidad
        dz  = (box[1][2]-box[0][2])/cantidad
        #print "diccionario  box=", box, "  dx", dx, "dy", dy, "dz", dz
        for AtomoL in listaCoordenadas:
            Atomo = tuple(AtomoL)
            pos   =   posicion(Atomo,box,cantidad,applyPBCs)
            if applyPBCs: aPCB = applyPCB(Atomo, box, cantidad)   
            else: aPCB = Atomo
            #print "diccionario Atomo     ", Atomo, " en pos    ", pos
            try:
                diccionario[pos].add(aPCB)
            except KeyError:
                if applyPBCs: raise
                else: continue

            for dpx in  [-1,1]:
                mdpx  = max(dpx,0)
                bx    = math.fabs(Atomo[0] - ((pos[0]+mdpx)*dx+box[0][0])) 
                if bx < VDW: 
                    diccionario[((pos[0]+dpx)%cantidad,pos[1],pos[2])].add(Atomo)

                for dpy in  [-1,1]:
                    mdpy  = max(dpy,0)
                    by    = math.fabs(Atomo[1] - ((pos[1]+mdpy)*dy+box[0][1])) 
                    if by < VDW:
                        diccionario[ (pos[0], (pos[1]+dpy)%cantidad,pos[2]) ].add(Atomo)
                    if bx < VDW and by < VDW:
                        diccionario[ ((pos[0]+dpx)%cantidad,(pos[1]+dpy)%cantidad,pos[2])].add(Atomo)
                    for dpz in  [-1,1]:
                        mdpz  = max(dpz,0)
                        bz    = math.fabs(Atomo[2] - ((pos[2]+mdpz)*dz+box[0][2]) )
                        if bz < VDW:
                            diccionario[ (pos[0], pos[1], (pos[2]+dpz)%cantidad) ].add(Atomo)
                        if bx < VDW and bz < VDW:
                            diccionario[ ((pos[0]+dpx)%cantidad,pos[1], (pos[2]+dpz)%cantidad) ].add(Atomo)
                        if by < VDW and bz < VDW:
                            diccionario[ (pos[0], (pos[1]+dpy)%cantidad,(pos[2]+dpz)%cantidad) ].add(Atomo)
                        if bx < VDW and by < VDW and bz < VDW:
                            diccionario[ ((pos[0]+dpx)%cantidad,(pos[1]+dpy)%cantidad,(pos[2]+dpz)%cantidad) ].add(Atomo)

        # convertir diccionario a listas de listas
        for pos in diccionario:
            atomos = list()
            for atom in diccionario[pos]:
                atomos.append(list(atom))
                diccionario[pos] = atomos

        return diccionario
#---------------------------------------------------------
def diccionarioOld(box, listaCoordenadas, cantidad):
        diccionario = {}
        VDW = 1.5
        dx  = (box[1][0]-box[0][0])/cantidad
        dy  = (box[1][1]-box[0][1])/cantidad
        dz  = (box[1][2]-box[0][2])/cantidad
        for Atomo in listaCoordenadas:
            #print Atomo
            pos = posicion(Atomo,box,cantidad)
            x = math.fabs  (Atomo[0]  -(pos[0]+1*dx))
            y = math.fabs  (Atomo[1]  -(pos[1]+1*dy))
            z = math.fabs  (Atomo[2]  -(pos[2]+1*dz))
            x1 = math.fabs (Atomo[0]  -(pos[0]*dx))
            y1 = math.fabs (Atomo[1]  -(pos[1]*dy))
            z1 = math.fabs (Atomo[2]  -(pos[2]*dz))
            #print "x", x, "y", y, "z", z, "x1", x1, "y1", y1, "z1", z1
            if pos not in diccionario:
                diccionario.update({pos: [Atomo]})
            else:
                diccionario[pos].append(Atomo)
            if x < VDW:
                diccionario.update({(pos[0]-1, pos[1], pos[2]): [Atomo]})
                #print "*X*"
            if y < VDW:
                diccionario.update({(pos[0], pos[1]-1, pos[2]): [Atomo]})
                #print "*Y*"
            if z < VDW:
                diccionario.update({(pos[0], pos[1], pos[2]-1): [Atomo]})
                #print "*Z*"
            if x1 < VDW:
                diccionario.update({(pos[0]+1, pos[1], pos[2]): [Atomo]})
                #print "*X1*"
            if y1 < VDW:
                diccionario.update({(pos[0], pos[1]+1, pos[2]): [Atomo]})
                #print "*Y1*"
            if z1 < VDW:
                diccionario.update({(pos[0], pos[1], pos[2]+1): [Atomo]})
                #print "*Z1*"
        return diccionario    
#------X--------------------------------------------------------------------------------------------------------
    
def distancia(puntos, newCoordinate, dmin): 
    for atom in puntos:
        d = math.sqrt (((atom[0]-newCoordinate[0])**2) + ((atom[1]-newCoordinate[1])**2) + ((atom[2]-newCoordinate[2])**2))
        #print "d=", d
        if d < dmin:
            return False
    return True

#------X--------------------------------------------------------------------------------------------------------


def distancias(puntos, newCoordinate):  
    dists = []  
    for atom in puntos:
        dists.append(math.sqrt (((atom[0]-newCoordinate[0])**2) + ((atom[1]-newCoordinate[1])**2) + ((atom[2]-newCoordinate[2])**2)))
    return dists

    
#------X--------------------------------------------------------------------------------------------------------

def _reduceNames(atomTypes):
    ''' Reduces the length of the names of the atom types. (a defect in Wolffia)
    '''
    atomTypes = sorted(atomTypes)
    redAtomTypes = [''.join([i for i in t if not i.isdigit()]) for t in  atomTypes]

    symbol = ''
    for i in range(len(redAtomTypes)):
        if symbol != redAtomTypes[i]:
            ind = 0
            symbol = redAtomTypes[i]
            continue
        redAtomTypes[i] += str(ind)
        ind += 1

    translation = {atomTypes[i]:redAtomTypes[i] for i in range(len(redAtomTypes))}
    return translation
      
#=========================================================================


class MixtureException(Exception):
    SAME_NAME = 1
    def __init__(self, errno=0, message="Mixture error."):
        self.errorNumber = errno
        self.message = message
        Exception.__init__(self)
        
class Mixture(Graph):
    """
    A Mixture is a collection of instances of the Molecule class.
    """

    _CHARACTERS = " QWERTYUIOPASDFGHJKLZXCVBNM1234567890"

    def __init__(self, mixture=None, mixName = "Unnamed"):
        Graph.__init__(self)
        self.trad= dict()
        self.atomOrder = []
        self.mixName = mixName
        #self.version = VersionControl()
        #print "Mixture__init__", self.__dict__.keys()
        self.modificationTime = time.process_time()
        #self.IDIndex   = dict()
        self.molNameIndex = dict()
        
        # new in version 0.4-23
        self.solvents = dict()
        self.trad = None
        
        
        
        #if mixture != None:
        #    raise MixtureError("Mixture copy constructor not implemented yet.")

    
    #-------------------------------------------------------------
    def __buildTranslatorTable__(self):
        """Builds translation dictionary that assigns a unique name to atom names in the mixture.
    
        This is important in order to produce correct force field files.
        Used by add() and remove() methods.  Not meant to be called manually.
        """
        start = time.process_time()
        #print "Mixture __buildTranslatorTable__ starting", time.process_time() - start, self.trad
        # build translation table
        # check consistency
        #if self.trad != None: return
        #print "Mixture __buildTranslatorTable__ empezando"
        
        indexTable     = dict()
        atomTypes = set()
        self.trad           = dict()
        #usedNames      = list()
        #typeWasRenamed = False
        writtenFF = dict()
        for molecule in self:
            mol = self.getMolecule(molecule)
            
            ff  = mol.getForceField()
            newFF = True
            for f2 in writtenFF.keys():#reuse the translation for other molecule if FFs are the same
                #print("__buildTranslatorTable__ comparacion ",  ff, f2.getForceField()," = ", ff == f2.getForceField())
                if ff == f2.getForceField():
                    self.trad[molecule] = writtenFF[f2]
                    newFF = False
                    break

            if newFF:
                self.trad[molecule] = dict()
                writtenFF[mol] = self.trad[molecule]
                #print "renameTypes in molecule ",mol.molname()
            
                for atom in mol:
                    a = mol.getAtomAttributes(atom).getInfo().typeName()
                    if not a in self.trad[molecule].keys():
                        t = a
                        #typeWasRenamed = t in usedNames
                        strFormat = "%s%0" + str(4-len(t)) + "X"
                        #if len(t) < 2: t += 'X'
                        #t = t[:2]
                        if not t in indexTable.keys(): indexTable[t] = 0
                        else: indexTable[t] += 1
                        t = strFormat % (t, indexTable[t])
                        #if len(t) > 4:
                        #    raise MixtureException("Too many atoms types " + t + " in __buildTranslatorTable__.")
                        #print "__buildTranslatorTable__  renameTypes type ", a, "->", t
                        #a.setType(t)
                        self.trad[molecule][a] = t
                        atomTypes.add(t)
                        #usedNames.append(t)
        #print("Mixture __buildTranslatorTable__ self.trad", self.trad)
        redAtomTypes = _reduceNames(atomTypes)
        atomTypes = list(atomTypes)
        for molecule in self:
            self.trad[molecule] = {k:redAtomTypes[self.trad[molecule][k]] for k in self.trad[molecule]}
        #print "Mixture __buildTranslatorTable__ self.trad", self.trad
        #print "Mixture __buildTranslatorTable__ finished", time.process_time() - start


    
        #print self.trad
    
    def _reduceTypeNames(self):
        ''' Reduces the length of the names of the atom types. (a defect in Wolffia)
        '''
        #atomTypes = set()
        atomNames = set()
        #atomFullnames = set()
        for molid in self.molecules():
            molecule = self.getMolecule(molid)
            for atom in molecule:
                #atomTypes.add(molecule.getAtomAttributes(atom).getInfo().getType())
                atomNames.add(molecule.getAtomAttributes(atom).getInfo().getName())
                #atomFullnames.add(molecule.getAtomAttributes(atom).getInfo().getFullname())

        #typeTranslation = _reduceNames(atomTypes)
        nameTranslation = _reduceNames(atomNames)
        #fullNameTranslation = _reduceNames(atomFullnames)
        #print(atomTypes,typeTranslation)
        for molid in self.molecules():
            self.getMolecule(molid).change_types(nameTranslation)

        #return typeTranslation, nameTranslation, fullNameTranslation
        return nameTranslation
      
        
    def _len(self):
        
        return self.__len__()
            

    #-------------------------------- CUSTOM METHODS --------------------------------
    def add(self, mol, checkForInconsistentNames=False):
        """
        Merges mol into self.

        @type  mol: Molecule.
        @param mol: Molecule to be added to the mixture.
        """
        from wolffialib.chemicalGraph.solvent.Solvent import Solvent
        #import inspect
        #print("Mixture.add, caller=",inspect.stack()[1])#[3]
        self.setChanged()
        #print("Mixture.add ", mol.__class__)

        #print("Mixture add", type(mol))
        #assert(isinstance(mol, Molecule))   JSE restore after rescue

        #print "Mixture.add mol.molname()", mol.molname(), checkForInconsistentNames
        nodeName = self.newMolName(mol.molname())
        self.add_node(nodeName, attrs=[mol])
        
        if checkForInconsistentNames and mol.molname()[:8] != "SOLVENT(" and not isinstance(mol, Solvent):
            self.checkExistingMoleculeNames(mol)
        
        #print "Mixture.add mol.molname() ============> added", mol.molname()
        return nodeName


    def addBond(self, atom1, atom2):
        """
        Adds a bond between two atoms.  If the atoms belong to different molecules it will merge them into one.
        
        atom1 and atom2 are two pairs  [<name of molecule>, <atom>]
        
        returns a pair of molecules: (augmentedMolecule, removedMolecule)
        """
        self.setChanged()
        #print("Mixture addBond", atom1, atom2)
        endAtom     = atom2[1]
        endMol      = self.getMolecule(atom2[0])
        startAtom   = atom1[1]
        startMol    = self.getMolecule(atom1[0])

        if atom2[0] == atom1[0]:
            startMol.addBond(startAtom, endAtom)
            return (startMol, None)
        else:
            startMol.merge(endMol, [[startAtom, endAtom]], keepTypes=False)
            self.remove(atom2[0])
            return (startMol, endMol)


    
    def angleCount(self):
        ''' Counts all angles'''
        '''
        res = 0
        for molecule in self:
            res += len(self.getMolecule(molecule).angles())
        return res
        '''
        return sum([len(self.getMolecule(molecule).angles()) for molecule in self])
    
    def atomsGenerator(self, molecules=None, atomTypes=None, elements=None, fixed=None):
        '''
        Atom generator.
        Optional parameters added to filter according to different criteria.
        Eventually this will be able to handle regular expressions.
        
        parameters:
            molecules: object that responds to the 'in' operator with names of molecules or None for all molecules.
            atomTypes, elements, fixed: sent to Molecule.atomsGenerator()
        '''
        for m in self.moleculeGenerator():
            if molecules == None or m.molname() in molecules:
                for a in m.atomsGenerator(atomTypes=None, elements=None):
                    yield a

    def bonds(self):
        res = 0
        for molecule in self.moleculeGenerator():
            res += len(molecule.bonds())
        return res


    def boundingSphere(self):
        """
        Estimates the diameter of the smallest bounding sphere containing the mixture.

        Actually, it computes the length diagonals of the containing box.
        """

        box = self.enclosingBox()
        center = [(box[0][0]+box[1][0])/2., (box[0][1]+box[1][1])/2., (box[0][2]+box[1][2])/2.]
        dx =box[0][0]-box[1][0]
        dy = box[0][1]-box[1][1]
        dz = box[0][2]-box[1][2]
        diameter = math.sqrt(dx*dx+dy*dy+dz*dz)
        return [center, diameter]


    def charge(self):
        totalCharge = 0
        for molecule in self:
            totalCharge += self.getMolecule(molecule).charge()
        return totalCharge

    def center(self):
        x,y,z = [0.,0.,0.] 
        for mol in self.moleculeGenerator():
            center = mol.center()
            order = mol.order()
            x += center[0] * order
            y += center[1] * order
            z += center[2] * order
        #print "Mixture center ", x,y,z
        return [x / self.order(), y / self.order(), z / self.order()]
    

    def checkExistingMoleculeNames(self, mol):
        '''
        renames molecule if there is another molecule in the Mixture with the same name but with different structure of force field. 
        If there is an isomorphic molecule with the same force field it changes the ff object of the new molecule to the one by the existing molecule (even for isomers!).  This make storage use more efficient and changes in the force field of one molecule is shared by all others with the same ff

        returns True if molecule was renamed AND it is a new species
        '''
        #import inspect
        #print("Mixture.checkExistingMoleculeNames, caller=",inspect.stack()[1])

        #print("checkExistingMoleculeNames starting")
        molecules = [m for m in self.moleculeGenerator() if m != mol]
        #print("Mixture.checkExistingMoleculeNames molecules: ",len(molecules))
        oldName = mol.molname()
        while molecules:  # find conflict
            existingMolecule = molecules.pop()
            #print("Mixture.checkExistingMoleculeNames ", mol.molname(),existingMolecule.molname(),existingMolecule.getForceField() == mol.getForceField(), existingMolecule.sameSpeciesAs(mol))
            if mol == existingMolecule: continue
            if existingMolecule.molname() == mol.molname() \
            and not ( existingMolecule.sameSpeciesAs(mol)  and existingMolecule.getForceField() == mol.getForceField() ):
                # new unique molecule
                mol.rename(self.newMolName(mol.molname()))
                mol.setForceField(mol.getForceField().copy())  # jse 20151130 Different molecules should not share FF
                #warnings.warn("Molecule renamed as " + mol.molname() + " since there is an isomorphic molecule named " + oldName + " with a different force field.", SyntaxWarning)
                #print("Molecule renamed as " + mol.molname() + " since there is an isomorphic molecule named " + oldName + " with a different force field.")
                return True
            if existingMolecule.getForceField() == mol.getForceField() and existingMolecule.sameSpeciesAs(mol):
                #print "checkExistingMoleculeNames", existingMolecule.getForceField()._ANGLES.keys(), mol.getForceField()._ANGLES.keys()
                #mol.rename(self.newMolName(mol.molname()))
                mol.rename(existingMolecule.molname())
                #warnings.warn("Molecule renamed as " + mol.molname() + " a similar species as " + str(existingMolecule) + " with the same forcefield.", SyntaxWarning)
                #print("Molecule renamed as " + mol.molname() + " a similar species as " + str(existingMolecule) + " with the same forcefield.")
                #raise MixtureException(MixtureException.SAME_NAME, "Non-isomorphic molecules with same name " + mol.molname())
                return True

        '''
        print("Mixture.checkExistingMoleculeNames molecules2: ",len(molecules))
        if not molecules: return False  # no problem
        
        while molecules:  # find compatible molecule
            #print("checkExistingMoleculeNames find compatible molecule")
            existingMolecule = molecules.pop()
            print("Mixture.checkExistingMoleculeNames ", mol.molname(),existingMolecule.molname(),existingMolecule.getForceField() == mol.getForceField(), existingMolecule.sameSpeciesAs(mol))
        '''
        return False

    

    def checkExistingMoleculeNamesBAK(self, mol):
        '''
        renames molecule if there is another molecule in the Mixture with the same name but with different structure of force field. 
        If there is an isomorphic molecule with the same force field it changes the ff object of the new molecule to the one by the existing molecule (even for isomers!).  This make storage use more efficient and changes in the force field of one molecule is shared by all others with the same ff

        returns True if molecule was renamed
        '''
        #import inspect
        #print "Mixture.checkExistingMoleculeNames, caller=",inspect.stack()[1]

        for existingMolecule in self.moleculeGenerator():
            #existingMolecule  = self.getMolecule(existingMoleculeID)
            #print "Mixture.checkExistingMoleculeNames, existingMolecule  = ",existingMolecule
            if existingMolecule.molname() == mol.molname() and not (existingMolecule is mol):
                #print "add existingMolecule.molname() == mol.molname()", existingMolecule.__repr__(), mol.__repr__()
                #print "add existingMolecule.molname() == mol.molname()", existingMolecule.molname(), mol.molname()
                #print "add existingMolecule.getForceField() == mol.getForceField()", existingMolecule.getForceField(), mol.getForceField()
                #print "add existingMolecule.getForceField() == mol.getForceField()", existingMolecule.getForceField().getTypes(), mol.getForceField().getTypes()
                #print "add existingMolecule.getForceField() == mol.getForceField()", existingMolecule.getForceField().__dict__, mol.getForceField().__dict__
                oldName = mol.molname()
                #print "checkExistingMoleculeNames", existingMolecule.getForceField()._ANGLES.keys(), mol.getForceField()._ANGLES.keys()
                if not existingMolecule.isIsomorphicTo(mol):
                    mol.rename(self.newMolName(mol.molname()))
                    mol.setForceField(mol.getForceField().copy())  # jse 20151130 Different molecules should not share FF
                    #print "add not existingMolecule.isIsomorphicTo(mol)", oldName, mol.molname(),  mol.getForceField()
                    warnings.warn("Molecule renamed as " + mol.molname() + " since it is not isomorphic to the existing molecule with ID " + str(existingMolecule) + ".", SyntaxWarning)
                    #raise MixtureException(MixtureException.SAME_NAME, "Non-isomorphic molecules with same name " + mol.molname())
                    return True
                elif not existingMolecule.getForceField() == mol.getForceField():
                    mol.rename(self.newMolName(mol.molname()))
                    mol.setForceField(mol.getForceField().copy())  # jse 20151130 Different molecules should not share FF
                    #for k in existingMolecule.getForceField()._ANGLES:
                    #    print k,existingMolecule.getForceField()._ANGLES[k][1], mol.getForceField()._ANGLES[k][1]
                    #raise MixtureException(MixtureException.SAME_NAME, "Isomorphic molecules with different force fields have the same names")
                    warnings.warn("Molecule renamed as " + mol.molname() + " since there is an isomorphic molecule named " + oldName + " with a different force field.", SyntaxWarning)
                    print("Molecule renamed as " + mol.molname() + " since there is an isomorphic molecule named " + oldName + " with a different force field.")
                    return True
                mol.setForceField(existingMolecule.getForceField())
                return False  # ANTES HAY QUE HACER QUE LOS DOS FF SEAN EL MISMO EN MEMORIA
        return False

    
    def createMixture(self,mixedChemicalGraph,moleculeName):       
                    
        molecules = mixedChemicalGraph.connectedComponents()     
        # finally, add the molecules to the mixture                  
        for m in molecules:
                #return 
            mol = Molecule(moleculeName, molecule=m)
            self.add(mol)         

    def countMoleculesNamed(self, molname):
        result =  list()
        for molid in self:
            result.append(self.getMolecule(molid).molname())
        return result.count(molname)


    def enclosingBox(self):
        #  CUIDADO CON boxmin y boxmax iniciales

        if self.order() == 0:
            boxmin = [0., 0., 0.]
            boxmax = [2.,2.,2.]
        else:
            molecules = list(self.nodes())
            box = self.getMolecule(molecules[0]).enclosingBox()
            boxmin = [box[0][0], box[0][1], box[0][2]]
            boxmax = [box[1][0], box[1][1], box[1][2]]
            molecules.pop(0)

            for molName in molecules:
                box = self.getMolecule(molName).enclosingBox()
                boxmin = [min(boxmin[0], box[0][0]), min(boxmin[1], box[0][1]), min(boxmin[2], box[0][2])]
                boxmax = [max(boxmax[0], box[1][0]), max(boxmax[1], box[1][1]), max(boxmax[2], box[1][2])]
        return [boxmin, boxmax]

    def equivalenceClasses(self):
        equiv = dict()
        for molid in self:
            molecule = self.getMolecule(molid)
            molName = molecule.molname()
            #print "equivalenceClasses ", molName
            if not equiv.has_key(molName):
                equiv[molName] = list()
            equiv[molName].append(molecule)
        return equiv


	#--------------------------------------------------------------------
	# If progress != None, it is an object that responds to he folowing methods:
	#   .setLabelText("Removing collisions")
	#   .setRange(0,molNum)
	#   .setValue(0)

    def fillBox(self, box, solv, molNum, checkCollisions=False, replaceCollisions=False, applyPCBs=True, progressTitle=None):
        import math, random
        import numpy as np
        from wolffialib.chemicalGraph.solvent.Solvent import Solvent
        from wolffialib.Container import Sphere, Box
        from sklearn.metrics.pairwise import euclidean_distances  # used in fillBox()
        from wolffialib.io.PrintBar import PrintBar
        
        solventMolecules = Solvent(solv)#.__class__)

        randomPoint = box.randomPoints()
        
        #calculate the volume for a single solvent molecule
        solvCenter = [0., 0., 0.]
        pos = solv.massCenter()
        solv.moveBy([solvCenter[0]-pos[0], solvCenter[1]-pos[1], solvCenter[2]-pos[2]])
        solvDiameter = math.pow(box.getBoxVolume() / molNum, 1./3.)
        if solvDiameter == 0: return
        
        progressMax   = molNum
        progressCount = 0
        if progressTitle != None:    
            progress = PrintBar(0, progressMax)
            progress.setLabelText(progressTitle)
            progress.setRange(0,molNum)
            progress.setValue(0)
        else:
            progress = None
        
        solvRadius = solvDiameter / 2
        newPos = solv.massCenter()
        
        # lopps over a sequence of adding solvent and removing collisions
        originalCoords = self.getAtomsCoordinatesAsArray()
        solvRadius = solvDiameter / 2.0 + 1.5
        
        #print("fillBox solvent {} with {} atoms.... ".format(solv, len(solv)))
        #print("fillBox anadiendo... ", progressMax-progressCount, ': ', end=', ')
        while progressCount < progressMax:  # adds solvent
            #random rotation for solvent atoms
            rx = random.uniform(0, 360)
            ry = random.uniform(0, 360)
            rz = random.uniform(0, 360)
            
            #random displacement for solvent atoms
            newPos = next(randomPoint)
           
            #generate new molecule and assign next position
            mol = solv.copy()
            mol.rotateDeg(rx, ry, rz)
        
            if checkCollisions and len(originalCoords) > 0:
                #print("fillBox: " , originalCoords.shape, newPos.shape)
                atomDistances = euclidean_distances(originalCoords, [newPos])

                if np.min(atomDistances) > solvRadius:
                    #print 'fillBox: añadiendo', progressCount, np.min(atomDistances), newPos
                    mol.moveBy(newPos)
                    #nodeName = self.addMolecule(mol, checkForInconsistentNames=False)
                    #self.shownMolecules.show(nodeName)
                    solventMolecules.addCoordinates(mol)
                else:
                    if replaceCollisions: progressCount -= 1
            else:
                mol.moveBy(newPos)
                solventMolecules.addCoordinates(mol)
        
            progressCount += 1
            if progress != None:    progress.setValue(progressCount)
            del mol
            #print("{} ({})".format(progressCount,len(solventMolecules)), end=', ')
        #print()
        
                
        # add solvent and rename with the given name
        nodeName = self.add(solventMolecules, checkForInconsistentNames=True)
        #self.shownMolecules.show(nodeName)
        #print "fillBox ", mol.molname(),progressMax
        solv.rename(solventMolecules.molname())
        progressMax -= 1
        if progress != None: progress.close()

        
        
    def fixSelection(self, value=True, **kwargs):
        for mol in self.molecules():
            self.getMolecule(mol).fixSelection(value=value, **kwargs)
            
    def getMixtureName(self):
        return self.mixName


    def getModificationTime(self):
        if not self.__dict__.has_key('modificationTime'):
            self.modificationTime = time.process_time()
        return self.modificationTime

    
    def getMolecule(self, name):
        """
        Returns molecule with given name.

        @type  name: Mixture.
        @param name: name of the molecule.

        @rtype:  Molecule
        @return: Molecule with given name.
        """
        return self.node_attributes(name)[0]


    def getMoleculeID(self, molecule):
        for n in self.nodes():
            #print("getMoleculeID =", n)
            if self.getMolecule(n) == molecule:
                return n
        return None
    
    def getSolvent(self):
        s = set()
        for mol in self.moleculeGenerator():
            if mol.isSolvent(): s.add(mol)
        return s

    def hasMoleculeID(self, m): return m in self.nodes()
    
    def duplicateMolecule(self, molName):
        self.setChanged()
        newMol = Molecule(molecule=self.getMolecule(molName))
        newMol.moveBy([0.,3.,0.])
        return self.add(newMol)

    def loadWFM(self, filename):
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("Loading molecule from " + filename)
        
        #print("Mixture.load_ importing cPickle")
        import pickle #Tremenda aportación por carlos cortés
        #print "History.load_ imported cPickle, starting to load"

        mix = Mixture()
        with open(filename, "rb") as f:
            try:
                mix = pickle.load(f)
            except UnicodeDecodeError:
                mix = pickle.load(f, encoding='latin1')
        #print("loadWFM mix", mix)
		
        f.close()
		
        self.merge(mix, checkForInconsistentNames=False)
        self.setChanged()
            
    def loadOldWFM(self, filename):
        ''' Loads WFM files pickled with Python2
        '''
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("Loading molecule from " + filename)
        
        print("Mixture.load_ importing cPickle")
        import pickle 
        
        mix = Mixture()
        with open(filename, "rb") as f:
            mix = pickle.load(f, encoding='latin1')
        for mol in mix['node']:
            print(mol)
            self.add(mix['node'][mol]['attrs'])
        f.close()
        self.setChanged()
            
    def readFileBAK(self, moleculeFile,fileType=None):
        if fileType == None:
            fileType = os.path.splitext(moleculeFile)[1][1:].strip() # get filename extension
        #print "Mixture.readFile reading", moleculeFile,fileType
        return pybel.readfile(fileType, moleculeFile).next()
    
    def readStringBAK(self, fileContents, fileType=None):
        if fileType == None:
            fileType = "pdb" # a completely arbitrary assumption
        return pybel.readstring(fileType, fileContents)
            
            
    def load(self, pdbFile=None,psfFile=None,moleculeFile=None,fileType=None,id=None):
        """
        Loads a single frame in the coordinate file and merges the content to the current 
        mixture.
        The contents of the pdbFile could be in any format supported by    pyBel.   
        Connectivity will be determined by the PSF file is present.
        moleculeFile should have the content of the coordinate file if pdbFile == None.
        """
        from wolffialib.io.CoordinateFile import CoordinateFile, CoordinateString

        if pdbFile != None:
            reader = CoordinateFile(pdbFile,fileType,psfFile,id)
        else:
            #print "Mixture load ", fileType
            reader = CoordinateString(moleculeFile,id,fileType)

        self.merge(reader.next())
        

    def loadBAK(self, pdbFile=None,psfFile=None,moleculeFile=None,fileType=None,id=None):
        """
        Loads and parses the coordinate file (pdbFile could be in any format supported by
        pyBel).   
        Connectivity will be determined by the PSF file is present.

        @type  pdbFile: string
        @param pdbFile: PDB filename.
        """

        self.setChanged()

        if not(pdbFile == None):
            #mol          = pybel.readfile("pdb", pdbFile).next()
            mol          = self.readFile(pdbFile,fileType)
            moleculeName = os.path.basename(pdbFile).split('.')[0]
            
            
        elif not(moleculeFile == None):
            mol          = self.readString(moleculeFile, fileType)
            
            if fileType   == "pdb" and not(id==None): 
                moleculeName = id+"_PDB"
                
            elif fileType == "sdf" and not(id==None): 
                moleculeName = id+"_NCI-CADD"
                
            else: 
                moleculeName = "loadedPDB"
        atoms               = mol.atoms
        #print"cant. atomos = ",len(atoms)              
        flag                = False

        chemicalGraphMixed  = ChemicalGraph()
        # add nodes
        etable              = openbabel.OBElementTable()
            


        if not(psfFile == None):
            psf=PSF(psfFile)

            if len(atoms) != len(psf.atoms):
                raise MixtureError("Ammount of atoms in "+pdbFile + " and "+psfFile + " files are different ("+str( len(atoms))+" vs "+str(len(psf.atoms))+").")
            flag = True
            bonds = psf.bonds
            
        for n in range(len(atoms)):
            atom=atoms[n]                
            atomType = atom.type # Hay que revisar esto, aqui debe ir otra cosa
            symbol   = etable.GetSymbol(atom.atomicnum)
            coords   = list(atom.coords)
            #print "Mix load", coords
            name     = etable.GetName(atom.atomicnum) 
            residue  = atom.OBAtom.GetResidue().GetName()
            psfType  = atom.type
            charge   = atom.partialcharge
            mass     = atom.atomicmass    
            if flag:
                psfType  = psf.getType(n)
                charge   = psf.getCharge(n)
                mass     = psf.getMass(n)


            atr = AtomAttributes(    atomType, symbol, psfType, coords, charge, mass, 1, 1, 1, name, residue)
            chemicalGraphMixed.add_node(n+1, attrs=[atr])

        # add edges

        if flag:
            for b in bonds:
                #if progress.wasCanceled():
                    #print "fillBox cancelado"
                    #self.setChanged() Como hacer un back a esto?
                    #progress.hide()
                    #return
                try:  # avoids adding an edge twice
                    chemicalGraphMixed.add_edge(b)
                except AdditionError:
                    pass            
                #progressCount += 1
                #progress.setValue(progressCount)
        else:            
            for bond in openbabel.OBMolBondIter(mol.OBMol):   
                chemicalGraphMixed.add_edge([bond.GetBeginAtom().GetIdx(),bond.GetEndAtom().GetIdx()])       
                    
        molecules = chemicalGraphMixed.connectedComponents()      
        # finally, add the molecules to the mixture                  
        for m in molecules:
                #return 
            mol = Molecule(moleculeName, molecule=m)
            self.add(mol)         


    def loadAndInffer(self, pdbFile, prmFile):
        """
        Loads and parses PDB coordinate file and PSF topology file containing molecules.

        @type  pdbFile: string
        @param pdbFile: PDB filename.

        @type  psfFile: string
        @param psfFile: PDB filename.
        """
        self.setChanged()
        
        structure = PDBParser(PERMISSIVE=True).get_structure("ChemicalGraph", pdbFile)
        atomsGen=structure.get_atoms()
        atoms = [a for a in atomsGen]
        # residues = [r.get_resname() for r in structure.get_residues()]
        # chains = [c for c in structure.get_chains()]
        prm=PRM(prmFile)
        # print len(atoms), " != ", len(psf.atoms)
        #print "PDB atoms ",atoms
        #print "PSF atoms ",psf.atoms
        # print psf.atoms
        if len(atoms) != len(psf.atoms):
            raise MixtureError("Ammount of atoms in "+pdbFile + " and "+psfFile + " files are different ("+str( len(atoms))+" vs "+str(len(psf.atoms))+").")

        mixed = ChemicalGraph()

        # add nodes
        # elements = psf.get_elements()
        # charges = psf.get_charges()
        # masses = psf.get_masses()
        for n in range(len(atoms)):
            atom=atoms[n]
            #print "llamada a AtomAttributes", [elements[n], atom.get_coord(), charges[n], masses[n]]
            atr = AtomAttributes(    atom.get_name(), atom.element, psf.getType(n), atom.get_coord(), psf.getCharge(n), psf.getMass(n), 
                        atom.get_bfactor(), atom.get_occupancy(), atom.get_altloc(), 
                        atom.get_fullname(),atom.get_parent().get_resname())
            #print "----------------------->", str(atr)
            mixed.add_node(n+1, attrs=[atr])

        # add edges
        for n1 in range(len(atoms)):
            for n2 in range(n1+1,len(atoms)):
                key1 = mixed.getAttributes(atoms[n1]).getType() + ' ' + mixed.getAttributes(atoms[n2]).getType()
                key2 = mixed.getAttributes(atoms[n2]).getType() + ' ' + mixed.getAttributes(atoms[n1]).getType()
                if prm["BOND"].hasKey(key1):
                    d = mixed.getAtomAttributes(atoms[n1]).distanceTo(mixed.getAtomAttributes(atoms[n2]))
                elif prm["BOND"].hasKey(key2):
                    d = mixed.getAtomAttributes(atoms[n1]).distanceTo(mixed.getAtomAttributes(atoms[n2]))
                else:
                    d = 1000
                if abs(d - prm["BOND"][1]) < 0.1:
                    try:  # avoids adding an edge twice
                        mixed.add_edge([n1,n2])
                    except AdditionError:
                        pass

        # add everything else
        #mixed.add_angles(psf.get_angles())
        #mixed.add_dihedrals(psf.get_dihedrals())

        # print "attr prev connectedComponents=", mixed.atoms_attributes()
        molecules = mixed.connectedComponents()
        # print "connectedComponents=", molecules

        # finally, add the molecules to the mixture
        count = self.order() + 1
        for m in molecules:
            #mol = Molecule(pdbFile+"("+str(count)+")", molecule=m)
            #mol = Molecule("mol_"+str(count), molecule=m)
            mol = Molecule("loadedPDB", molecule=m)
            self.add(mol)
            count += 1


    def merge(self, mix, checkForInconsistentNames=True):
        '''
        Merge two mixtures.
        '''
        self.setChanged()
        for mol in mix:
            #print("Mixture.merge merging ", mix.getMolecule(mol).molname())
            self.add(mix.getMolecule(mol), checkForInconsistentNames)

    
    def moleculeNames(self):
        result =  set()
        for molid in self:
            result.add(self.getMolecule(molid).molname())
        return result


    def molecules(self):
        return self.moleculeIDs()
    
    def moleculeGenerator(self):
        '''
        Generator of molecules in mixture.  (New in v1.137)
        '''
        for mol in self:
            yield self.getMolecule(mol)
            
    def moleculeIDs(self):
        return self.nodes()  


    def moveBy(self, displ):
        for molecule in self:
            self.getMolecule(molecule).moveBy(displ)
            

    def newMolID(self, molid):
        #print "newMolID ", self.__dict__
        self.setChanged()
        if self.IDIndex.has_key(molid):
            self.IDIndex[molid] += 1
        else:
            self.IDIndex[molid] = 1
        return molid + "_" + str(self.IDIndex[molid])


    def newMolName(self, molname):
        #print "newMolName ", molname, self.molNameIndex.keys()
        self.setChanged()
        if molname in self.molNameIndex:
            #print "newMolName ",self.molNameIndex[molname] 
            self.molNameIndex[molname] += 1
        else:
            self.molNameIndex[molname] = 1
        return molname + "_" + str(self.molNameIndex[molname])
    
    
    def node_attributes(self, molid):
        #print("node_attributes", self.nodes.keys())
        return self.nodes[molid]['attrs']


    def overlapingMolecules(self, refMolNames, pbc=None, applyPBCs=True):
        """
        Finds all the molecules overlapping a given molecule.
        pbc = periodic boundary conditions (class Drawer)   (new in version 1.136)
        """
        from wolffialib.chemicalGraph.ForceField import ForceField, NonBond
        cantCajas = 8

        faces = pbc.getFaces()
        #print "overlapingMolecules face=", faces
        box = [[faces[0],faces[2],faces[4]],[faces[1],faces[3],faces[5]]]

        #print "sacando coordenadas"
        listaCoordenadas = []
        maxVDW = 1.5
        for refMolName in refMolNames:
            refMol = self.getMolecule(refMolName)
            # sacar lista de atomos de molecula refMol
            for atom2 in refMol:
                vdWr1 = refMol.getForceField().nonBond(refMol.getAtomAttributes(atom2).getInfo().getType())[NonBond._SIGMA] 
                maxVDW = max(maxVDW, vdWr1)
                listaCoordenadas.append(refMol.getAtomAttributes(atom2).getCoord())

        #print "crear diccionario de cajas"
        #crear diccionario de cajas con la lista listaCoordenadas
        # JORDAN
        atomosEnSubCajas = diccionario(box, listaCoordenadas, cantCajas, maxVDW * 2, applyPBCs)
        #print "diccionario", atomosEnSubCajas
                  


        #print "busca moleculas en self que chocan"
        # busca moleculas en self que chocan y las anade a collidingMolecules
        collidingMolecules = set()
        progreso = 0
        for mol in self:
            progreso += 1
            #if progreso % 100 == 0: print "overlaping, ", progreso, " de ", len(self)
            if not (mol in refMolNames):
                m = self.getMolecule(mol)
                atoms = m.atoms()
                for atom in atoms:
                    acoordinates = m.getAtomAttributes(atom).getCoord()
                    #acoordinates = applyPCB(m.getAtomAttributes(atom).getCoord(), box, cantCajas)
                    #vdWr1 = m.getForceField().nonBond(m.getAtomAttributes(atom).getInfo().getType())[NonBond._SIGMA]
                    # determinar si acoordinates chocan con alguien en diccionario de listaCoordenadas
                    # JORDAN
                    pos = posicion(acoordinates, box, cantCajas)
                    if atomosEnSubCajas.has_key(pos): 
                        pruebaDistancia = distancia(atomosEnSubCajas[pos], acoordinates, 1.3)
                        #print "distancias: ", acoordinates, distancias(listaCoordenadas, acoordinates)
                        
                        #si choca entonces anade
                        if pruebaDistancia == False:
                            collidingMolecules.add(mol)
                    
        return collidingMolecules
    
    def overlapingMolecules3(self, refMolName, pbc=None):
        """
        Finds all the molecules overlapping a given molecule.
        pbc = periodic boundary conditions (class Drawer)   (new in version 1.136)
        """
        
        refMol = self.getMolecule(refMolName)
        
        faces = pbc.getFaces()
        #print "overlapingMolecules face=", faces
        box = [[faces[0],faces[2],faces[4]],[faces[1],faces[3],faces[5]]]
        
        # sacar lista de moleculas de molecula refMol
        listaCoordenadas = []
        for atom2 in refMol:
            listaCoordenadas.append(refMol.getAtomAttributes(atom2).getCoord())
        
        #crear diccionario de cajas con la lista listaCoordenadas
        # JORDAN
        atomosEnSubCajas = diccionario(box, listaCoordenadas, 11)
                  
    
    
        
        # busca moleculas en self que chocan y las anade a collidingMolecules
        collidingMolecules = set()
        for mol in self:
            if mol != refMolName:
                m = self.getMolecule(mol)
                atoms = m.atoms()
                vdWr1 = m.getForceField().nonBond(m.getAtomAttributes(atom).getInfo().getType())[NonBond._SIGMA] 
                for atom in atoms:
                    acoordinates = m.getAtomAttributes(atom).getCoord()
                    vdWr2 = refMol.getForceField().nonBond(refMol.getAtomAttributes(atom2).getInfo().getType())[NonBond._SIGMA] 
                    #vdWr1 = m.getForceField().nonBond(m.getAtomAttributes(atom).getInfo().getType())[NonBond._SIGMA]
                    # determinar si acoordinates chocan con alguien en diccionario de listaCoordenadas
                    # JORDAN
                    pruebaDistancia = distancia(listaCoordenadas, acoordinates, vdWr1 + vdWr2)
                    #print "distancias: ", acoordinates, distancias(listaCoordenadas, acoordinates)
                    
                    #si choca entonces anade
                    if pruebaDistancia == False:
                        collidingMolecules.add(mol)
                    
        return collidingMolecules
    

    def overlapingMoleculesCOPIA2(self, refMolName, pbc=None):
        """
        Finds all the molecules overlapping a given molecule.
        pbc = periodic boundary conditions (class Drawer)   (new in version 1.136)
        """
        refMol = self.getMolecule(refMolName)
        
        faces = pbc.getFaces()
        box = [[faces[0],faces[2],faces[4]],[faces[1],faces[3].faces[5]]]
        
        # sacar lista de moleculas de molecula refMol
        listaCoordenadas = []
        for atom2 in refMol:
            listaCoordenadas.append(refMol.getAtomAttributes(atom2).getCoord())
        #crear diccionario de cajas con la lista listaCoordenadas
        # JORDAN
        
        
                
        
        
        # busca moleculas en self que chocan y las anade a collidingMolecules
        """
            collidingMolecules = set()
                for mol in self:
                    m = self.getMolecule(mol)
                    atoms = m.atoms()
                    for atom in atoms:
                        acoordinates = m.getAtomAttributes(atom).getCoord()
                        # determinar si acoordinates chocan con alguien en diccionario de listaCoordenadas
                    
                
                
                
                # JORDAN
                
                #si choca entonces anade
                if JORDAN:
                    collidingMolecules.add(mol)
                    
        
        return collidingMolecules
        
        1"""

    def overlapingMoleculesCopia(self, refMolName, pbc=None):
        """
        Finds all the molecules overlapping a given molecule.
        pbc = periodic boundary conditions (class Drawer)   (new in version 1.136)
        """
        from wolffialib.chemicalGraph.ForceField import ForceField, NonBond
        refMol = self.getMolecule(refMolName)
        # the enclosing box aims to easily discard molecules that are too far
        '''
        refBox = refMol.enclosingBox()
        refBox[0][0] -= 1.5
        refBox[0][1] -= 1.5
        refBox[0][1] -= 1.5
        refBox[1][0] += 1.5
        refBox[1][1] += 1.5
        refBox[1][1] += 1.5
        '''
        ml = set()
        for mol in self:
            #print "overlapingMolecules ", mol
            m = self.getMolecule(mol)
            atoms = m.atoms()
            collides = False
            for atom in atoms:
                ac = m.getAtomAttributes(atom).getCoord()
                #if (ac[0] >= refBox[0][0] and ac[0] <= refBox[1][0]) and (ac[1] >= refBox[0][1] and ac[1] <= refBox[1][1]) and (ac[2] >= refBox[0][2] and ac[2] <= refBox[1][2]): 
                vdWr1 = m.getForceField().nonBond(m.getAtomAttributes(atom).getInfo().getType())[NonBond._SIGMA] 
                for atom2 in refMol:
                    d = m.getAtomAttributes(atom).distanceTo(refMol.getAtomAttributes(atom2),pbc)
                    vdWr2 = refMol.getForceField().nonBond(refMol.getAtomAttributes(atom2).getInfo().getType())[NonBond._SIGMA] 
                    if 2*d < vdWr1 + vdWr2:
                        #print m.getAtomAttributes(atom).getType(),refMol.getAtomAttributes(atom2).getType(),(vdWr1 + vdWr2)/2
                        ml.add(mol)
                        collides = True
                        break
                if collides: break
        #print "overlapingMolecules ", len(ml)
        return ml


    def order(self):
        res = 0
        for molecule in self:
            res += self.getMolecule(molecule).order()
        return res
        #return sum([self.getMolecule(molecule).order() for molecule in self])

    def atomsCount(self):
        return self.order()
    
    
    #def readFiles(self, pdbFile=None,psfFile=None,moleculeFile=None,fileType=None,id=None):
        """
        Loads and parses PDB coordinate file.
        
        @type  pdbFile: string
        @param pdbFile: PDB filename.
        """
        '''
        import openbabel.pybel
        import openbabel.openbabel as ob
        
        print("readFiles ",pdbFile )
        self.setChanged()
        if not(pdbFile == None):
            mol          = next(openbabel.pybel.readfile("pdb", pdbFile))
            moleculeName = os.path.basename(pdbFile).split('.')[0]
        elif not(moleculeFile == None):
            mol          = openbabel.pybel.readstring(fileType, moleculeFile)
            
            if fileType   == "pdb" and not(id==None): 
                moleculeName = id+"_PDB"
                
            elif fileType == "sdf" and not(id==None): 
                moleculeName = id+"_NCI/CADD"
                
            else: 
                moleculeName = "loadedPDB"
        atoms               = mol.atoms             
        flag                = False

        
        print("readFiles mol ",mol )
        chemicalGraphMixed  = ChemicalGraph()
        # add nodes
        #etable              = ob.OBElementTable()
            
        
        
        if psfFile != None:
            psf=PSF(psfFile)
        
            if len(atoms) != len(psf.atoms):
                raise MixtureError("Ammount of atoms in "+pdbFile + " and "+psfFile + " files are different ("+str( len(atoms))+" vs "+str(len(psf.atoms))+").")
            bonds = psf.bonds
        else: psf = None
        
        for n in range(len(atoms)):
            print("readFiles atoms[n] ",atoms[n]  )
            
            atom=atoms[n]                
            atomType = atom.type # Hay que revisar esto, aqui debe ir otra cosa
            print("readFiles atomType ",atomType)
            symbol   = ob.GetSymbol(atom.atomicnum)
            print("readFiles symbol ",symbol)
            coords   = list(atom.coords)
            #print "Mix load", coords
            print("readFiles coords ",coords)
            name     = ob.GetName(atom.atomicnum) 
            residue  = atom.OBAtom.GetResidue().GetName()
            psfType  = atom.type
            charge   = atom.partialcharge
            print("readFiles charge ",charge)
            mass     = atom.atomicmass    
            if psf:
                psfType  = psf.getType(n)
                charge   = psf.getCharge(n)
                mass     = psf.getMass(n)
                
            ainf = AtomInfo(atomType, symbol, psfType, charge, mass, 1, 1, 1, name, residue)
            atr = AtomAttributes(ainf, coords)
            chemicalGraphMixed.add_node(n+1, attrs=[atr])
            print("readFiles chemicalGraphMixed ", len(chemicalGraphMixed))
           
        # add edges
        
        if psf:
            for b in bonds:
                 print("readFiles bonds ", b)
                 try:  # avoids adding an edge twice
                    chemicalGraphMixed.add_edge(b)
                 except Exception:
                     pass
        else:          
            for bond in openbabel.OBMolBondIter(mol.OBMol):   
                chemicalGraphMixed.add_edge([bond.GetBeginAtom().GetIdx(),bond.GetEndAtom().GetIdx()])

        print("readFiles chemicalGraphMixed ", len(chemicalGraphMixed))
        print("readFiles moleculeName ",moleculeName )
        return chemicalGraphMixed, moleculeName  
        '''
  
                            
    def remove(self, molID):
        """
        Removes molecule with molname  (first found)

        @type  molname: String.
        @param molname: name of Molecule to be added to the mixture.
        """
        #import inspect
        #print "Mixture.remove, caller=",inspect.stack()[1]
        #print "Mixture.remove", molID, "\'"+self.getMolecule(molID).molname()+"\'" ,self.moleculeNames()
        #print "remove self.molNameIndex.keys()", molID, self.molNameIndex.keys()
        self.setChanged()

        mol = self.getMolecule(molID)
        #try:
            #mol = self.getMolecule(molID)
        #except KeyError:
            #print "Mixture.remove(): Tried to remove ineistent molecule ", molID
            #return  #nothing to remove

        molname = mol.molname()
        self.remove_node(molID)
        if not molname in self.moleculeNames() and molname in self.molNameIndex.keys():
            del self.molNameIndex[molname]
            #print "remove deleted", mol.molname(), self.molNameIndex.keys()

        #self.__buildTranslatorTable__()

    def removeFrom(self, molIDs):
        """
        Removes molecules in  molIDs

        @type  molIDs: iterable container of molecules IDs.
        @param molIDs: IDs of Molecules to be removed from the mixture.
        """
        """
        for id in molIDs: self.remove(id)
        """
        self.setChanged()

        #molnames = [self.getMolecule(molID).molname() for molID in molIDs]
        self.remove_nodes_from(molIDs)
        """
        for molname in molIDs:
            if not molname in self.moleculeNames() and molname in self.molNameIndex.keys():
                del self.molNameIndex[molname]
                print "remove deleted", molname, self.molNameIndex.keys()
        """

        #self.__buildTranslatorTable__()

    def removeAtomsFromSphere(self, diameter, shownMolecules):
        self.setChanged()
        endAtom   = diameter[1][1]
        endMol    = self.getMolecule(diameter[1][0])
        coord     = [(diameter[0][2][0]+diameter[1][2][0])/2., (diameter[0][2][1]+diameter[1][2][1])/2., (diameter[0][2][2]+diameter[1][2][2])/2.]

        #dummy atom as center of sphere
        centerAt  = AtomAttributes( AtomInfo('', '', '', 0,0),coord)

        radius    = centerAt.distanceTo(endMol.getAtomAttributes(endAtom))
        #shownMolecules
        #print 'removeAtomsFromSpherev centerAt',diameter,coord,radius,shownMolecules

        #for molName in shownMolecules:
        for currentMolecule in shownMolecules.shownList(None):
            #currentMolecule = self.getMolecule(molName)
            molName = self.getMoleculeID(currentMolecule)
            if molName != None:
                molecules       = currentMolecule.removeAtomsFromSphere(coord, radius)
                #print 'removeAtomsFromSphere',molName, [m.molname() for m in molecules]
                #print 'Mixture.removeAtomsFromSphere',molName, currentMolecule.getForceField().getTypes()
                
                # finally, add the pieces to the mixture
                for m in molecules:
                    mol = Molecule(currentMolecule.molname(), molecule=m)
                    #print "removeAtomsFromSphere  pieces" , m,mol.order()
                    mol.setForceField(currentMolecule.getForceField())
                    self.add(mol)
                self.remove(molName)
                shownMolecules.remove(currentMolecule)
        del centerAt
        
    def removeBonds(self, molecule, edgesList,shownMolecules=[]):
        """
        Remove bonds.  Removing bonds may split or empty molecules.

        @type  edgesList: list of tuples of 2 atoms.
        @param edgesList: list of bonded atoms.
        """
        #print "Mixture.removeBonds recibio mezla con ", len(self.molecules()), " moleculas", self.bonds(), " enlaces"
        newMolecules = self.getMolecule(molecule).removeBonds(edgesList)
        currentMolecule = self.getMolecule(molecule)
        self.remove(molecule)
        shownMolecules.updateMixture(self)
        #print "Mixture.removeBonds tiene ", len(self.molecules()), " moleculas", self.bonds(), " enlaces lugo de remover"
        # finally, add the pieces to the mixture
        for m in newMolecules:
            mol = Molecule(currentMolecule.molname(), molecule=m)
            mol.setForceField(currentMolecule.getForceField())
            self.add(mol)
        #print "Mixture.removeBonds tiene ", len(self.molecules()), " moleculas", self.bonds(), " enlaces luego de reanadir"

        
    def renameMolecule(self, molID, newName):
        '''
        Renames molecule and checks for consistency
        '''
        import inspect
        self.setChanged()
        #print "Mixture.renameMolecule, caller=",inspect.stack()[1][3]
        self.getMolecule(molID).rename(newName)
        self.checkExistingMoleculeNames(self.getMolecule(molID))
        
        
    def rotateDeg(self, angleX, angleY, angleZ):
        for molecule in self:
            self.getMolecule(molecule).rotateDeg(angleX, angleY, angleZ)

    def save(self, filename):

        #print "Mixture.save_ importing cPickle"
        import cPickle as pickle #Tremenda aportación por carlos cortés.
        #print "Mixture.save_ imported cPickle, starting to save"
        f = open(filename, "w")
        pickle.dump(self.__dict__, f)
        f.close()
        #print "Mixture.save_ imported cPickle, save sucessful"

            
    def setChanged(self):
        '''
        should be calld when the composition of the mixture changes.
        '''
        self.modificationTime = time.process_time()
        self.trad = None

        #print "setChanged",self.modificationTime
    

    def setMixtureName(self, n):
        self.setChanged()
        self.mixName = n


    def updateCoordinates(self, filename):
        """
        Update the coordinates of the mixture.  It is meant to load results from simumations.

        @type: string
        @param: coordinates file's name
        """
        import numpy as np
        #print "Mixture updateCoordinates "
        self.setChanged()
        if isinstance(filename, str):
            f = open(filename, "r")
        else:
            f = filename
        
        updateInfo = []
        num = 0
        for line in f:
            if line[:4] == "ATOM" or line[:6] == "HETATM":
                try:
                    #num = int(line[6:11])-1 # produces error when system has more than 99999 atoms
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    #print ("Mixture.updateCoordinates ", num,x,y,z)
                    #self.atomOrder[num].setCoord([x,y,z])
                    updateInfo.append([num,x,y,z])
                    num += 1
                except (IndexError,ValueError):
                    print("Mixture.updateCoordinates failed to update atom ",num)
                    break
        if len(updateInfo) != self.atomsCount():
            print(len(updateInfo), self.number_of_nodes())
            raise MixtureError("Inconsistent atom counts between mixture and read file in Mixture.updateCoordinates().")
        for atom in updateInfo:
            molecule, atomNum = self.atomOrder[atom[0]]
            self.getMolecule(molecule).setAtomCoordinates(atomNum,np.array([atom[1],atom[2],atom[3]]))
            #print ("Mixture.updateCoordinates 2 ", atom[0],atom[1],atom[2],atom[3])
            
        f.close()


    def updateCoordinatesFromArray(self, coordsArray):
        import numpy as np
        #start = time.process_time()
        #print("Mixture updateCoordinatesFromArray len(coordsArray)", len(coordsArray))
        for i in range(self.order()):
            try:
                #print "updateCoordinatesFromArray ", i
                p = 3*i
                x = coordsArray[p]
                y = coordsArray[p+1]
                z = coordsArray[p+2]
                #print("updateCoordinatesFromArray xyz", x,y,z)
                #self.atomOrder[i].setCoord([x,y,z])
                molecule, atomNum = self.atomOrder[i]
                self.getMolecule(molecule).setAtomCoordinates(atomNum,np.array([x,y,z]))
            except (IndexError,ValueError):
                print("Mixture.updateCoordinatesFromArray failed to update atom ",i)
                break
        #print "updateCoordinatesFromArray finished time=", time.process_time() - start
            

    def getAtomsCoordinatesAsArray(self):
        import numpy as np
        coordArray = np.empty((self.order(), 3))
        i = 0
        for molecule in self:
            mol = self.getMolecule(molecule)
            for atom in mol:
                atr = mol.getAtomAttributes(atom)
                #print 'getAtomsCoordinatesAsArray: ', i
                coordArray[:i,:] = atr.getCoord()
                i += 1

        return coordArray

    def updateMixture(self,mix):
        self.setChanged()
        self.__dict__ = mix.__dict__
        #for mol in self:
        #    print "mix @t NanoCADState",self.mixture.getMolecule(mol)._name

    def upgrade(self, version):
        #print "Mixture update ", version
        if version < "1.137":
            from wolffialib.chemicalGraph.AtomAttributes import AtomAttributes,AtomInfo
            for mol in self:
                molecule = self.getMolecule(mol)
                molecule.atomTypesTable = dict()
                for atom in molecule:
                    a = molecule.getAtomAttributes(atom)
                    t = AtomInfo(a._name,a._element,a._type,a._charge,a._mass,fullname = a._fullname,res=a._residue,chain=a._chain,res_seq = a._res_seq)
                    molecule.setAtomAttributes(atom,AtomAttributes(t,numpy.array(a.getCoord())))
                molecule.getForceField().upgrade(version)

        if version < "1.31":
            #print "Mixture update 1.31"
            from wolffialib.chemicalGraph.AtomAttributes import AtomAttributes,AtomInfo
            for mol in self:
                molecule = self.getMolecule(mol)
                molecule.atomTypesTable = dict()
                for atom in molecule:
                    ai = molecule.getAtomAttributes(atom).getInfo()
                    ai.setCharge(molecule.getForceField().nonBond(ai.getType())[2])
                    #print "Mixture update ", ai.getType(), molecule.getForceField().nonBond(ai.getType()),ai.getCharge()
                    #t = AtomInfo(a._name,a._element,a._type,a._charge,a._mass,fullname = a._fullname,res=a._residue,chain=a._chain,res_seq = a._res_seq)
                    #molecule.setAtomAttributes(atom,AtomAttributes(t,numpy.array(a.getCoord())))
                molecule.getForceField().upgrade(version)

    def writeFiles(self,baseFilename, fixedMolecules=[], progressTitle=None):
        from wolffialib.io.PrintBar import PrintBar
              
        if progressTitle != None:    
            progress = PrintBar(0, 4)
            progress.setLabelText(progressTitle+", writing files")
            progress.setRange(0,3)
            progress.setValue(0)
        else:
            progress = None

        self._reduceTypeNames()
        
        #start = time.process_time()
        #print "Mixture writeFiles ", baseFilename
        self.writePDB(baseFilename+".pdb",fixedMolecules)
        if progress != None:    progress.setValue(1)
        #print "Mixture writeFiles writePDB", time.process_time() - start
        self.writePSF(baseFilename+".psf")
        if progress != None:    progress.setValue(2)
        #print "Mixture writeFiles writePSF", time.process_time() - start
        self.writePRM(baseFilename+".prm")
        if progress != None:
            progress.setValue(3)
            progress.close()

        #print "Mixture writeFiles writePRM", time.process_time() - start
    
    def setAtomOrder(self):
        self.atomOrder = []
        for molecule in self:
            for atom in self.getMolecule(molecule):
                self.atomOrder.append((molecule, atom))
        
    def writePDB(self, pdbFile=None, fixedMolecules=[]):
        """
        Writes a PDB coordinates file.
    
        @type  pdbFile: string
        @param pdbFile: PDB filename.  If None it will write to sys.stdout.
        """
        #start = time.process_time()
        #print ( "Mixture writePDB __buildTranslatorTable__", fixedMolecules)
        self.__buildTranslatorTable__()
        self.setAtomOrder()
        
        if pdbFile==None:
            fd = sys.stdout
            #print "writePDB imprimiendo stdout"
        else:
            fd = open(pdbFile, 'w')
            #print "writePDB(",pdbFile,")"
    
        #self.atomOrder = []
        count = 1
    
        #print "Mixture writePDB writing coordinates", time.process_time() - start
        renumbering = dict()  
        #print("Mixture.writePDB moleculas:", list(self))
        for molecule in self:
            mol = self.getMolecule(molecule)
            renumbering[mol] = dict()
            try:    fixed = molecule in fixedMolecules
            except: fixed = False
            #print("Mixture.writePDB mol: {} ({},{})".format(molecule, mol.molname(),fixed))
            for atom in mol:
                #print("Mixture.writePDB mol:", mol, atom, molecule in fixedMolecules)
                atr = mol.getAtomAttributes(atom)
                fd.write(atr.PDBline(count, self.trad[molecule], fixed)+"\n")
                #self.atomOrder.append((molecule, atom))
                renumbering[mol][atom] = count
                count += 1
        
        mixture = self
        fd.write("ENDMDL\n")
        #print "Mixture writePDB writing connect", time.process_time() - start
        for molecule in mixture:
            mol = mixture.getMolecule(molecule)
            for atom in mol:
                #print "Mixture writePDB writing neighbors", mol, atom
                neighbors = list(mol.neighbors(atom))
                if len(neighbors) > 0:
                    fd.write("CONECT %4i" % (renumbering[mol][atom]))
                    for bond in neighbors:
                        if renumbering[mol][bond] > renumbering[mol][atom]:
                            fd.write(" %4i" % (renumbering[mol][bond]))
                    fd.write("\n")
            
        #print "Mixture writePDB writing finished", time.process_time() - start
        if pdbFile != None:
            fd.close()


    def writePRM(self, prmFile=None):
        """
        Writes a PRM force field file.
    
        @type  prmFile: string
        @param prmFile: PRM force field  filename.  If None it will write to sys.stdout.
        """
        from wolffialib.chemicalGraph.io.PRM import PRMError
    
        self.__buildTranslatorTable__()
        open(prmFile, "w").close()   # create empty file

        writtenForceFields = []
        for molecule in self.trad:
            mol = self.getMolecule(molecule)
            #print "ForceField writePRM: ", mol.molname()
            ff = mol.getForceField()
            ff.addZeroAngles( mol.angleTypes())
            #if not ff in writtenForceFields:
            if not self.trad[molecule] in writtenForceFields:
                try: ff.writeCHARMM(prmFile, mode="a", trad=self.trad[molecule])
                except : raise
                
                writtenForceFields.append(self.trad[molecule])
                #print "Mixture writePRM",ff._ANGLES
            #print "Mixture writePRM",molecule,writtenForceFields
            #print "Mixture writePRM", prmFile
    
    #-------------------------------------------------------------
    def writePSF(self, psfFile=None):
        """
        Writes a PSF topology file.
    
        @type  psfFile: string
        @param psfFile: PSF filename.  If None it will write to sys.stdout.
        """
        self.__buildTranslatorTable__()
        PSF.write(self,  psfFile)
    
    #-------------------------------------------------------------
    def writePSF2(self, psfFile=None):
        """
        Writes a PSF topology file.
    
        @type  psfFile: string
        @param psfFile: PSF filename.  If None it will write to sys.stdout.
        """
    
        if psfFile==None:
            fd = sys.stdout
            #print "writePSF imprimiendo stdout"
        else:
            fd = open(psfFile, 'w')
            #print "writePSF(",psfFile,")"
    
        # write ATOM section
        fd.write("PSF\n\n       1 !NTITLE\n REMARKS \n\n%8i !NATOM\n" % self.order())
        count = 1
        for molecule in self:
            mol = self.getMolecule(molecule)
            for atom in mol:
                atr = mol.getAtomAttributes(atom)
                fd.write(atr.PSFline(count, self.trad[molecule])+"\n")
                count += 1
            
        # write BOND section
        fd.write("\n%8i !NBOND\n" % self.bonds())
        count = 0
        bondCount = 0
        for molecule in self:
            mol = self.getMolecule(molecule)
            bondsT = mol.bonds()
            #nbonds = len(bondsT)
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
            
    def writeWFM(self, filename=None):
        import pickle
        if filename == None:
            filename = self.getMixtureFileName()
        
        with open(filename, "wb") as f:
            pickle.dump(self, f,protocol=pickle.HIGHEST_PROTOCOL)
    
        
#-------------------------------------------------------------
class MixtureError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class VersionControl:
    def __init__(self):
        self.trackers = dict()
        self.modificationTime = time.process_time()
        
    def hasChanged(self, tracker, keepTime=False):
        if self.trackers.has_key(tracker):
            mt = self.trackers[tracker]
            if not keepTime:
                self.trackers[tracker] = self.modificationTime
            return mt < self.modificationTime
        else:
            self.trackers[tracker] = self.modificationTime
            return True
    
    def setChanged(self):
        self.modificationTime = time.process_time()
        
    def reset(self):
        self.modificationTime = time.process_time()
        self.trackers = dict()


#==========================================================================
if __name__ == '__main__':
    print("Testing Mixture class")
    from wolffialib.chemicalGraph.solvent.WATER import WATER
    from wolffialib.chemicalGraph.solvent.THF import THF
    from wolffialib.chemicalGraph.solvent.DMF import DMF
    
    mix = Mixture()
    agua =  mix.add(WATER())
    agua =  mix.add(WATER())
    mix.add(THF())
    mix.add(DMF())
    
    for mol in mix.moleculeGenerator(): print(mol)
    
    for atom in mix.atomsGenerator(): print(atom)
    
