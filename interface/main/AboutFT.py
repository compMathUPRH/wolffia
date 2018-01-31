#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------
#  load.py
#  Version 0.2, Abril, 2012
#
#  Description: load.py creates a QDialog to load psf and pdb files 
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, Frances  Martínez Miranda, 

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


from PyQt4 import QtGui
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from ui_AboutFT import Ui_layAboutFt
#from conf.Wolffia_conf import WOLFFIA_GRAPHICS, WOLFFIA_STYLESHEET


class AboutFT(QtGui.QDialog):
	def __init__(self, parent=None):
		super(AboutFT, self).__init__(parent,modal=1)
		
		self.ui = Ui_layAboutFt()
		self.ui.setupUi(self)
		
		self.ui.saveBEx.setIcon(QtGui.QIcon().fromTheme("media-floppy"))
		self.ui.loadBEx.setIcon(QtGui.QIcon().fromTheme("document-open"))
		self.ui.questBEx.setIcon(QtGui.QIcon().fromTheme("help-faq"))
	
	def on_saveFB_pressed(self):
		self.ui.aboutSK.setCurrentIndex (1)
	
	def on_loadFB_pressed(self):
		self.ui.aboutSK.setCurrentIndex (2)
	
	
	def on_forceTB_pressed(self):
		self.ui.aboutSK.setCurrentIndex (4)
	
	
	def on_okB_pressed(self):
		self.close()
	
