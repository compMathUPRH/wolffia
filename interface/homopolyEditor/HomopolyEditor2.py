#!/usr/bin/python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  HomopolyEditor.py
#  Version 0.1, November, 2011
#
#  Homopolymer builder.
#  Produces PDF and PSF files for mollecular dynamics simulations.
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
import sys, os
import math

from PyQt5 import QtGui, QtCore
from ui_homopolyEditor import Ui_HomopolyEditor

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import NANOCAD_MOLECULES

from lib.chemicalGraph.Mixture import Mixture
from lib.chemicalGraph.molecule.polymer.Homopolymer import Homopolymer
from interface.main.MixtureViewer import MixtureViewer

class HomopolyEditor(QtGui.QDialog):
	# Class Fields:
	# ui: stores reference tu user interface
	# files: [string, string], PDF and PSF filenames
	# homopol: Mixture, an Homopolymer
	# homopolPreview: MixtureViewer

	DISPL = {"PMMA":[3.7, 0], "PolyCYT":[6.0, 1]}

	def __init__(self, key, appState, parent=None):
		super(HomopolyEditor, self).__init__(parent, modal=1)
	
		self.ui = Ui_HomopolyEditor()
		self.ui.setupUi(self)

		self.state	= appState	
		self.type 	= key
		#self.slideFactor = 50
		#self.files 	= None

		self.homopolPreview = MixtureViewer()
		self.ui.viewerLayout.addWidget(self.homopolPreview)

		self.ui.lengthDSpinner.setValue(self.DISPL[self.type][0])
		self.ui.lengthDSpinner.setSingleStep(self.DISPL[self.type][0])
		self.ui.lengthDSpinner.setMinimum(self.DISPL[self.type][0])
		self.ui.lengthSlider.setValue(self.DISPL[self.type][0])	
		self.ui.lengthSlider.setTickInterval(self.DISPL[self.type][0])
		self.ui.lengthSlider.setMinimum(self.DISPL[self.type][0])
		self.ui.stackedWidget.setCurrentIndex(self.DISPL[self.type][1])
		
		self.generateHomopol()
		self.generateHomopol()
		
		if __name__ != '__main__':
			self.ui.saveButton.setHidden(True)

	def generateHomopol(self):
		self.ui.headerLabel.setText(str(self.type) + " Editor")
		n = self.ui.nSpinBox.value()
		self.homopol = Mixture()
		exec("from chemicalGraph.molecule.polymer." + str(self.type) + " import " + str(self.type))
		self.homopol.add(eval(str(self.type) + "(n)"))
		self.homopolPreview.setMixture(self.homopol)

	# Manages signals
	def on_nSpinBox_valueChanged(self, value):
		self.generateHomopol()	
		length = self.DISPL[self.type][0]*value
		self.ui.lengthDSpinner.setValue(length)
		self.ui.lengthSlider.setValue(length)	

	def on_lengthDSpinner_valueChanged(self, value):
		n = int(math.floor(value/self.DISPL[self.type][0]))
		self.ui.nSpinBox.setValue(n)	
		self.generateHomopol()	
		#self.ui.lengthSlider.setValue(value)

	def on_lengthSlider_sliderMoved(self, value):
		n = int(math.floor(value/self.DISPL[self.type][0]))
		self.ui.nSpinBox.setValue(n)	
		self.generateHomopol()		
		self.ui.lengthDSpinner.setValue(value)	

	def on_okButton_pressed(self):
		self.generateHomopol()
		self.state.addMixture(self.homopol)
		self.close()

	'''
	def on_saveButton_pressed(self):
		from NanotubeSaveDialog import NanotubeSaveDialog

		# generate tube
		self.generateTubes()

		ntDialog = NanotubeSaveDialog(self.tubes,files=self.files, parent=self)
		ntDialog.show()
		ntDialog.exec_()
		self.files = ntDialog.getFileNames()
		print self.files 
	'''
	
	def on_cancelButton_pressed(self):
		self.close()
#---------------------------------------------------------------------------
if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	load_gui = HomopolyEditor(NanoCADState())
	load_gui.show()
	sys.exit(app.exec_())

