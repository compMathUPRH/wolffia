#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------
#  load.py
#  Version 0.2, Abril, 2012
"""
    Copyright 2011, 2012: Melissa  López Serrano, 

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
import sys,os

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')

from ui_AboutLoad import Ui_aboutLoad


class AboutLoad(QtGui.QDialog):
	def __init__(self, parent=None):
		super(AboutLoad, self).__init__(parent,modal=1)
			
		self.ui = Ui_aboutLoad()
		self.ui.setupUi(self)
	

	def on_okButton_pressed(self):
		self.close()


















