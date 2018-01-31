# -*- coding: utf-8 -*-
'''
Created on Mar 16, 2012

@author: jse
'''
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, 

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
from PyQt4 import QtCore, QtGui
from lib.chemicalGraph.Mixture import Mixture
import platform
from conf.Wolffia_conf import *

#=====================================================================
class PreviewButton(QtGui.QPushButton):
    def __init__(self, state, viewer, parent=None, molname="", initState=True, editor=None):
        super(PreviewButton, self).__init__(parent)
        self.state = state     
        self.shownMolecules = state.shownMolecules
        self.mixture = state.mixture
        self.viewer = viewer
        self.show = initState
        self.moleculeEditor = editor
        self.parent = parent

        #print "PreviewButton__init__ ",molname, initState
        self.setObjectName(molname)
        self._WOLFFIA_OS = platform.system()
        self.iconShow = QtGui.QIcon(WOLFFIA_GRAPHICS+"show.gif")
        self.iconHide = QtGui.QIcon(WOLFFIA_GRAPHICS+"hide.gif")
        #print "PreviewButton ", NANOCAD_BASE+"/interface/graphics/show.gif"
        self.setFlat(True)
        super(PreviewButton, self).setIcon(self.iconHide)
        self.setIcon()
        #self.viewer.update()
        #if parent == self.loaded and not(parent==None) :
            #print "PreviewButton ",parent==None
            #QtCore.QObject.connect(self, QtCore.SIGNAL('clicked()'), self._mySignal)


    
    def mousePressEvent (self, QMouseEvent):
        from BuildTab import ShownSolvent
        self.show = not self.show
        print "mousePressEvent:self.show**************************************",self.show
		
	'''
		if self.objectName()[:8] == "SOLVENT(":
			for solv in self.mixture.molecules():
				if solv[:8] == "SOLVENT(":
					if self.show:
						self.shownMolecules.show(solv)
					else:
						self.shownMolecules.hide(solv)
		'''
	if ShownSolvent.isSolvent(self.objectName()):
			objectSolventType = ShownSolvent.solventType(str(self.objectName()))
			for solv in self.mixture.molecules():
				if ShownSolvent.isSolvent(solv) and ShownSolvent.solventType(solv) == objectSolventType:
					if self.show:
						self.shownMolecules.show(solv)
					else:
						self.shownMolecules.hide(solv)
	elif self.show: 
		    self.shownMolecules.show(str(self.objectName()))
		    #print "mousePressEvent:show",str(self.objectName())
	else:         
		    self.shownMolecules.hide(str(self.objectName()))
		    #print "mousePressEvent:hide",str(self.objectName())
		
	if hasattr(self.parent,'_checkShowShiftModifier_'):
		    self.parent._checkShowShiftModifier_(self,self.show)
		
	self.setIcon()
	if self.moleculeEditor == None: self.viewer.update()
	else: self.viewer.update()

#    def paintEvent(self, e):
#        super(PreviewButton, self).paintEvent(e)
#        self.setIcon()
        
    def setIcon(self):
        if self.show:
            super(PreviewButton, self).setIcon(self.iconHide)
        else:
            super(PreviewButton, self).setIcon(self.iconShow)
                
    def isShown(self):
        return self.show
    
    def setShown(self, update=True):
        self.show = True
        self.shownMolecules.show(str(self.objectName()))
        self.setIcon()
        if update: self.viewer.update()
            
    def setHidden(self, update=True):
        self.show = False
        self.shownMolecules.hide(str(self.objectName()))
        self.setIcon()
        if update: self.viewer.update()
        #print "setIcon", self.viewer
        #self.viewer.update()

#=====================================================================
class FixedButton(QtGui.QPushButton):
    def __init__(self, state, viewer, parent=None, molname="", initState=True):
        super(FixedButton, self).__init__(parent)
        self.state = state     
        self.fixedMolecules = state.fixedMolecules
        self.mixture = state.mixture
        self.viewer = viewer
        self.fixed = initState
        self.parent = parent

        #print "PreviewButton__init__ ",molname, initState
        self.setObjectName(molname)
        self._WOLFFIA_OS = platform.system()
        self.iconShow = QtGui.QIcon(WOLFFIA_GRAPHICS+"pin16off.png")
        self.iconHide = QtGui.QIcon(WOLFFIA_GRAPHICS+"pin16.png")
        #print "FixedButton ", NANOCAD_BASE+"/interface/graphics/show.gif"
        self.setFlat(True)
        super(FixedButton, self).setIcon(self.iconHide)
        self.setIcon()


   
    def mousePressEvent (self, QMouseEvent):
        from BuildTab import ShownSolvent
	self.fixed = not self.fixed
		#print "FixedButton mousePressEvent:self.fixed",self.fixed
	'''
		if self.objectName()[:8] == "SOLVENT(":
			for solv in self.mixture.molecules():
				if solv[:8] == "SOLVENT(":
					if self.fixed:
						self.fixedMolecules.fix(solv)
					else:
						self.fixedMolecules.loose(solv)
		'''
	if ShownSolvent.isSolvent(self.objectName()):
			objectSolventType = ShownSolvent.solventType(str(self.objectName()))
			for solv in self.mixture.molecules():
				if ShownSolvent.isSolvent(solv) and ShownSolvent.solventType(solv) == objectSolventType:
					if self.fixed:
						self.fixedMolecules.fix(solv)
					else:
						self.fixedMolecules.loose(solv)
	elif self.fixed: 
		    self.fixedMolecules.fix(str(self.objectName()))
		    #print "mousePressEvent:show",str(self.objectName())
	else:         
		    self.fixedMolecules.loose(str(self.objectName()))
		    #print "mousePressEvent:hide",str(self.objectName())
		    
	self.parent._checkFixedShiftModifier_(self,self.fixed)
	self.setIcon()
		#self.viewer.update()

#    def paintEvent(self, e):
#        super(FixedButton, self).paintEvent(e)
#        self.setIcon()
        
    def setIcon(self):
        if self.fixed:
            super(FixedButton, self).setIcon(self.iconHide)
        else:
            super(FixedButton, self).setIcon(self.iconShow)
                
    def isFixed(self):
        return self.fixed
    
    def setFixed(self, update=True):
        self.fixed = True
        self.fixedMolecules.fix(str(self.objectName()))
        self.setIcon()
        if update: self.viewer.update()
            
    def setLoose(self, update=True):
        self.fixed = False
        self.fixedMolecules.loose(str(self.objectName()))
        self.setIcon()
        if update: self.viewer.update()
        #print "setIcon", self.viewer
        #self.viewer.update()

