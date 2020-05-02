# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
"""
  Container.py
  
  Wolffia Container module.

    A container is a geometrical shape that is meant to contain a mixture.
    If periodic boundary conditions are set the Container is the base cell.
    
    
  Last modification for Version 3.0, April, 2020 by José O. Soter Esteva from
  module previously named Drawer.

    Copyright 2011, 2012, 2020: José O.  Sotero Esteva, Carlos J.  Cortés Martínez, 

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


#import NanoCAD_conf
import sys, os, math
from lib.chemicalGraph.molecule.solvent.WATER import WATER

#sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
#from conf.Wolffia_conf import NANOCAD_MOLECULES

_AVOGRADRO_CONSTANT_ = 6.02214129e+23

class Container:
    '''
        Container for the Mixture.
    '''
    
    DENSITY = {None:[0,0,1],WATER: [0.9970479,298.15,18.01528], "Chloroform":[1.483,298.15,119.38], "Chloroform (4 atoms)": [1.483,298.15,119.38], "Acetone": [0.786,293.15,58.08], "THF": [0.886,293.15,72.11], "Argon": [5.537, 0.03049,39.948], "Methanol": [0.791,293.15,32.04], "Selected Molecule": [0.9970479,298.15,18.01528]}
    DI = 0
    TI = 1
    MI = 2

    def __init__(self, cid=None):
        '''
            id (int): identifier (LAMPS style)
        '''
        # Lammps-style variables
        self.id = cid
        
        # NAMD-style parameters
        self.cellOrigin        = None
        self.wrapWater          = False
        self.wrapAllMolecules   = False
        
    def lammpsCommand(self, mixture):
        ''' to be done '''
        pass

    def getCellOrigin(self):
        return self.cellOrigin

    def setCellOrigin(self, o):
            self.cellOrigin = o

    def setId(self, cid): self.id = cid
    
    def amountSolventMolecules(self, solvent):
            #import numpy
            global _AVOGRADRO_CONSTANT_
            D = self.DENSITY[solvent][self.DI]
            MM = self.DENSITY[solvent][self.MI]
            V = self.volume() / 1E24
            if V == 0: return 0
            
            #print "computeMolecules ", D,V,MM,D * V / MM * _AVOGRADRO_CONSTANT_
            n = int(D * V / MM * _AVOGRADRO_CONSTANT_)
    
            return n

# ===========================================
class Box(Container):
    '''
        Defines a box with rectangular anlges (similar to block in LAMMPS)
    '''
    def __init__(self, cid=None, maxsMins=None):
        '''        
            maxsMins = (xmin, xmax, ymin, ymax, zmin, zmax) or None
        '''
        super(Box, self).setId(cid)
    
        self.setMaxsMins(maxsMins)
    
    def getMaxsMins(self): return self.maxsMins
    
    def getBoxDimension(self):
            #calculate box's length, width, and height
            dimension = self.getCellBasisVectors()
            #print "Box.getCellBasisVectors", dimension
            if dimension == None:
                return [2.0,2.0,2.0]
            else:
                return [dimension[0][0], dimension[1][1], dimension[2][2]] 

    def getCellBasisVectors(self):
        ''' returns cell basis vector NAMD style'''
        #print "Box.getCellBasisVectors", self.__dict__
        #return self.cellBasisVectors
        return [[self.maxsMins[1]-self.maxsMins[0], 0.0, 0.0], 
                [0.0, self.maxsMins[3]-self.maxsMins[2], 0.0],
                [0.0, 0.0, self.maxsMins[5]-self.maxsMins[4]]
               ]
        
    
    def getBoxVolume(self):
            dimension = self.getBoxDimension()
            #print "Box.getBoxVolume", dimension
            return dimension[0]*dimension[1]*dimension[2]

    def getCenter(self):
        cellBasisVectors = self.getCellBasisVectors()
        x = (cellBasisVectors[0][0]+cellBasisVectors[1][0]+cellBasisVectors[2][0])/2
        y = (cellBasisVectors[0][1]+cellBasisVectors[1][1]+cellBasisVectors[2][1])/2
        z = (cellBasisVectors[0][2]+cellBasisVectors[1][2]+cellBasisVectors[2][2])/2
        return [x,y,z]

    def getFaces(self):
        cellBasisVectors = self.getCellBasisVectors()
        left = self.cellOrigin[0]
        right = left + cellBasisVectors[0][0]
        bottom = self.cellOrigin[1]
        top = bottom + cellBasisVectors[1][1]
        zNear = self.cellOrigin[2]
        zFar = zNear + cellBasisVectors[2][2]
            
        return [left, right, bottom, top, zNear, zFar]

    def lammpsCommand(self):
        return "region {:d} style block {}".format(self.id, ' '.join(self.maxsMins))
    
    def setMaxsMins(self, maxsMins):
        self.maxsMins = maxsMins
        self.setCellOrigin((maxsMins[0], maxsMins[2], maxsMins[4]))
        
    def volume(self):
            '''
            volume
            '''
            return (self.maxsMins[1]-self.maxsMins[0]) * \
                (self.maxsMins[3]-self.maxsMins[2]) * \
                (self.maxsMins[5]-self.maxsMins[4])

#==========================================
class Prism(Container):
    '''
        Defines a parallepiped, Similar to cell in NAMD or prism in LAMMPS.
    '''
    def __init__(self):
        self.cellBasisVectors     = None
        
        self.setWrapAllMolecules(self.wrapAllMolecules)
        self.setWrapWater(self.wrapWater)
        
    def setWrapWater(self, val):
            self.wrapWater = val
            
    def setWrapAllMolecules(self, val):
            self.wrapAllMolecules = val
            
    def getWrapWater(self):
            return self.wrapWater
        
    def getWrapAllMolecules(self):
            return self.wrapAllMolecules

    def getCenter(self):
            x = (self.cellBasisVectors[0][0]+self.cellBasisVectors[1][0]+self.cellBasisVectors[2][0])/2
            y = (self.cellBasisVectors[0][1]+self.cellBasisVectors[1][1]+self.cellBasisVectors[2][1])/2
            z = (self.cellBasisVectors[0][2]+self.cellBasisVectors[1][2]+self.cellBasisVectors[2][2])/2
            return [x,y,z]

    def hasCell(self):
            '''
            Determines if there is a valid cell.  Eliminates inconsistencies in case they are found.
            '''
            #print "hasCell", self.__dict__
            if self.getCellBasisVectors() != None and self.getCellOrigin() != None:
                try:
                    self.getBoundingSphere()    # this method uses almost all of the object fields\
                                                # any problem should be trapped here.
                except:
                    return False
            else: return False
            return True

    def readNAMD(self,archivo):
            from lib.communication.namd.SimThread import  NAMDcell
            try:
                cell = NAMDcell(archivo)
                box = cell.getBox()

                self.setCellBasisVectors([[box[0][0][0], 0.0, 0.0],
                                        [0.0, box[0][1][1], 0.0],
                                        [0.0, 0.0, box[0][2][2]]])
                self.setCellOrigin(box[1])
            except:
                self.setCellBasisVectors([[None,None,None],[None,None,None],[None,None,None]])
                self.setCellOrigin([None,None,None])
            

    def setCellBasisVectors(self, v):
            self.cellBasisVectors = v
            #print "setCellBasisVectors", self.__dict__

    def getCellBasisVectors(self):
            #print "getCellBasisVectors", self.__dict__
            return self.cellBasisVectors
    
    def getBoundingSphere(self):
            #print "getBoundingSphere" ,self.cellOrigin ,self.cellBasisVectors
            far = [ self.cellBasisVectors[0][0]        \
                       + self.cellBasisVectors[1][0]   \
                       + self.cellBasisVectors[2][0] , \
                    self.cellBasisVectors[0][1]        \
                       + self.cellBasisVectors[1][1]   \
                       + self.cellBasisVectors[2][1] , \
                    self.cellBasisVectors[0][2]        \
                       + self.cellBasisVectors[1][2]   \
                       + self.cellBasisVectors[2][2]]
            cx = self.cellOrigin[0] + far[0] / 2
            cy = self.cellOrigin[1] + far[1] / 2
            cz = self.cellOrigin[2] + far[2] / 2
            d  = math.sqrt(far[0]**2 + far[1]**2 + far[2]**2)
            return [[cx,cy,cz], d]
        
    def getCellBasisVector1(self):
            return self.cellBasisVectors[0]

    def getCellBasisVector2(self):
            return self.cellBasisVectors[1]

    def getCellBasisVector3(self):
            return self.cellBasisVectors[2]

    def clear(self):
            self.setCellBasisVectors(None)
            self.setCellOrigin(None)
            self.setSphericalBC(None)
        
    def getCellOrigin(self):
            return self.cellOrigin

    def hasSphere(self):
            return self.sphericalBC != None
        
    def setSphericalBC(self, s):
            self.sphericalBC = s
        
    def setSphericalBCk1(self, k):
            self.sphericalBCk1 = k
        
    def setSphericalBCexp1(self, e):
            self.sphericalBCexp1 = e
        
    def getSphericalBC(self):
            return self.sphericalBC
        
    def getSphericalBCcenter(self):
            return self.sphericalBC[0]
        
    def getSphericalBCr1(self):
            return self.sphericalBC[1]


    def volume(self):
            '''
            ONLY VALID FOR A BOX!!!!
            '''
            return self.getCellBasisVector1()[0] * self.getCellBasisVector2()[1] * self.getCellBasisVector3()[2]
    
    #---------------------------------------------------------------------
    def removeCollisions(self, mix, originalMolecules, pbc, gui=False):
            '''
            if gui:
                progress      = QtGui.QProgressDialog("Solvating...", QtCore.QString(), 0, 3, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
                progress.setWindowModality(QtCore.Qt.WindowModal)
            '''
         
            initCount = len(mix)
            collisions = mix.overlapingMolecules(originalMolecules, pbc=pbc)
            #if gui:    progress.setValue(1)
            #print "colisiones... ", len(collisions)
            toRemove  = set(collisions).difference(set(originalMolecules))
            #if gui:    progress.setValue(2)
            #print "removeCollisions removiendo... ", len(toRemove)
            self._history.currentState().removeMoleculesFrom(toRemove)
            
            #if gui:    progress.hide()
            return initCount-len(mix)

    
if __name__ == "__main__":
    ''' run some tests'''
    
    print("Tests for Box class")
    box = Box(1, (1,3,3,5,5,7))
    
    print("box.volume()", end='')       ; assert box.volume() == 8,       " Failed." ; print(" ... passed")
    print("box.getBoxVolume()", end='') ; assert box.getBoxVolume() == 8, " Failed." ; print(" ... passed")
    print("box.getCenter()", end='') ; assert box.getCenter() == [1.0, 1.0, 1.0], " Failed." ; print(" ... passed")
    