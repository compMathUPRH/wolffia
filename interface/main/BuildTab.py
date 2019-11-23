# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  BuildTab.py
#  Version 0.1, October, 2011
#
#  Wolffia tab for merging and managing molecules.
# 
"""
	Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
	Melissa  López Serrano, Frances J. Martínez Miranda 

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
from ui_BuildTab import Ui_buildTab

import sys,os, platform, time, random
import warnings
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import WOLFFIA_GRAPHICS, NANOCAD_BASE, C_MOLECULE_CATALOG, WOLFFIA_DIR

from lib.chemicalGraph.Mixture import Mixture
from lib.chemicalGraph.molecule.element.Element import *
import logging
from WFileDialogs import WFileDialog
from PropertyEditor import PropertyEditor
#from MixtureViewer import * 
from SettingsDialog import WDirectoryDialog
from WWidgets import PreviewButton,FixedButton

from WFileDialogs import WFileNameDialog

class BuildTab(QtGui.QFrame):   
	def __init__(self, hist, parent=None, previewer=None, settings=None):
		super(BuildTab, self).__init__(parent)

		#print "buildTab init in"
		self.history		 = hist
		self.mixModification = 0
		self.wolffia		 = parent
		self.allowUpdate	 = True
		self.buildPreview	= previewer
		self.settings		= settings
		self.clipboard	   = None
		self.prevSelection   = None
		self.prevShow		= None
		self.prevFixed	   = None

		#widgets import 
		self.ui = Ui_buildTab()
		self.ui.setupUi(self)
		self.ui.structManager.setSortingEnabled (False)

		px = QtGui.QPixmap()
		self._WOLFFIA_OS = platform.system()
		px.load(WOLFFIA_GRAPHICS+"hide.gif", format=None)
		ico = QtGui.QIcon()
		ico.addPixmap(px, state=QtGui.QIcon.On)
		self.ui.structManager.horizontalHeaderItem(0).setIcon(ico)

		px2 = QtGui.QPixmap()
		px2.load(WOLFFIA_GRAPHICS+"pin16.png", format=None)
		fixico = QtGui.QIcon()
		fixico.addPixmap(px2, state=QtGui.QIcon.On)
		self.ui.structManager.horizontalHeaderItem(1).setIcon(fixico)

		#initialize editor
		self.editor = PropertyEditor(self.buildPreview, self.history)
		self.ui.editorLayout.addWidget(self.editor)
		self.buildPreview.setBuildTab(self)

		#initialize tool buttons
		self.ui.removeButton.setIcon(QtGui.QIcon().fromTheme("edit-cut",	QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "edit-cut.png")	))
		self.ui.updateButton.setIcon(QtGui.QIcon().fromTheme("system-software-update",	QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "system-software-update.png")	))
		self.ui.removeButton.setFlat(True)
		self.ui.duplicateButton.setIcon(QtGui.QIcon().fromTheme("edit-paste",	QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "edit-paste.png")	))
		self.ui.copyButton.setIcon(QtGui.QIcon().fromTheme("edit-copy",	QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "edit-copy.png")	))
		self.ui.saveWFMbutton.setIcon(QtGui.QIcon().fromTheme("document-save",	QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "document-save.png")	))
		self.ui.addCustomButton.setIcon(QtGui.QIcon().fromTheme("document-open",	QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "document-open.png")	))

		self.showCheckboxes = dict()

		self.firstUpdate = True
		#print "buildTab init out", QtGui.QWidget.keyboardGrabber ()
		
		#self.setBuildTabEnabled()
		self.cMol = C_MOLECULE_CATALOG


	def _checkFixedShiftModifier_(self, basePin, selected):
		for i in range(self.ui.structManager.rowCount()):
			if self.ui.structManager.cellWidget(i,1) == basePin:
				row = i
				break

		modifiers = QtGui.QApplication.keyboardModifiers()
		if modifiers == QtCore.Qt.ShiftModifier and self.prevFixed != None:
			if self.prevFixed[1] == selected:
				if row < self.prevFixed[0]: ind = range(row+1,self.prevFixed[0]+1)
				else: ind = range(self.prevFixed[0],row)
				for i in ind:
					pin = self.ui.structManager.cellWidget(i, 1)
					#if selected: pin.setFixed(update=False)
					if self.prevFixed[1]: pin.setFixed(update=False)
					else: pin.setLoose(update=False)
		self.prevFixed = [row,selected]
		#self.buildPreview.update()
		
	def _checkShowShiftModifier_(self, baseEye, selected):
		#find row
		for i in range(self.ui.structManager.rowCount()):
			if self.ui.structManager.cellWidget(i,0) == baseEye:
				row = i
				break

		modifiers = QtGui.QApplication.keyboardModifiers()
		if modifiers == QtCore.Qt.ShiftModifier and self.prevShow != None:
			if self.prevShow[1] == selected:
				if row < self.prevShow[0]: ind = range(row,self.prevShow[0])
				else: ind = range(self.prevShow[0]+1,row)
				for i in ind:
					pin = self.ui.structManager.cellWidget(i, 0)
					#if selected: pin.setShown(update=False)
					if self.prevShow[1]: pin.setShown(update=False)
					else: pin.setHidden(update=False)
		self.prevShow = [row,selected]
		#self.buildPreview.update()
		
	#---------------------------------------------------------------
	def on_structManager_cellPressed(self, i,j):  
		#print "on_structManager_cellPressed ",  i,j
		mouse_state=QtGui.qApp.mouseButtons()
		if QtGui.qApp.mouseButtons()==QtCore.Qt.LeftButton:
			#print "on_structManager_cellPressed ", QtGui.qApp.mouseButtons()==QtCore.Qt.LeftButton, mouse_state==QtCore.Qt.NoButton 
			QtGui.qApp.sendEvent (self.ui.structManager, QtCore.QEvent(QtCore.QEvent.MouseButtonPress))
			#self.ui.structManager.cellPressed.emit(i,j)
	
	#activates the Structure Catalog
	def on_molCatalog_itemActivated(self, item):  
		#print "on_molCatalog_itemActivated in"
		self.key = str(item.text(0))
		self.parent = item.parent().text(0)
		
		def moleculeDialog(self, dialog):
			dialog.show()
			dialog.exec_()
			self.addMixture(dialog.getMixture())
			self.buildPreview.update()
		
		# Polymers 
		if self.key == "Polyaniline":
			from interface.PANI.paniEditor import PANIBuilder
			pani = PANIBuilder(self.history.currentState(), self, settings=self.settings)
			moleculeDialog(self, pani)
		elif self.key == "PEDOT":
			from interface.PEDOT.pedotEditor import PEDOTBuilder
			pedot = PEDOTBuilder(self.history.currentState(), self, settings=self.settings)
			moleculeDialog(self, pedot)
		elif self.key == "PSS":
			from interface.PSS.pssEditor import PSSBuilder
			pss = PSSBuilder(self.history.currentState(), self, settings=self.settings)
			moleculeDialog(self, pss)
		elif self.key == "Cellulose":
			from interface.celluloseEditor.CelluloseEditor import CelluloseEditor
			c = CelluloseEditor(self.history.currentState(), self, settings=self.settings)
			moleculeDialog(self, c)
		elif self.key == "ssDNA":
			print "ssDNA is not yet implemented!"
		elif self.parent == "Homopolymer":
			from interface.homopolyEditor.HomopolyEditor import HomopolyEditor
			homopol = HomopolyEditor(self.key, self.history.currentState(), settings=self.settings)
			moleculeDialog(self, homopol)
		  
		
		
		# Carbon Allotropes
		elif self.key == "swCNT":
			from interface.nanotubeEditor.nanotubeEditor import NanotubeBuilder
			cnt = NanotubeBuilder(self, self.settings)
			moleculeDialog(self, cnt)
		elif self.key == "Graphene":
			from interface.grapheneEditor.grapheneEditor import GrapheneBuilder
			graph = GrapheneBuilder(self, self.settings)
			moleculeDialog(self, graph)
		elif self.key == "Diamond":
			from interface.diamondEditor.diamondEditor import DiamondBuilder
			diamond = DiamondBuilder(self, self.settings)
			moleculeDialog(self, diamond)
		
		# Solvents
		elif self.key == "THF":
			from lib.chemicalGraph.molecule.solvent.THF import THF
			self.addMolecule(THF())
		elif self.key == "DMF":
			from lib.chemicalGraph.molecule.solvent.DMF import DMF
			self.addMolecule(DMF())
		elif self.key == "Water":
			from lib.chemicalGraph.molecule.solvent.WATER import WATER
			self.addMolecule(WATER())
		elif self.key == "Chloroform":
			from lib.chemicalGraph.molecule.solvent.CLF import CLF
			self.addMolecule(CLF())
		elif self.key == "Chloroform (4 atoms)":
			from lib.chemicalGraph.molecule.solvent.CLF4 import CLF4
			self.addMolecule(CLF4())
		elif self.key == "Hydrogen Peroxide":
			from lib.chemicalGraph.molecule.solvent.H2O2 import H2O2
			self.addMolecule(H2O2())
		elif self.key == "Xylene":
			from lib.chemicalGraph.molecule.solvent.Xylene import Xylene
			self.addMolecule(Xylene())
		elif self.key == "AcetoneAllH":
			from lib.chemicalGraph.molecule.solvent.AcetoneAllH import AcetoneAllH
			self.addMolecule(AcetoneAllH())
		elif self.key == "AcetoneNoH":
			from lib.chemicalGraph.molecule.solvent.AcetoneNoH import AcetoneNoH
			self.addMolecule(AcetoneNoH())
		
		# Surfactants
		elif self.key == "SDS":
			from lib.chemicalGraph.molecule.solvent.SDS import SDS
			self.addMixture(SDS())
			
		elif self.key == "SDBS":
			from lib.chemicalGraph.molecule.solvent.SDBS import SDBS
			self.addMixture(SDBS())
			
		elif self.key == "PABA-Tetradecane":
			from lib.chemicalGraph.molecule.solvent.PABA import PABA_Tetradecane
			self.addMolecule(PABA_Tetradecane())
			
		elif self.key == "PABA-Heptane":
			from lib.chemicalGraph.molecule.solvent.PABA import PABA_Heptane
			self.addMolecule(PABA_Heptane())
			
		elif self.key == "PABA-Pentane":
			from lib.chemicalGraph.molecule.solvent.PABA import PABA_Pentane
			self.addMolecule(PABA_Pentane().changeResidues("PAB"))
			
		# Ions
		elif self.key == "Na":
			from lib.chemicalGraph.molecule.solvent.Na import Na
			self.addMolecule(Na())

                # Custom section - CORALS
                elif self.key == "CORALS":
                        from interface.coralsEditor.coralsEditor import CoralsBuilder
                        corals = CoralsBuilder(self, self.settings)
                        moleculeDialog(self, corals)
	
		else:
			self.addMolecule(Element(Element.nameToSymbol(self.key.split(' ')[0])))
		
		self.update()
		self.buildPreview.update()

	def on_addCustomButton_pressed(self):
		from interface.classifier.Load import Load
		self.history.push()
		loader = Load(self)
		loader.show()
		loader.exec_()

		self.addMixture(loader.getMixture())
		self.buildPreview.update()
		self.update()
		self.buildPreview.update()


	def on_copyButton_pressed(self):
		if not self.ui.copyButton.isFlat():
			if (self.wolffia.simRunning):
					message = QtGui.QMessageBox(1, "Warning", "There's a simulation running right now.")
					message.exec_()
			else:	  
				self.copy()
		if not self.ui.removeButton.isFlat():
			if (self.wolffia.simRunning):
					message = QtGui.QMessageBox(1, "Warning", "There's a simulation running right now.")
					message.exec_()
			else:	  
				self.copy()

	def on_catalogButton_pressed(self):
		if not self.ui.catalogButton.isFlat():
			selected = self.editor.selectedMolecules()
			#print "SELCTEDDDDDD >>." , selected[0]
			if (self.wolffia.simRunning):
					message = QtGui.QMessageBox(1, "Warning", "There's a simulation running right now.")
					message.exec_()
			
			elif selected == []:
				QtGui.QMessageBox.warning(self, "Wolffia's warning", "Please select a molecule.", QtGui.QMessageBox.Ok)
				return
			
			else:
				#print "on_catalogButton_pressed",  self.ui.molCatalog.topLevelItemCount()
				customTreeWidget = self.ui.molCatalog.topLevelItem (self.ui.molCatalog.topLevelItemCount()-1)
				#print "on_catalogButton_pressed childCount", customTreeWidget.childCount ()
				
				print "SELCTEDDDDDD >>." , selected
				mixtureToSave = Mixture()
				print "mixtureToSave >>>>", mixtureToSave
				molName = ""
				print "molName >>>>" , molName
				for mol in selected:
					print "mol >>>>", mol
					mixtureToSave.add(mol.copy(), True)
					print "mixtureToSave agregados >>>>" ,mixtureToSave
					if molName == "":
						molName = mol.molname()
					else:
						molName += ("-" + mol.molname())
						
				print "SELECETEDDDD: ", selected , "mixtureToSave Final" , mixtureToSave
				print "############################################################"
				#Pregunta el nombre de la molecula que quiere guardar en el catalogo
				nameMolGUI = QtGui.QInputDialog(self)
				nameMolGUI.setTextValue(str(selected[0]))
				
				nameMol, ok = nameMolGUI.getText(self, "Custom Molecule", "Set Molecule Name:",0,str(selected[0]))
	
				
				print "value ",nameMol," ok ",ok
				if ok:		
					#Guarda archivo en .cMolecule dentro de .wolffia
					cMixFileName = "/" + nameMol + ".wfm"
					cMixFileDir = WOLFFIA_DIR + C_MOLECULE_CATALOG + cMixFileName
					if os.path.exists(cMixFileDir):
						print "archivo existe" , cMixFileDir
						nameMol = nameMol + "*"
						cMixFileName = "/" + nameMol + ".wfm"
						cMixFileDir = WOLFFIA_DIR + C_MOLECULE_CATALOG + cMixFileName
						
					print "cMixFileDir>>>>>" , cMixFileDir
					#Add a child to Custom Molecule in the Molecular Structure Catalog 
					nameQT = QtGui.QTreeWidgetItem()
					nameQT.setText(0,nameMol)
					customTreeWidget.addChild(nameQT)
					#customTreeWidget.addChild(QtGui.QTreeWidgetItem())
					print "NAMEMOL1", nameMol												 
					self.history.currentState().getMixture().save(cMixFileDir)


					
				
				
				#Guarda archivo en .cMolecule dentro de .wolffia 
				#MixtureToSave are selected
				#cMixtureToSave = Mixture("To save")
				#Nombre del Archivo que se va a guardar es cMolName
				#cMolName = str(nombre.textValue()) + ".wfm"
				#for mol in selected:
				#   print "mol:", mol
				#	cMixtureToSave.add(mol.copy(), False)
					
				#Directorio en donde se va a guardar es dirCmolName
				#dirCmolName = self.settings.workingFolder + self.cMol
				
				#try:
				#	print "TRYYYYYYYYYYYYyyyyy"
				#	basename = str(dirCmolName.path() +  "/" + cMolName)
				#	print "basename" , basename
				#	mixtureToSave.writePDB(basename)
				   
				
				#except:
				#	QtGui.QMessageBox.warning(self, "Wolffia's warning", cMolName + " could not be saved.", QtGui.QMessageBox.Ok) 
				

				
				#print "cmolName >>>>>>>>>",cMolName, "directorio: >>>>>>", dirCmolName		 
				#selected.writePDB(cMolName)
				#print "SAVEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE "
				#print ""
				
	def on_catalogButton_pressed(self):
		if not self.ui.removeButton.isFlat():
			if (self.wolffia.simRunning):
					message = QtGui.QMessageBox(1, "Warning", "There's a simulation running right now.")
					message.exec_()
			else:
				print "on_catalogButton_pressed",  self.ui.molCatalog.topLevelItemCount()
				customTreeWidget = self.ui.molCatalog.topLevelItem (self.ui.molCatalog.topLevelItemCount()-1)
				print "on_catalogButton_pressed childCount", customTreeWidget.childCount ()
				selected = self.editor.selectedMolecules()
				nombre = QtGui.QInputDialog(self)
				nombre.setTextValue(str(selected[0]))
				nombre.exec_()
				customTreeWidget.addChild(QtGui.QTreeWidgetItem([str(nombre.textValue())]))

	def on_duplicateButton_pressed(self):
		if not self.ui.duplicateButton.isFlat():
			if (self.wolffia.simRunning):
					message = QtGui.QMessageBox(1, "Warning", "There's a simulation running right now.")
					message.exec_()
			else:	  
				self.history.push()
				self.duplicate()
				self.buildPreview.update()


	def on_removeButton_pressed(self):
		#print "on_removeButton_pressed"
		if not self.ui.removeButton.isFlat():
			if (self.wolffia.simRunning):
					message = QtGui.QMessageBox(1, "Warning", "There's a simulation running right now.")
					message.exec_()
			else:	  
				progress	  = QtGui.QProgressDialog("Removing...", QtCore.QString(), 0, 5, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
				progress.setWindowModality(QtCore.Qt.WindowModal)
				
				progress.setValue(1)
				self.history.push()
				progress.setValue(2)
				self.remove()
				progress.setValue(3)
				self.editor.reset()
				progress.setValue(4)
				self.buildPreview.update()
				#self.buildPreview.setMixture(self.history.currentState().getMixture())
				progress.setValue(5)
				progress.hide()
	#-------------------------------------------------------------------------------
	def on_saveWFMbutton_pressed(self, saveState = True):
		#print "on_saveWFMbutton_pressed "
		if not saveState: return
		
		else:
			#mixFile = self.history.currentState().getBuildDirectory() + self.history.currentState().getMixtureName() + ".wfm" 
			self.history.currentState().save()
			d = WFileNameDialog(self, 'Save current Mixture', self.history.currentState().getBuildDirectory(), "Mixture file (*.wfm)")
			if d.isReady():
				filename = d.fullFilename()
				#print "FILENAME = ", filename
				#print "on_saveWFMbutton_pressed >>>>> ","\'"+filename[-4:]+"\'"
				if filename[-4:] != ".wfm" and QtGui.QMessageBox.question (self, "Wolffia's message", "File does not end with .wfm. Add extension?", "Yes", "No") == 0:
					filename += ".wfm"
					if os.path.exists(filename) and QtGui.QMessageBox.question (self, "Wolffia's message", "File exists.", "Overwrite", "Cancel") != 0:
						return
				self.history.currentState().getMixture().save(filename)
	
				QtGui.QMessageBox.information(self, "Wolffia's message", filename + " saved.", QtGui.QMessageBox.Ok)

	

	def on_saveButton_pressed2(self, saveFiles=True):
		if not saveFiles: return
		mixName = self.history.currentState().getMixtureName()
		d = WDirectoryDialog(self, 'Specify directory to save ' + mixName + ".pdb and " + mixName + ".psf", self.settings.workingFolder)
		
		if d.accepted():
			basename = d.path() +  "/" + mixName
			import os
			if not (os.path.exists(basename + ".pdb") or os.path.exists(basename + ".psf")) or QtGui.QMessageBox.question (self, "Wolffia's message", "File exists.", "Overwrite", "Cancel") == 0:
				mix = self.history.currentState().getMixture()
				mix.writePDB(basename + ".pdb")
				mix.writePSF(basename + ".psf")
	
				QtGui.QMessageBox.information(self, "Wolffia's message", mixName + ".pdb and " + mixName + ".psf saved.", QtGui.QMessageBox.Ok)

	def on_saveButton_pressed3(self, saveFiles=True):
		if not saveFiles: return
		selected = self.editor.selectedMolecules()
		#print "on_saveButton_pressed ", selected
		if selected == []:
			QtGui.QMessageBox.warning(self, "Wolffia's warning", "Could not determine the molecule to be saved.\nPlease select one.", QtGui.QMessageBox.Ok)
			return

		mixtureToSave = Mixture("To save")
		molName = ""
		for mol in selected:
			mixtureToSave.add(mol.copy(), False)
			if molName == "":
				molName = mol.molname()
			else:
				molName += ("-" + mol.molname())
		
		d = WDirectoryDialog(self, 'Specify directory to save ' + molName + ".pdb and " + molName + ".psf", self.settings.workingFolder)
		
		try:
			if d.accepted():
				basename = str(d.path() +  "/" + molName)
				#import os
				if not (os.path.exists(basename + ".pdb") or os.path.exists(basename + ".psf")) or QtGui.QMessageBox.question (self, "Wolffia's message", "File exists.", "Overwrite", "Cancel") == 0:
					#mix = self.history.currentState().getMixture()
					#print "on_saveButton_pressed ", basename
					mixtureToSave.writePDB(basename + ".pdb")
					mixtureToSave.writePSF(basename + ".psf")
		
					QtGui.QMessageBox.information(self, "Wolffia's message", molName + ".pdb and " + molName + ".psf saved.", QtGui.QMessageBox.Ok)
		except:
				QtGui.QMessageBox.warning(self, "Wolffia's warning", molName + ".pdb and " + molName + ".psf could not be saved.", QtGui.QMessageBox.Ok)

	#------------------------------------------------------------------------------------------

	def on_updateButton_pressed(self):
		#print "on_updateButton_pressed "
		
		QtGui.QMessageBox.information(self, "Wolffia's message", "Updates can only be done from coordinate files\nproduced by simulations prepared with Wolffia.\nOther files will produce unexpected results..", QtGui.QMessageBox.Ok)

		d = WFileDialog(self, 'Specify coordinate file to load.', self.settings.workingFolder, filter="*.pdb *.coor")
		
		if d.accepted():
			self.history.push()
			try:
				self.history.currentState().mixture.updateCoordinates(str(d.fullFilename()))
		
				self.buildPreview.update()
				QtGui.QMessageBox.information(self, "Wolffia's message", "Coordinates updated.", QtGui.QMessageBox.Ok)
			except:
				QtGui.QMessageBox.warning(self, "Wolffia's warning", "Coordinates could not be updated.", QtGui.QMessageBox.Ok)
				self.history.back()

	def on_structManager_itemChanged(self, wi):
		#if isinstance(wi, myTableWidgetItem) and wi.name != "(no name)" and wi.isSelected():
		if wi.column() == 2:
			row = wi.row()
			mol = str(self.ui.structManager.item(row, 4).text())
			
			if str(wi.text()) == "":
				wi.setText(self.history.currentState().getMixture().getMolecule(mol).molname())
			elif mol[:8] == "SOLVENT(":
				if wi.text() != self.history.currentState().getMixture().getMolecule(mol).molname():
					nameLen = len(mol)
					sepPos = mol.rfind("_")
					for molecule in self.history.currentState().getMixture():
						if mol[:sepPos] == molecule[:sepPos]:
							with warnings.catch_warnings(record=True) as w:
								#print "on_structManager_itemChanged",molecule,str(wi.text()),str(wi.text())+molecule[sepPos:]
								self.history.currentState().getMixture().renameMolecule(molecule, str(wi.text()))
							if len(w) > 0: 
								QtGui.QMessageBox.information(self, "Error", str(w[-1].message))
					self.update()
					
			else:
				#print "on_structManager_itemChanged changing molecule with id ", mol
				#print "on_structManager_itemChanged", self.history.currentState().getMixture().getMolecule(mol).molname(), "->", str(wi.text()), " row=", row
				if wi.text() != self.history.currentState().getMixture().getMolecule(mol).molname():
					self.history.push()
					with warnings.catch_warnings(record=True) as w:
						self.history.currentState().getMixture().renameMolecule(mol, str(wi.text()))
					if len(w) > 0: 
						QtGui.QMessageBox.information(self, "Error", str(w[-1].message))
					self.update()
			
					#self.history.currentState().getMixture().getMolecule(mol).rename(str(wi.text()))
					#print "on_structManager_itemChanged getMixture:",self.history.currentState().getMixture()

	def on_structManager_cellClicked(self, row, col):
		#update editor with selected molecule	
		#print "on_structManager_cellClicked",row,col
		
		molecules = self.history.currentState().getMixture().moleculeIDs()
		molecules.sort()
		
		#mol = molecules[row]
		mol = str(self.ui.structManager.item(row, 4).text())
		#print "on_structManager_cellClicked",row,col,mol
		if col == 0:
			item = self.ui.structManager.itemAt(row, col)   
			#print "detecto"
		elif col == 2:
			#print "on_structManager_cellClicked B"
			#selected = self.editor.setMolecule(self.history.currentState().getMixture().getMolecule(mol), str(mol), True)
			m = self.history.currentState().getMixture().getMolecule(mol)
			#print "on_structManager_cellClicked B2",m,mol
			selected = self.editor.setMolecule(m, str(mol), True)
			#print "on_structManager_cellClicked C", selected
			
			# if shift key is pressed perform multiple selects
			modifiers = QtGui.QApplication.keyboardModifiers()
			if modifiers == QtCore.Qt.ShiftModifier and self.prevSelection != None:
				if self.prevSelection[1] == selected:
					if row < self.prevSelection[0]: ind = range(row+1,self.prevSelection[0])
					else: ind = range(self.prevSelection[0]+1,row)
					for i in ind:
						mol = str(self.ui.structManager.item(i, 4).text())
						m = self.history.currentState().getMixture().getMolecule(mol)
						if self.prevSelection[1]:
							self.editor.removeSelection(m, str(mol))
						else:
							self.editor.setMolecule(m, str(mol), removeIfPresent=False)
							
			self.prevSelection = [row, selected]
			self.ui.removeButton.setFlat(False)
			self.ui.duplicateButton.setFlat(self.clipboard == None or len(self.clipboard) == 0)
			self.ui.copyButton.setFlat(False)
			self.ui.catalogButton.setFlat(False)
			
			
			self.repaint()
			self.buildPreview.update()
			#print "on_structManager_cellClicked D"

		#self.update()
		#self.buildPreview.update()
		return
	

	@QtCore.pyqtSlot()
	def on_saveButton_triggered(self, saveFiles=True):
		if not saveFiles: return
		d = WFileNameDialog(self, 'Save Files', self.history.currentState().getBuildDirectory())
		if d.isReady():
			self.history.currentState().setMixtureName(d.mixname())
			self.history.currentState().writeFiles(d.fullFilename())
			mesg = self.history.currentState().getMixtureName() + '.pdb, '  + self.history.currentState().getMixtureName() + '.psf and '  + self.history.currentState().getMixtureName() + '.prm'
			info = QtGui.QErrorMessage(self)
			info.setModal(True) # blocks Wolffia
			info.showMessage("The files " + mesg + " have been successfully saved in " + d.path())

	
	def on_showCheckbox(self, on):
		print "on_showCheckbox", 
		

	def addMolecule(self, mol, remember=True):
		if mol != None:
			self.editor.reset()
			with warnings.catch_warnings(record=True) as w:
				self.history.currentState().addMolecule(mol)
				self.buildPreview.setMixture(self.history.currentState().getMixture(),True)
				#print "addMolecule len(w)",len(w)
				if len(w) > 0: 
					QtGui.QMessageBox.information(self, "Error", str(w[-1].message))
			if remember: self.history.push()


	def addMixture(self, mix, remember=True):
		if mix != None:
			for mol in mix:
				self.addMolecule(mix.getMolecule(mol), False)
				#self.history.currentState().addMixture(mix)
			if remember: self.history.push()

	def chosenMolecules(self):
		count = self.ui.structManager.topLevelItemCount()
		for i in range(count):
			item = self.ui.structManager.itemAt(i,1)
			#print item.isChecked()

	def copy(self):
		selected = self.editor.selectedMolecules()
		#print "copy ", selected
		if selected == []:
				errorgui = QtGui.QErrorMessage(self)
				errorgui.setModal(True) # blocks Wolffia
				errorgui.showMessage( "Error: no molecule chosen.")
		else:
			self.clipboard = Mixture("Clipboard")
			for mol in selected:
				#print "copy", mol
				#self.clipboard.add(self.history.currentState().getMixture().getMolecule(molname).copy(), False)
				self.clipboard.add(mol.copy(), False)
		#print "copy update<", self.editor.selected()
		self.update()
		#print "copy >", self.editor.selected()
		
		
	def duplicate(self):
		from sets import Set
		#print "duplicate ", self.clipboard.molecules()
		currentIDs = Set(self.history.currentState().getMixture().molecules())
		try:
			newMols = self.clipboard.copy()
			newMols.moveBy([random.uniform(0., 0.1),random.uniform(0., 0.1),random.uniform(0., 0.1)])
			self.history.currentState().getMixture().merge(newMols)
		except:
			errorgui = QtGui.QErrorMessage(self)
			errorgui.setModal(True) # blocks Wolffia
			errorgui.showMessage("Error: could not duplicate molecules." )

		# select pasted molecules
		newMols = Set(self.history.currentState().getMixture().molecules()) - currentIDs
			
		progressMax   = len(newMols)-1
		progressCount = 0
		progress	  = QtGui.QProgressDialog("Adding...", QtCore.QString(), 0, progressMax, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
		progress.setWindowModality(QtCore.Qt.WindowModal)
		
		#print "duplicate ", self.history.currentState().getMixture().molecules(),newMols
		self.editor.reset()
		for mol in newMols:
			self.editor.setMolecule(self.history.currentState().getMixture().getMolecule(mol), mol)
			self.history.currentState().shownMolecules.show(mol)
			progressCount += 1
			progress.setValue(progressCount)
		self.insertAllToManager()
		progress.hide()
		
		self.update()
				
	def insertAllToManager(self):
		from lib.chemicalGraph.molecule.solvent.Solvent import Solvent
		start = time.clock()
		#print "insertAllToManager ",self.history.currentState().getMixture().molecules()
		
		
		self.mixModification = self.history.currentState().getMixture().getModificationTime()
		#self.ui.structManager.setRowCount(len(self.history.currentState().mixture))
		self.ui.structManager.setRowCount(0)
		row = 0
		solventShown   = ShownSolvent()
		shownMolecules = self.history.currentState().shownMolecules
		molecules	  = self.history.currentState().getMixture().moleculeIDs()
		#print "insertAllToManager ",molecules
		
		#progress	  = QtGui.QProgressDialog("Storing...", "Abort", 0, len(molecules), self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
		#progress.setWindowModality(QtCore.Qt.WindowModal)
		#progress.setAutoClose(True)
		#progress.setMinimumDuration(0)
		
		self.ui.structManager.blockSignals(True)
		molecules.sort()
		molNum = 0
		for molName in molecules:
			#molName = self.history.currentState().getMixture().getMolecule(mol).molname()
			#print "insertAllToManager ",ShownSolvent.isSolvent(molName),solventShown.isShown(molName)
			if not ShownSolvent.isSolvent(molName) or not solventShown.isShown(molName):
				self.ui.structManager.setRowCount(row+1)
				#insert checkbox on column 1
		
				checkBox = PreviewButton(self.history.currentState(),
										self.buildPreview, molname=str(molName), parent=self,
										initState=shownMolecules.isShown(str(molName)),
										editor=self.editor)
				checkBox.setToolTip("Show or hide.")
				self.ui.structManager.setCellWidget(row, 0, checkBox)
		
				pin = FixedButton(self.history.currentState(),
										self.buildPreview, molname=str(molName), parent=self,
										initState=self.history.currentState().fixedMolecules.isFixed(str(molName)))
				pin.setToolTip("Fixes position of the molecule.")
				self.ui.structManager.setCellWidget(row, 1, pin)
		
				#print "insertAllToManager",str(self.history.currentState().mixture.getMolecule(molName)._name) , molecules
				
				#insert molname on column 2
				baseMolName = str(self.history.currentState().mixture.getMolecule(molName).molname())
				#print "insertAllToManager  creando item para ", baseMolName

				#if isinstance(self.history.currentState().mixture.getMolecule(molName), Solvent):
				#	baseMolName += "(solvent)"
				newitem = QtGui.QTableWidgetItem(baseMolName)
				newitem.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
				newitem.setToolTip("Click to select or double click to edit the name.")
				self.ui.structManager.setItem(row, 2, newitem)
		
				#print "insertAllToManager",self.editor.getId(),molName
				if  molName in self.editor.selectedNames():
					newitem.setBackgroundColor (QtCore.Qt.green)
		
				#insert atom count on column 3
				newitem = QtGui.QTableWidgetItem(str(self.history.currentState().mixture.getMolecule(molName).order()))
				newitem.setFlags(QtCore.Qt.ItemIsEnabled)
				self.ui.structManager.setItem(row, 3, newitem)
		
				#insert id on column 4
				newitem = QtGui.QTableWidgetItem(str(molName))
				newitem.setFlags(QtCore.Qt.ItemIsEnabled)
				self.ui.structManager.setItem(row, 4, newitem)
		
				row += 1
				solventShown.setAsShown(molName) 
				#print "insertAllToManager solventShown.setAsShown(molName) ", solventShown.isShown(molName)
			elif not ShownSolvent.isSolvent(molName):
				self.history.currentState().shownMolecules.show(molName)
		
			molNum += 1
			#progress.setValue(molNum)
		
		
		#self.buildPreview.setMixture(self.history.currentState().getMixture())
		#self.chosenMolecules()
		
		self.ui.structManager.blockSignals(False)
		self.ui.removeButton.setFlat(len(self.editor) == 0)
		#self.ui.duplicateButton.setFlat(self.editor.ident == None)
		self.ui.copyButton.setFlat(len(self.editor) == 0)
		self.ui.catalogButton.setFlat(len(self.editor) == 0)
		self.ui.duplicateButton.setFlat(self.clipboard == None or len(self.clipboard) == 0)
		
		
		#self.ui.removeButton.setFlat(molNum == 0)
		#self.ui.duplicateButton.setFlat(molNum == 0)
		
		#progress.hide()
		stop = time.clock()
		#print "insertAllToManager time",stop-start


	def showEvent(self, e):
		#print "buildTab showEvent"
		#start = time.clock()
		#if self.firstUpdate:
		#	self.update()
		#	self.firstUpdate = False

		self.update()
		super(BuildTab, self).showEvent(e)
		#print "buildTab showEvent time",time.clock()-start


	def remove(self):
		#print "remove"
		self.copy()
		selected = self.editor.selectedNames()
		#print "BuildTab.remove ", selected
					
		try:
			self.history.currentState().removeMoleculesFrom(selected)
			'''
			for molname in selected:
				self.history.currentState().removeMolecule(molname)
			'''
			
			#print "BuildTab.remove ", selected, " removed "
		except:
			#errorgui = QtGui.QErrorMessage(self)
			#errorgui.setModal(True) # blocks Wolffia
			#errorgui.showMessage("Error: could not delete molecule " 
			#	+ molname + "." )
			logging.getLogger(self.__class__.__name__).warning("Could not delete molecules " 
				+ selected + ".")
		self.editor.reset()
		self.update()
		
	def repaint(self):
		selected = self.editor.selectedNames()
		for row in range(self.ui.structManager.rowCount()):
			#print "repaint ", self.ui.structManager.item(row,4).text()
			if self.ui.structManager.item(row,4).text() in selected:
				self.ui.structManager.item(row, 2).setBackgroundColor (QtCore.Qt.green)
			else:
				self.ui.structManager.item(row, 2).setBackgroundColor (QtCore.Qt.white)
			

	def reset(self):
		#print "buildTab reset in"
		self.buildPreview.reset()
		self.editor.reset() 
		self.prevSelection   = None
		self.prevShow		= None
		self.prevFixed	   = None
		#print "buildTab reset out"


	def update(self):
		#start = time.clock()

		#print "updating buldTab, mixture=", self.history.currentState().getMixture()
		self.insertAllToManager()
		#print "buildTab update insertAllToManager",time.clock()-start
		#self.buildPreview.setMixture(self.history.currentState().getMixture())		
		self.mixModification = time.clock()
		
		self.ui.structManager.resizeColumnToContents(0)
		self.ui.structManager.resizeColumnToContents(1)
		self.ui.structManager.resizeColumnToContents(2)
		self.ui.structManager.resizeColumnToContents(3)
		
		self.editor.update()
		#self.buildPreview.update()
		#self.wolffia.update()
		#print "buildTab update time",time.clock()-start
		self.repaint()


	'''
	def on_searchLine_returnPressed(self):
		query = QtHelp.QHelpSearchQuery(QtHelp.QHelpSearchQuery.DEFAULT, self.ui.searchLine.text())				
		search = QtHelp.QHelpSearchEngine()
		search.search()	
		search.resultWidget()
	'''


class ShownSolvent:
	def __init__(self):
		self.solventList = dict()
		
	@staticmethod
	def isSolvent(molName): return molName[:8] == "SOLVENT("

	@staticmethod
	def solventType(molName): 
		if ShownSolvent.isSolvent(molName):
			return molName[8:molName.find(')')]
		else: return ""

	def isShown(self, solventName):
		#print "ShownSolvent isShown",solventName,self.solventList
		if ShownSolvent.isSolvent(solventName):
			#print "ShownSolvent isShown buscando"
			solvType = ShownSolvent.solventType(solventName)
			if not self.solventList.has_key(solvType): self.setAsNotShown(solventName)
			return self.solventList[solvType]
		return False
	
	def set(self,solventName, state=True):
		if ShownSolvent.isSolvent(solventName):
			self.solventList[ShownSolvent.solventType(solventName)] = state
			
	def setAsShown(self,solventName):
		#print "ShownSolvent setAsShown", solventName
		self.set(solventName, True)
			
	def setAsNotShown(self,solventName):
		self.set(solventName, False)
