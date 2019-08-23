# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  SettingsDialog.py
#  Version 0.1, January, 2012
#
#  Set default settings.
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

import os, sys
from PyQt5 import QtGui
from ui_SettingsDialog import Ui_settingsDialog

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import *
from .WFileDialogs import WDirectoryDialog, WFileDialog
from Wolffia_conf import WOLFFIA_DIR, _WOLFFIA_OS, WOLFFIA_VERSION, WOLFFIA_DEFAULT_MIXTURE_NAME #@UnresolvedImport
from subprocess import check_output

class SettingsDialog(QtGui.QDialog):
    '''
    Class Fields:
    _projectName
    _defaultDir

    '''

    def __init__(self, settings, parent=None):
        '''
        
        :param settings:
        :param parent:
        '''
        super(SettingsDialog, self).__init__(parent, modal = 1)

        self.settings = settings
        self.wolffia = parent
        self.workingFolder = settings.workingFolder
        #oldFolder = self.workingFolder
        self.ui = Ui_settingsDialog()
        self.ui.setupUi(self)
        
        #initialize widgets
        self.ui.highResolutionButton.blockSignals(True)
        self.ui.solventHighResolutionButton.blockSignals(True)
        
        self.ui.highResolutionButton.setChecked(self.settings.highResolution)
        self.ui.solventHighResolutionButton.setChecked(self.settings.solventHighResolution)
        #self.ui.highResolutionButton.setChecked(self.settings.solventHighResolution)
        self.ui.axesCheckBox.setChecked(self.settings.showAxes)
        self.ui.labelsCheckBox.setChecked(self.settings.showLabels)
        self.ui.defDirLine.setText(self.settings.workingFolder)
        self.ui.viewHelpcheckBox.setChecked(self.settings.showHelp)
        self.ui.namD.setChecked(self.settings.MDPackage == "NAMD")
        self.ui.gromacs.setChecked(self.settings.MDPackage == "GROMACS")
        self.ui.resetButton.setIcon(QtGui.QIcon().fromTheme("edit-clear"))
        self.ui.gromacs.setEnabled(False)
        self.ui.namD.setEnabled(False)
        self.ui.defMDPlaceLabel.setText(self.settings.namdLocation)
        self.ui.version.setText(WOLFFIA_VERSION)
        
        self.ui.highResolutionButton.blockSignals(False)
        self.ui.solventHighResolutionButton.blockSignals(False)

#===============================================================================
#        
#    #---------------------------------------------------------------
#    def setProjectName(self, name):
#        self._projectName = name
#        self.state.setMixtureName(self._projectName)
#        self.update()
# 
#    #---------------------------------------------------------------
#    def setDefaultDir(self, default):
#        self._defaultDir = default
#        self.state.setBuildDirectory(self._defaultDir)
#        self.update()
#        
#    #- --------------------------------------------------------------
#    def getProjectName(self):
#        return self._projectName
# 
#    #---------------------------------------------------------------
#    def getDefaultDir(self):
#        return self._defaultDir 
# 
#    #---------------------------------------------------------------
#===============================================================================
    def update(self):
        """
            Updates the labels to show the current default dir and the mixture name
        """
        #self.ui.projectLine.setText(self.state.getMixtureName())
        self.ui.defDirLine.setText(self.state.getBuildDirectory())

    #---------------------------------------------------------------
    def on_highResolutionButton_stateChanged(self, check):
        '''
        
        :param check:
        '''
        self.settings.setHighResolution(check)
        self.wolffia.settingsChanged()

    #---------------------------------------------------------------
    def on_solventHighResolutionButton_stateChanged(self, check):
        '''
        
        :param check:
        '''
        self.settings.setSolventHighResolution(check)
        self.wolffia.settingsChanged()

    #---------------------------------------------------------------
    def on_labelsCheckBox_stateChanged(self,check):
        '''
        
        :param check:
        '''
        self.settings.setShowLabels(check)
        self.wolffia.settingsChanged()
        
    #--------------------------------------------------------------
    def on_axesCheckBox_stateChanged(self,check):
        '''
        
        :param check:
        '''
        self.settings.setShowAxes(check)
        self.wolffia.settingsChanged()

    #--------------------------------------------------------------
    def on_viewHelpcheckBox_stateChanged(self,check):
        '''
        
        :param check:
        '''
        self.settings.setShowHelp(check)
        self.wolffia.settingsChanged()
            
    #---------------------------------------------------------------
    def on_defDirButton_pressed(self):
        """
            Shows the QFile Dialog to change the default directory.
        """
        d = WDirectoryDialog(self, 'Select Directory', self.workingFolder)
        if d.accepted():
            #print "got here, ", d.path()
            self.ui.defDirLine.setText(d.path() + "/")
            
    #---------------------------------------------------------------
    def on_defMDPlaceButton_pressed(self):
        """
            Shows the QFile Dialog to change the default directory.
        """
        d = WFileDialog(self, 'Select MD executable', self.workingFolder)
        if d.accepted() and d.fullFilename() != self.ui.defMDPlaceLabel.text():
            self.ui.defMDPlaceLabel.setText(d.fullFilename())
    #--------------------------------------------------------------
    def on_resetButton_pressed(self):
        """
            Resets the mixture to the default directory and name
        """
        self.ui.defDirLine.setText(WOLFFIA_DIR)
        
    #--------------------------------------------------------------
    def on_resetMDButton_pressed(self):
        '''
            Uses the command WHEREIS on Linux and WHERE on Windows to search for the NAMD2 binary file.
        '''
        if _WOLFFIA_OS == "Windows":
            self.ui.defMDPlaceLabel.setText(check_output(["where", "namd2"]).split(' ')[1].rstrip('\n'))
        else:
            self.ui.defMDPlaceLabel.setText(check_output(["whereis", "namd2"]).split(' ')[1].rstrip('\n'))
    #--------------------------------------------------------------
        
    def on_buttonBox_rejected(self):
        '''
        
        '''
        #print "on_buttonBox_rejected"
        self.close()

    #--------------------------------------------------------------
    def on_buttonBox_accepted(self):
        '''
        
        '''        
        if self.ui.namD.isChecked():
            self.MDPackage = "NAMD"
            self.settings.namdLocation = str(self.ui.defMDPlaceLabel.text())
            print("SettingsDialog.on_buttonBox_accepted, namdLocation:", self.settings.namdLocation)
        if self.ui.gromacs.isChecked():
            self.MDPackage = "GROMACS"

        if self.settings.workingFolder != self.ui.defDirLine.text():
            #self.wolffia.reset()
            self.settings.setWorkingDirectory(str(self.ui.defDirLine.text()))
            self.wolffia.mixtureDialog()
            #self.settings.setCurrentMixture(WOLFFIA_DEFAULT_MIXTURE_NAME)
            print(self.settings.workingFolder)
            print(self.settings.currentMixtureLocation())
            self.close()

        self.close()
