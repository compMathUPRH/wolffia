# -*- coding: utf-8 -*-
'''
Created on Jun 29, 2012

'''
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
from collections import OrderedDict
from conf.Wolffia_conf import WOLFFIA_GRAPHICS

class PreviewerToolbar(QtGui.QToolBar):
    '''
    classdocs
    '''
    def __init__(self, previewer = None, parent = None, settings = None):
        '''
        Constructor
        '''
        super(PreviewerToolbar, self).__init__(parent)
        
        self.previewer = previewer
        self.wolffia = parent
        self.settings = settings
        
        #These two lists contain the settings buttons and the mode buttons.
        self.modeButtons = OrderedDict([("rotate" , ""), ("move", ""), ("zoom", ""), ("select", ""), ("separator", ""), ("pore", ""), ("square", ""), ("makeBonds", "")])
        self.settingsButtons = OrderedDict([("resolution" , ""), ("labels", ""), ("axis", ""), ("helpToggle", "")])
        
        #Esta porqueria no acepta QSpacerItem, tuve que usar QLabel para que actue como spacer
        stretchWidgetOne = QtGui.QLabel(self)
        stretchWidgetTwo = QtGui.QLabel(self)
        stretchWidgetOne.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        stretchWidgetTwo.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        
        self.addWidget(stretchWidgetOne)
        #loop initiates the QPushButtons, adds it to the QToolbar and connects the signal triggered 
        #the different slots. 
        for actions in list(self.modeButtons.keys()):
            if actions == "separator":
                self.addSeparator()
            else:
                self.modeButtons[actions] = QtGui.QPushButton(self)
                self.modeButtons[actions].setIcon(QtGui.QIcon(str(WOLFFIA_GRAPHICS) + actions + ".png"))
                self.addWidget(self.modeButtons[actions])
                self.modeButtons[actions].setCheckable(True)
                self.modeButtons[actions].pressed.connect(getattr(self, actions))
                self.modeButtons[actions].setStyleSheet(
                              "QPushButton { background-color: #EDECEB; border-radius: 15px;  border: 5px solid #B3DEAF; padding: 5px; }"
                              "QPushButton:checked { background-color: #009900 }"
                              )

        
        #tooltips
        self.modeButtons["rotate"].setToolTip("Rotate")
        self.modeButtons["select"].setToolTip("Select molecules")
        self.modeButtons["move"].setToolTip("Move")
        self.modeButtons["pore"].setToolTip("Create a pore")
        self.modeButtons["square"].setToolTip("Squares")
        self.modeButtons["makeBonds"].setToolTip("Connect atoms")
        self.modeButtons["zoom"].setToolTip("Zoom")
        
        self.modeButtons["rotate"].setChecked(True)
        self.addWidget(stretchWidgetTwo)
        self.rotate()

    def rotate(self):
        '''
        
        '''
        self.clearChecked()
        self.modeButtons["rotate"].setDown(True)
        
        self.previewer.setMode("rotate")
        
    def move(self):
        '''
        
        '''
        self.clearChecked()
        self.modeButtons["move"].setDown(True)
        self.previewer.setMode("move")
        
    def select(self):
        '''
        
        '''
        self.clearChecked()
        self.modeButtons["select"].setDown(True)
        self.previewer.setMode("select")
        
    def pore(self):
        '''
        
        '''
        if self.wolffia.simRunning:
            QtGui.QMessageBox.information(self, "Wolffia's message", "Can't do that.", QtGui.QMessageBox.Ok)
        else:
            self.clearChecked()
            self.modeButtons["pore"].setDown(True)
            self.previewer.setMode("pore")
        
    def makeBonds(self):
        '''
        
        '''
        if self.wolffia.simRunning:
            QtGui.QMessageBox.information(self, "Wolffia's message", "Can't do that.", QtGui.QMessageBox.Ok)
        else:
            self.clearChecked()
            self.modeButtons["makeBonds"].setDown(True)
            self.previewer.setMode("makeBonds")
        
    def square(self):
        '''
        
        '''
        if self.wolffia.simRunning:
            QtGui.QMessageBox.information(self, "Wolffia's message", "Can't do that.", QtGui.QMessageBox.Ok)
        else:     
            self.clearChecked()
            self.modeButtons["square"].setDown(True)
            self.previewer.setMode("square")    
    
    def zoom(self):
        '''
        
        '''
        self.clearChecked()
        self.modeButtons["zoom"].setDown(True)
        
        self.previewer.setMode("zoom")
        
    def clearChecked(self):
        '''
        
        '''
        for actions in list(self.modeButtons.keys()):
            if actions != "separator":
                self.modeButtons[actions].setChecked(False)

        