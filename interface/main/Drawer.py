# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  NanoCadState.py
#  Version 0.5, November, 2011
#
#  Wolffia Drawer
#
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Carlos J.  Cortés Martínez, 

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
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
#from conf.Wolffia_conf import NANOCAD_MOLECULES



class Drawer:
	def __init__(self):
		#print "Drawer__init__"
		self.cellBasisVectors 	= None
		self.cellOrigin			= None
		self.sphericalBC 		= None		
		self.sphericalBCk1		= 10
		self.sphericalBCexp1	= 2
		self.wrapWater          = False
		self.wrapAllMolecules   = False

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

	def hasCell(self):
		'''
		Determines if there is a valid cell.  Eliminates inconsistencies in case they are found.
		'''
		#print "hasCell", self.__dict__
		if self.getCellBasisVectors() != None and self.getCellOrigin() != None:
			try:
				self.getBoundingSphere()	# this method uses almost all of the object fields\
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
			print("readNAMD ", box)
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
		
	def setCellOrigin(self, o):
		self.cellOrigin = o

	def getCellBasisVector1(self):
		return self.cellBasisVectors[0]

	def getCellBasisVector2(self):
		return self.cellBasisVectors[1]

	def getCellBasisVector3(self):
		return self.cellBasisVectors[2]

	def getCenter(self):
		x = (self.cellBasisVectors[0][0]+self.cellBasisVectors[1][0]+self.cellBasisVectors[2][0])/2
		y = (self.cellBasisVectors[0][1]+self.cellBasisVectors[1][1]+self.cellBasisVectors[2][1])/2
		z = (self.cellBasisVectors[0][2]+self.cellBasisVectors[1][2]+self.cellBasisVectors[2][2])/2
		return [x,y,z]

	def getFaces(self):
		left = self.cellOrigin[0]
		right = left + self.cellBasisVectors[0][0]
		bottom = self.cellOrigin[1]
		top = bottom + self.cellBasisVectors[1][1]
		zNear = self.cellOrigin[2]
		zFar = zNear + self.cellBasisVectors[2][2]
		
		return [left, right, bottom, top, zNear, zFar]

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
		if gui:
			progress      = QtGui.QProgressDialog("Solvating...", QtCore.QString(), 0, 3, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
			progress.setWindowModality(QtCore.Qt.WindowModal)

		initCount = len(mix)
		collisions = mix.overlapingMolecules(originalMolecules, pbc=pbc)
		if gui:	progress.setValue(1)
		#print "colisiones... ", len(collisions)
		toRemove  = set(collisions).difference(set(originalMolecules))
		if gui:	progress.setValue(2)
		print("removeCollisions removiendo... ", len(toRemove))
		self._history.currentState().removeMoleculesFrom(toRemove)
		
		if gui:	progress.hide()
		return initCount-len(mix)

	
	#---------------------------------------------------------------------
	def getBoxDimension(self):
		#calculate box's length, width, and height
		dimension = self.getCellBasisVectors()
		#print "Drawer.getCellBasisVectors", dimension
		if dimension == None:
		    return [2.0,2.0,2.0]
		else:
		    return [dimension[0][0], dimension[1][1], dimension[2][2]] 

	#---------------------------------------------------------------------
	def getBoxVolume(self):
		dimension = self.getBoxDimension()
		#print "Drawer.getBoxVolume", dimension
		return dimension[0]*dimension[1]*dimension[2]

