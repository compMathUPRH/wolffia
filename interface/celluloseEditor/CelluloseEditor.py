#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#  HomopolyEditor.py
#  Version 0.1, November, 2011
#
#  Homopolymer builder.
#  Produces PDF and PSF files for molecular dynamics simulations.
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

from PyQt4 import QtGui, QtCore
from ui_celluloseEditor import Ui_CelluloseEditor 

import sys, os, math
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../')

from conf.Wolffia_conf import NANOCAD_MOLECULES, WOLFFIA_STYLESHEET
from lib.chemicalGraph.Mixture import Mixture
from lib.chemicalGraph.molecule.polymer.Homopolymer import Homopolymer
from interface.main.MixtureViewer import MixtureViewer
from interface.main.History import History

#-------------------------------------------------------------------------------

class CelluloseEditor(QtGui.QDialog):
	"""
	Wolffia's dialogue to produce homopolymers.
	"""
	# Class Fields:
	# ui: stores reference to user interface
	# files: [string, string], PDB and PSF filenames
	# homopol: Mixture, an Homopolymer
	# homopolPreview: MixtureViewer

	def __init__(self, appState, parent=None, settings=None):
		"""
		Constructor for homopolymer editor.
		
		Parameters used:
		parent  :	Window, widget or object that was used to call this dialogue
		settings:	Settings
		"""

		super(CelluloseEditor, self).__init__(parent, modal=1)

		self.settings		= settings
		self.state			= appState
		self.files			= None
		self.isAdded		= False
		self.history		= History()
		self.homopolPreview	= MixtureViewer(self.history, self, None)
		self.ui				= Ui_CelluloseEditor()

		self.ui.setupUi					    (self)
		self.generateCellulose				()
		self.ui.viewerLayout.addWidget		(self.homopolPreview)
		self.ui.headerLabel.setText			("Cellulose Crystal Editor")
		self.ui.lengthDSpinner.setSingleStep(self.poly.DISPL)
		self.ui.lengthDSpinner.setMinimum	(self.poly.DISPL)
		self.ui.lengthSlider.setTickInterval(self.poly.DISPL)
		self.ui.lengthSlider.setMinimum		(self.poly.DISPL)
		self.ui.nSpinBox.setValue		    (2)
		
		image = os.path.dirname(os.path.realpath(__file__))+"/images/" +self.poly.IMAGE
		self.ui.diagram.setPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8(image)).scaledToHeight(100,1))

		if self.settings != None:
			self.homopolPreview.setHighResolution	(self.settings.highResolution)
			self.homopolPreview.setLabeling			(self.settings.showLabels)
			self.homopolPreview.showAxes			(self.settings.showAxes)
			self.homopolPreview.showHelp			(settings.showHelp)
			self.ui.okButton.setText				("OK")

		try:
			self.setStyleSheet(open(WOLFFIA_STYLESHEET,'r').read())
		except:
			print "WARNING: Could not read style specifications"
		self.homopolPreview.update()


	def generateCellulose(self):
		"""
		Arguments:
		n:  number of monomers per chain
		nx: number of chains per plane
		nz: number of stacked planes
		"""
		DISPL_100 = [8.0,0.0,4.0,3.0] # dx, dy, dz, dxz
		DISPL_010 = [7.3,0.0,4.0]
		DISPL_110 = [6.5,0.0,7.0]

		n = self.ui.nSpinBox.value()
		nx = self.ui.horizontalSpinBox.value()
		nz = self.ui.layersSpinBox.value()

		self.homopol = Mixture()
		from chemicalGraph.molecule.polymer.Cellulose import Cellulose
		
		if self.ui.radio100.isChecked():
			for i in range(nx):
				for j in range(nz):
					# alpha or betha structure
					if self.ui.buttonA.isChecked(): self.poly = Cellulose(n, 'a')
					else:                           self.poly = Cellulose(n, 'b')
					# locate the polymer chain			
					#self.poly.moveby([DISPL_100[0] * (i+(j%2)/2.), DISPL_100[1] * ((i+j)%2), DISPL_100[2] * j])
					self.poly.moveby([DISPL_100[0] * i + DISPL_100[3] * (j%2), DISPL_100[1] * (i%2), DISPL_100[2] * j])
					self.homopol.add(self.poly)
					
		if self.ui.radio110.isChecked():
			for i in range(nx):
				for j in range(nz):
					# alpha or betha structure
					if self.ui.buttonA.isChecked(): self.poly = Cellulose(n, 'a')
					else:                           self.poly = Cellulose(n, 'b')
					# locate the polymer chain	
					self.poly.rotateDeg(0., 45.0, 0.)	
					self.poly.moveby([DISPL_110[0] * i, DISPL_110[1] * ((i+j)%2), DISPL_110[2] * j])
					self.homopol.add(self.poly)	
					
		if self.ui.radio010.isChecked(): 
			for i in range(nx):
				for j in range(nz):
					# alpha or betha structure
					if self.ui.buttonA.isChecked(): self.poly = Cellulose(n, 'a')
					else:                           self.poly = Cellulose(n, 'b')
					# locate the polymer chain	
					self.poly.rotateDeg(0., 0., 90.)	
					self.poly.moveby([DISPL_010[0] * (i+(j%2)/2.), DISPL_010[1] * ((i+j)%2), DISPL_010[2] * j])
					self.homopol.add(self.poly)

		self.history.currentState().reset()
		self.history.currentState().addMixture(self.homopol)
		self.homopolPreview.update()

	def getMixture(self):
		return self.history.currentState().getMixture()


	# Signal managers
	def on_nSpinBox_valueChanged(self):
		self.generateCellulose()
		length = self.poly.DISPL*self.ui.nSpinBox.value()
		self.ui.lengthDSpinner.setValue(length)
		self.ui.lengthSlider.setValue(length)

	def on_lengthDSpinner_valueChanged(self):
		n = round(self.ui.lengthDSpinner.value()/self.poly.DISPL)
		self.ui.nSpinBox.setValue(n)
		self.ui.lengthSlider.setValue(n*self.poly.DISPL)

	def on_lengthSlider_sliderReleased(self):
		n = int(self.ui.lengthSlider.value()/self.poly.DISPL)
		self.ui.nSpinBox.setValue(n)

	def on_horizontalSpinBox_valueChanged(self): 
		self.generateCellulose()

	def on_layersSpinBox_valueChanged(self): 
		self.generateCellulose()
		
	#---------------------------------------------------------------------
	def on_buttonB_toggled(self, checked):
		self.ui.buttonA.setChecked(not checked)
		self.generateCellulose()

	def on_buttonA_toggled(self, checked):
		self.ui.buttonB.setChecked(not checked)
		self.generateCellulose()

	#---------------------------------------------------------------------
	def on_button110_toggled(self, checked):
		if checked:
			self.ui.button100.setChecked(not checked)
			self.ui.button010.setChecked(not checked)
			self.generateCellulose()

	def on_button100_toggled(self, checked):
		if checked:
			self.ui.button110.setChecked(not checked)
			self.ui.button010.setChecked(not checked)
			self.generateCellulose()

	def on_button010_toggled(self, checked):
		if checked:
			self.ui.button100.setChecked(not checked)
			self.ui.button110.setChecked(not checked)
			self.generateCellulose()
			
	#---------------------------------------------------------------------
	def on_radio100_toggled(self, checked):
		if checked:
			self.ui.radio110.setChecked(not checked)
			self.ui.radio010.setChecked(not checked)
			self.generateCellulose()
			
	def on_radio110_toggled(self, checked):
		if checked:
			self.ui.radio100.setChecked(not checked)
			self.ui.radio010.setChecked(not checked)
			self.generateCellulose()
			
	def on_radio010_toggled(self, checked):
		if checked:
			self.ui.radio110.setChecked(not checked)
			self.ui.radio100.setChecked(not checked)
			self.generateCellulose()
	#---------------------------------------------------------------------						
	def on_okButton_pressed(self):
		self.generateCellulose()
		self.isAdded = True
		self.close()

	def on_cancelButton_pressed(self):
		self.history.currentState().reset()
		self.close()


	def closeEvent(self, e):
		if not self.isAdded:
			self.history.currentState().updateMixture(Mixture())

	def wheelEvent(self, e):
		super(HomopolyEditor, self).wheelEvent(e)

#-------------------------------------------------------------------------------
if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	# Hay que arreglar esto!! Metodo NanoCADState ya no existe. ~ Radames
	from interface.main.History import NanoCADState
	load_gui = CelluloseEditor(NanoCADState())
	load_gui.show()
	sys.exit(app.exec_())
