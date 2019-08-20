# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  NanoCadState.py
#  Version 0.1, November, 2011
#
#  NanoCAD state update.
#
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Melissa  López Serrano, 

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


'''
Created on Feb 8, 2012

@author: jse
'''

import sys, os, time, copy, tempfile
import logging
from lib.chemicalGraph.Mixture import Mixture #@UnresolvedImport
from Drawer import Drawer
from conf.Wolffia_conf import WOLFFIA_DEFAULT_MIXTURE_LOCATION, WOLFFIA_DEFAULT_MIXTURE_NAME, WOLFFIA_VERSION #@UnresolvedImport
from lib.chemicalGraph.molecule.Molecule import Molecule
import cPickle as pickle #Tremenda aportación por carlos cortés.

from sklearn.metrics.pairwise import euclidean_distances  # used in fillBox()

__MAX_SIZE__ = 10

class History(list):
	'''
	classdocs
	'''
	
	def __init__(self, bb=None, fb=None, state=None, loadFile=None, loadDir=None):
		'''
		Constructor
		'''
		#print "History __init__(", bb, fb, state,loadDir , loadFile
		self.backButton = bb
		self.forwardButton = fb
		self.currentIdx = -1
		
		if state == None:
		    self.current = NanoCADState()
		    if loadFile == None:
		        self.current.reset()
		    else:
				if loadDir == None:
				    self.current.load(loadFile)
				else:
				    self.current.load(loadDir + "/" + loadFile)
				    self.current.setCurrentDirectory(loadDir)
				    #print "History dir changed to ",loadDir,self.current.getCurrentDirectory()
		else:
			self.current = state
		
		#self.push(self.current)
		self.checkButtons()
		#print "History exiting dir ",self.getCurrentState().getBuildDirectory()
	
	def clear(self):
		while len(self) > 0:
			self.pop().close()
		self.currentIdx = -1
		del self.current
		self.current = NanoCADState()
			
	def push(self, st=None, force=False):
		#import inspect
		#print "push, caller=",inspect.stack()[1][3]
		if st == None:
		        st = self.currentState()
		
		assert(isinstance(st, NanoCADState))
		for i in range(len(self)-1, self.currentIdx, -1):
		    self.pop(i) 
		
		#if not self.isEmpty(): self.pop()
		
		# copies state, then copies ShownMolecules manually
		#newState = copy.deepcopy(st)
		#newState.shownMolecules = ShownMoleculesSet(newState.mixture)
		#for mol in st.mixture: newState.shownMolecules.show(mol)
		#print "push getBuildDirectory", self.getCurrentState().getBuildDirectory()
		tmpPush = tempfile.NamedTemporaryFile(prefix="temp"+self.getCurrentState().getMixtureName(), dir=self.getCurrentState().getBuildDirectory(), delete=True, suffix='.wfy')
		#print "push name", tmpPush.name
		self.append(tmpPush)
		self.currentState().save(fileObject=tmpPush)
		
		#self.append(newState)
		#self.append(st)
		
		self.currentIdx += 1
		if len(self) > __MAX_SIZE__:
		    self.pop(0)
		    self.currentIdx -= 1
		self.checkButtons()
	        
	def back(self):
	    if self.currentIdx > 0:
			self.currentIdx -= 1
			self.getCurrentState().load(self[self.currentIdx]) # v 1.1.33
			self.checkButtons()
			#return self[self.currentIdx]
			#self.currentIdxState().restoreForceField()
	    else:
	        raise HistoryException("Wolffia's history is empty.")
	
	def forward(self):
	    if self.currentIdx < len(self)-1:
			self.currentIdx += 1
			self.getCurrentState().load(self[self.currentIdx]) # v 1.1.33
			self.checkButtons()
			#self.currentState().restoreForceField()
			#return self[self.currentIdx]
	    else:
	        raise HistoryException("Forwarding to future of Wolffia's history.")
	
	def isEmpty(self):
	    return len(self) == 0
	
	def checkButtons(self):
	    if self.backButton != None:
	        #if self.currentIdx >= 0: print "checkButtons ", self.currentIdx, self[self.currentIdx].name
	        self.backButton.setDisabled(False)
	        self.forwardButton.setDisabled(False)
	        if self.currentIdx <= 0:
	            self.backButton.setDisabled(True)
	        if self.currentIdx >= len(self)-1:
	            self.forwardButton.setDisabled(True)
	            
	        #print "checkButtons chaqueando pos=", self.currentIdx, " len=", len(self)
	        #for state in self:
	        #    print "checkButtons ",state.mixture.order(), ", ",state.mixture
	        
	def currentState(self):
		'''
	    if self.currentIdx >= 0:
			#return self[self.currentIdx]
			return self.current
	    else:
	        return None
	    '''
		return self.current
	
	        
	def getCurrentState(self): return self.current
	
	def reset(self):
		self.getCurrentState().reset()
		self.clear()
    
    
    
