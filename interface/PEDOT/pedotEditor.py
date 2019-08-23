#!/usr/bin/python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  PEDOTBuilder.py
#  Version 0.1, October, 2011
#
#  Single-wall pedot builder.
#  Produces PDF and PSF files for mollecular dynamics simulations.
#  Based on NanotubeBuilder's design.
#
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, 

    Computational Science Group, Department of Mathematics, 
    University of Puerto Rico at Humacao 
    <jse@math.uprh.edu>.

    (On last names: Most hispedotc people, Puerto Ricans included, use two surnames; 
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

from PyQt5 import QtGui, QtCore
from ui_pedotEditor import Ui_PEDOTEditor

# find CNT class and import
import sys, os
if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../')
#import NanoCAD_conf
from conf.Wolffia_conf import NANOCAD_MOLECULES
from lib.chemicalGraph.molecule.polymer.PEDOT import PEDOT
from lib.chemicalGraph.Mixture import Mixture
from MixtureViewer import MixtureViewer
from History import History

class PEDOTBuilder(QtGui.QDialog):
	# Class Fields:
	# ui: stores reference tu user interface
	# files: [string, string], PDF and PSF filenames
	# tubes: Mixture, a Tube
	# tubePreview: MixtureViewer

	def __init__(self, appState, parent=None, settings=None):
		super(PEDOTBuilder, self).__init__(parent, modal=1)

		self.state = appState

		self.ui = Ui_PEDOTEditor()
		self.ui.setupUi(self)

		image = os.path.dirname(os.path.realpath(__file__))+"/PEDOT.png"
		self.ui.PEDOTdiagram.setPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8(image)))

		self.history = History()
		self.isAdded = False

		self.pedotPreview = MixtureViewer(self.history, self, None)
		self.ui.viewerLayout.addWidget(self.pedotPreview)
		if settings != None:
			self.pedotPreview.setHighResolution(settings.highResolution)
			self.pedotPreview.setLabeling(settings.showLabels)
			self.pedotPreview.showAxes(settings.showAxes)
			self.pedotPreview.showHelp(settings.showHelp)

		self.files = None
		self.slideFactor = 50
		self.ui.mSpinBox.setValue(1)
		self.ui.nSpinBox.setValue(1)

		if __name__ != '__main__':
			self.ui.saveButton.setHidden(True)

		self.generatePolymer()
		self.pedotPreview.update()


	def generatePolymer(self):
		n          = self.ui.nSpinBox.value()
		m          = self.ui.mSpinBox.value()
		monomers   = self.ui.monomersSpinBox.value()
		self.pedot  = Mixture()

		self.history.currentState().reset()
		self.history.currentState().addMolecule(PEDOT(n, m, monomers))
		self.pedotPreview.update()

	def getMixture(self):
		return self.history.currentState().getMixture()

	# Manages signals
	def on_horizontalSlider_valueChanged(self,pos):
		self.ui.monomersSpinBox.setValue(pos/self.slideFactor)

	def on_monomersSpinBox_valueChanged(self,val):
		val = int(val)
		if val < 100:
			self.slideFactor = 50
		elif val < 1000:
			self.slideFactor = 5
		else:
			self.slideFactor = 1
		self.ui.horizontalSlider.setValue(val*self.slideFactor)
		self.generatePolymer()

	def on_mSpinBox_valueChanged(self,val):
		if self.ui.nSpinBox.value() == 0 and self.ui.mSpinBox.value() == 0:
			self.ui.mSpinBox.setValue(1)
		self.generatePolymer()

	def on_nSpinBox_valueChanged(self,val):
		if self.ui.nSpinBox.value() == 0 and self.ui.mSpinBox.value() == 0:
			self.ui.nSpinBox.setValue(1)
		self.generatePolymer()

	'''
	def on_emeraldineButton_toggled(self, selected):
		if selected:
			self.ui.mSpinBox.setValue(0)
			self.ui.mSpinBox.setDisabled(True)
			self.ui.nSpinBox.setEnabled(True)
			if self.ui.nSpinBox.value() == 0:
				self.ui.nSpinBox.setValue(1)

	def on_leucoemeraldineButton_toggled(self, selected):
		if selected:
			self.ui.nSpinBox.setValue(0)
			self.ui.nSpinBox.setDisabled(True)
			self.ui.mSpinBox.setEnabled(True)
			if self.ui.mSpinBox.value() == 0:
				self.ui.mSpinBox.setValue(1)
	'''

	def on_mixedButton_toggled(self, selected):
		if selected:
			#self.ui.nSpinBox.setValue(0)
			self.ui.nSpinBox.setEnabled(True)
			self.ui.mSpinBox.setEnabled(True)
			if self.ui.mSpinBox.value() == 0:
				self.ui.mSpinBox.setValue(1)
			if self.ui.nSpinBox.value() == 0:
				self.ui.nSpinBox.setValue(1)
	@QtCore.pyqtSlot()
	def on_OKButton_pressed(self):
		#print "on_OKButton_pressed"
		self.generatePolymer()
		self.isAdded = True
		self.close()

	'''
	# Hiding this, no longer in use. ~Radames
	@QtCore.pyqtSlot()
	def on_saveButton_pressed(self):
		from PEDOTSaveDialog import PEDOTSaveDialog

		# generate tube
		self.generatePolymer()

		ntDialog = PEDOTSaveDialog(self.pedot,files=self.files, parent=self)
		ntDialog.show()
		ntDialog.exec_()
		self.files = ntDialog.getFileNames()
		print self.files

	@QtCore.pyqtSlot()
	def on_previewButton_pressed(self):
		self.generatePolymer()
	'''

	@QtCore.pyqtSlot()
	def on_cancelButton_pressed(self):
		self.close()

	@QtCore.pyqtSlot()
	def closeEvent(self, e):
		if not self.isAdded:
			self.history.currentState().reset()


#---------------------------------------------------------------------------
if __name__ == '__main__':
	import sys
	from History import NanoCADState
	app = QtGui.QApplication(sys.argv)
	load_gui = PEDOTBuilder(NanoCADState())
	load_gui.show()
	sys.exit(app.exec_())

