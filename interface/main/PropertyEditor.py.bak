# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  PropertyEditor.py
#  Version 0.1, October, 2011
#  Widget for managing molecules.
#
#  Part of the Wolffia simulation controller
#
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 

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

from sets import Set
from PyQt4 import QtCore, QtGui
from ui_PropertyEditor import Ui_propertyEditor
from lib.chemicalGraph.Mixture import Mixture

class PropertyEditor(QtGui.QWidget):
    def __init__(self, viewer, history):
        super(PropertyEditor, self).__init__()

        # set class fields
        self.viewer = viewer
        self.history = history

        #widgets import
        self.ui = Ui_propertyEditor()
        self.ui.setupUi(self)
        
        self.tree = self.ui.propertyTree
        self.tree.  setColumnWidth(0, 100)
        self.tree.  setColumnWidth(1, 140)        

        #initializes widgets on tree
        self.xRotate = QtGui.QDoubleSpinBox(self.tree)
        self.xRotate.  setSingleStep (10.)
        self.xRotate.  setRange (-360., 360.)
        xRotateAt    = self.tree.topLevelItem(1).child(0)
        
        self.yRotate = QtGui.QDoubleSpinBox(self.tree)
        self.yRotate.  setSingleStep (10.)
        self.yRotate.  setRange (-360., 360.)
        yRotateAt    = self.tree.topLevelItem(1).child(1)
        
        self.zRotate = QtGui.QDoubleSpinBox(self.tree)
        self.zRotate.  setSingleStep (10.)
        self.zRotate.  setRange (-360., 360.)
        zRotateAt    = self.tree.topLevelItem(1).child(2)

        self.xMoveBy = QtGui.QDoubleSpinBox(self.tree)
        self.xMoveBy.  setSingleStep (0.5)
        self.xMoveBy.  setRange (-1000., 1000.)
        xMoveByAt    = self.tree.topLevelItem(2).child(0)
        
        self.yMoveBy = QtGui.QDoubleSpinBox(self.tree)
        self.yMoveBy.  setSingleStep (0.5)
        self.yMoveBy.  setRange (-1000., 1000.)
        yMoveByAt    = self.tree.topLevelItem(2).child(1)
        
        self.zMoveBy = QtGui.QDoubleSpinBox(self.tree)
        self.zMoveBy.  setSingleStep (0.5)
        self.zMoveBy.  setRange (-1000., 1000.)
        zMoveByAt    = self.tree.topLevelItem(2).child(2)
        
        #adds widgets to tree 
        self.tree.setItemWidget(xRotateAt, 1, self.xRotate)  
        self.tree.setItemWidget(yRotateAt, 1, self.yRotate)                
        self.tree.setItemWidget(zRotateAt, 1, self.zRotate)   

        self.tree.setItemWidget(xMoveByAt, 1, self.xMoveBy)  
        self.tree.setItemWidget(yMoveByAt, 1, self.yMoveBy)                
        self.tree.setItemWidget(zMoveByAt, 1, self.zMoveBy)
         
        #manages widget events
        self.xRotate.valueChanged.connect(self.Rotate)
        self.yRotate.valueChanged.connect(self.Rotate)
        self.zRotate.valueChanged.connect(self.Rotate)

        self.xMoveBy.valueChanged.connect(self.MoveBy)
        self.yMoveBy.valueChanged.connect(self.MoveBy)
        self.zMoveBy.valueChanged.connect(self.MoveBy)

        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)

        #initialize tree window
        self.reset()

    def reset(self):
        #print "PropertyEditor reset "
        self.mixture  = Mixture(None)
        self.registry = dict()
        #self.ident    = None
        
        self.resetBoxes()
        self.setToolTip("Select molecules to activate.")
        self.setEnabled(False)
        self.update()

    def update(self):
        # update resistry
        presentMolecules = self.history.currentState().getMixture().molecules()
        #print "PropertyEditor update  ",presentMolecules, self.registry
        regKeys = self.registry.keys()
        for regKey in regKeys:
            if not regKey in presentMolecules:
                if self.mixture.hasMoleculeID(regKey): self.mixture.remove(regKey)
                self.registry.pop(regKey)

        self.resetBoxes()
        QtGui.QWidget.update(self)

    def resetBoxes(self):
        if len(self) == 0:
            self.tree.topLevelItem(0).setText(1, "")
        else:
            self.tree.topLevelItem(0).setText(1, str(self))
        self.dx = 0.
        self.dy = 0.
        self.dz = 0.
        self.anglex = 0.
        self.angley = 0.
        self.anglez = 0.
        
        self.xRotate.setValue(0.)
        self.yRotate.setValue(0.)
        self.zRotate.setValue(0.)

        self.xMoveBy.setValue(0.)
        self.yMoveBy.setValue(0.)
        self.zMoveBy.setValue(0.)

    #show molecule name in the editor
    def setMolecule(self, molecule, ident, removeIfPresent=False):
        '''
        Returns True if the molecule ends up selected, False otherwise..
        '''
        from BuildTab import ShownSolvent
        #print "PropertyEditor setMolecule new", ident,  self.registry
        if not self.registry.has_key(ident):
            if ShownSolvent.isSolvent(ident):
                mixture = self.history.currentState().getMixture()
                mixtureNames = mixture.molecules()
                #print "PropertyEditor setMolecule SOLVENT(",mixtureNames
                pos = ident.find(')')+1
                for mol in mixtureNames:
                    if mol[:pos] == ident[:pos]:
                        self.registry[mol] = self.mixture.add(mixture.getMolecule(mol), False)
                        self.registry[mol] = mixture.getMolecule(mol)
            else:
                #print "PropertyEditor setMolecule adding", ident
                self.registry[ident] = molecule
                #print "PropertyEditor setMolecule adding to mixture", ident, self.mixture.molecules()
                self.mixture.add(molecule, False)
            
            #self.ident = ident
            #self.ident = self.getId()
            self.setToolTip("Manage molecules' positions.")
            self.setEnabled(True)
            return False
            self.resetBoxes()
        else:
            #print "PropertyEditor setMolecule duplicate",ident,  self.registry
            if removeIfPresent:
				if ShownSolvent.isSolvent(ident):
					mixture = self.history.currentState().getMixture()
					mixtureNames = mixture.molecules()
					pos = ident.find(')')+1
					for mol in mixtureNames:
						#print "PropertyEditor removing ",ident[:pos], mol[:pos]
						if mol[:pos] == ident[:pos]:
							#print "PropertyEditor OK "
							self.removeSelection(mixture.getMolecule(mol), mol)
				else:
					self.removeSelection(molecule, ident)
				return True
        #print "PropertyEditor setMolecule reseting"
        #print "PropertyEditor setMolecule finished"


    def removeSelection(self, molecule, ident):
        if self.registry.has_key(ident):
            self.mixture.remove(self.mixture.getMoleculeID(molecule))
            self.registry.pop(ident)
            #print "PropertyEditor removeSelection removed:",ident
            if len(self.registry) == 0:
                self.reset()
            #print "PropertyEditor setMolecule reseting"
            self.resetBoxes()
    
    def hasSelections(self): return len(self.registry) > 0

    def selectedMolecules(self):
    	#print "selectedMolecules ", self.registry
        return self.registry.values()

    def selectedNames(self):
    	#print "selectedMolecules ",self.registry
        return self.registry.keys()

    def __str__(self):
        return str(self.registry.keys())

    def __len__(self):
        return len(self.registry)
    
    #show rotation values in the editor     
    def Rotate(self):        
    	if self.mixture.order() > 0:
	        x = self.xRotate.value()
	        y = self.yRotate.value()
	        z = self.zRotate.value()
	        value = str(x) + " x " + str(y) + " x " + str(z)
	        self.tree.topLevelItem(1).setText(1, value)
	        center = self.mixture.center()
	        self.mixture.moveBy([-xx for xx in center])
	        #print "Rotate ", x-self.anglex,y-self.angley,z-self.anglez
	        self.mixture.rotateDeg(x-self.anglex,y-self.angley,z-self.anglez)
	        self.mixture.moveBy(center)
	        self.anglex = x
	        self.angley = y
	        self.anglez = z
	
	        self.history.currentState().getMixture().setChanged()
	        self.viewer.update()
        else:
            self.tree.topLevelItem(1).setText(1, "0 x 0 x 0")

    def MoveBy(self):
        x = self.xMoveBy.value()
        y = self.yMoveBy.value()
        z = self.zMoveBy.value()

        value = str(x) + " x " + str(y) + " x " + str(z)
        self.tree.topLevelItem(2).setText(1, value)  
        self.mixture.moveBy([x-self.dx,y-self.dy,z-self.dz])
        self.dx = x
        self.dy = y
        self.dz = z
        self.history.currentState().getMixture().setChanged()
        self.viewer.update()

    def getId(self):
        return str(self.mixture.moleculeNames())
    
if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    editor = PropertyEditor()
    editor.show()
    sys.exit(app.exec_())
