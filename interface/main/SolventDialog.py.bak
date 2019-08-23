# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  SolventDialog.py
#  Version 0.1, February, 2012
#
#  Set parameteres for creating solvent box.
#  Uses (P + n2a / V2)(V- nb) = nRT
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
import os, sys
import math
from PyQt4 import QtGui, QtCore
from ui_SolventDialog import Ui_solventDialog

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import *

_AVOGRADRO_CONSTANT_ = 6.02214129e+23

class SolventDialog(QtGui.QDialog):
	'''
	Class Fields:
	_solvent
	_quantity
	_pressure
	_temp
	_vol
	_gasConst
	_attraction
	_molarConc

	'''
        # VDW_CONSTANTS from:  http://www2.ucdsb.on.ca/tiss/stretton/database/van_der_waals_constants.html
	VDW_CONSTANTS = {"Water":[5.537, 0.03049], "Chloroform":[15.34, 0.1019], "Chloroform (4 atoms)":[15.34, 0.1019], "Acetone":[16.02, 0.1124], "THF": [16.39,0.1082], "Argon": [5.537, 0.03049]}
    # DENSITY[solvent] = [Density in g/cm3, temperatue in K, molar mass]
	DENSITY = {"Water": [0.9970479,298.15,18.01528], "Chloroform":[1.483,298.15,119.38], "Chloroform (4 atoms)": [1.483,298.15,119.38], "Acetone": [0.786,293.15,58.08], "THF": [0.886,293.15,72.11], "Argon": [5.537, 0.03049,39.948], "Methanol": [0.791,293.15,32.04]}
	DI = 0
	TI = 1
	MI = 2
	
	def __init__(self, hist, vol, parent=None):
		super(SolventDialog, self).__init__(parent, modal = 1)		
		self.history 		=	hist

		#import widgets
		self.ui 			= 	Ui_solventDialog()
		self.ui.setupUi(self)

		#gets box volume from setup
		self.ui.volLineEdit.setText(str(vol/1000.0))

		#initialize 
		self._solvent 		=	str(self.ui.solventComboBox.currentText())
		#self._pressure		=	self.ui.pressureSpinner.value()				# atm
		#self._temp			=	self.ui.tempSpinner.value()					# Kelvin	
		self._vol			=	float(self.ui.volLineEdit.text())			# nm3
		self._gasConst		=	0.0821										# L*atm/mol*K
		self._attraction	=	self.VDW_CONSTANTS[self._solvent][0]		# bar*L^2/mol^2
		self._molarConc		=	self.VDW_CONSTANTS[self._solvent][1]		# L/mol
		self._density       =   self.DENSITY[self._solvent][self.DI]
		self.ui.densitySpinBox.setValue(self._density)
		self._keepAmmount   =   False
		self.allowMolBoxChange = True
		#self.on_pressureSpinner_valueChanged()
		#self.on_molBox_valueChanged()

	#----------------------------------------------------------------
	def getSolvent(self):
		return self._solvent

	#----------------------------------------------------------------
	def getAmount(self):
		return self._amount

	#----------------------------------------------------------------
	def getPressure(self):
		return self._pressure

	#----------------------------------------------------------------
	def getTemp(self):
		return self._temp

	#----------------------------------------------------------------
	def getVol(self):
		return self._vol

	#----------------------------------------------------------------
	def getGasConst(self):
		return self._gasConst

	#----------------------------------------------------------------
	def getAttraction(self):
		return self._attraction

	#----------------------------------------------------------------
	def getMolarConc(self):
		return self._molarConc

	def computeMolecules(self):
		import numpy
		global _AVOGRADRO_CONSTANT_
		D = self._density
		MM = self.DENSITY[self._solvent][self.MI]
		V = self._vol / 1E23
		if V == 0: return 0
		
		print "computeMolecules ", D,V,MM,D * V * MM * _AVOGRADRO_CONSTANT_
		n = int(D * V * MM * _AVOGRADRO_CONSTANT_)

		return n
		
	def computeDensity(self):
		"""
		Computes pressure from volume (V), temperature (T) and ammount of molecules (N).
		"""
		global _AVOGRADRO_CONSTANT_
		V = self._vol / 1E23
		MM = self.DENSITY[self._solvent][self.MI]
		print "computeDensity ", self._amount, V,MM, self._amount / V * MM * _AVOGRADRO_CONSTANT_
		return self._amount / V / MM / _AVOGRADRO_CONSTANT_
	


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
		self._solvent 		= 	str(self.ui.solventComboBox.currentText())
		self._attraction	=	self.VDW_CONSTANTS[self._solvent][0]		
		self._molarConc		=	self.VDW_CONSTANTS[self._solvent][1]	
		self.on_pressureSpinner_valueChanged()

	#----------------------------------------------------------------
	def on_cancelButton_pressed(self):
		self._amount = 0
		self.close()

	def closeEvent(self, e):
		if not self._keepAmmount: self._amount = 0
		print "closeEvent ", e.type()
		#super(SolventDialog, self).closeEvent(e)
	#----------------------------------------------------------------
	def on_okButton_pressed(self):
		self._keepAmmount = True
		self.close()

	#----------------------------------------------------------------		
	def wheelEvent(self, e):
		super(SolventDialog, self).wheelEvent(e)







