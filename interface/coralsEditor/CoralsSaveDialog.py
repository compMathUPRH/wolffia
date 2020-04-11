# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  GrapheneSaveDialog.py
#  Version 0.1, October, 2011
#
#  Part of the single-wall graphene builder.
#  Gets PDF and PSF files names.
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Melissa  López Serrano, 

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

import os, sys
from PyQt4 import QtGui, QtCore
from ui_coralsSaveDialog import Ui_CoralsSaveDialog

# find CNT class and import
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from Wolffia_conf import NANOCAD_MOLECULES

from Graphene import Graphene


class CoralsSaveDialog(QtGui.QDialog):
	# Class Fields:
	# ui: stores reference tu user interface
	# pdbFile: string, PDF filename
	# graphene: Mixture, a Graphene

	def __init__(self,graphene,files=None, parent=None):
		super(CoralsSaveDialog, self).__init__(parent, modal = 1)

		self.ui = Ui_CoralsSaveDialog()
		self.ui.setupUi(self)

		if files != None:
			self.ui.pdbFilename.setText(files[0])
			self.ui.psfFilename.setText(files[1])
		self.graphene = graphene

	def getFileNames(self):
		if self.ui.pdbFilename.text() == '':
			return None
		else:
			return [str(self.ui.pdbFilename.text()), str(self.ui.psfFilename.text())]

	@QtCore.pyqtSlot()
	def on_okButton_pressed(self):
		pdbFile = str(self.ui.pdbFilename.text())
		if pdbFile == '':
			QtGui.QMessageBox.warning(self,
                                "Error",
                                "You must enter at least a PDF filename.")
		else:
			#print "CNT(", self.n, ", ", self.m, ", ", self.grapheneLength 
			#graphene = Graphene(self.n, self.m, self.grapheneLength)
			self.graphene.writePDB(pdbFile)
			psfFile = str(self.ui.psfFilename.text())
			if psfFile != '':
				self.graphene.writePSF(psfFile)
			self.close()

	@QtCore.pyqtSlot()
	def on_browsePDBButton_pressed(self):
		fn = str(QtGui.QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(),"PDB (*.pdb *.PDB)"))
		if fn.find(".pdb") != len(fn) - 4 and fn.find(".PDB") != len(fn) - 4 :
			fn += ".pdb"
		self.ui.pdbFilename.setText(fn)

	@QtCore.pyqtSlot()
	def on_browsePSFButton_pressed(self):
		fn = str(QtGui.QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(),"PSF (*.psf *.PSF)"))
		if fn.find(".psf") != len(fn) - 4 and fn.find(".PSF") != len(fn) - 4 :
			fn += ".psf"
		self.ui.psfFilename.setText(fn)

	@QtCore.pyqtSlot()
	def on_cancelButton_pressed(self):
		#self.ui.pdbFilename.setText('')
		#self.ui.psfFilename.setText('')
		self.close()

