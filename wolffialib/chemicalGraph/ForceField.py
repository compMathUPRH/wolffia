# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Frances  Martínez Miranda, 
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

#import re, copy
#import math
import threading

import sys,os, time
#if __name__ == '__main__':
#	sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../')
#	print sys.path
from conf.Wolffia_conf import CHARMM_FORCE_FIELDS
from wolffialib.chemicalGraph.io.PRM import PRM
from wolffialib.chemicalGraph.io.PRM import PRMError


#_CHARMM_PARAMETER_FILES_=["par_all27_prot_na.prm","par_all32_lipid.prm","par_all35_ethers.prm","par_all36_carb.prm","par_all36_cgenff.prm"]
#_CHARMM_FILES_= ["prot","lipid","ethers","carb","gen"]
_CHARMM_PARAMETER_FILES_=[ \
                          "par_all32_lipid.prm",  \
                          "par_all35_ethers.prm", \
                          "par_all36_carb.prm", \
                          "par_all27_prot_na.prm", \
                          "par_silicates.prm", \
                          "par_all36_cgenff.prm"]
_CHARMM_FILES_= [ \
                 "All-Hydrogen Lipid", \
                 "All-hydrogen ether", \
                 "All-hydrogen carbohydrate", \
                 "All-Hydrogen Proteins", \
                 "Silicates", \
                 "General Force Field"]


class NonBond:
    _EPSILON = 0
    _SIGMA   = 1
    #_CHARGE  = 2




