# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Carlos J.  Cortés Martínez, 

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

import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import *


class StructureManagerWidget(QtGui.QTreeWidget):   
	def __init__(self, parent=None):
		super(StructureManagerWidget, self).__init__(parent)


	#list all molecules in the Structure Manager
	def insertMixture(self, mixture):
		start = time.clock()
		self.clear()
		for molName in mixture:
			print("insertMixture", molName)
			row = QtGui.QTreeWidgetItem(self)
			self.addTopLevelItem(row)

			showCheckbox = QtGui.QCheckBox()
			showCheckbox.setChecked(True)
			row.setText(0, str(1))
			self.setItemWidget(row, 1, showCheckbox)   	#!!!!
			row.setText(2, mixture.getMolecule(molName).molname())
			row.setText(3, str(mixture.getMolecule(molName).order()))    	 
		stop = time.clock()
		print("insertMixture time",stop-start)


	#activates the Structure Catalog
	def itemActivated(self, item, col):  
			#print item.text(col)
			pass

