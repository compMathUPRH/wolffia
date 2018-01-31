#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#  NanotubeBuilder.py
#  Version 0.1, October, 2011
#
#  Single-wall nanotube builder.
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

from PyQt4 import QtGui, QtCore
from ui_nanotubeEditor import Ui_NanotubeEditor

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../')

from conf.Wolffia_conf import NANOCAD_MOLECULES, WOLFFIA_STYLESHEET
from lib.chemicalGraph.molecule.allotrope.Tube import Tube
from lib.chemicalGraph.molecule.allotrope.Hexagonal2D import Hexagonal2D
from lib.chemicalGraph.Mixture import Mixture
from interface.main.MixtureViewer import MixtureViewer
from interface.main.History import History
from interface.main.Settings import Settings

class NanotubeBuilder(QtGui.QDialog):
	"""
	Wolffia's dialogue box to produce nanotubes.
	"""
	# Class Fields:
	# ui: stores reference to user interface
	# files: [string, string], PDB and PSF filenames
	# tubes: Mixture, a Tube
	# tubePreview: MixtureViewer

	def __init__(self, parent=None, settings=None):
		"""
		Constructor for nanotube editor.
		
		Parameters used:
		parent  :	Window, widget or object that was used to call this dialogue
		settings:	Settings
		"""
		
		super(NanotubeBuilder, self).__init__(parent, modal=1)
		
		self.settings		= settings
		self.isAdded		= False
		self.files			= None
		# esto hay que arreglarlo!
		self.history		= History()
		self.tubePreview	= MixtureViewer(self.history, self, None)
		self.ui				= Ui_NanotubeEditor()
		
		self.ui.setupUi					(self)
		self.ui.viewerLayout.addWidget	(self.tubePreview)
		self.generateTubes				()
		self.ui.nSpinBox.setMaximum(200)
		self.ui.mSpinBox.setMaximum(200)
		if self.settings:
			self.tubePreview.setHighResolution	(settings.highResolution)
			self.tubePreview.setLabeling		(settings.showLabels)
			self.tubePreview.showAxes			(settings.showAxes)
			self.tubePreview.showHelp			(settings.showHelp)
			self.ui.OKButton.setText			("OK")
		
		try:
			self.setStyleSheet(open(WOLFFIA_STYLESHEET,'r').read())
		except:
			print "WARNING: Could not read style specifications"
		self.tubePreview.update()

	def generateTubes(self):
		n			= self.ui.nSpinBox.value()
		m			= self.ui.mSpinBox.value()
		tubeLength	= self.ui.tubeLengthSpinBox.value()
		
		self.history.currentState().reset()
		self.history.currentState().addMolecule(Tube(n, m, tubeLength))
		self.modified = False
		
	def getMixture(self):
		return self.history.currentState().getMixture()

	# Signal managers
	def on_horizontalSlider_valueChanged(self,pos):
		self.ui.tubeLengthSpinBox.setValue(pos/10.)
		self.modified = True

	def on_tubeLengthSpinBox_valueChanged(self,val):
		self.ui.horizontalSlider.setValue(int(float(val)*10))
		self.modified = True

	def on_mSpinBox_valueChanged(self,val):
		if self.ui.armchairButton.isChecked():
			self.ui.nSpinBox.setValue(self.ui.mSpinBox.value())
		self.modified = True

	# Toggles between the three different types of nanotube layouts
	def on_armchairButton_toggled(self, selected):
		if selected:
			self.ui.nSpinBox.setValue(self.ui.mSpinBox.value())
			self.ui.nSpinBox.setDisabled(True)
		self.modified = True

	def on_chiralButton_toggled(self, selected):
		if selected:
			self.ui.nSpinBox.setEnabled(True)
		self.modified = True

	def on_zigZagButton_toggled(self, selected):
		if selected:
			self.ui.nSpinBox.setValue(0)
			self.ui.nSpinBox.setDisabled(True)
		self.modified = True

	@QtCore.pyqtSlot()
	def on_cancelButton_pressed(self):
		self.close()

	@QtCore.pyqtSlot()
	def on_OKButton_pressed(self):
		if self.modified: self.generateTubes()
		if self.settings:
			self.isAdded = True
			self.close()
		else:
			from NanotubeSaveDialog import NanotubeSaveDialog
			ntDialog = NanotubeSaveDialog(self.getMixture(),files=self.files, parent=self)
			ntDialog.show()
			ntDialog.exec_()
			self.files = ntDialog.getFileNames()
			print self.files

	@QtCore.pyqtSlot()
	def on_previewButton_pressed(self):
		self.generateTubes()
		self.tubePreview.update()

	def closeEvent(self, e):
		if not self.isAdded:
			self.history.currentState().updateMixture(Mixture())

#-------------------------------------------------------------------------------

if __name__ == '__main__':
	import sys

	app = QtGui.QApplication(sys.argv)
	# Hay que arreglar esto!! Metodo NanoCADState ya no existe. ~ Radames
	load_gui = NanotubeBuilder()
	load_gui.show()
	sys.exit(app.exec_())
