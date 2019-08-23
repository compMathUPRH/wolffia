#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#  GrapheneBuilder.py
#  Version 0.1, October, 2011
#
#  Single-wall Graphene builder.
#  Produces PDF and PSF files for molecular dynamics simulations.
#
#  Authors:
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
from ui_grapheneEditor import Ui_GrapheneEditor

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')

from conf.Wolffia_conf import WOLFFIA_STYLESHEET
from lib.chemicalGraph.molecule.allotrope.Graphene import Graphene
from lib.chemicalGraph.Mixture import Mixture
from interface.main.MixtureViewer import MixtureViewer
from interface.main.History import History, NanoCADState

#-------------------------------------------------------------------------------

class GrapheneBuilder(QtGui.QDialog):
	"""
	Wolffia's dialogue box to produce graphenes
	"""
	# Class Fields:
	# ui: stores reference tu user interface
	# files: [string, string], PDB and PSF filenames
	# graphene: Mixture, a Graphene
	# graphenePreview: MixtureViewer

	def __init__(self, parent=None, settings=None):
		"""
		Constructor for graphene editor.
		
		Parameters used:
		parent  :	Window, widget or object that was used to call this dialogue
		settings:	Settings
		"""

		super(GrapheneBuilder, self).__init__(parent, modal=1)

		self.ui					= Ui_GrapheneEditor()
		self.isAdded			= False
		self.settings			= settings
		self.history			= History()
		self.graphenePreview	= MixtureViewer(self.history, self, None)
		self.files				= None

		self.ui.setupUi					(self)
		self.ui.viewerLayout.addWidget	(self.graphenePreview)
		self.generateGraphene			()

		if self.settings:
			self.graphenePreview.setHighResolution	(self.settings.highResolution)
			self.graphenePreview.setLabeling		(self.settings.showLabels)
			self.graphenePreview.showAxes			(self.settings.showAxes)
			self.graphenePreview.showHelp			(self.settings.showHelp)
			self.ui.OKButton.setText				("OK")

		try:
			self.setStyleSheet(open(WOLFFIA_STYLESHEET,'r').read())
		except:
			print("WARNING: Could not read style specifications")
			
		self.graphenePreview.update()

	def generateGraphene(self):
		n = self.ui.nSpinBox.value()
		m = self.ui.mSpinBox.value()
		grapheneLength = self.ui.grapheneLengthSpinBox.value()
		self.history.currentState().reset()
		self.history.currentState().addMolecule(Graphene(n, m, grapheneLength))
		self.graphenePreview.update()

	def getMixture(self):
		return self.history.currentState().getMixture()


	# Manages signals
	def on_horizontalSlider_valueChanged(self,pos):
		self.ui.grapheneLengthSpinBox.setValue(pos/10.)

	def on_grapheneLengthSpinBox_valueChanged(self,val):
		self.ui.horizontalSlider.setValue(int(float(val)*10))


	@QtCore.pyqtSlot()
	def on_OKButton_pressed(self):
		if self.settings:
			self.generateGraphene()
			#self.state.addMixture(self.graphene)
			self.isAdded = True
			self.close()
		else:
			from .GrapheneSaveDialog import GrapheneSaveDialog
			self.generateGraphene()
			ntDialog = GrapheneSaveDialog(self.graphene,files=self.files, parent=self)
			ntDialog.show()
			ntDialog.exec_()
			self.files = ntDialog.getFileNames()
			print(self.files)

	@QtCore.pyqtSlot()
	def on_previewButton_pressed(self):
		self.generateGraphene()

	@QtCore.pyqtSlot()
	def on_cancelButton_pressed(self):
		self.close()

	def closeEvent(self, e):
		if not self.isAdded:
			self.history.currentState().updateMixture(Mixture())

#-------------------------------------------------------------------------------
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	# Hay que arreglar esto!! Metodo NanoCADState ya no existe. ~ Radames
	load_gui = GrapheneBuilder(NanoCADState())
	load_gui.show()
	sys.exit(app.exec_())
