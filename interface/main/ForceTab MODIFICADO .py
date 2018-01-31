# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  ForceTab.py
#  Version 0.1, December, 2011
#
#  Wolffia: tab for setting force field parameter values.
#
#  Authors:
#  Mirgery Medina Cuadrado
#  José O. Sotero Esteva  (jse@mate.uprh.edu)
#  Melissa López Serrano
#
#  Department of Mathematics
#  University of Puerto Rico at Humacao
#
#  Acknowledgements: The main funding source for this project has been provided
#  by the UPR-Penn Partnership for Research and Education in Materials program, 
#  USA National Science Foundation grant number DMR-0934195. 
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui, QtHelp, QtOpenGL
from ui_ForceTab import Ui_forceTab
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys,os, time
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from Wolffia_conf import *

from interface.main.MixtureViewer import MixtureViewer


class ForceTab(QtGui.QFrame):   
	def __init__(self, hist, parent, previewer):
		super(ForceTab, self).__init__(parent)


		self.history                            =	hist
		self.allForceField                      = 	{}
		self.generated 				=	time.clock()
		self.allowUpdate = True
		self.selectedMolecule = None
		self.forcePreview = previewer
		#print "ForceTab, self.forcePreview ", self.forcePreview
		#widgets import 
		self.ui = Ui_forceTab()
		self.ui.setupUi(self)

		#activates the previewer
		#self.forcePreview = MixtureViewer(hist, parent=self)
		#self.ui.forcePreviewLayout.addWidget(self.forcePreview)

		#Buttons
		self.ui.saveButton.setIcon(QtGui.QIcon().fromTheme("media-floppy", QtGui.QIcon(str(NANOCAD_BASE+"\\interface\\graphics\\") +"media-floppy.png")))
		self.ui.loadButton.setIcon(QtGui.QIcon().fromTheme("document-open", QtGui.QIcon(str(NANOCAD_BASE+"\\interface\\graphics\\") +"document-open.png")))

		#self.update()

	#def paintEvent (self,  event):
	#	QtGui.QFrame.paintEvent(self, event)
	#	self.updateTAB()

	def showEvent(self, e):
		#print "ForceTab.showEvent " 
		self.update()
		super(ForceTab, self).showEvent(e)
		#self.update()

	#def hideEvent(self,e):		 
	#	self.wolffia.update()
	
	def reset(self):
		self.forcePreview.reset()

	def update(self):
		#print "ForceTab.update " 
		self.insertAllToNonBondTable()
		self.insertAllBondTable()
		self.insertAllAngleTable()
		self.insertAllDihedralTable()
		self.generated = time.clock()
		#self.history.currentState().storeForceField()
		#self.forcePreview.update()


	def updateTAB(self):
		self.forcePreview.setMixture(self.history.currentState().getMixture())

	#------------------------------------------------------------------------------------
	#list all molecules in the Structure Manager
	def insertAllToNonBondTable(self):
		# count nonb in all molecules
		row = 0
		rows = 0
		nombVals = dict()
		self.ui.nonBondTable.setRowCount(0)
		displayedMols=list()
	
		for molName in self.history.currentState().mixture:
		    molecule = self.history.currentState().mixture.getMolecule(molName)
		    if not molecule.molname() in displayedMols:
				#print "insertAllToNonBondTable ", molecule.molname()
				self.allForceField[molName] = {"nonBonded" : [], "Bonds" : [] , "Angles": [], "Dihedrals": []}
				displayedMols.append(molecule.molname() )
				
				ff = molecule.getForceField()
				types = molecule.atomTypes()
				rows += len(types)+1
				self.ui.nonBondTable.setRowCount(rows)
				  
				# display molecule name
				nameW = QtGui.QTableWidgetItem(molecule.molname())
				nameW.setBackgroundColor(QtCore.Qt.gray)
				self.ui.nonBondTable.setItem(row, 0, nameW)
				row += 1
				
				for aType in types:
					atomType = QtGui.QTableWidgetItem(aType)
					atomType.setFlags(QtCore.Qt.ItemIsEnabled)
					self.ui.nonBondTable.setItem(row, 0, atomType)
					
					epsilon = ForceSpinBox([-5, 0], 6, parent=self, fl=ff, \
					method= "setNonBond(\"" + aType + "\", self.value(), 0)")
					self.ui.nonBondTable.setCellWidget(row, 1, epsilon)
					epsilon.setValue(ff.nonBond(aType)[0])
					
					rmin = ForceSpinBox([0.000000, 20], 6, parent=self, fl=ff, \
					method= "setNonBond(\"" + aType + "\", self.value(), 1)")
					self.ui.nonBondTable.setCellWidget(row, 2, rmin)
					rmin.setValue(ff.nonBond(aType)[1])
					
					nombVals[aType] = [epsilon, rmin] 
					
					row += 1
				self.allForceField[molName]["nonBonded"]=nombVals
	#---------------------------------------------------------------
	#list all molecules in the Structure Manager
	def insertAllBondTable(self):
	
		row = 0
		rows = 0
		bonds = dict()
		self.ui.bondsTable.setRowCount(0)
		displayedMols=list()
		for molName in self.history.currentState().mixture:
		    molecule = self.history.currentState().mixture.getMolecule(molName)
		    if not molecule.molname() in displayedMols:
			    displayedMols.append(molecule.molname())
			    
			    ff = molecule.getForceField()
			    bondTypes = molecule.bondTypes()
			    rows += len(bondTypes)+1
			    self.ui.bondsTable.setRowCount(rows)
			    
			    # display molecule name
			    nameW = QtGui.QTableWidgetItem(molecule.molname())
			    nameW.setBackgroundColor(QtCore.Qt.gray)
			    self.ui.bondsTable.setItem(row, 0, nameW)
			    row += 1
			   
			    for [t1,t2] in bondTypes:
				atomType = QtGui.QTableWidgetItem(t1+"-"+t2)
				atomType.setFlags(QtCore.Qt.ItemIsEnabled)
				self.ui.bondsTable.setItem(row, 0, atomType)
				
				Kb = ForceSpinBox([000.000, 999.999], 3, parent=self, fl=ff, \
					method= "setBond(\"" + t1 + "\", \"" + t2 + "\", self.value(), 0)")
				self.ui.bondsTable.setCellWidget(row, 1, Kb)
				Kb.setValue(ff.bond(t1,t2)[0])
				
				b0 = ForceSpinBox([0.0000, 5], 4, parent=self, fl=ff, \
				method= "setBond(\"" + t1 + "\", \"" + t2 + "\", self.value(), 1)")
				self.ui.bondsTable.setCellWidget(row, 2, b0)
				b0.setValue(ff.bond(t1,t2)[1])
				 
				bonds[t1,t2] = [Kb, b0] 
				
				row += 1
			    self.allForceField[molName]["Bonds"]=bonds
		#---------------------------------------------------------------
		#list all molecules in the Structure Manager
	def insertAllAngleTable(self):
	
		row = 0
		rows = 0
		angles = dict()
		self.ui.dihedralTable.setRowCount(0)
		displayedMols=list()
		for molName in self.history.currentState().mixture:
		    molecule = self.history.currentState().mixture.getMolecule(molName)
		    if not molecule.molname() in displayedMols:
			    displayedMols.append(molecule.molname())
			    
			    ff = molecule.getForceField()
			    angleTypes = molecule.angleTypes()
			    rows += len(angleTypes)+1
			    self.ui.anglesTable.setRowCount(rows)
			    
			    # display molecule name
			    nameW = QtGui.QTableWidgetItem(molecule.molname())
			    nameW.setBackgroundColor(QtCore.Qt.gray)
			    self.ui.anglesTable.setItem(row, 0, nameW)
			    row += 1
			   
			    for [t1,t2,t3] in angleTypes:
				atomType = QtGui.QTableWidgetItem(t1+"-"+t2+"-"+t3)
				atomType.setFlags(QtCore.Qt.ItemIsEnabled)
				self.ui.anglesTable.setItem(row, 0, atomType)
				
				Kth = ForceSpinBox([000.000, 999.999], 3,  parent=self, fl=ff, \
				method= "setAngle(\"" + t1 + "\", \"" + t2 +"\",\"" + t3 + "\", self.value(), 0)")
				self.ui.anglesTable.setCellWidget(row, 1, Kth)
				Kth.setValue(ff.angle(t1,t2,t3)[0])
				
				a0 = ForceSpinBox([0.0000, 180], 4,   parent=self, fl=ff, \
				method= "setAngle(\"" + t1 + "\", \"" + t2 +"\",\"" + t3 + "\", self.value(), 1)")
				self.ui.anglesTable.setCellWidget(row, 2, a0)
				a0.setValue(ff.angle(t1,t2,t3)[1])
		
				angles[t1,t2,t3] = [Kth, a0] 
		
				row += 1
		
			    self.allForceField[molName]["Angles"]=angles
	#---------------------------------------------------------------
	#list all molecules in the Structure Manager
	#faltan para cambiar su valor
	def insertAllDihedralTable(self):
	
		row = 0
		rows = 0
		dihedrals = dict()
		self.ui.dihedralTable.setRowCount(0)
		displayedMols=list()
		for molName in self.history.currentState().mixture:
		    molecule = self.history.currentState().mixture.getMolecule(molName)
		    if not molecule.molname() in displayedMols:
			    displayedMols.append(molecule.molname())

			    ff = molecule.getForceField()
			    dihedralTypes = molecule.dihedralTypes()
			    rows += len(dihedralTypes)+1
			    self.ui.dihedralTable.setRowCount(rows)
			    
			    # display molecule name
			    nameW = QtGui.QTableWidgetItem(molecule.molname())
			    nameW.setBackgroundColor(QtCore.Qt.gray)
			    self.ui.dihedralTable.setItem(row, 0, nameW)
			    row += 1
			   
			    for [t1,t2,t3,t4] in dihedralTypes:
				atomType = QtGui.QTableWidgetItem(t1+"-"+t2+"-"+t3+"-"+t4)
				atomType.setFlags(QtCore.Qt.ItemIsEnabled)
				self.ui.dihedralTable.setItem(row, 0, atomType)
				
				Kchi = ForceSpinBox([0.0000, 99.9999], 4, parent=self, fl=ff, \
					method = "setDihedral(\"" + t1 + "\", \"" + t2 + "\", \"" + t3 + "\", \"" + t4 + "\", self.value(), 0)")
				self.ui.dihedralTable.setCellWidget(row, 1, Kchi)
				Kchi.setValue(ff.dihedral(t1,t2,t3,t4)[0])
				
				n = ForceSpinBox([0, 9], 0, parent=self, fl=ff, \
				    method = "setDihedral(\"" + t1 + "\", \"" + t2 + "\", \"" + t3 + "\", \"" + t4 + "\", self.value(), 1)")
				self.ui.dihedralTable.setCellWidget(row, 2, n)
				n.setValue(ff.dihedral(t1,t2,t3,t4)[1])
				
				Delta = ForceSpinBox([000.00, 999.99], 2, parent=self, fl=ff, \
					method = "setDihedral(\"" + t1 + "\", \"" + t2 + "\", \"" + t3 + "\", \"" + t4 + "\", self.value(), 2)")
				self.ui.dihedralTable.setCellWidget(row, 3, Delta)
				Delta.setValue(ff.dihedral(t1,t2,t3,t4)[2])
		
				dihedrals[t1,t2,t3,t4] = [Kchi,Delta] 
		
				row += 1
			    self.allForceField[molName]["Dihedrals"]=dihedrals
	#------------------------------------------------------------------------
	#messageAboutTab(): All about the Tab  

	def messageAboutTab(self):
		mAtab = QtGui.QMessageBox.information(self, 'About The Force Field Tab',
	'This step intends to help the user set up the force values of the molecular system. The table will contain the default force fields among molecular structures.')

	#------------------------------------------------------------------------
	@QtCore.pyqtSlot()
	def on_aboutTab_pressed(self):
		self.messageAboutTab()

	#-----------------------------------------------------------------------
	def on_nonBondTable_itemClicked(self, item):
		#print "on_nonBondTable_item ", item.text()
		self.selectedMolecule = item.text()

	def on_saveButton_pressed(self): 	
		self.storeForceField()
		mesg = 'Save ' + self.history.currentState().getMixtureName() + '.prm, '
		self.history.currentState().getMixture().writePRM(str(QtGui.QFileDialog.getSaveFileName(self, mesg,self.history.currentState().getBuildDirectory())) + ".prm")
	#----------------------------------------------------------------------
	def on_loadButton_pressed(self):
		if self.selectedMolecule == None:
		    errorgui = QtGui.QErrorMessage(self)
		    errorgui.setModal(True) # blocks Wolffia
		    errorgui.showMessage( "Please select a molecule by clicking on its name in the NONBONDED section.")
		    return
	
		mesg = "Load File.prm"
		file = QFileDialog.getOpenFileName(self, mesg)
		#print file +"***file***"
		if len(file) > 0:
		    self.history.push()
		    for molName in self.history.currentState().mixture:
			molecule = self.history.currentState().mixture.getMolecule(molName)
			#print "on_loadButton_pressed changing ff of " , self.selectedMolecule , " ... checking ", molecule.molname()
			if molecule.molname() == self.selectedMolecule:
			    #print "       on_loadButton_pressed YES, changing ff of " , self.selectedMolecule
			    molecule.getForceField().loadCHARMM(file)
			    #print "       on_loadButton_pressed ", molecule.getForceField(),molecule.getForceField()._NONBONDED
		    self.update()

	#----------------------------------------------------------------------
	# def ForceCount (self):


		         
	#----------------------------------------------------------------------
	def on_defaultForField_cellClicked(self, row, col):
	 count = 0
	 for mol in self.history.currentState().getMixture().molecules():
	  if count == row:
		self.editor.setMolecule(self.history.currentState())
		break
				
	  count += 1
	#--------------------------------------------------------------------
	def chosenForField(self):
		count = self.ui.defaultForField.topLevelItemCount()
		for i in range(count):
			item = self.ui.defaultForField.itemAt(i,1)
	#--------------------------------------------------------------------
	def change(self):
		self.history.push()

	def storeForceField(self):
		picklesan = {"nonBonded" : [], "Bonds" : [] , "Angles": [], "Dihedrals": []}
		print "AQUI ESTOY, WEPA"
		if self.allForceField != None:
			for molName in self.allForceField:
				print molName
				for bonds in self.allForceField[molName]:
					print bonds	
					if bonds == "Dihedrals":
						pass						
						#for types in self.allForceField[molName][bonds]:		
						#	print self.allForceField[molName][bonds][types][0].value()
						#	print self.allForceField[molName][bonds][types][1].value()
						#	print self.allForceField[molName][bonds][types][2].value()

					if bonds == "nonBonded":
						for types in self.allForceField[molName][bonds]:		
							print self.allForceField[molName][bonds][types][0].value()
							print self.allForceField[molName][bonds][types][1].value()


					elif bonds == "Angles":
						for types in self.allForceField[molName][bonds]:		
							print self.allForceField[molName][bonds][types][0].value()
							print self.allForceField[molName][bonds][types][1].value()
					else:
						for types in self.allForceField[molName][bonds]:
							print types
							print self.allForceField[molName][bonds][types][0].value()
							print self.allForceField[molName][bonds][types][1].value()			
		return picklesan
#--------------------------------------------------------------------
class ForceSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, spinRange=[0,1000], decimals=4, colorIfZero="Yellow", parent=None, fl=None, method=None):
        QtGui.QDoubleSpinBox.__init__(self,parent)
        QtCore.QObject.connect(self, QtCore.SIGNAL("editingFinished()"), self.change)
        if parent != None: QtCore.QObject.connect(self, QtCore.SIGNAL("editingFinished()"), parent.change)
        self.setDecimals(decimals)
        self.setRange(spinRange[0], spinRange[1])
        self.color = colorIfZero
        self.parent = parent
        self.ff = fl
	self.method = method
        #print "ForceSpinBox ", fl
        
    def setValue(self, x):
        QtGui.QDoubleSpinBox.setValue(self, x)
        if x == 0 :
            self.setStyleSheet('background: '+self.color)

    def change(self):
        #print "valueChanged  " , "self.ff." + self.method
        if self.ff != None:
            eval("self.ff." + self.method)     