class HistoryException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)





class NanoCADState(object):
	def __init__(self, parent=None, filename=None, log=None):
	    #import inspect
	    #print "NanoCADState.init, caller=",inspect.stack()[1]
	    self.parent		    =	parent
	    self.log            =   log
	    self.wolffiaVerion  =   WOLFFIA_VERSION
	    self.mixture		=	Mixture(mixName = WOLFFIA_DEFAULT_MIXTURE_NAME)
	    self.workingDir     =   WOLFFIA_DEFAULT_MIXTURE_LOCATION + "/" 
	    self.drawer		    =	None
	    self.simTabValues	=	None
	    self.minTabValues	=	None
	    self.shownMolecules =   None
	    self.fixedMolecules =   None
	    
	    self.reset()
	    if not filename == None:
	        self.load(filename)
	    #print "NanoCADState__init__", self.forceFieldStorage.keys()
	
	#-------------------------- methods ------------------------------------
	def reset(self):
	    #self.forceFieldStorage    =    None
	    #self.mixture        =    Mixture(mixName = WOLFFIA_DEFAULT_MIXTURE_NAME)
	    self.mixture        =    Mixture(mixName = self.mixture.getMixtureName())
	    self.wolffiaVerion = WOLFFIA_VERSION
	    self.simTabValues    =    None
	    self.minTabValues    =    None
	
	    #self.mixture.setChanged()
	    #self.forceFieldStorage = dict()
	    
	    #self.buildDir = WOLFFIA_DEFAULT_MIXTURE_LOCATION + "/" + self.mixture.getMixtureName()
	    #self.workingDir = os.getcwd()
	    self.drawer = Drawer()
	    self.shownMolecules = ShownMoleculesSet(self.mixture)
	    self.fixedMolecules = FixedMolecules()
	    #print "NanoCADState reset"
	
	#--------------------------------------------------------------------

	def save(self, filename=None, fileObject=None):
	
		if fileObject <> None:
			f = fileObject
			f.seek(0)
			pickle.dump(self.__dict__, f)
		else:
			if filename == None:
				#filename = WOLFFIA_DEFAULT_MIXTURE_LOCATION + "/" + WOLFFIA_DEFAULT_MIXTURE_NAME + ".wfy"
				filename = self.getBuildDirectory()+"/"+self.getMixtureName() + ".wfy"
			
			#print "History.save_ importing cPickle"
			#print "History.save_ imported cPickle, starting to save"
			#print "History.save_ self.getBuildDirectory(), self.getMixtureName() ", self.getBuildDirectory(), self.getMixtureName()
			try: 
			    f = open(filename, "w")
			except IOError:
			    print filename + ": File does not exist."
			pickle.dump(self.__dict__, f)
			f.close()
		
		#print "NanoCADState.save, save sucessful", f.name
	
	
	#--------------------------------------------------------------------------------
	def writeFiles(self, filename=None):  
		from chemicalGraph.io.PRM import PRMError
		if filename == None:
		    filename = self.getBuildDirectory()+"/"+self.getMixtureName()
		#print "NanoCADState writeFiles,", filename
		
		try: self.getMixture().writeFiles(filename, self.fixedMolecules.fixedList())
		except : raise
	
	
	#--------------------------------------------------------------------------------
	def packFiles(self, mixBaseFilename, filename, progressSignal=None):
		import zipfile
		
		if progressSignal != None: progressSignal.emit(0)
		
		self.writeFiles(filename=mixBaseFilename)
		if progressSignal != None: progressSignal.emit(50)

		self.save()  # .wfy  saved because it may have changed w/r to the one when the MixtureBrowser was created
		
		# .coor, .vel and .conf files preserve configuration of last run
		
		#print "NanoCADState packFiles ", mixBaseFilename, filename
		file1 = zipfile.ZipFile(filename , "w")
		if progressSignal != None: progressSignal.emit(60)
		#mixBaseFilename = str(self.settings.currentMixtureLocation()) + "/" + self.history.currentState().getMixtureName()
		#mixBaseFilename = str(self.getBuildDirectory()) + "/" + self.getMixtureName()
		#print "packFiles mixname", mixBaseFilename
		
		#for name in glob.glob(str(self.settings.currentMixtureLocation()) + "/*"):
		#	file1.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
		extensionsNotPacked = ""
		extensionsToPack = [".prm",".pdb",".psf",".wfy",".conf",".coor",".vel",".xsc"]
		progress = 60
		for ext in extensionsToPack:
			#if progress.wasCanceled(): break
			confFilename = mixBaseFilename+ext
			if not os.path.isfile(confFilename):
				#print "packFiles confFilename NotPacked",confFilename
				extensionsNotPacked += " " + ext
			else:
				file1.write(confFilename, os.path.basename(confFilename), zipfile.ZIP_DEFLATED)
			progress += 5
			if progressSignal != None: progressSignal.emit(progress)
		
		file1.close()
		return extensionsNotPacked
	
	#--------------------------------------------------------------------
	def load(self, filename=None):
		import cPickle as pickle #Tremenda aportación por carlos cortés
		#import inspect
		#print "NanoCADState.load, caller1=",inspect.stack()[1]
		#print "NanoCADState.load, caller2=",inspect.stack()[2]
		#print "NanoCADState.load, caller3=",inspect.stack()[3]
		if filename == None:
		    filename = WOLFFIA_DEFAULT_MIXTURE_LOCATION + "/" + WOLFFIA_DEFAULT_MIXTURE_NAME + ".wfy"
		    
		logger = logging.getLogger(self.__class__.__name__)
		
		if hasattr(filename, 'read'): # new in v 1.132
			logger.info("Loading state from " + str(filename.name))
			filename.seek(0)
			self.__dict__ = pickle.load(filename)
			f = filename
		else:
			logger.info("Loading state from " + str(filename))
			if not os.path.exists(filename):
			    self.reset()
			    self.save(filename)
			    return
			#print "History.load_ importing cPickle"
			#print "History.load_ imported cPickle, starting to load"
			
			try:
			    f = open(filename, "r")
			    self.__dict__ = pickle.load(f)
			    f.close()
			except Exception as e:
				import traceback
				traceback.print_exc()
				#print "NanoCADState.load_ Exeption ", e, " when unpickling file."
				from PyQt4 import QtGui
				gui = QtGui.QErrorMessage.qtHandler()
				QtGui.QErrorMessage.showMessage( gui, "Error: could not open configuration file " 
				    + filename + "." )
				logger.warning("Error: could not open configuration file " + filename + "." )
		
		if not hasattr(self, "fixedMolecules"):  # introduced in v 0.24
		    self.fixedMolecules = FixedMolecules()
		if self.wolffiaVerion < "0.24-4":
		    self.simTabValues["pmeGridSp"] = 1.0
		
		logger.info( "Loaded mixture from version " + self.wolffiaVerion + ". Current version is " + WOLFFIA_VERSION)
		
		if self.wolffiaVerion < "0.24-42":
		#if True:
		    #print "YES, mixture=",self.getMixture().molecules()
		    for mol in self.getMixture():
		        #print "load ", self.getMixture().getMolecule(mol).getForceField()._NONBONDED
		        molecule = self.getMixture().getMolecule(mol)
		        self.getMixture().getMolecule(mol).copyChargesToForceField()
		        self.wolffiaVerion =  "0.24-42"
		        #print "load ", self.getMixture().getMolecule(mol).getForceField()._NONBONDED
		#else: print "NO"
		
		if self.wolffiaVerion < "0.24-43":
		    temp = ShownMoleculesSet(self.getMixture())
		    temp.addDictionary(self.shownMolecules)
		    del self.shownMolecules
		    self.shownMolecules = temp
		    
		if self.wolffiaVerion < "0.24-44":
		    #print "History.load_ fixing self bonds"
		    for m in self.mixture:  #remove bonds to self
		        molecule = self.mixture.getMolecule(m)
		        for atom in molecule:
		            if molecule.has_edge(atom, atom):
		                molecule.remove_edge(atom, atom)
		
		    #print "History.load_  self bonds removed"
		
		# trick for backward compatibility
		for mol in self.getMixture():
		    molecule = self.getMixture().getMolecule(mol)
		    #print "load inspecting ",molecule.__class__
		    if str(molecule.__class__)[-10:] == "Molecule\'>":
		        molecule.__class__ = Molecule
		        #print "molecule class changed", molecule.__class__
		
		if self.wolffiaVerion < "1.13":  	# until further versions
											# self.mixture.mixName should be the same as 
											# self.parent.settings.currentMixtureName.
			print "History.load_ self.mixture.mixName should be the same as self.parent.settings.currentMixtureName"
			try:
				self.mixture.setMixtureName(self.parent.settings.currentMixtureName) 
			except: pass
		
		if self.wolffiaVerion < "1.131":  	# fix for 1.13 did not work. 
											# self.parent.settings.currentMixtureName is being
											# eliminated in this version.
			print "History.load_ self.mixture.mixName should be the same as self.parent.settings.currentMixtureName"
			try:
				self.parent.settings.setMixtureLocation(self.parent.settings.currentMixtureName)
				del self.parent.settings.currentMixtureName
			except: pass
			
		# other fixes ===========================
		if  self.shownMolecules == None:
			 self.shownMolecules = ShownMoleculesSet(self.getMixture())
		# end other fixes ===========================
			
		if self.wolffiaVerion < "1.31": 
			self.getMixture().upgrade(self.wolffiaVerion)
			
		#from PyQt4 import QtGui
		if self.wolffiaVerion < WOLFFIA_VERSION: 
			#QtGui.QMessageBox.information(self.parent,"Wolffia", "Simulation version updated from "+str(self.wolffiaVerion)+" to "+str(WOLFFIA_VERSION))
			print "NANOCADState.load: Simulation version updated from "+str(self.wolffiaVerion)+" to "+str(WOLFFIA_VERSION)
		self.wolffiaVerion =  WOLFFIA_VERSION
		print "NanoCADState.load_ imported cPickle, load sucessful", f.name
		#print "History.load self.shownMolecules", self.shownMolecules
		#self.shownMolecules.showAll()
	
	#--------------------------------------------------------------------
	# If progress != None, it is an object that responds to he folowing methods:
	#   .setLabelText("Removing collisions")
	#   .setRange(0,molNum)
	#   .setValue(0)

	def fillBox(self, solv, molNum, checkCollisions=False, replaceCollisions=False, applyPCBs=True, progress=None):
		import math, random
		import numpy as np
		from lib.chemicalGraph.molecule.solvent.Solvent import Solvent

		solventMolecules = Solvent(solv.__class__)

		remaining = -1   # to track removng collissions
		
		totalDim = self.getDrawer().getBoxDimension()
		boxmin = self.getDrawer().getCellOrigin()
		boxmax =[ boxmin[0]+totalDim[0], boxmin[1]+totalDim[1], boxmin[2]+totalDim[2] ]
		
		#calculate the volume for a single solvent molecule
		center = [0., 0., 0.]
		pos = solv.massCenter()
		solv.moveBy([center[0]-pos[0], center[1]-pos[1], center[2]-pos[2]])
		#solvDiameter = solv.diameter()+ _SEPARATION_BETWEEN_SOLVENTS_
		solvDiameter = math.pow(self.getDrawer().getBoxVolume() / molNum, 1./3.)
		if solvDiameter == 0: return
		
		row = math.floor(totalDim[1]/solvDiameter)
		col = math.floor(totalDim[0]/solvDiameter)
		dep = math.floor(totalDim[2]/solvDiameter)

		progressMax   = molNum
		progressCount = 0
		if progress != None:	
			progress.setLabelText("Adding solvent")
			progress.setRange(0,molNum-1)
			progress.setValue(0)
		
		solvRadius = solvDiameter / 2
		newPos = solv.massCenter()
		refCoor = boxmin
		
		#boxmax[0] -= solvDiameter/2.
		#boxmax[1] -= solvDiameter/2.
		#boxmax[2] -= solvDiameter/2.
		
		if progress != None:	
			progress.setLabelText("Adding solvent")
			progress.setRange(progressCount,progressMax)
			progress.setValue(progressCount)

		# lopps over a sequence of adding solvent and removing collisions
		originalMolecules = self.getMixture().molecules()
		originalCoords = self.getMixture().getAtomsCoordinatesAsArray()
		solvRadius = solvDiameter / 2.0 + 1.5

		#print "anadiendo... ", progressMax-progressCount
		while progressCount < progressMax:  # adds solvent
			#random rotation for solvent atoms
			rx = random.uniform(0, 360)
			ry = random.uniform(0, 360)
			rz = random.uniform(0, 360)
			
			#random displacement for solvent atoms
			rdx = random.uniform(boxmin[0], boxmax[0])
			rdy = random.uniform(boxmin[1], boxmax[1])
			rdz = random.uniform(boxmin[2], boxmax[2])
			
			#generate new molecule and assign next position
			mol = solv.copy()
			mol.rotateDeg(rx, ry, rz)
			newPos = np.array([[rdx, rdy, rdz]])

			if checkCollisions:
				atomDistances = euclidean_distances(originalCoords, newPos)
				if np.min(atomDistances) > solvRadius:
					#print 'fillBox: añadiendo', progressCount, np.min(atomDistances), newPos
					mol.moveBy(list(newPos)[0])
					#nodeName = self.addMolecule(mol, checkForInconsistentNames=False)
					#self.shownMolecules.show(nodeName)
					solventMolecules.addCoordinates(mol)
				else:
					#print 'fillBox: colision'
					if replaceCollisions: progressCount -= 1

			progressCount += 1
			if progress != None:	progress.setValue(progressCount)
			del mol
		
				
		# add solvent and rename with the given name
		nodeName = self.addMolecule(solventMolecules, checkForInconsistentNames=True)
		self.shownMolecules.show(nodeName)
		#print "fillBox ", mol.molname(),progressMax
		solv.rename(solventMolecules.molname())
		progressMax -= 1
		
		#print "tiempo ", time.clock() - start
		#print "Molecules after cleaning: ",mix.order()


	def fillBoxBAK(self, solv, molNum, checkCollisions=False, replaceCollisions=False, applyPCBs=True, progress=None):
		import math, random
		remaining = -1   # to track removng collissions
		
		totalDim = self.getDrawer().getBoxDimension()
		boxmin = self.getDrawer().getCellOrigin()
		boxmax =[ boxmin[0]+totalDim[0], boxmin[1]+totalDim[1], boxmin[2]+totalDim[2] ]
		
		#calculate the volume for a single solvent molecule
		center = [0., 0., 0.]
		pos = solv.massCenter()
		solv.moveBy([center[0]-pos[0], center[1]-pos[1], center[2]-pos[2]])
		#solvDiameter = solv.diameter()+ _SEPARATION_BETWEEN_SOLVENTS_
		solvDiameter = math.pow(self.getDrawer().getBoxVolume() / molNum, 1./3.)
		if solvDiameter == 0: return
		
		row = math.floor(totalDim[1]/solvDiameter)
		col = math.floor(totalDim[0]/solvDiameter)
		dep = math.floor(totalDim[2]/solvDiameter)

		progressMax   = molNum
		progressCount = 0
		if progress != None:	
			progress.setLabelText("Adding solvent")
			progress.setRange(0,molNum-1)
			progress.setValue(0)
		
		solvRadius = solvDiameter / 2
		newPos = solv.massCenter()
		refCoor = boxmin
		
		boxmax[0] -= solvDiameter/2.
		boxmax[1] -= solvDiameter/2.
		boxmax[2] -= solvDiameter/2.
		
		# add first molecule and rename solvent with the given name
		mol = solv.copy()
		mol.moveBy([random.uniform(boxmin[0], boxmax[0]), random.uniform(boxmin[1], boxmax[1]), random.uniform(boxmin[2], boxmax[2])])
		nodeName = self.addMolecule(mol, checkForInconsistentNames=True)
		self.shownMolecules.show(nodeName)
		#print "fillBox ", mol.molname(),progressMax
		solv.rename(mol.molname())
		progressMax -= 1
		
		if progress != None:	
			progress.setLabelText("Adding solvent")
			progress.setRange(progressCount,progressMax)
			progress.setValue(progressCount)

		# lopps over a sequence of adding solvent and removing collisions
		while progressCount < progressMax:

			originalMolecules = self.getMixture().molecules()
			
			#print "anadiendo... ", progressMax-progressCount
			while progressCount < progressMax:  # adds solvent
				#random rotation for solvent atoms
				rx = random.uniform(0, 360)
				ry = random.uniform(0, 360)
				rz = random.uniform(0, 360)
				
				#random displacement for solvent atoms
				rdx = random.uniform(boxmin[0], boxmax[0])
				rdy = random.uniform(boxmin[1], boxmax[1])
				rdz = random.uniform(boxmin[2], boxmax[2])
				
				#generate new molecule and assign next position
				mol = solv.copy()
				mol.rotateDeg(rx, ry, rz)
				newPos = [rdx, rdy, rdz]
				mol.moveBy(newPos)
				#mol.rename("SOLVENT("+mol.molname()+")")
				nodeName = self.addMolecule(mol, checkForInconsistentNames=False)
				self.shownMolecules.show(nodeName)
	
				progressCount += 1
				if progress != None:	progress.setValue(progressCount)
		
			# remove collisions
			if checkCollisions:
				if progress != None:	
					progress.setLabelText("Removing collisions")

				mix = self.getMixture()
				collisions = mix.overlapingMolecules(originalMolecules, pbc=self.getDrawer(),applyPBCs=applyPCBs)

				toRemove  = set(collisions).difference(set(originalMolecules))
				if remaining < 0: remaining = len(toRemove)
				#print "remaining", remaining
				#print "removiendo... ", len(toRemove)
				#print "faltan... ", remaining-len(toRemove)
				if progress != None:
					progress.setRange(0,remaining)
					progress.setValue(remaining-len(toRemove))
				self.removeMoleculesFrom(toRemove)

				if replaceCollisions: progressCount -= len(toRemove)
				
				
		#print "tiempo ", time.clock() - start
		#print "Molecules after cleaning: ",mix.order()


	def getMixture(self):
	    return self.mixture
	
	def getDrawer(self):
	    return self.drawer
	
	def name(self):
	    return self.mixture.mixName
	
	def getMixtureName(self):
	    return self.mixture.mixName
	
	def getBuildDirectory(self):
		#return self.buildDir  # no longer used
		try:
			return self.workingDir
		except:
			self.workingDir     =   WOLFFIA_DEFAULT_MIXTURE_LOCATION + "/" 
	    	return self.workingDir
	    
	def getCurrentDirectory(self):
	    return self.getBuildDirectory()
	
	def getSimTabValues(self): return self.simTabValues
	
	def updateMixture(self,mix):
	    #self.setChanged()
	    self.mixture = mix
	    self.shownMolecules.updateMixture(self.mixture)
	    self.fixedMolecules.updateMixture(self.mixture)
	    #for mol in self.mixture:
	    #    print "mix @t NanoCADState",self.mixture.getMolecule(mol)._name
	
	def addMixture(self,mix):
	    #print "History addMixture",mix
	    #self.mixture.merge(mix)
	    for mol in mix:
	        self.addMolecule(mix.getMolecule(mol))
	
	def addMolecule(self,mol, checkForInconsistentNames=True):
	    print "NanoCADState addMolecule",mol
	    molname = self.mixture.add(mol, checkForInconsistentNames)
	    self.shownMolecules.show(molname)
	    return molname
	
	def removeMolecule(self, mol):
	    #import inspect
	    #print "NanoCADState.removeMolecule, caller=",inspect.stack()[1]
	    #self.forceFieldStorage    =    None
	    
	    self.shownMolecules.remove(mol)
	    self.getMixture().remove(mol)
	
	def removeMoleculesFrom(self, mols):
	    self.getMixture().removeFrom(mols)
	    self.updateMixture(self.getMixture())
	    #self.getMixture().removeFrom(mols)
	
	def duplicateMolecule(self, mol):
	    newName = self.getMixture().duplicateMolecule(mol)
	    self.shownMolecules.show(newName)
	
	def setMixtureName(self, n):
	    self.mixture.mixName = n
	
	def setDrawer(self, dr):
	    self.drawer = dr
	
	def setBuildDirectory(self, d):
	    #print "buildDirectory changed to, " , d
	    #self.buildDir = d  # no longer used
	    self.workingDir = d
	
	def setCurrentDirectory(self, d):
	    self.workingDir = d
	
	def setSimTabValues(self, simVals):
	    self.simTabValues = simVals.copy()
	    
	def hasBox(self):
	    return self.drawer != None and self.drawer.hasCell()


