# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  Wolffia.py
#  First version, October, 2011
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, Carlos J.  Cortés Martínez, Frances  Martínez Miranda, 
    Radamés J.  Vega Alfaro, 
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

import sys,os
import logging

from PyQt4 import QtCore, QtGui
#from ui_Wolffia import Ui_Wolffia
#from NanoCADState import NanoCADState
# load configuration info
wolfiadir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(wolfiadir+'/../../')

from History import History
from Settings import Settings
from SettingsDialog import SettingsDialog
from interface.main.WFileDialogs import WFileNameDialog, WFileDialog
from interface.main.WTimer import WTimer

from ui_Wolffia import Ui_Wolffia
from MixtureBrowser import MixtureBrowser
from MixtureViewer import MixtureViewer 
from PreviewerToolbar import PreviewerToolbar
from EnergyPlot import EnergyPlot, KineticsPlot
from conf.Wolffia_conf import WOLFFIA_GRAPHICS, WOLFFIA_STYLESHEET, WOLFFIA_VERSION,C_MOLECULE_CATALOG


class Wolffia(QtGui.QMainWindow):
	__TITLE__ = "Wolffia " + WOLFFIA_VERSION
	def __init__(self, parent=None):
	    super(Wolffia, self).__init__(parent)
	    self.allowUpdate = True
	    self.sharedGlList = None
	    self.simRunning = False    #Keeps check if there's a simulation running

	
	    # Create and display the splash screen
	    splash_pix = QtGui.QPixmap(WOLFFIA_GRAPHICS+'/Wolffialogo.png')
	    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	    splash.setMask(splash_pix.mask())
	    splash.show()
	
	    # Create Wolffia's working directory
	        
	    self.settings = Settings()
	    self.cusMolDir = C_MOLECULE_CATALOG
	    

	    if os.path.isdir(self.settings.getSettingsDirectory()):
	        if os.path.exists(self.settings.getSettingsDirectory()):
	            if not os.path.exists(self.settings.getTempDirectory()):
	                os.makedirs(self.settings.getTempDirectory())
	                time.sleep(2)
	                        
	    else:
	        if os.path.exists(self.settings.workingFolder):
	            gui = QtGui.QErrorMessage.qtHandler()
	            QtGui.QErrorMessage.showMessage( gui, "Error: " + self.settings.workingFolder 
	                + " is not a folder.  Please rename and try again." )
	            splash.finish(self)
	            sys.exit(app.exec_())
	
	
	        else:
	            splash.showMessage(self.__TITLE__ + ": Creating Wolffia's working folder.")
	            os.makedirs(self.settings.workingFolder + "Temp")
	            time.sleep(2)   
	 
	    ''' no automatic loading at strtup since v1.5
	    self.settings.load()
	    
	    if not os.path.isdir(self.history.getCurrentState().getBuildDirectory()):
	        os.makedirs(self.history.getCurrentState().getBuildDirectory())
	    '''

	    if self.settings.namdLocation=="":        self.settings.checkForNAMD()
	    
	    #set logging
	    logging.basicConfig(filename=self.settings.getSettingsDirectory()+ '/wolffia.log',
	                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	                        level=logging.DEBUG)
	    self.logger = logging.getLogger(self.__class__.__name__)
	    
	    self.ui = Ui_Wolffia()
	    self.ui.setupUi(self)
	    self.setWindowTitle(self.__TITLE__)
	    dockTittle = QtGui.QWidget(self)
	    self.ui.dockWidget.setTitleBarWidget(dockTittle)
	
	    try:
	        self.setStyleSheet(open(WOLFFIA_STYLESHEET,'r').read())
	    except:
	        print "WARNING: Could not read style specifications"
	
	    splash.showMessage(self.__TITLE__ + ": Main window.")
	
	    # tool buttons
	    self.ui.resetButton.setIcon(QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "mixtureIcon.png"))
	    self.ui.saveWFY.setIcon(QtGui.QIcon().fromTheme("document-save"    ))
	    self.ui.actionSave_as.setIcon(QtGui.QIcon().fromTheme("document-save-as"   ))
	    self.ui.undoButton.setIcon(QtGui.QIcon().fromTheme("edit-undo",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "edit-undo.png")    ))
	    self.ui.redoButton.setIcon(QtGui.QIcon().fromTheme("edit-redo",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "edit-redo.png")    ))
	    self.ui.actionLoad.setIcon(QtGui.QIcon().fromTheme("folder",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "document-open.png")    ))
	    self.ui.recentMixture.setIcon(QtGui.QIcon().fromTheme("document-open-recent",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "document-open.png")    ))
	    #self.ui.actionMixture.setIcon(QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "mixtureIcon.png"))
	    #self.ui.actionLog.setIcon(QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "logIcon-off.png"))
	    self.ui.settingsButton.setIcon(QtGui.QIcon().fromTheme("emblem-system",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "emblem-system.png")    ))
	    self.ui.exitButton.setIcon(QtGui.QIcon().fromTheme("application-exit",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "application-exit.png")    ))

	    self.setSaveButtonEnabled(False)
	    self.setSaveAsButtonEnabled(False)

	
	    splash.showMessage(self.__TITLE__ + ": Restoring previous session.")
	    #self.history = History(self.ui.undoButton, self.ui.redoButton, loadFile=self.history.getCurrentState().getBuildDirectory() + self.settings.currentSimulationName() + ".wfy")
	    self.history = History(self.ui.undoButton, self.ui.redoButton)# no aotumatic load at startup since v1.5, loadDir=self.history.getCurrentState().getBuildDirectory(), loadFile=self.settings.currentSimulationName() + ".wfy")
	    self.history.push()
	    #print "Wolffia returning build ", self.history.getCurrentState().getBuildDirectory()
	    self.setTitle()
	    
	    #initialize viewer
	    self.previewer = MixtureViewer(self.history, parent=self)#, mixture=self.history.currentState().getMixture(), sharedGL=None)
	    self.previewerToolbar = PreviewerToolbar(self.previewer, self, self.settings)
	    self.ui.previewLayout.addWidget(self.previewer)
	    self.ui.previewLayout.addWidget(self.previewerToolbar)
	    self.previewer.setHighResolution(self.settings.highResolution,False)
	    self.previewer.setSolventHighResolution(self.settings.solventHighResolution,False)
	    self.previewer.setLabeling(self.settings.showLabels,False)
	    self.previewer.showAxes(self.settings.showAxes,False)
	    self.previewer.showHelp(self.settings.showHelp,False)
	
	    self.energyPlot1 = EnergyPlot("Potential")
	    self.energyPlot2 = EnergyPlot("Bond")
	    self.ui.energyPlotsLayout.addWidget(self.energyPlot1)
	    self.ui.energyPlotsLayout.addWidget(self.energyPlot2)
	
	    self.kineticsPlot1 = KineticsPlot("Temperature")
	    self.kineticsPlot2 = KineticsPlot("Pressure")
	    self.ui.kineticsPlotsLayuot.addWidget(self.kineticsPlot1)
	    self.ui.kineticsPlotsLayuot.addWidget(self.kineticsPlot2)
	
	    self.tabs = []
	
	    # create and show main GUI
	    splash.showMessage(self.__TITLE__ + ": Importing modules.")
	    from BuildTab import BuildTab
	    from SetupTab import SetupTab
	    from ForceTab import ForceTab
	    from SimTab import SimTab
	    from MinTab import MinTab
	    from LogWindow import LogWindow
	    from Analysis import Analysis
	
	
	    #self.logWindow = LogWindow(self, self.ui.actionLog)
	    self.logWindow = LogWindow(self.ui)
	
	    # tabs initialization
	    #print "Wolffia, self.previewer", self.previewer
	    splash.showMessage(self.__TITLE__ + ": Loading Build Tab.")
	    self.buildTab = BuildTab(self.history, self, self.previewer, self.settings)
	    self.ui.buildLayout.addWidget(self.buildTab)
	    self.previewer.setBuildTab(self.buildTab)
	    #print "Wolffia, self.previewer", self.previewer
	
	    splash.showMessage(self.__TITLE__ + ": Loading Set-up Tab.")
	    self.setupTab = SetupTab(self.history, self, self.previewer)
	    self.ui.setupLayout.addWidget(self.setupTab)
	
	    splash.showMessage(self.__TITLE__ + ": Loading Force Field Tab.")
	    self.forceTab = ForceTab(self.history, self, self.previewer)
	    self.ui.forceLayout.addWidget(self.forceTab)
	
	    splash.showMessage(self.__TITLE__ + ": Loading Simulation Tab.")
	    self.simTab = SimTab(self.history, self.settings,  self, self.previewer)
	    self.ui.simTabLayout.addWidget(self.simTab)
	
	    splash.showMessage(self.__TITLE__ + ": Loading Minimization Tab.")
	    self.minTab = MinTab(self.history, self.settings, self.simTab, self, self.previewer)
	    self.ui.minTabLayout.addWidget(self.minTab)
	    splash.showMessage(self.__TITLE__ + ": Starting...")
	    
	    splash.showMessage(self.__TITLE__ + ": Loading Analysis Tab.")
	    self.analysis = Analysis( self.history, self, self.previewer, self.settings)
	    self.ui.analysisLayout.addWidget(self.analysis)

	    self.setTabsEnabled(False)


	    self.tabs = [self.buildTab,self.setupTab,self.forceTab,self.simTab,self.minTab,self.analysis]
	    splash.finish(self)
	
	def askForUnsavedMixture(self):
		if not self.history.isCurrentMixtureSaved():
			return QtGui.QMessageBox.question(self, "Warning", "Current simulation was not saved. Continue?", QtGui.QMessageBox.Ok, QtGui.QMessageBox.No)
		else:
			return QtGui.QMessageBox.Ok


	@QtCore.pyqtSlot()
	def on_actionLoad_triggered(self, checked = True):
	    print "on_actionLoad_triggered", checked
	    if not checked:  return
	    if self.simRunning:
	        QtGui.QMessageBox.information(self, "Stop!", "This action is not allowed while a simulation/minimization is running.", QtGui.QMessageBox.Ok)
	    else:
	        if self.askForUnsavedMixture() == QtGui.QMessageBox.No:     return

	        d = WFileDialog(self, 'Load mixture', self.history.currentState().getBuildDirectory(), "Wolffia file (*.wfy)")
	        print "on_actionLoad_triggered d.accepted()", d.accepted()
	        if d.accepted():
				filename = d.fullFilename()
				if not os.path.exists(str(filename)):
					QtGui.QMessageBox.information(self, "Wolffia's message", "Did not find file " + filename + ". Data not loaded.", QtGui.QMessageBox.Ok)
					return
				self.history.push()

				folder = self.history.currentState().getBuildDirectory()  # remember current folder
				mName = self.history.currentState().getMixture().getMixtureName()
				self.history.currentState().load(filename)
				print "on_actionLoad_triggered ",self.history.currentState().getMixture().getMixtureName(),self.history.currentState().getBuildDirectory(), " to ", mName , folder
				#self.history.currentState().setBuildDirectory(folder)
				#self.history.currentState().getMixture().setMixtureName(mName)

				self.update()
				self.setTabsEnabled(True)
				self.setSaveButtonEnabled(True)
				self.setSaveAsButtonEnabled(True)
				self.setTitle()
				self.history.currentState().setCurrentMixtureSaved(True)
				QtGui.QMessageBox.information(self, "Wolffia's message", filename + " loaded.", QtGui.QMessageBox.Ok)
	       
	
	def on_actionMixture_triggered(self, checked = None):
	    if checked == None:  return
	    #print "on_actionMixture_triggered"
	    if self.simRunning:
	        QtGui.QMessageBox.information(self, "Stop!", "This action is not allowed while a simulation/minimization is running.", QtGui.QMessageBox.Ok)
	    else:
	    	self.saveWolffiaState()
	    	self.mixtureDialog()
	    	
	    	
	def mixtureDialog(self):
	        prevMixtueName = self.settings.currentSimulationName()
	        browser        = MixtureBrowser(self.settings, self.history, self)
	        #self.previewer.update()
	        browser.exec_()
	        #print "on_actionMixture_triggered regreso",prevMixtueName,browser.settings.currentSimulationName()
	        if prevMixtueName != browser.settings.currentSimulationName():
	            #print "on_actionMixture_triggered cambio la mezcla"
	            self.previewer.setMixture(self.history.currentState().getMixture(),adjustViewingVolume=True)
	    #print "on_actionMixture_triggered  salioo"
	    
	def on_actionPack_triggered(self, checked = None):
	#    This will deal with choosing the directory to place the .zip of the whole folder at
	    pass
	
	
	def on_clearButton_pressed(self, logAction=True):
	    if not logAction: return
	    self.logWindow.clear()
	
	
	def on_exitButton_triggered(self, bool1 = None):
	    '''
	    
	    :param bool1:
	    '''
	    if bool1 == None:    return
	    self.close()
	
	
	def on_redoButton_triggered(self, redo=True):
	    if not redo: return
	    if self.simRunning:
	        QtGui.QMessageBox.information(self, "Stop right there!", "This action is not allowed while a simulation/minimization is running.", QtGui.QMessageBox.Ok)
	    else:
	        self.history.forward()
	        self.update()
	        self.previewer.update()
	
	
	def on_resetButton_triggered(self, val=True):
	    print "on_resetButton_triggered ", val
	    if not val: return
	    if self.askForUnsavedMixture() == QtGui.QMessageBox.No:     return

	    msgBox = QtGui.QMessageBox(self)
	    msgBox.setText("Delete the current mixture?\nAny simulations that are running will be terminated.")
	    #msgBox.setInformativeText("Do you want to save your changes?")
	    msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
	    msgBox.setDefaultButton(QtGui.QMessageBox.Cancel);
	    ret = msgBox.exec_()
	    if ret == QtGui.QMessageBox.Ok:
	        self.reset()
	               
	        d = WFileNameDialog(self, 'File for new Mixture', self.history.getCurrentState().getBuildDirectory(), "Wolffia file (*.wfy)")
	        if d.isReady():
	            filename = d.fullFilename()
	            if filename[-4:] != ".wfy" and QtGui.QMessageBox.question (self, "Wolffia's message", "File does not end with .wfy. Add extension?", "Yes", "No") == 0:
	                filename += ".wfy"
	                if os.path.exists(filename) and QtGui.QMessageBox.question (self, "Wolffia's message", "File exists.", "Overwrite", "Cancel") != 0:
	                    return

	            print "on_resetButton_triggered ","\'"+filename+"\'"
	            self.history.currentState().setBuildDirectory(os.path.dirname(str(filename)))
	            self.history.currentState().getMixture().setMixtureName(os.path.splitext(os.path.basename(str(filename)))[0])
	            self.setTitle()

	            self.history.currentState().save(filename)
	            self.setTabsEnabled(True)
	            QtGui.QMessageBox.information(self, "Wolffia's message", filename + " created.", QtGui.QMessageBox.Ok)
	

	def on_actionSave_as_triggered(self, saveState=True):
	    '''
	    
	    :param saveState:
	    '''
	    print "on_actionSave_as_triggered "
	    if not saveState: return
	    if self.simRunning:
	        QtGui.QMessageBox.information(self, "Warning", "This action is not allowed while a simulation/minimization is running.", QtGui.QMessageBox.Ok)
	    else:
	        #mixFile = self.history.getCurrentState().getBuildDirectory() + self.history.currentState().getMixtureName() + ".wfy"
	        self.history.currentState().save()
	        #print "on_saveWFY_triggered ",  mixFile 
	               
	        d = WFileNameDialog(self, 'Save current data', self.history.getCurrentState().getBuildDirectory(), "Wolffia file (*.wfy)")
	        if d.isReady():
	            filename = d.fullFilename()
	            print "on_actionSave_as_triggered ","\'"+filename+"\'"
	            if filename[-4:] != ".wfy" and QtGui.QMessageBox.question (self, "Wolffia's message", "File does not end with .wfy. Add extension?", "Yes", "No") == 0:
	                filename += ".wfy"
	                if os.path.exists(filename) and QtGui.QMessageBox.question (self, "Wolffia's message", "File exists.", "Overwrite", "Cancel") != 0:
	                    return
	            self.history.currentState().setBuildDirectory(os.path.dirname(str(filename)))
	            self.history.currentState().getMixture().setMixtureName(os.path.splitext(os.path.basename(str(filename)))[0])
	            self.setTitle()

	            self.history.currentState().save(filename)
	
	            QtGui.QMessageBox.information(self, "Wolffia's message", filename + " saved.", QtGui.QMessageBox.Ok)
	
	def on_saveWFY_triggered(self, saveState=True):
	    '''
	    
	    :param saveState:
	    '''
	    print "on_saveWFY_triggered "
	    if not saveState: return
	    if self.simRunning:
	        QtGui.QMessageBox.information(self, "Warning", "This action is not allowed while a simulation/minimization is running.", QtGui.QMessageBox.Ok)
	    else:
	        #mixFile = self.history.getCurrentState().getBuildDirectory() + self.history.currentState().getMixtureName() + ".wfy"
	        self.history.currentState().save()
	
	        QtGui.QMessageBox.information(self, "Wolffia's message", self.history.currentState().getMixtureName() + " saved.", QtGui.QMessageBox.Ok)
	
	
	def on_settingsButton_triggered(self, openDialog=True):
	    '''
	    
	    '''
	    #self.history.push()
	    #sDialog = SettingsDialog(self.history.currentState())
	    if openDialog:
	    	self.saveWolffiaState()
	        settingW=SettingsDialog(self.settings,self)
	        settingW.show()
	        settingW.exec_()
	        #print "on_settingsButton_triggered self.settings.highResolution=", self.settings.highResolution
	        #self.previewer.setHighResolution(self.settings.highResolution)
	        #self.previewer.setLabeling(self.settings.showLabels)
	        #self.previewer.showAxes(self.settings.showAxes)
	        #self.previewer.showHelp(self.settings.showHelp)
	        #self.previewer.setLabeling(self.settings.)
	        #self.setTitle()
	    
	
	def on_undoButton_triggered(self, undo=True):
	    if not undo: return
	    if self.simRunning:
	        QtGui.QMessageBox.information(self, "Warning", "This action is not allowed while a simulation/minimization is running.", QtGui.QMessageBox.Ok)
	    else:
	        self.history.back()
	        self.update()
	        #self.previewer.update()
	
	
	#--------------------------------------------------------------------------------
	def closeEvent(self, event):
	    if (self.simRunning):
	            quit_msg = "There is a simulation running, are you sure you wish to exit?"
	            reply = QtGui.QMessageBox.question(self, 'Warning!', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
	            if reply == QtGui.QMessageBox.No:
	                event.ignore()
	                return
	            else:
	                try:
	                    self.simTab.cancelSim()
	                except:
	                    self.minTab.stopMin()
	    elif not self.history.isCurrentMixtureSaved():
	        reply = QtGui.QMessageBox.question(self, 'Warning!', "Current mixture was not saved. Save?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
	        if reply == QtGui.QMessageBox.Yes:
	            self.saveWolffiaState()
	    print "closeEvent", event
	    import threading
	    print "closeEvent procesos: ", self.minTab.simRun.isAlive(), threading.enumerate()
	    threading.enumerate()[1].do_run = False
	    threading.enumerate()[1].join()
	    print "closeEvent procesos: ", threading.enumerate()
	    event.accept()
	
	
	def configurationFilesBasename(self):
		return str(self.history.getCurrentState().getBuildDirectory()) + str(self.history.currentState().getMixture().getMixtureName())
	
	
	def reset(self):
		folder = self.history.currentState().getBuildDirectory()  # remember current folder
		mName = self.history.currentState().getMixture().getMixtureName()
		self.history.reset()
		print "Wolffia.reset ",self.history.currentState().getMixture().getMixtureName(),self.history.currentState().getBuildDirectory(), " to ", mName , folder

		#self.history.currentState().setBuildDirectory(folder)
		#self.history.currentState().getMixture().setMixtureName(mName)
		#self.history.currentState().save()
		
		for tab in self.tabs:
		    tab.reset()
		self.update()
		self.previewer.update()
	    
	
	def saveWolffiaState(self, baseFilename=None):
	    """
	        saves the current state of wolffia, usually before the window closes
	    """
	    if baseFilename == None:
	    	baseFilename = self.history.currentState().getMixtureFileName()
	    self.history.currentState().setSimTabValues(self.simTab.getValues())
	    self.history.currentState().minTabValues = self.minTab.getValues()
	    
	    print "saveWolffiaState ",baseFilename , self.configurationFilesBasename()
	    self.history.currentState().save(filename=baseFilename)
	    self.settings.save()
	
	def settingsChanged(self):
	    '''
	    
	    '''
	    self.previewer.setHighResolution(self.settings.highResolution)
	    self.previewer.setSolventHighResolution(self.settings.solventHighResolution)
	    self.previewer.setLabeling(self.settings.showLabels)
	    self.previewer.showAxes(self.settings.showAxes)
	    self.previewer.showHelp(self.settings.showHelp)
	    
	def setTabsEnabled(self, status=True):
	    self.ui.wolffiaTabs.setEnabled(status)

	def setTitle(self):
		print "self.setTitle()", self.history.getCurrentState().getMixtureName()
		self.setWindowTitle(self.__TITLE__ + " - " + self.history.getCurrentState().getMixtureName())
	
	def setSaveButtonEnabled(self, status=True):
		print "setSaveButtonEnabled"
		self.ui.saveWFY.setEnabled(status)

	def setSaveAsButtonEnabled(self, status=True):
		print "setSaveAsButtonEnabled"
		self.ui.actionSave_as.setEnabled(status)

	
	def setDefaultTabs(self):
	    for tab in self.tabs:
	        try:
	            tab.setDefaultValues()
	        except:
	            print "Wolffia.py:setDefaultTabs: Tab has no setDefaultValues"
	            
	def update(self):
	
		#timer = WTimer("Wolffia")
		if self.allowUpdate:
			print "wolffia.update, updating Wolffia"
			self.allowUpdate = False
			self.setTitle()
			for tab in self.tabs:
				#timer2 = WTimer("Wolffia calling"+str(tab))
				#print "Wolffia.update() updating ", tab
				tab.update()
				#timer2.report()
			self.previewer.update()
			self.allowUpdate = True
	
	    #timer.report()

    
#--------------------------------------------------------------------------------

if __name__ == '__main__' or __name__ == 'interface.main.Wolffia':
    import time
    
    app = QtGui.QApplication(sys.argv)

    app.processEvents()

    gui = Wolffia()
    print "cargado"
    screen = QtGui.QDesktopWidget().screenGeometry()
    gui.setGeometry(screen & gui.geometry())
    gui.show()
    sys.exit(app.exec_())
