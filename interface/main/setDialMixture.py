#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------
#  setDialMixture.py
#  Version 0.2, Abril, 2012
#
#  Description: load.py creates a QDialog to load psf and pdb files 
#
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, Carlos J.  Cortés Martínez, Frances  Martínez Miranda, 

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
import sys, os, shutil
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import *
from ui_setDialMixture import Ui_laySetDialMixture

class setDialMixture(QtGui.QDialog):
    '''
    Class that extends QDialog used to give the user the option to choose between exporting
    the mixture to the new chosen directory or creating a new mixture in it.
    '''
    def __init__(self,settings,newFolder, parent=None):
        super(setDialMixture, self).__init__(parent,modal=1)
        
        self.settings = settings
        self.wolffia  = parent		
        self.ui = Ui_laySetDialMixture()
        self.ui.setupUi(self)
        self.newFolder = newFolder
        #self.previewer = MixtureViewer(self.history,None)
        self.ui.directoryName.setText(self.settings.workingFolder)
        
        #initialize widgets
        self.ui.copy.setChecked(True)
        #self.settings.workingFolder = self.ui.defDirLine.text()
        #self.ui.directoryName = self.settings.workingFolder

    #------------------------------------------------------------------

    def on_pushOK_pressed(self):
        '''
        If new mixture has been checked on the window, the program will change
        the working folder to the location specified before and create
        a new, fresh mixture "Unnamed" on it.
        
        If the user specifies to COPY the mixture to the new location,
        the it will be a simple process of moving the folder and all
        it's contents to that location and changing the working folder to it.
        In the special case that the user chose a place with a folder that has
        the same name as the mixture, the contents of the folder will be moved to
        that folder which shares the name of the mixture.
        '''
        if self.ui.newM.isChecked():
            self.wolffia.reset()
            self.settings.workingFolder = str(self.newFolder)
            self.settings.setCurrentMixture("Unnamed") #piensa en darle la opcion, de darle un nombre, al usuario
            print(self.settings.workingFolder)
            print(self.settings.currentMixtureLocation())
            self.close()
        else:
            mixN = self.settings.currentMixtureName 
            dirName = self.newFolder + mixN 
            print(self.newFolder, dirName)
            try:
                shutil.copytree(self.settings.workingFolder + mixN,dirName)
            except OSError:
                fileList = os.listdir(self.settings.workingFolder + mixN) #List of the current items inside the directory
                fileList = [self.settings.workingFolder + mixN+"/"+filename for filename in fileList] #list of every item inside the folder
                                
                #moves every file to the new folder
                for f in fileList:
                    shutil.copy2(str(f), dirName)
            self.settings.workingFolder = self.newFolder
            self.close()
         
        