import inspect
class ShownMoleculesSet(set):
    def __init__(self, mixture):
        print "ShownMoleculesSet,__init__ caller=",inspect.stack()[1]#[3], mixture, type(mixture)
        if isinstance(mixture,list):
                self.mixture = Mixture()
                for m in mixture: self.mixture.add(m)
                self.showAll()
        else: self.mixture = mixture
    
    def show(self, mol):
        #print "ShownMolecules show",mol
        self.add(mol)
    
    def showAll(self, mixture=None):
        if mixture != None: self.addMolecules(mixture)
        for mol in self.mixture:
                self.add(mol)

    def add(self, mol):
        super(ShownMoleculesSet, self).add(self.mixture.getMolecule(mol))

    def hide(self, mol):
        self.discard(mol)

    def remove(self, mol):
        #print "ShownMoleculesSet remove ",mol
        #try:
        if isinstance(mol, Molecule):
            super(ShownMoleculesSet, self).remove(mol)
        else:
            super(ShownMoleculesSet, self).remove(self.mixture.getMolecule(mol))
        #except:
            #pass

    def discard(self, mol):
		super(ShownMoleculesSet, self).discard(self.mixture.getMolecule(mol))

    '''
    def discardFrom(self, molIDSet):
		molset = set([ self.mixture.getMolecule(m) for m in molIDSet])
		super(ShownMoleculesSet, self).difference(set(molSet))
	'''

    def duplicate(self, mol):
        pass

    def __deepcopy__(self, memo):
        '''
        Blocks deepcopy because it takes too long.  Copy done manually in push()
        '''
        pass

    def isShown(self, mol):
        #print "isShown ", mol, mol in self.keys(), self[mol]
        try:
            return self.mixture.getMolecule(mol) in self
        except:
            return False
        
    def shownList(self, mixture):
    	print "WARNING: ShownMoleculesSet deprecated."
        return list(self)
    
    def addMolecules(self, mixture):
        for mol in mixture:
            self.add(mol)

    def addDictionary(self, shDict):
        '''
        Adds information from a ShownMolecules object.
        '''
        for mol in shDict:
            if shDict[mol]: self.add(mol)

    def updateMixture(self,mixture):
        self.intersection_update(
            set(
                [self.mixture.getMolecule(mol) for mol in mixture]
        )   )
        self.mixture = mixture

    def names(self):
        return [self.mixture.getMoleculeID(molecule) for molecule in self]
    