class ForceField(object):
	"""
	Class Fields:
	filename
	_NONBONDED 
	_BONDS
	_ANGLES
	_DIHEDRALS
	"""

	# Positions of bond constants
	KR = 0
	R0 = 1

	def __init__(self,molecule=None,filename=None):
		self.filename   = filename
		#self._CHARGES   = dict()
		self._NONBONDED = dict()
		if molecule != None:
			self.molname    = molecule.molname()
			for t in molecule.atomTypes(): self._NONBONDED[t] = [0.,0.]
		else: self.molname    = "(molecule)"
		
		self._BONDS     = dict()
		self._MASS      = dict()
		self._ANGLES    = dict()
		self._DIHEDRALS = dict()
		self._IMPROPER  = dict()
		self._HBONDS    = dict()
		
		if filename != None:
			self.load(filename)
	
	def __addChargeFieldToNonBond__(self):
	    '''
	    For backward compatibility with versions prior to 0.24-42
	    '''
	    for l in self._NONBONDED:
	        if len(self._NONBONDED[l]) == 2:
	            self._NONBONDED[l].append(0.)
	            
	
	def __eq__(self, other):
	    if isinstance(other, self.__class__):
	        #print "ForceField __eq__", self._NONBONDED, other._NONBONDED, self._NONBONDED == other._NONBONDED
	        if not self._NONBONDED == other._NONBONDED:
	        	#print self._NONBONDED
	        	#print other._NONBONDED
	            pass
	        return  self._NONBONDED == other._NONBONDED \
	            and self._BONDS     == other._BONDS \
	            and self._MASS      == other._MASS \
	            and self._ANGLES    == other._ANGLES \
	            and self._DIHEDRALS == other._DIHEDRALS \
	            and self._IMPROPER  == other._IMPROPER \
	            and self._HBONDS    == other._HBONDS
	    else:
	        return False
	
	
	@staticmethod
	def _listToKey(l):
	    [t1, t2, t3, t4] = l
	    return t1 + " " + t2 + " " + t3 + " " + t4
	    
	
	def __tr__(self, elt):
	    if self.trad == None or not elt in self.trad:
	        return elt
	    else:
	        return self.trad[elt]
	
	
	def addZeroAngles(self, angles):
		for [t1,t2,t3] in angles:
		    if t1 < t3:
		        if not (t1, t2, t3) in self._ANGLES.keys():
		            self._ANGLES[(t1, t2, t3)] = [0.,0.]
		    else:
		        if not (t3, t2, t1) in self._ANGLES.keys():
		            self._ANGLES[(t3, t2, t1)] = [0.,0.]
	
	def addZeroParameters(self, molecule):
	    aTypes = molecule.atomTypes()
	    for t in aTypes:
	        if not t in self._NONBONDED.keys():
	            self._NONBONDED[t] = [0.,0.,0.]
	        #print "FF addZeroParameters self._NONBONDED.keys() ",t,id(self._NONBONDED[t])
	    aTypes = molecule.bondTypes()
	    for t in aTypes:
	        if not t in self._BONDS.keys():
	            self.setBond((t[0],t[1]), 0.,0)
	            self.setBond((t[0],t[1]), 0.,1)
	    #print "FF addZeroParameters self._BONDS.keys() ",self._BONDS.keys()
	    aTypes = molecule.atomTypes()
	    for t in aTypes:
	        if not t in self._MASS.keys():
	            self._MASS[t] = 0.
	    aTypes = molecule.angleTypes()
	    for t in aTypes:
	        if not t in self._ANGLES.keys():
	            self.setAngle((t[0],t[1],t[2]), 0.,0)
	            self.setAngle((t[0],t[1],t[2]), 0.,1)
	    aTypes = molecule.dihedralTypes()
	    for t in aTypes:
	        if not t in self._DIHEDRALS.keys():
	            self.setDihedral((t[0],t[1],t[2],t[3]), 0.,0)
	            self.setDihedral((t[0],t[1],t[2],t[3]), 0 ,1)
	            self.setDihedral((t[0],t[1],t[2],t[3]), 0.,2)
	
	
	def angle(self, t1, t2, t3):
		try:
		    if t1 < t3:
		        return self._ANGLES[(t1, t2, t3)]
		    else:
		        return self._ANGLES[(t3, t2, t1)]
		except:
		    return [0.,0.]
	
	
	def bond(self, t1, t2):
	    try:
	        if t1 < t2:
	            return self._BONDS[(t1, t2)]
	        else:
	            return self._BONDS[(t2, t1)]
	    except:
	        return [0.,0.]
	
	'''
	removed in version 1.31
	def charge(self, t):
		#print "ForceField charge", t, self._NONBONDED
		#return self._NONBONDED[t][NonBond._CHARGE]
		 try:
		     #print "ForceField charge B1", t, self._NONBONDED, "OK"
		     return self._NONBONDED[t][NonBond._CHARGE]
		 except:
		     #print "ForceField charge B2", t, self._NONBONDED, "OK"
		     return 0.
	'''
	
	def clean(self, types):
		'''
		This is a temporary fix for removing unused types from the data fields.
		'''
		#types = [t.typeName() for t in typesObj]
		for t in list(self._NONBONDED.keys()):
		    if not t in types: del self._NONBONDED[t]
		
		for b in list(self._BONDS.keys()):
			#print "FF clean bond",b
			if not(b[0] in types or b[1] in types): del self._BONDS[b]
		
		for a in list(self._ANGLES.keys()):
			if not(a[0] in types or a[1] in types or a[2] in types): del self._ANGLES[a]
			
		for d in list(self._DIHEDRALS.keys()):
			if not(d[0] in types or d[1] in types or d[2] in types or d[3] in types): 
				del self._DIHEDRALS[d]
		
		'''
		for i in self._IMPROPER.keys():
		    if i.split(' ') in types: del self._IMPROPER[i]
		
		for h in self._HBONDS.keys():
		    if h.split(' ') in types: del self._HBONDS[h]
		'''
	
	    
	
	def copy(self):
	    import copy
	    return copy.deepcopy(self)
	
	
	def dihedral(self, t1, t2, t3, t4):
	    types = self.sortDihedral(t1, t2, t3, t4)
	    #print "FF dihedral",types,self._DIHEDRALS.keys()
	    if types in self._DIHEDRALS.keys():
	        return self._DIHEDRALS[types]
	    '''
	    count = 0
	    while (count < 2):
	        for i in range(4):
	            ti = types[i]
	            types[i] = "X"
	            if self._listToKey(types) in self._DIHEDRALS.keys():
	                return self._DIHEDRALS[self._listToKey(types)]
	            for j in range(i+1, 4):
	                tj = types[j]
	                types[j] = "X"
	                if self._listToKey(types) in self._DIHEDRALS.keys():
	                    return self._DIHEDRALS[self._listToKey(types)]
	                types[j] = tj
	            types[i] = ti
	        types.reverse()
	        count += 1
	'''
	    return [0., 0., 0.]
	
	
	def getTypes(self):
	    return self._NONBONDED.keys()
	
	
	def guess(self, molecule, timeLimit=float("inf"), options=_CHARMM_FILES_, includeHydrogens=True):
	    """
	    Spawns a thread for each CHARMM file.  They run until the specified time limit expires.
	    """
	    
	    minPot = float("inf")
	    pareoMin = list()
	    pairings = None
	    #timeSlot = timeLimit / len(options)
	    
	    self.addZeroParameters(molecule)
	    
	    timeSlot = timeLimit
	    for fftype in options:
	        fn       = _CHARMM_PARAMETER_FILES_[_CHARMM_FILES_.index(fftype)]
	        #print "ForceField guess", fftype, fn
	        charmFF  = ForceField(None, filename=CHARMM_FORCE_FIELDS+fn)
	        pareoMin.append(FFPairings(molecule,charmFF, timeLimit=timeSlot, includeHydrogens=includeHydrogens))
	        
	    for pThread in pareoMin:
	        pThread.start()
	        
	    active = True
	    while active:
	        active = False
	        for pThread in pareoMin:
	            active = active or pThread.isAlive()
	            #print "ForceField guess > ", pThread.getMatches()
	            #print "ForceField guess > pThread.minPot < minPot", pThread.minPot, minPot
	            if pThread.minPot < minPot:
	                minPot = pThread.minPot
	                pairings = pThread
	    return pairings
	
	def isDefined(self, k):
	    return k in self._NONBONDED
	
	
	def hasType(self,t):
		from wolffialib.chemicalGraph.AtomAttributes import AtomInfo
		if isinstance(t, AtomInfo):
			return t in self.getTypes()
		else:
			return t in self.getTypes()
	
	
	def load(self,filename):
	    """
	    Reads force field.  Assumes PRM format.
	    
	    @type  filename: string
	    @param filename: PRM filename.
	    """
	
	    self.loadCHARMM(filename)
	
	
	def loadCHARMM(self,filename):
		"""
		Reads force field in loadCHARMM format.
		
		@type  filename: string
		@param filename: PRM filename.
		"""
		reader = PRM(self.molname, filename)
		#print "loadCHARMM reader =", reader['BOND'].keys()
		self.filename = filename
		
		if len(self._NONBONDED) == 0: #load everything
				self._NONBONDED = reader['NONB']
				for b in reader['BOND']:
					self._BONDS[tuple(b.split(' '))] = reader['BOND'][b]
				for a in reader['ANGL']:
					self._ANGLES[tuple(a.split(' '))] = reader['ANGL'][a]
				for d in reader['DIHE']:
					self._DIHEDRALS[tuple(d.split(' '))] = reader['DIHE'][d]
		else:
			for t in self._NONBONDED:
				[epsilon,rd,  ch] = reader['NONB'][t]
				self.setNonBond(t, rd, NonBond._SIGMA)
				self.setNonBond(t, epsilon, NonBond._EPSILON)
			#print "loadCHARMM self._NONBONDED = ", self._NONBONDED
				
			for t1 in self._NONBONDED:
				for t2 in self._NONBONDED:
					try: 
						self._BONDS[(t1,t2)] = reader['BOND'][t1+' '+t2]
						#print "loadCHARMM self._BONDS[[t1,t2]] = ", self._BONDS[(t1,t2)] ,reader['BOND'][t1+' '+t2]
					except: pass
					try: 
						self._BONDS[(t2,t1)] = reader['BOND'][t2+' '+t1]
						#print "loadCHARMM self._BONDS[[t2,t1]] = ", self._BONDS[(t2,t1)] ,reader['BOND'][t2+' '+t1]
					except: pass
			#print "loadCHARMM self._BONDS = ", self._BONDS
		
			for t1 in self._NONBONDED:
				for t2 in self._NONBONDED:
					for t3 in self._NONBONDED:
						try: self._ANGLES[(t1,t2,t3)] = reader['ANGL'][t1+' '+t2+' '+t3]
						except: pass
						try: self._ANGLES[(t3,t2,t1)] = reader['ANGL'][t3+' '+t2+' '+t1]
						except: pass
		
			#print "loadCHARMM self._ANGLES = ", self._ANGLES
			
			for t1 in self._NONBONDED:
				for t2 in self._NONBONDED:
					for t3 in self._NONBONDED:
						for t4 in self._NONBONDED:
							try: self._DIHEDRALS[(t1,t2,t3,t4)] = reader['DIHE'][t1+' '+t2+' '+t3+' '+t4]
							except: pass
							try: self._DIHEDRALS[(t4,t3,t2,t1)] = reader['DIHE'][t4+' '+t3+' '+t2+' '+t1]
							except: pass
			#print "loadCHARMM", reader['DIHE'],self._DIHEDRALS
	
	
	def merge(self, ff, typesToMerge=None):
	    """
	    Merges valued from second force field into self.
	    """
	    pars = ["_NONBONDED", \
	            "_BONDS"    , \
	            "_MASS"     , \
	            "_ANGLES"   , \
	            "_DIHEDRALS", \
	            "_IMPROPER" , \
	            "_HBONDS"     ]
	    
	    #print "ForceField merge typesToMerge", typesToMerge
	    if typesToMerge == None: typesToMerge = ff._NONBONDED.keys()
	    #print "ForceField merge typesToMerge2", typesToMerge
	    
	    for pType in pars:
		    #print "ForceField merge", pType, self.__dict__[pType]
		    #print "ForceField merff", pType, ff.__dict__[pType]
		    for k in ff.__dict__[pType].keys():
		        copyOK =True
		        for aType in k:
		            #print "for aType in k.split(' '): ", aType
		            copyOK = aType in typesToMerge
		            if not copyOK: break
		        if copyOK or k in typesToMerge:  # k in typesToMerge  fixed NONB problem
		            self.__dict__[pType][k] = ff.__dict__[pType][k]
		            #print ">",k
		#print "ForceField merge 2 ", pType, self.__dict__[pType]
	
	
	def nonBond(self, t):
	    try:
	        return self._NONBONDED[t]
	    except:
	        return [0.,0.,0.]
	
			
	def renameTypes(self, nameTable):
	    #print "renameTypes  ", nameTable, self._NONBONDED.keys()
	    resultDict = dict()
	    for nonb in self._NONBONDED.keys():
	        if nonb in nameTable:
	            #resultDict[nameTable[nonb]] = nameTable.getForceField()._NONBONDED[nameTable[nonb]]
	            resultDict[nameTable[nonb]] = self._NONBONDED[nonb]
	        else:
	            nameTable[nonb] = nonb
	            resultDict[nonb] = self._NONBONDED[nonb]
	    self._NONBONDED = resultDict
	    
	    #print "renameTypes2 ", nameTable, self._NONBONDED.keys()
	    resultDict = dict()
	    for bond in self._BONDS.keys():
	        t1, t2 = bond
	        try:
	        	resultDict[(nameTable[t1], nameTable[t2])] = self._BONDS[bond]
	        except KeyError:
	        	pass
	    self._BONDS = resultDict
	    
	    resultDict = dict()
	    for angle in self._ANGLES.keys():
	        t1, t2, t3 = angle
	        try:
	        	resultDict[(nameTable[t1], nameTable[t2], nameTable[t3])] = self._ANGLES[angle]
	        except KeyError:
	        	pass
	    self._ANGLES = resultDict
	    
	    resultDict = dict()
	    for dih in self._DIHEDRALS.keys():
	        t1, t2, t3, t4 = dih
	        try:
	        	resultDict[(nameTable[t1], nameTable[t2], nameTable[t3], nameTable[t4])] = self._DIHEDRALS[dih]
	        except KeyError:
	        	pass
	    self._DIHEDRALS = resultDict
	    
	    
	def setAngle(self, t, val, pos):
		assert(isinstance(t,tuple))
		if t[2] < t[0]:
		    t = (t[2], t[1], t[0])
		if not t in self._ANGLES:
		    self._ANGLES[t] = [0,0]
		self._ANGLES[t][pos] = val
		
		#if self._ANGLES[t] == [0,0]:
		#    self._ANGLES.pop(t)
		
	
	def setBond(self, t, val,pos):
		assert(isinstance(t,tuple))
		if t[1] < t[0]:
		    t = (t[1],t[0])
		if not t in self._BONDS:
		    self._BONDS[t] = [0,0]
		self._BONDS[t][pos] = val
		
		#if self._BONDS[t] == [0,0]:
		#    self._BONDS.pop(t)
	
	
	'''
	removed in version 1.31
	def setCharge(self, t, val):
	    print "ForceField setCharge ", t, val
	    self.setNonBond(t, val, NonBond._CHARGE)
	'''
	
	
	def setDihedral(self, t, val, pos):
		assert(isinstance(t,tuple))
		t = self.sortDihedral(t[0], t[1], t[2], t[3])
		if not t in self._DIHEDRALS:
		    self._DIHEDRALS[t] = [0,0,0]
		self._DIHEDRALS[t][pos] = val
		
		#if self._DIHEDRALS[t] == [0,0,0]:
		#    self._DIHEDRALS.pop(t)
	
	
	def setNonBond(self, t, val, nbPar):
	    '''
	    Sets the non-bond parameters associated to type 't'
        
	    str t: a type name
	    float val: a value for the parameter.
	    NonBond pos: one of the static values in NonBond class defined above.
	    '''
	    if not t in self._NONBONDED:
	        self._NONBONDED[t] = [0,0,0]
	    self._NONBONDED[t][nbPar] = val
	    #print "setNonBond ", t, val, pos, id(self), id(self._NONBONDED[t])
	    
	    #if self._NONBONDED[t] == [0,0,0]:
	    #    self._NONBONDED.pop(t)
	
	
	@staticmethod
	def sortDihedral(t1, t2, t3, t4):
	    if t1 < t4 or (t1 == t4 and t2 < t3):
	        return (t1, t2, t3, t4)
	    else:
	        return (t4, t3, t2, t1)
	
	
	def update(self, ff, keepTypes=True):
	    '''
	    Updates self with non-zero parameters in ff. (this is why dct.update() is not used)
	    '''
	    if ff.filename != None: self.filename = ff.filename
	
	    for t in ff._NONBONDED:
	        if ff._NONBONDED[t] != [0.,0.,0.]: self._NONBONDED[t] = ff._NONBONDED[t]
	        
	    for b in ff._BONDS:
	        if ff._BONDS[b] != [0.,0.]: self._BONDS[b] = ff._BONDS[b]
	        
	    for a in ff._ANGLES:
	        if ff._ANGLES[a] != [0.,0.]: self._ANGLES[a] = ff._ANGLES[a]
	        
	    for d in ff._DIHEDRALS:
	        if ff._DIHEDRALS[d] != [0.,0,0.]: self._DIHEDRALS[d] = ff._DIHEDRALS[d]
	    #print "FF update", self._NONBONDED
	
	def upgrade(self, version):
		if version < "1.137":
			newB = dict()
			for b in self._BONDS:
				if isinstance(b,tuple): return # FF already updated
				newB[tuple(b.split(' '))]     = self._BONDS[b]
			del self._BONDS
			self._BONDS = newB
			
			newA = dict()
			for a in self._ANGLES:
				if isinstance(a,tuple): return # FF already updated
				newA[tuple(a.split(' '))]    = self._ANGLES[a]
			del self._ANGLES
			self._ANGLES = newA
			
			newD = dict()
			for d in self._DIHEDRALS:
				if isinstance(d,tuple): return # FF already updated
				newD[tuple(d.split(' '))] = self._DIHEDRALS[d]
			del self._DIHEDRALS
			self._DIHEDRALS = newD
	
	#-----------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------
	def writeCHARMM(self,filename, mode="w", trad=None):
		#print "FF.writeCHARMM: ", self._ANGLES, trad
		prm = PRM(self.molname,None,mass=self._MASS,nonb=self._NONBONDED,bond=self._BONDS,angl = self._ANGLES,dihe=self._DIHEDRALS,impr=self._IMPROPER,hbon=self._HBONDS)
		try: 
			prm.writeCHARMM(filename, mode, trad)
		except : 
			#print "writeCHARMM"
			raise


