# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  SetupTab.py
#  Version 0.1, December, 2011
#
#  NanoCAD main window.
#
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, 

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

from PyQt5 import Qt, QtCore, QtGui
from ui_SetupTab import Ui_setupTab

import sys,os,math,time

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import *

#from interface.main.History import History, NanoCADState
from interface.main.MixtureViewer import MixtureViewer
from interface.main.Drawer import Drawer

_BOX_INCREASE_FACTOR = 1.2
#_SEPARATION_BETWEEN_SOLVENTS_ = 8 #0.0334 molecules/A**-3.
_AVOGRADRO_CONSTANT_ = 6.02214129e+23

class SetupTab(QtGui.QFrame):  

	"""
	Class fields: 
	_solvent
	"""

	SOLVENT_TO_CLASS = {"Water":"WATER", "Chloroform":"CLF", "Chloroform (4 atoms)":"CLF4", "Acetone":"AcetoneAllH", "THF":"THF", "Argon":"Argon"}
	
	# DENSITY[solvent] = [Density in g/cm3, temperatue in K, molar mass]
	DENSITY = {None:[0,0,1],"Water": [0.9970479,298.15,18.01528], "Chloroform":[1.483,298.15,119.38], "Chloroform (4 atoms)": [1.483,298.15,119.38], "Acetone": [0.786,293.15,58.08], "THF": [0.886,293.15,72.11], "Argon": [5.537, 0.03049,39.948], "Methanol": [0.791,293.15,32.04], "Selected Molecule": [0.9970479,298.15,18.01528]}
	DI = 0
	TI = 1
	MI = 2
	
	def __init__(self, hist, parent, preview):
		super(SetupTab, self).__init__(parent)

		self._history 	= 		hist
		self._solvent 	= 		None
		self.wolffia    =       parent
		self.allowUpdate = True
		self.firstUpdate = True
		self.preview = preview

		#widgets import 
		self.ui = Ui_setupTab()
		self.ui.setupUi(self)

		#activates the previewer
		#self.preview = MixtureViewer(hist, parent=self, sharedGL=GlList)
		#self.ui.setupPreviewLayout.addWidget(self.preview)
		
		self.ui.boundStackedWidget.setEnabled(False)
		
			#self.ui.boundStackedWidget.setEnabled(True)	
		self.setBoundBox()
		self.setCellOriginSpinners()
		
		# initialize solvent section
		self._solvent 		=	str(self.ui.solventComboBox.currentText())
		self._density       =   self.DENSITY[self._solvent][self.DI]
		self._vol           = 0.0
		self.ui.densitySpinBox.setValue(self._density)
		self.ui.addButton.setIcon(QtGui.QIcon().fromTheme("list-add"))
		self.ui.removeButton.setIcon(QtGui.QIcon().fromTheme("list-remove"))
		self.updateVolume()

	def setBoundBox(self):
		self.ui.boxBoundButton.setChecked(self._history.currentState().hasBox())
		self.ui.noneRButton.setChecked(not self._history.currentState().hasBox())

	def updateVolume(self):
		if self._history.currentState().hasBox():
			self.ui.volLineEdit.setText("%.3f" % (self.getBoxVolume()/1000))
			self._vol			=	self.getBoxVolume()			# nm3
		else:
			self.ui.volLineEdit.setText(str(0.0))
			self._vol			=	0.0			# nm3
		self.on_densitySpinBox_valueChanged()
	
	def updateAmmount(self):
		if self._history.currentState().hasBox():
			self.computeMolecules()
		else:
			self._amount = 0
		self.ui.molBox.setValue(self._amount)

	def computeMolecules(self):
		#import numpy
		global _AVOGRADRO_CONSTANT_
		D = self._density
		MM = self.DENSITY[self._solvent][self.MI]
		V = self._vol / 1E24
		if V == 0: return 0
		
		#print "computeMolecules ", D,V,MM,D * V / MM * _AVOGRADRO_CONSTANT_
		n = int(D * V / MM * _AVOGRADRO_CONSTANT_)

		return n
		
	def computeDensity(self):
		"""
		Computes pressure from volume (V), temperature (T) and ammount of molecules (N).
		"""
		global _AVOGRADRO_CONSTANT_
		V = self._vol / 1E24
		MM = self.DENSITY[self._solvent][self.MI]
		#print "computeDensity ", self._amount, V,MM, self._amount / V * MM * _AVOGRADRO_CONSTANT_
		return self._amount  * MM/ V / _AVOGRADRO_CONSTANT_
	


	def on_densitySpinBox_valueChanged(self):
		self._density = self.ui.densitySpinBox.value()
		self._amount = self.computeMolecules()
		self.ui.molBox.blockSignals(True)
		self.ui.molBox.setValue(self._amount)
		self.ui.molBox.blockSignals(False)
		#self.updateFields()

	def on_molBox_valueChanged(self):
		self._amount = self.ui.molBox.value()
		self._density = self.computeDensity()
		self.ui.densitySpinBox.blockSignals(True)
		self.ui.densitySpinBox.setValue(self._density)
		self.ui.densitySpinBox.blockSignals(False)
		#self.updateFields()


	#----------------------------------------------------------------
	def on_solventComboBox_currentIndexChanged(self, solvent):
		#print "on_solventComboBox_currentIndexChanged ", str(self.ui.solventComboBox.currentText()),str(self.ui.solventComboBox.currentText()) == "Selected Molecule"
		if str(self.ui.solventComboBox.currentText()) == "Selected Molecule" and len(self.wolffia.buildTab.editor.selectedMolecules()) != 1:
			Error = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Error!", "Please select ONE molecule")
			Error.exec_()
			for i in range(self.ui.solventComboBox.count()):
				if self.ui.solventComboBox.itemText(i) == self._solvent:
					self.ui.solventComboBox.setCurrentIndex(i)
			return
		
		self._solvent =	str(self.ui.solventComboBox.currentText())
		self.ui.densitySpinBox.setDisabled(self._solvent == "Selected Molecule")
		self._density = self.DENSITY[self._solvent][self.DI]
		if self._solvent == "Selected Molecule":
			import math
			boxVol = self._history.currentState().getDrawer().volume()
			molVol = math.pow(self.wolffia.buildTab.editor.selectedMolecules()[0].diameter(),3) * 4.19
			self.ui.molBox.setValue(int(boxVol/molVol))  # division by 2 is completely arbitrary
		else:
			self.ui.densitySpinBox.setValue(self._density)
			self.updateAmmount()
	#---------------------------------------------------------------------
	def on_noneRButton_toggled(self, checked):
		if checked:
			#self.clear()		
			#self.ui.addButton.setEnabled(False)
			self.ui.boundStackedWidget.setEnabled(False)
			self._history.currentState().setDrawer(Drawer())
			self.ui.noneRButton.setChecked(True)
			
		self.ui.boxBoundButton.blockSignals(True)
		self.ui.boxBoundButton.setChecked(not checked)
		self.ui.boxBoundButton.blockSignals(False)
		
		self.update()

	#---------------------------------------------------------------------
	def on_boxBoundButton_toggled(self, checked):
		#create box boundary
		#self.clear()
		#self.setBoxBoundary()
		
		if checked:
			#update widgets status
			self.ui.boundStackedWidget.setEnabled(True)
			self.ui.boundStackedWidget.setCurrentIndex(0)
			#self.ui.solvateButton.setEnabled(True)
			drawer = self._history.currentState().getDrawer()
			if not drawer.hasCell():
				self.setBoxBoundary()
		else:
			self.ui.noneRButton.setChecked(True)
			
		self.ui.noneRButton.blockSignals(True)
		self.ui.noneRButton.setChecked(not checked)
		self.ui.noneRButton.blockSignals(False)

		self.update()

	def on_removeButton_pressed(self):
		self._history.push()
		mixture = self._history.currentState().getMixture()
		mixtureNames = mixture.molecules()
		
		progress	  = QtGui.QProgressDialog("Removing...", QtCore.QString(), 0, len(mixtureNames), self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
		progress.setWindowModality(QtCore.Qt.WindowModal)
				
		prefix = "SOLVENT(" + self.SOLVENT_TO_CLASS[self._solvent]
		print("on_removeButton_pressed ",prefix)
		pos = len(prefix)
		i = 1
		toRemove = list()
		for mol in mixtureNames:
			if mol[:pos] == prefix:
				#self._history.currentState().removeMolecule(mol)
				toRemove.append(mol)
			i += 1
			progress.setValue(i)
		self._history.currentState().removeMoleculesFrom(toRemove)

		progress.hide()
		self.preview.update()

	#---------------------------------------------------------------------
	def on_lengthDSpinner_editingFinished(self):
		drawer = self._history.currentState().getDrawer()
		if drawer.hasCell():
			self.ui.lengthSlider.setValue(self.ui.lengthDSpinner.value())
			
			basis   = drawer.getCellBasisVectors()
			oldCter = drawer.getCellOrigin()
			oldO    = drawer.getCenter()
				
			if self.ui.ratioPCheckBox.isChecked() or self.ui.equalCheckBox.isChecked():	
				ratio = float(self.ui.lengthDSpinner.value()) - basis[0][0]			
				newBasis =[[basis[0][0]+ratio, 0, 0], [0, basis[1][1]+ratio, 0], [0, 0, basis[2][2]+ratio]]
				drawer.setCellBasisVectors(newBasis)
				newCter = drawer.getCenter()
				drawer.setCellOrigin([oldO[0]-newCter[0]+oldCter[0], oldO[1]-newCter[1]+oldCter[1], oldO[2]-newCter[2]+oldCter[2] ])
				#self.setCellOriginSpinners()
			else:
				self.setCustomBox()

		self.update()

	#---------------------------------------------------------------------
	def on_widthDSpinner_editingFinished(self):
		self.ui.widthSlider.setValue(self.ui.widthDSpinner.value())
		if self._history.currentState().getDrawer().hasCell():
			self.setCustomBox()	

	#---------------------------------------------------------------------				
	def on_heightDSpinner_editingFinished(self):
		self.ui.heightSlider.setValue(self.ui.heightDSpinner.value())
		if self._history.currentState().getDrawer().hasCell():
			self.setCustomBox()

	#---------------------------------------------------------------------				
	def on_lengthSlider_sliderMoved(self,value):
		self.ui.lengthDSpinner.setValue(value)
		self.on_lengthDSpinner_editingFinished()

	#---------------------------------------------------------------------				
	def on_widthSlider_sliderMoved(self,value):
		self.ui.widthDSpinner.setValue(value)
		self.on_widthDSpinner_editingFinished()

	#---------------------------------------------------------------------				
	def on_heightSlider_sliderMoved(self,value):
		#print "on_heightSlider_sliderMoved value",type(value), value
		self.ui.heightDSpinner.setValue(value)
		self.on_heightDSpinner_editingFinished()

	#---------------------------------------------------------------------
	def setCustomBox(self):
		drawer = self._history.currentState().getDrawer()
		oldCter = drawer.getCellOrigin()
		oldO    = drawer.getCenter()
			
		newBasis =[[float(self.ui.lengthDSpinner.value()), 0, 0], [0, float(self.ui.widthDSpinner.value()), 0], [0, 0, float(self.ui.heightDSpinner.value())]]
		drawer.setCellBasisVectors(newBasis)
		newCter = drawer.getCenter()
		drawer.setCellOrigin([oldO[0]-newCter[0]+oldCter[0], oldO[1]-newCter[1]+oldCter[1], oldO[2]-newCter[2]+oldCter[2] ])

		self.update()

	#---------------------------------------------------------------------
	def on_perXSpinner_valueChanged(self):
		if self._history.currentState().getDrawer().hasCell():
			b = self._history.currentState().getDrawer().getCellOrigin()
			b[0] =  self.ui.perXSpinner.value()
			self._history.currentState().getDrawer().setCellOrigin(b)
		self.update()

	#---------------------------------------------------------------------
	def on_perYSpinner_valueChanged(self):
		if self._history.currentState().getDrawer().hasCell():
			b = self._history.currentState().getDrawer().getCellOrigin()
			b[1] =  self.ui.perYSpinner.value()
			self._history.currentState().getDrawer().setCellOrigin(b)
		self.update()

	#---------------------------------------------------------------------
	def on_perZSpinner_valueChanged(self):
		if self._history.currentState().getDrawer().hasCell():
			b = self._history.currentState().getDrawer().getCellOrigin()
			b[2] =  self.ui.perZSpinner.value()
			self._history.currentState().getDrawer().setCellOrigin(b)
		self.update()

	#---------------------------------------------------------------------		
	def on_solvateButton_pressed(self):
		#drawer = self._history.currentState().getDrawer()
		vol = self.getBoxVolume()
		#print "vol",vol

		from .SolventDialog import SolventDialog
		dialog = SolventDialog(self._history.currentState(), vol)
		dialog.show()
		dialog.exec_()
		
		if self.ui.boxBoundButton.isChecked and dialog.getAmount() != 0:
			self.fillBox(dialog.getSolvent(), dialog.getAmount())
			#self.preview.update()
				
	def on_addButton_pressed(self):
		print("on_addButton_pressed init ", len(self._history.currentState().getMixture()))
		originalMolecules = set(self._history.currentState().getMixture().molecules())
		self.fillBox(self._solvent, self._amount)
		#originalMolecules = originalMolecules.intersection(set(self._history.currentState().getMixture().molecules()))
		'''
		while True:
			remaining = self.removeCollisions(self._history.currentState().getMixture(), originalMolecules, self._history.currentState().getDrawer())
			if not self.ui.collisionsBox.isChecked() or remaining <= 0: break
			originalMolecules = set(self._history.currentState().getMixture().molecules())
			self.fillBox(self._solvent, remaining)
		'''
		if str(self._solvent) == "Selected Molecule":
			self.wolffia.buildTab.remove()  #remueve la molecula selleccionada que se va a usar de solvente mas abajo
		print("on_addButton_pressed end ", len(self._history.currentState().getMixture()))

		'''
		#self.preview.update()
		molNum        = len(mix) - len(originalMolecules)
		progressMax   = molNum
		progress      = QtGui.QProgressDialog("Removing collisions...", QtCore.QString(), 0, progressMax, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
		progress.setWindowModality(QtCore.Qt.WindowModal)

		remaining = 1
		while remaining > 0:
			collisions = mix.overlapingMolecules(originalMolecules, pbc=pbc)
			#print "colisiones... ", len(collisions)
			toRemove  = set(collisions).difference(set(originalMolecules))
			remaining = molNum - len(toRemove)
			print "removiendo... ", len(toRemove)
			self._history.currentState().removeMoleculesFrom(toRemove)
			progress.setValue(molNum-remaining)

		progress.hide()
		'''


	#---------------------------------------------------------------------		
	def on_waterWrap_stateChanged(self, state):
		self._history.currentState().getDrawer().setWrapWater(state == QtCore.Qt.Checked)

	#---------------------------------------------------------------------				
	def on_wrapAllMolecules_stateChanged(self, state):
		self._history.currentState().getDrawer().setWrapAllMolecules(state == QtCore.Qt.Checked)
	#---------------------------------------------------------------------
    #def on_hydrogenBonding_stateChanged(self,state)
    
    #mixture = self.getMixture
    
    
    
    #--------------------------------------------------------------------- 
        
        
        
        
        
        
	#---------------------------------------------------------------------		
	def on_ratioPCheckBox_toggled(self, checked):
		if checked:
			#update related widgets
			self.ui.equalCheckBox.setChecked(False)
			self.ui.widthSlider.setEnabled(False)
			self.ui.widthDSpinner.setEnabled(False)
			self.ui.heightDSpinner.setEnabled(False)
			self.ui.heightSlider.setEnabled(False)
			
			#regenerate box boundary
			self.setBoxBoundary()
		else:
			self.ui.widthSlider.setEnabled(True)
			self.ui.widthDSpinner.setEnabled(True)
			self.ui.heightDSpinner.setEnabled(True)
			self.ui.heightSlider.setEnabled(True)

	#---------------------------------------------------------------------
	def on_setMinBoxButton_pressed(self):
		#print "on_minBoxButton_pressed"
		self.setBoxBoundary()
		#self.ui.ratioPCheckBox.setChecked(True)
		
	#---------------------------------------------------------------------
	def on_equalCheckBox_toggled(self, checked):
		drawer = self._history.currentState().getDrawer()

		if checked:
			#disabled related widgets
			self.ui.ratioPCheckBox.setChecked(False)
			self.ui.widthSlider.setEnabled(False)
			self.ui.widthDSpinner.setEnabled(False)
			self.ui.heightDSpinner.setEnabled(False)
			self.ui.heightSlider.setEnabled(False)
			
			#find biggest dimension
			basis   = drawer.getCellBasisVectors()
			dim = [float(basis[0][0]), float(basis[1][1]), float(basis[2][2])]
			val = max(dim)
				
			oldCter = drawer.getCellOrigin()
			oldO    = drawer.getCenter()	
					
			newBasis =[[val, 0, 0], [0, val, 0], [0, 0, val]]
			drawer.setCellBasisVectors(newBasis)
			newCter = drawer.getCenter()
			drawer.setCellOrigin([oldO[0]-newCter[0]+oldCter[0], oldO[1]-newCter[1]+oldCter[1], oldO[2]-newCter[2]+oldCter[2] ])
			
			#disable user for creating smaller cube 
			box = drawer.getCellBasisVectors()
			self.ui.lengthDSpinner.setValue(box[0][0])
			self.ui.widthDSpinner.setValue(box[1][1])
			self.ui.heightDSpinner.setValue(box[2][2])
			self.update()
		else:
			self.ui.widthSlider.setEnabled(True)
			self.ui.widthDSpinner.setEnabled(True)
			self.ui.heightDSpinner.setEnabled(True)
			self.ui.heightSlider.setEnabled(True)
			
	#---------------------------------------------------------------------		
	def setBoxBoundary(self):
		#defines periodic boundary box
		drawer = self._history.currentState().getDrawer()
		box = self._history.currentState().getMixture().enclosingBox()
		#print "setBoxBoundary", box
		
		dim = [box[1][0]-box[0][0], box[1][1]-box[0][1], box[1][2]-box[0][2]] 
		drawer.setCellBasisVectors(  [  [dim[0], 0, 0],[0, dim[1], 0],[0, 0, dim[2]]  ]  )
		drawer.setCellOrigin([box[0][0], box[0][1], box[0][2]])
		
		#disable user for creating smaller box 
		box = drawer.getCellBasisVectors()
		#self.ui.lengthDSpinner.setMinimum(box[0][0])
		#self.ui.widthDSpinner.setMinimum(box[1][1])
		#self.ui.heightDSpinner.setMinimum(box[2][2])
		self.ui.perXSpinner.setValue(drawer.getCellOrigin()[0])
		self.ui.perYSpinner.setValue(drawer.getCellOrigin()[1])
		self.ui.perZSpinner.setValue(drawer.getCellOrigin()[2])
		
		self.update()

	#---------------------------------------------------------------------
	def setCustomBox2(self):
		drawer = self._history.currentState().getDrawer()
		oldCter = drawer.getCellOrigin()
		oldO    = drawer.getCenter()
			
		newBasis =[[float(self.ui.lengthDSpinner.value()), 0, 0], [0, float(self.ui.widthDSpinner.value()), 0], [0, 0, float(self.ui.heightDSpinner.value())]]
		drawer.setCellBasisVectors(newBasis)
		newCter = drawer.getCenter()
		drawer.setCellOrigin([oldO[0]-newCter[0]+oldCter[0], oldO[1]-newCter[1]+oldCter[1], oldO[2]-newCter[2]+oldCter[2] ])

		self.update()

	#---------------------------------------------------------------------			
	def setSphereBoundary(self):
		#defines sphere boundary box
		sphere = self._history.currentState().getMixture().boundingSphere()
		#print "setSphereBoundary", sphere
		self._drawer.setSphericalBC(sphere)
		self.update()	

	#---------------------------------------------------------------------				
	def setCellOriginSpinners(self):
		draw = self._history.currentState().getDrawer()
		if draw != None and draw.hasCell():
			self.ui.perXSpinner.setEnabled (True)
			self.ui.perYSpinner.setEnabled (True)
			self.ui.perZSpinner.setEnabled (True)
			b = draw.getCellOrigin()
			#print "setCellOriginSpinners ", b
			self.ui.perXSpinner.setValue   (b[0])
			self.ui.perYSpinner.setValue   (b[1])
			self.ui.perZSpinner.setValue   (b[2])
		else:
			self.ui.perXSpinner.setEnabled (False)
			self.ui.perYSpinner.setEnabled (False)
			self.ui.perZSpinner.setEnabled (False)
			self.ui.perXSpinner.setValue   (0.)
			self.ui.perYSpinner.setValue   (0.)
			self.ui.perZSpinner.setValue   (0.)

	#---------------------------------------------------------------------					
	def setCellBasisVectorsSpinners(self):
		draw = self._history.currentState().getDrawer()
		if draw != None and draw.hasCell():
			#print "setCellBasisVectorsSpinners hasCell"
			dimension = draw.getCellBasisVectors()
			self.ui.lengthDSpinner.setEnabled (True)
			if not (self.ui.ratioPCheckBox.isChecked() or self.ui.equalCheckBox.isChecked()):
				self.ui.widthDSpinner.setEnabled  (True)
				self.ui.heightDSpinner.setEnabled (True)
			self.ui.lengthDSpinner.setValue   (dimension[0][0])
			self.ui.widthDSpinner.setValue    (dimension[1][1])
			self.ui.heightDSpinner.setValue   (dimension[2][2])
		else:
			#print "setCellBasisVectorsSpinners no Cell"
			self.ui.lengthDSpinner.setValue   (0.)
			self.ui.widthDSpinner.setValue    (0.)
			self.ui.heightDSpinner.setValue   (0.)
			self.ui.lengthDSpinner.setEnabled (False)
			self.ui.widthDSpinner.setEnabled  (False)
			self.ui.heightDSpinner.setEnabled (False)

	#---------------------------------------------------------------------
	def setAllSpinners(self):
		self.setCellBasisVectorsSpinners()
		self.setCellOriginSpinners()
		
	#---------------------------------------------------------------------
	def setAllSliders(self):
		draw = self._history.currentState().getDrawer()
		if draw != None and draw.hasCell():
			#print "setAllSliders hasCell"
			dimension = draw.getCellBasisVectors()
			self.ui.lengthSlider.setEnabled (True)
			if not (self.ui.ratioPCheckBox.isChecked() or self.ui.equalCheckBox.isChecked()):
				self.ui.widthSlider.setEnabled  (True)
				self.ui.heightSlider.setEnabled (True)
			try:
				self.ui.lengthSlider.setValue   (dimension[0][0])
				self.ui.widthSlider.setValue    (dimension[1][1])
				self.ui.heightSlider.setValue   (dimension[2][2])
			except TypeError as e: # recovers from NaNs
				print("SetupTab.setAllSliders() recovering from: ", e)
				self._history.currentState().getDrawer().clear()
		else:
			#print "setAllSliders no Cell"
			self.ui.lengthSlider.setValue   (0.)
			self.ui.widthSlider.setValue    (0.)
			self.ui.heightSlider.setValue   (0.)
			self.ui.lengthSlider.setEnabled (False)
			self.ui.widthSlider.setEnabled  (False)
			self.ui.heightSlider.setEnabled (False)
		
	#---------------------------------------------------------------------
	def clear(self):
		self._history.currentState().getDrawer().clear()
		self.ui.lengthDSpinner.setMinimum(0.)
		self.ui.widthDSpinner.setMinimum(0.)
		self.ui.heightDSpinner.setMinimum(0.)

		#self.update()

	#---------------------------------------------------------------------
	def fillBox_bak(self, solvent, molNum):
		self._solvent = solvent
		self._history.push()
		originalMolecules = self._history.currentState().getMixture().molecules()
		
		totalDim = self.getBoxDimension()
		boxmin = self._history.currentState().getDrawer().getCellOrigin()
		boxmax =[ boxmin[0]+totalDim[0], boxmin[1]+totalDim[1], boxmin[2]+totalDim[2] ]
		
		exec("from lib.chemicalGraph.molecule.solvent." + self.SOLVENT_TO_CLASS[str(self._solvent)] + " import *")
		solv = eval(self.SOLVENT_TO_CLASS[str(self._solvent)] + "()")
		
		#calculate the volume for a single solvent molecule
		center = [0., 0., 0.]
		pos = solv.massCenter()
		solv.moveBy([center[0]-pos[0], center[1]-pos[1], center[2]-pos[2]])
		#solvDiameter = solv.diameter()+ _SEPARATION_BETWEEN_SOLVENTS_
		solvDiameter = math.pow(self.getBoxVolume() / molNum, 1./3.)
		
		row = math.floor(totalDim[1]/solvDiameter)
		col = math.floor(totalDim[0]/solvDiameter)
		dep = math.floor(totalDim[2]/solvDiameter)
		progressMax   = 2 * row * col
		progressCount = 0
		progress      = QtGui.QProgressDialog("Solvating...", "Abort", 0, progressMax, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
		progress.setWindowModality(QtCore.Qt.WindowModal)
		
		#move molecule to one corner to start ordering 
		#
		#             reference point    ___\  ________
		#                           / /     /|
		#                        /_______/ |
		#                        |  |____|_|
		#                        | /    | /
		#                        |/______|/
		#
		#set new position for next solvent molecule
		solvRadius = solvDiameter / 2
		newPos = solv.massCenter()
		#refCoor = [boxmin[0]-newPos[0] + solvRadius, boxmax[1]-newPos[1] + solvRadius, boxmin[2]-newPos[2] + solvRadius]
		refCoor = boxmin
		
		boxmax[0] -= solvDiameter/2
		boxmax[1] -= solvDiameter/2
		boxmax[2] -= solvDiameter/2
		for disp in [0,-solvDiameter/2]:
		    dx = refCoor[0] + solvDiameter + disp
		    while dx < boxmax[0]:
		        dy = refCoor[1] + solvDiameter + disp
		        while dy < boxmax[1]:
		            if progress.wasCanceled():
		                #print "fillBox cancelado"
		                progress.hide()
		                self._history.back()
		                self.update()
		                return
		            dz = refCoor[2] + solvDiameter + disp
		            while dz < boxmax[2]:
		                #random rotation for solvent atoms
		                rx = random.uniform(-360, 360)
		                ry = random.uniform(-360, 360)
		                rz = random.uniform(-360, 360)
		                
		                #random displacement for solvent atoms
		                rdx = random.uniform(-solvRadius, solvRadius)
		                rdy = random.uniform(-solvRadius, solvRadius)
		                rdz = random.uniform(-solvRadius, solvRadius)
		
		                #generate new molecule and assign next position
		                mol = solv.copy()
		                mol.rotateDeg(rx, ry, rz)
		                lastPos = mol.massCenter()
		                newPos = [dx-lastPos[0]+rdx, dy-lastPos[1]+rdy, dz-lastPos[2]+rdz]
		                mol.moveBy(newPos)
		                mol.rename("SOLVENT("+mol.molname()+")")
		                nodeName = self._history.currentState().addMolecule(mol)
		                self._history.currentState().shownMolecules.show(nodeName)
		                #print "fillBox", nodeName
		                dz += solvDiameter
		            progressCount += 1
		            progress.setValue(progressCount)
		            dy += solvDiameter
		        #self.preview.setMixture(self._history.currentState().getMixture()) # gives feedback to the user
		        dx += solvDiameter
		
		mix = self._history.currentState().getMixture()
		#print "removing solvent ", solv
		#print "Molecules before cleaning: ",mix.order()
		for solvate in originalMolecules:
		    collisions = mix.overlapingMolecules(solvate)
		    #print "To be removed:", collisions
		    for m in collisions:
		        #print "comparing ", mix.getMolecule(m), " and ", solv
		        if mix.getMolecule(m) == solv:
		            self._history.currentState().shownMolecules.hide(str(m))
		            mix.remove_node(m)
		#print "Molecules after cleaning: ",self._history.currentState().getMixture()    
		#self.parent.update()
		self.preview.update()
		progress.hide()
        
	#def hideEvent(self,e):		 
	#	self.wolffia.update()



	def showEvent(self, e):
		#print "SetupTab showEvent"
		self.allowUpdate = True
		#self.on_boxBoundButton_toggled(None)
		#if self.firstUpdate:
		#	self.preview.update()
		#	self.update()
		#	self.firstUpdate = False
		#else:
		#	self.preview.paintGL()
			
			
		self.update()
		#self.preview.update()
		super(SetupTab, self).showEvent(e)
		#print "SetupTab showEvent out"

	def fillBox(self, solvent, molNum):
		self._solvent = solvent
		self._history.push()
		
		if str(self._solvent) == "Selected Molecule":
			solv = self.wolffia.buildTab.editor.selectedMolecules()[0]
			#self.wolffia.buildTab.remove()  #remueve la molecula selleccionada que se va a usar de solvente mas abajo
		else:
			if str(self._solvent) == "Argon":
				exec("from lib.chemicalGraph.molecule.gas." + self.SOLVENT_TO_CLASS[str(self._solvent)] + " import *")
			else:
				exec("from lib.chemicalGraph.molecule.solvent." + self.SOLVENT_TO_CLASS[str(self._solvent)] + " import *")
				
			solv = eval(self.SOLVENT_TO_CLASS[str(self._solvent)] + "()")

		solv = solv.copy()
		solv.rename("SOLVENT("+solv.molname()+")")
		solv.setAsSolvent()
		
		progress      = QtGui.QProgressDialog("Solvating...", "Abort", 0, 10, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
		progress.setWindowModality(QtCore.Qt.WindowModal)
		progress.setAutoClose(False)
		self._history.currentState().fillBox(solv, molNum, self.ui.collisionsBox.isChecked(), True, self.ui.pcbBox.isChecked(), progress)
		self.preview.setMixture(self._history.currentState().getMixture(),True)
		progress.hide()
		self.preview.update()






	#---------------------------------------------------------------------
	def update(self):
		start = time.clock()

		#import inspect
		#print "updating setupTab, caller=",inspect.stack()[1][3]

		self.setAllSpinners()
		self.setAllSliders()
		self.setBoundBox()
		self.preview.setBox(self._history.currentState().getDrawer())
		self.updateVolume()
			
		# unset PME in simTab if there is no box
		try:
			if self.wolffia.simTab.pme.isChecked() and not self._history.currentState().getDrawer().hasCell() and self._history.currentState().simTabValues != None:
				QtGui.QMessageBox(1, "Notification", "Particle Mesh Ewald in the Simulation tab has been set off because boundary conditions are not set.").exec_()
				self._history.currentState().simTabValues["pme"] = False
				self.wolffia.simTab.pme.nextCheckState()
		except AttributeError:
			pass # probably Sim tab has not been created yet

		self.allowUpdate = True

		#print "setupTab update time",time.clock()-start

	def reset(self):
		self.clear()
		self.ui.noneRButton.setChecked(True)
		self.ui.boxBoundButton.setChecked(False)
		self.preview.reset()
		
	#---------------------------------------------------------------------
	#def paintEvent(self, e):
	#	print "SetupTab paintEvent"
	#	super(SetupTab, self).paintEvent(e)
	#	self.preview.paintEvent(e)
	#	QtGui.QWidget.update(self)

		
	#=========================================================================
	#  Funciones movidas a otras clases
	# ========================================================================
	def getBoxVolume(self):
		return self._history.currentState().getDrawer().getBoxVolume()