class ShownMolecules(dict):
    def __init__(self, mixtute=None):
        '''
        parameter mixture ignored.  Added for baackward compatibility in version 0.43
        '''
        self.modified = time.clock()
        #print "ShownMolecules", self.modified
    
    '''
    def show(self, mol):
        #print "ShownMolecules show",mol
        self[mol] = True
        self.modified = time.clock()
           
    def hide(self, mol):
        self[mol] = False
        self.modified = time.clock()
    
    def remove(self, mol):
        if self.has_key(mol):
            self.pop(mol)


    def duplicate(self, mol):
        if self.has_key(mol):
            self.pop(mol)


    def isShown(self, mol):
        #print "isShown ", mol, mol in self.keys(), self[mol]
        if not mol in self.keys():
            self[mol] = True
        return self[mol]

    def shownList(self, mixture):
        result = list()
        molecules = mixture.molecules()
        for m in self.keys():
            if m in molecules:
                if self[m]: result.append(m)
            else: del self[m] # a bad fix to inconsistent management of data structures
        return result
    
    def modificationTime(self):
        if not self.__dict__.has_key("modified"):
            self.modified = time.clock()
            #print "modificationTime *"
        return self.modified
    
    def addMolecules(self, mixture):
        for mol in mixture:
            if not mol in self.keys():
                self[mol] = True
        for mol in self.keys():
            if not mol in mixture:
                self.pop(mol)
    '''


class FixedMolecules(dict):
    def __init__(self):
        pass
        #print "ShownMolecules", self.modified
    
    def fix(self, mol):
        #print "ShownMolecules show",mol
        self[mol] = True
           
    def loose(self, mol):
        self[mol] = False
    
    def remove(self, mol):
        if self.has_key(mol):
            self.pop(mol)


    def duplicate(self, mol):
        if self.has_key(mol):
            self.pop(mol)


    def isFixed(self, mol):
        #print "isShown ", mol, mol in self.keys(), self[mol]
        if not mol in self.keys():
            self[mol] = False
        return self[mol]

    def fixedList(self):
        result = list()
        for m in self.keys():
            if self[m]: result.append(m)
        return result
    
    def hasFixedMolecules(self):
        return len(self) > 0
    
    def addMolecules(self, mixture):
        for mol in mixture:
            if not mol in self.keys():
                self[mol] = False
        for mol in self.keys():
            if not mol in mixture:
                self.pop(mol)

    def updateMixture(self,mixture):
        self.addMolecules(mixture)

        
