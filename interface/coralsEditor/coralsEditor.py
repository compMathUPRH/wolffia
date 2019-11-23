#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#  GrapheneBuilder.py
#  Version 0.1, October, 2011
#
#  CORALS builder.
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
#from ui_grapheneEditor import Ui_GrapheneEditor
from ui_coralsEditor import Ui_CoralsEditor

from lib.chemicalGraph.molecule.polymer.Cellulose import Cellulose
from lib.chemicalGraph.molecule.solvent.PABA import PABA_Pentane
from lib.chemicalGraph.molecule.element.Element import C
from lib.chemicalGraph.Mixture import Mixture
import random
random.seed()
from math import ceil

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')

from conf.Wolffia_conf import WOLFFIA_STYLESHEET
from lib.chemicalGraph.molecule.allotrope.Graphene import Graphene
from lib.chemicalGraph.Mixture import Mixture
from interface.main.MixtureViewer import MixtureViewer
from interface.main.History import History, NanoCADState

#-------------------------------------------------------------------------------

class CoralsBuilder(QtGui.QDialog):
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

		super(CoralsBuilder, self).__init__(parent, modal=1)

		self.ui				= Ui_CoralsEditor()
		self.isAdded			= False
		self.settings			= settings
		self.history			= History()
		self.coralsPreview              = MixtureViewer(self.history, self, None)
		self.files			= None

		self.ui.setupUi	    		(self)
		self.ui.viewerLayout.addWidget	(self.coralsPreview)
		self.generateCorals()

		if self.settings:
			self.coralsPreview.setHighResolution	(self.settings.highResolution)
			self.coralsPreview.setLabeling		(self.settings.showLabels)
			self.coralsPreview.showAxes		(self.settings.showAxes)
			self.coralsPreview.showHelp		(self.settings.showHelp)
			self.ui.OKButton.setText		("OK")

		try:
			self.setStyleSheet(open(WOLFFIA_STYLESHEET,'r').read())
		except:
			print "WARNING: Could not read style specifications"
			
		self.coralsPreview.update()

	def generateCorals(self):
		Y_dim = self.ui.ydimensionsSpinBox.value()
		X_dim = self.ui.xdimensionsSpinBox.value()
                Z_dim = 1

		coralsRadius = self.ui.coralsRadiusSpinBox.value()
                dx = self.ui.surfaceDistanceSpinBox_3.value()
                dy = self.ui.surfaceDistanceSpinBox_3.value()
                dz = self.ui.surfaceDistanceSpinBox_3.value()
		self.history.currentState().reset()

		#self.history.currentState().addMolecule(Graphene(n, m, coralsRadius))

                # generate corals


                # Define mixture
                corals_mixture = Mixture()

                for i in range(X_dim):
                    for j in range(Y_dim):
                        for k in range(Z_dim):
                            atom= C()
                            #atom.moveby([dx * i, dy * j, dz * k])
                            if j % 2 == 0:
                                atom.moveby([dx * i, dy * j, dz * k])
                            else:
                                atom.moveby([dx * i + dx/2., dy * j, dz * k])
                            corals_mixture.add(atom)

                # Get the coordinates and the center of the atom
                coorList = list()
                for m in corals_mixture.moleculeGenerator():
                    for atom in m:
                        coorList.append(m.getAtomAttributes(atom).getCoord())

                x = 0
                y = 0
                for value in coorList:
                    x += value[0]
                    y += value[1]

                print "Average Center of the Circle"
                center = [x/len(coorList), y/len(coorList)]

                # Ratio value
                #ratio = 30

                # check if value is inside Circle
                inside_atoms = list()
                for atom in coorList:
                    # center atoms
                    if (atom[0]-center[0])**2 + (atom[1]-center[1])**2 <= coralsRadius**2:
                        inside_atoms.append(atom)
                    # right upper corner
                    elif (atom[0]- (X_dim * dx))**2 + (atom[1]- (Y_dim * dy))**2 <= coralsRadius**2:
                        inside_atoms.append(atom)
                    # origin case
                    elif (atom[0]- 0.0)**2 + (atom[1]- 0.0)**2 <= coralsRadius**2:
                        inside_atoms.append(atom)
                    # left upper corner
                    elif (atom[0]- 0.0)**2 + (atom[1]- (Y_dim * dy))**2 <= coralsRadius**2:
                        inside_atoms.append(atom)
                    # right lower corner
                    elif (atom[0]- (X_dim * dx))**2 + (atom[1]- 0.0)**2 <= coralsRadius**2:
                        inside_atoms.append(atom)

                #adding PABA
                paba = PABA_Pentane()
                paba.rename("PABApentane1")
                paba.removeAtom(139) #remove hydrogen
                paba.removeAtom(69)  #remove oxygen
                paba.moveBy([-x for x in paba.center()])
                paba.rotateDeg(90.0, 0.0, 0.0)
                paba.moveBy([0.0,0.0,6.0])
                chrgToSubstract = -0.4181  # computed with Wolffia
                chrgToSubstractO200 = -0.0181  # computed with Wolffia

                for i in inside_atoms:
                    newPABA = paba.copy()
                    newPABA.moveBy(i)
                    corals_mixture.add(newPABA)

		self.history.currentState().addMixture(corals_mixture)
		self.coralsPreview.update()

	def getMixture(self):
		return self.history.currentState().getMixture()


	# Manages signals
	#def on_horizontalSlider_valueChanged(self,pos):
	#	self.ui.coralsRadiusSpinBox.setValue(pos/10.)

	#def on_coralsRadiusSpinBox_valueChanged(self,val):
	#	self.ui.horizontalSlider.setValue(int(val))


	@QtCore.pyqtSlot()
	def on_OKButton_pressed(self):
		if self.settings:
			self.generateCorals()
			#self.state.addMixture(self.graphene)
			self.isAdded = True
			self.close()
		else:
			from CoralsSaveDialog import CoralsSaveDialog
			self.generateCorals()
			ntDialog = CoralsSaveDialog(self.graphene,files=self.files, parent=self)
			ntDialog.show()
			ntDialog.exec_()
			self.files = ntDialog.getFileNames()
			print self.files

	@QtCore.pyqtSlot()
	def on_previewButton_pressed(self):
		self.generateCorals()

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
	load_gui = CoralsBuilder(NanoCADState())
	load_gui.show()
	sys.exit(app.exec_())
