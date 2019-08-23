# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  QClasses.py
#  Version 0.6, October, 2011
#
#  Includes classes that extend some QClasses like QComboBox and such
#
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

from PyQt5 import QtGui

#=================================================================================================

class ComboBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        super(ComboBox, self).__init__()
        
    def value(self):
        return self.currentIndex()

    def setValues(self, val):
        return self.setCurrentIndex(int(val))
#=================================================================================================

class CheckBox(QtGui.QCheckBox):
    def __init__(self, parent=None):
        super(CheckBox, self).__init__()

    def value(self):
        return self.isChecked()
    
    def setValues(self, val):
        self.setChecked(bool(val))
#==============================================================================================

class SpinBox(QtGui.QSpinBox):
    def __init__(self, parent=None):
        super(SpinBox, self).__init__()

    def setValues(self, val):
        self.setValue(int(val))

#================================================================================================

class DoubleSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, parent=None):
        super(DoubleSpinBox, self).__init__()

    def setValues(self, val):
        self.setValue(float(val))
#===============================================================================================

class OutputFileLabel(QtGui.QLabel):
    def __init__(self, parent=None):
        super(OutputFileLabel, self).__init__(parent)

    def mousePressEvent (self, ev):
        self.setText(str(QtGui.QFileDialog.getExistingDirectory(self, 'Choose the output directory')))
        
#=====================================================================================================

class InputFile(QtGui.QLabel):
    def __init__(self, parent=None):
        super(InputFile, self).__init__(parent)
        self.setText("default")

    def mousePressEvent (self, ev):
        self.setText(str(QtGui.QFileDialog.getOpenFileName(self, 'Choose the file')))

    def value(self):
        return self.text()
    
    def setValues(self, val):
        self.setText(val)    
    
