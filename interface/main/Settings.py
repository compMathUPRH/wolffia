# -*- coding: utf-8 -*-
'''
Created on Jun 12, 2012

@author: jse
'''

#  Wolffia settings.
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

# load configuration info
from conf.Wolffia_conf import WOLFFIA_DIR, WOLFFIA_DEFAULT_MIXTURE_NAME, WOLFFIA_STYLESHEET, WOLFFIA_VERSION, _WOLFFIA_OS #@UnresolvedImport
from subprocess import check_output
import os
from PyQt5 import QtCore, QtGui, QtWidgets


class Settings(object):
    '''
    Wolffia settings
    '''


    def __init__(self, filename=None):
        '''
        Constructor
        '''
        self.wolffiaVersion         = WOLFFIA_VERSION
        self.workingFolder          = WOLFFIA_DIR
        self.MDPackage              = "NAMD"
        self.highResolution         = True
        self.solventHighResolution  = False
        self.showAxes               = True
        self.showLabels             = False
        self.showHelp               = True
        self.skin                   = WOLFFIA_STYLESHEET
        self.simulationFolder       = WOLFFIA_DEFAULT_MIXTURE_NAME
        self.namdLocation           = ""

        if not filename == None:
            self.load(filename)

    def checkForNAMD(self):
        '''
        Program checks if it can find the NAMD2 executable in the path.
        This is only done once!
        '''

        if _WOLFFIA_OS == "Windows":
            self.namdLocation       = check_output(["where", "namd2"])
            if self.namdLocation == "":
                print("NAMD not found, proceed with caution.")
        else:
            try:
                self.namdLocation      = check_output(["whereis", "namd2"]).split(' ')[1].rstrip('\n')
                print("Settings.__init__(), NAMD found at ", self.namdLocation)
            except:
                self.namdLocation = ""
                print("NAMD not found, proceed with caution.\nPlease specify the executable in the settings window.")

    def reset(self):
        '''
        Resets all of the variables to their defaults
        '''

        self.workingFolder   = WOLFFIA_DIR
        self.MDPackage       = "NAMD"
        self.highResolution  = True
        self.solventHighResolution  = False
        self.showAxes        = True
        self.showLabels      = False
        self.showHelp        = False
        self.skin            = WOLFFIA_STYLESHEET
        self.simulationFolder = WOLFFIA_DEFAULT_MIXTURE_NAME

    def setMixtureLocation(self, loc):
        #Sets current location

        self.simulationFolder  = loc
        #print "setSimulationLocation ", self.currentMixtureLocation()
        if not os.path.isdir(self.currentMixtureLocation()):
            os.makedirs(self.currentMixtureLocation())

    def currentSimulationName(self):
        try:
            return self.simulationFolder
        except:  # move to History.load()?
            self.simulationFolder = WOLFFIA_DEFAULT_MIXTURE_NAME
            return self.simulationFolder

    def setHighResolution(self, st):
        '''
        Sets HighResolution
        '''
        self.highResolution  = st


    def allInHighResolution(self):
        try:
            return self.highResolution
        except:
            self.highResolution(True)
            return True

    def setSolventHighResolution(self, st):
        '''
        Sets HighResolution
        '''
        self.solventHighResolution  = st


    def solventInHighResolution(self):
        try:
            return self.solventHighResolution
        except:
            self.setSolventHighResolution(False)
            return False

    def setShowHelp(self, st):
        '''
        Sets show help flag for mixture previewer.
        '''
        self.showHelp  = st

    def setShowAxes(self, st):
        '''
        Sets HighResolution
        '''
        self.showAxes  = st

    def setShowLabels(self, st):
        '''
        Sets HighResolution
        '''
        self.showLabels  = st


    def currentMixtureLocation(self):
        '''
        Returns folder with current mixture info
        '''
        try:
            locDir = self.workingFolder + "/" + self.simulationFolder + "/"
        except AttributeError:
            locDir = self.workingFolder + "/" + WOLFFIA_DEFAULT_MIXTURE_NAME + "/"
        if _WOLFFIA_OS == "Windows":
            locDir.replace('\\' , "\\\\")
        return locDir


    def setWorkingDirectory(self, path):
        self.workingFolder = path

    def getWorkingDirectory(self): return self.workingFolder

    #--------------------------------------------------------------------
    def load(self, filename=None):
        '''

        :param filename:
        '''
        if filename == None:
            filename = WOLFFIA_DIR + "/" + "defaultSettings.wfc"
            if not os.path.exists(filename):
                self.reset()
                self.save(filename)
                return

        import pickle as pickle #Tremenda aportación por carlos cortés


        try:
            f = open(filename, "r")
            self.__dict__ = pickle.load(f)
            f.close()
            #print "Settings.load self.wolffiaVerion ", self.wolffiaVersion
        except:
            from PyQt5 import QtGui
            gui = QtWidgets.QErrorMessage.qtHandler()
            QtWidgets.QErrorMessage.showMessage( gui, "Error: could not open configuration file "
                + filename + "." )

        # backward compatibility checks
        if not hasattr(self, "solventHighResolution"):  # introduced in v 1.0
            self.solventHighResolution = False


    #--------------------------------------------------------------------
    def save(self, filename=None):
        '''

        :param filename:
        '''

        if filename == None:
            filename = WOLFFIA_DIR + "/" + "defaultSettings.wfc"

        import pickle as pickle #Tremenda aportación por carlos cortés.

        f = open(filename, "w")
        pickle.dump(self.__dict__, f)
        f.close()