#==========================================================================

#import openbabel

class FFPairings(threading.Thread):
    def __init__(self, molecule, ff, timeLimit=float("inf"), includeHydrogens=True):
        threading.Thread.__init__(self)
        self.FFcharm   = ff
        self.molecule  = molecule
        self.parMin    = None
        self.resultFF  = None
        self.minPot    = float('inf')
        self.matches   = 0

        self.timeLimit = timeLimit
        self.startTime = time.clock()

        if includeHydrogens:
	        self.tiposMol       = molecule.atomTypes() 
        else:
	        self.tiposMol       = list()  
	        for t in molecule.atomTypes():
		        if includeHydrogens or t[0] != 'H': 
			        self.tiposMol.append(t)

        self.tiposFF        = self.FFcharm._NONBONDED
        #print "FFPairings __init__  self.tiposMol ",  self.tiposMol
        #print "FFPairings __init__  self.tiposFF ",  self.tiposFF

        FFPairings.__sortElements  (self.tiposMol) 
        
    def run(self):
        #print "FFPairings run A ",   self.tiposMol, self.tiposFF.keys()
        self.__pareaListas(self.tiposMol, self.tiposFF.keys())
        if self.parMin != None:
	        self.resultFF  = ForceField(self.molecule)
	        self.resultFF.merge(self.molecule.getForceField())
	        #print "FFPairings run before ",   self.resultFF._NONBONDED.keys()
	        self.resultFF.renameTypes(self.parMin)
	        self.resultFF.merge(self.FFcharm, self.resultFF._NONBONDED.keys())
	        #print "FFPairings run",   self.resultFF._NONBONDED.keys()
	        #self.resultFF.merge(self.FFcharm, self.molecule.atomTypes())
    '''        
    def inverse(self):
        self.parMin = {v:k for k, v in self.parMin.items()}
        self.resultFF.renameTypes(self.parMin)
        return self
    '''        
        
    def getPairedForceField(self, oldFF):#, keepCharges=False):
        #print "FFPairings getPairedForceField  self.parMin",   self.parMin
        #print "FFPairings getPairedForceField, oldFF._NONBONDED",  oldFF._NONBONDED
        #print "FFPairings getPairedForceField, self.resultFF._NONBONDED",  self.resultFF._NONBONDED
        newFF = ForceField()

        for nonb  in self.parMin.keys():
            #print "FFPairings getPairedForceField self.parMin[nonb]", nonb,self.parMin[nonb],oldFF._NONBONDED.has_key(nonb),oldFF._NONBONDED.keys()
            newFF._NONBONDED[nonb] = list(self.resultFF._NONBONDED[self.parMin[nonb]])
            #if keepCharges and oldFF._NONBONDED.has_key(nonb): 
            #    newFF._NONBONDED[nonb][NonBond._CHARGE] = oldFF._NONBONDED[nonb][NonBond._CHARGE]

        #print "FFPairings getPairedForceField,oldFF._BONDS.keys()",  oldFF._BONDS.keys()
        for bond  in oldFF._BONDS.keys():
	        t1, t2 = bond
	        try:
	            vals   = [val for val in self.resultFF.bond(self.parMin[t1], self.parMin[t2])]
	            newFF.setBond(bond, vals[0], 0)
	            newFF.setBond(bond, vals[1], 1)
	        except KeyError:
	            pass
        #print "FFPairings getPairedForceField,oldFF._ANGLES.keys()",  oldFF._ANGLES.keys()
        for angle in oldFF._ANGLES.keys():
            t1, t2, t3 = angle
            try:
                vals   = [val for val in self.resultFF.angle(self.parMin[t1], self.parMin[t2], self.parMin[t3])]
                newFF.setAngle(angle, vals[0], 0)
                newFF.setAngle(angle, vals[1], 1)
            except KeyError:
                pass

        for dih in oldFF._DIHEDRALS.keys():
            t1, t2, t3, t4 = dih
            try:
                vals   = [val for val in self.resultFF.dihedral(self.parMin[t1], self.parMin[t2], self.parMin[t3], self.parMin[t4])]
                newFF.setDihedral(dih, vals[0], 0)
                newFF.setDihedral(dih, vals[1], 1)
                newFF.setDihedral(dih, vals[2], 2)
            except KeyError:
                pass
                   
        return newFF

    def getForceField(self):
        #print "FFPairings getForceField",   self.FFcharm._NONBONDED.keys()
        return self.resultFF

    def getPairing(self):
        #print "FFPairings getForceField",   self.FFcharm
        return self.parMin

    def getMatches(self): return self.matches
    
    @staticmethod
    def __sortElements(elts):
        """
        Sorts elements in list according to atomic number
        """
        table = openbabel.OBElementTable()
        res = list()
        for e in elts:
            for l in [3,2,1]:
                num = table.GetAtomicNum(e[:l])
                if num > 0:
                    res.append("%03d%s" % (num,e))
                    break
        res.sort()
        #print "__sortElements", res
        del elts[:]
        for e in res: elts.append(e[3:])
        #print "__sortElements", elts

    def __lj(self, a1, a2, pareo):
        e1, l1 = self.FFcharm.nonBond(pareo[a1.getType()])
        e2, l2 = self.FFcharm.nonBond(pareo[a2.getType()])
        e, l = (e1+e2)/2., (l1+l2)/2.
        q6 = (l/a1.distanceTo(a2))**6
        return 4 * e * (q6 - 1)*q6

    def __hbond(self, a1, a2, pareo):
        k, l = self.FFcharm.bond(pareo[a1.getType()], pareo[a2.getType()])
        return k * (a1.distanceTo(a2) - l)**2

    def __potencial(self, pareo):
        pot = 0.
        #pareados = self.keys()
        for atom1 in self.molecule:
            a1 = self.molecule.getAtomAttributes(atom1)
            for atom2 in self.molecule:
                if atom1 != atom2:
                    pot += self.__lj(a1, self.molecule.getAtomAttributes(atom2), pareo)
    
        for bond in self.molecule.bonds():
            #print "potencial", bond
            pot += self.__hbond(self.molecule.getAtomAttributes(bond[0]),self.molecule.getAtomAttributes(bond[1]), pareo)
    
        return pot

    def __cuadraEnlaces(self, pareo):
        #print "cuadraEnlaces ", pareo, 
        for bond in self.molecule.bonds():
            t1 = self.molecule.getAtomAttributes(bond[0]).getInfo().getType()
            t2 = self.molecule.getAtomAttributes(bond[1]).getInfo().getType()
            if t1 in pareo and t2 in pareo:
            	#print " molOK ",
                t1 = pareo[t1]
                t2 = pareo[t2]
                if not ((t1, t2) in self.FFcharm._BONDS or (t2, t1) in self.FFcharm._BONDS):
                    #print False
                    return False
        #print True
        return True

    def __prametersFound(self, pairs):
        '''
        Used as criterion to select the best Force field for the given molecule based
        on how many parameters have been found. Dihedrals counts will matter only if 
        there is a tie in angles counts.
        '''
         
        count = 0
        for t1,t2,t3 in self.molecule.angleTypes():
            #print "__prametersFound ", t1,t2,t3
            try:
             	k, l = self.FFcharm.angle(pairs[t1], pairs[t2], pairs[t3])
            except KeyError:
            	continue
            if k != 0 or l != 0: count += 1
        
        dT = self.molecule.dihedralTypes()
        count *= len(dT) # ensures that dihedrals count will matter only if there is a tie in angles count
        
        for t1,t2,t3,t4 in dT:
            #print "__prametersFound ", t1,t2,t3,t4
            try:
	            k, n, l = self.FFcharm.dihedral(pairs[t1], pairs[t2], pairs[t3], pairs[t4])
            except KeyError:
	            continue
            if k != 0 or l != 0: count += 1
        return count
    
    def __pareaListas(self, lista1, lista2, result=None, pareo=None):
        #print "__pareaListas ", pareo, lista1
        if result == None: result = list()
        if pareo  == None: pareo  = dict()
        if len(lista1) == 0:
            if self.__cuadraEnlaces(pareo): # or cuadraAngulos(pareo):
                #print "\n __pareaListas-pareo----> ", pareo
                if not pareo in result:
                    self.matches  += 1
                    result.append(pareo)
                    #pot = abs(self.__potencial(pareo))  # discarded in favor of measuring how may parameters are found
                    pot = -self.__prametersFound(pareo)
                    #print "\n-----> ", pareo
                    #print "\n-----> pot ", pot, " NEW", (pot  < self.minPot)
                    if pot  < self.minPot:
                        #print "-----> ", pareo, pot
                        #print "%8.2f\033[12D", pot
                        self.minPot = pot
                        self.parMin = dict(pareo)
                        #print "-----> ", self, pot
                        return True
        else:
            t1 = lista1.pop()
            subMatch = False
            if t1 in lista2:  # perfect matches considered first
            	lista2.remove(t1)
            	lista2.insert(0, t1)
            for t2 in lista2:
                #print "%6s" % t2,
                #sys.stdout.flush()
                #print "probando ", t1,' ', t2, "  pareo: ", pareo
                #time.sleep(.1)
                if t1[0] == t2[0]:
                    pareo[t1] = t2
                    if self.__cuadraEnlaces(pareo): # or cuadraAngulos(pareo):
                        #porProbar2.remove(t2)
                        if self.__pareaListas(lista1, lista2, result, pareo):
                        	subMatch = True
                        else:
                        	#print "__pareaListas", pareo
                        	pot = -self.__prametersFound(pareo)
                        	#if self.parMin == None or len(self.parMin) < len(pareo) or (len(self.parMin) == len(pareo) and pot  < self.minPot):
                        	if self.parMin == None or  pot  < self.minPot:
		                        self.minPot = pot
		                        self.parMin = dict(pareo)
		                        subMatch = True
                        		#print "sub--> ", -pot, len(pareo), pareo
                        #porProbar2.append(t2)
                    pareo.pop(t1)
                #print "\033[8D        \033[8D",
                if time.clock() - self.startTime > self.timeLimit: return
            lista1.append(t1)
            #print "__pareaListas ", lista1
            return subMatch
#==========================================================================
if __name__ == '__main__':
#    print( "Probando ForceField")
    m = ForceField("Probando ForceField")
    m.load("../../data/forceFields/PMMA.prm")
    print( "FF__main__: ", m._ANGLES)
    trad={'HT': 'ht', 'CZ':'XX'}
    
    m.writeCHARMM("/tmp/prueba.prm", trad=trad)
    print( "FF__main__: ", m._ANGLES)
    #print " Probando ForceFieldWriter"
    #r = ForceFieldWriter()
    #r.load("/home_inv/frances/Desktop/CLF.prm" )
    #print "load archivoWriter"

