# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  MinTab.py
#  Version 0.7, October, 2011
#
#  Wolffia's tab for energy minimization.
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

import sys, os, time, platform
from PyQt4 import QtCore, QtGui
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import _WOLFFIA_OS,WOLFFIA_GRAPHICS, WOLFFIA_USES_IMD
from QClasses import * #@UnusedWildImport
from ui_MinTab import Ui_minTab
from subprocess import signal, Popen, PIPE #@UnusedImport
from lib.communication.namd.Configuration import Configuration, ConfigurationError
from namdMinParm import parmDict
import logging
from chemicalGraph.io.PRM import PRMError


class MinTab(QtGui.QFrame):   
    '''
    Wolffia's tab for energy minimization.
    '''
    _PLOT_TIMER_TIMEOUT_ = 1
    _VIEWER_TIMER_TIMEOUT_ = 500
    checkState            =    {True:"On", False:"Off"}

    def __init__(self, hist, settings, sim, parent, preview):
		'''
		Constructor for MinTab
		
		:param hist: History
		:param settings: Settings
		:param sim: SimTab
		:param parent: Wolffia, Main Window
		:param preview: MixtureViewer
		'''
		super(MinTab, self).__init__(parent)
		
		self.parent         =   parent
		self.simTab         =   sim
		self._WOLFFIA_OS    =   platform.system()
		self.history        =   hist
		self.wolffia        =   parent
		self.allowUpdate    =   True
		self.preview        =   preview
		self.settings       =   settings
		self.log			=   parent.logWindow
		self.simRun         =   None
		#timers
		self.minTimer       =   QtCore.QTimer()
		self.minCoordTimer  =   QtCore.QTimer()
		self.modTime        =   0
		self.connect(self.minTimer, QtCore.SIGNAL('timeout()'), self.on_minTimer)
		self.connect(self.minCoordTimer, QtCore.SIGNAL('timeout()'), self.on_minCoordTimer)
		
		
		self.ui            =    Ui_minTab()
		self.ui.setupUi(self)
		self.minTree       =    self.ui.minTree
		
		
		self.energyPlot1   =    parent.energyPlot1
		self.energyPlot2   =    parent.energyPlot2
		
		# Dummy fields
		self.energySteps        =    QtGui.QSpinBox(None)
		self.trajectorySteps    =    QtGui.QSpinBox(None)
		self.restartSteps       =    QtGui.QSpinBox(None)
		self.energySteps.    setMaximum (9999999)
		self.trajectorySteps.setMaximum (9999999)
		self.restartSteps.   setMaximum (9999999)
		self.energySteps.    setValue (100)
		self.trajectorySteps.setValue (100)
		self.restartSteps.   setValue (100)
		
		#Different variables that define the positions of the objects
		#in simulation part of the TreeWidget
		minBabyStepAt        =    self.minTree.topLevelItem(0).child(2)
		minTinyStepAt        =    self.minTree.topLevelItem(0).child(1)
		minLineGoalAt        =    self.minTree.topLevelItem(0).child(3)
		minStepsAt           =    self.minTree.topLevelItem(0).child(0)
		
		#Different variables that define the positions of the objects
		#in simulation part of the TreeWidget
		exclusionAt         =    self.minTree.topLevelItem(1).child(0) #@UnusedVariable
		cutoffAt            =    self.minTree.topLevelItem(1).child(2) #@UnusedVariable
		useSwitchAt         =    self.minTree.topLevelItem(1).child(3) #@UnusedVariable
		switchDistAt        =    self.minTree.topLevelItem(1).child(4) #@UnusedVariable
		scalingAt           =    self.minTree.topLevelItem(1).child(1) #@UnusedVariable
		pairListDistAt      =    self.minTree.topLevelItem(1).child(5) #@UnusedVariable
		
		
		#Uses the parmDict dictionary to initialize all the objects, 
		#give them values and add them on the widgetTree
		for defaults in  parmDict.iterkeys():
		    if parmDict[defaults][1] == "InputFile":
		        vars(self)[defaults] = InputFile(self.minTree)
		        vars(self)[defaults].setEnabled(parmDict[defaults][2])
		    elif parmDict[defaults][1] == "CheckBox":
		        vars(self)[defaults] = CheckBox(self.minTree)
		        vars(self)[defaults].setChecked(parmDict[defaults][2])
		        vars(self)[defaults].setEnabled(parmDict[defaults][3])
		    elif parmDict[defaults][1] == "SpinBox":
		        vars(self)[defaults] = SpinBox(self.minTree)
		        vars(self)[defaults].setSuffix(parmDict[defaults][2])
		        vars(self)[defaults].setRange(parmDict[defaults][3], parmDict[defaults][4])
		        vars(self)[defaults].setEnabled(parmDict[defaults][5])
		        vars(self)[defaults].setSingleStep(parmDict[defaults][6])
		        vars(self)[defaults].setValues(parmDict[defaults][0])
		    elif parmDict[defaults][1] == "DoubleSpinBox":
		        vars(self)[defaults] = DoubleSpinBox(self.minTree)
		        vars(self)[defaults].setSuffix(parmDict[defaults][2])
		        vars(self)[defaults].setDecimals(parmDict[defaults][3])
		        vars(self)[defaults].setRange(parmDict[defaults][4], parmDict[defaults][5])
		        vars(self)[defaults].setEnabled(parmDict[defaults][6])
		        vars(self)[defaults].setSingleStep(parmDict[defaults][7])
		        vars(self)[defaults].setValues(parmDict[defaults][0])
		    elif parmDict[defaults][1] == "ComboBox":
		        vars(self)[defaults] = ComboBox(self.minTree)
		        cLen = len(parmDict[defaults])
		        vars(self)[defaults].setEnabled(parmDict[defaults][cLen - 1])
		        vars(self)[defaults].setCurrentIndex(parmDict[defaults][0])
		        for y in range(2, cLen - 1):
		            vars(self)[defaults].addItem(parmDict[defaults][y])
		    self.minTree.setItemWidget(vars()[defaults + "At"], 0, vars(self)[defaults]) #adds them all to the tree
		
		#Handling signals for specific slots 
		self.cutoff.editingFinished.connect(self.checkCutoff)
		self.pairListDist.editingFinished.connect(self.checkCutoff)
		self.switchDist.editingFinished.connect(self.checkCutoff)
		self.useSwitch.stateChanged.connect(self.useSwitchChanged)
		self.exclusion.currentIndexChanged.connect(self.checkScale)
		self.scaling.editingFinished.connect(self.updateSimTab)
		self.useSwitch.stateChanged.connect(self.updateSimTab)
		self.cutoff.editingFinished.connect(self.updateSimTab)
		self.pairListDist.editingFinished.connect(self.updateSimTab)
		self.switchDist.editingFinished.connect(self.updateSimTab)
		self.exclusion.currentIndexChanged.connect(self.updateSimTab)
		
		
		#
		size = QtCore.QSize(100,10)
		minBabyStepAt.setSizeHint(0,size)
		minTinyStepAt.setSizeHint(0,size)
		minLineGoalAt.setSizeHint(0,size)
		minStepsAt.setSizeHint(0,size)
		
		self.ui.minButton.setIcon(QtGui.QIcon().fromTheme("media-playback-start",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "media-playback-start.svg")    ))
		self.ui.stopButton.setEnabled(False)
		self.ui.stopButton.setIcon(QtGui.QIcon().fromTheme("media-playback-stop",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "media-playback-stop.svg")    ))
		self.ui.resetButton.setIcon(QtGui.QIcon().fromTheme("emblem-default",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "emblem-default.png")    ))
		
		#Restores the values the tab had before being closed
		self.initialize(self.history.currentState().minTabValues)
		
		self.exclude = self.exclusion  # backward compatibilitu < 0.24

    @QtCore.pyqtSlot()
    def on_stopButton_pressed(self):
        '''
        Calls the stopMin function
        '''
        self.stopMin()


    def getValues(self):
        '''
        Returns a dictionary containing values of all the 
        input widgets in the QTreeWidget
        [inputWidgetObjectName] [value]
        '''
        picklesan = dict()
        for elements in parmDict.keys():
            picklesan[elements] = vars(self)[elements].value()
        return picklesan
    
    def initialize(self, initVal):
        '''
        Restores the values the input widgets in the QTreeWidget 
        had before being closed.
        :param initVal: dictionary that contains the values of all the boxes in minTab
        '''
        if initVal != None:
            for elements in parmDict.keys():
                vars(self)[elements].setValues(initVal[elements])

    def setDefaultValues(self):
        '''
        Sets the default values in the input widgets 
        using the default parameter dictionary
        '''
        for elements in parmDict.keys():
                vars(self)[elements].setValues(parmDict[elements][0])


    def stopMin(self):
        '''
        Stop the minimization by killing the NAMD process, stopping all 
        the timers, killing the pipe(?) and stopping the simRun thread
        
        '''
        self.ui.minButton.setEnabled(False)
        self.ui.stopButton.setEnabled(False)

        if self.simRun != None:
            print "stopMin canceling"
            self.simRun.cancel()
            print "stopMin stopping timers"
            self.minTimer.stop()
            self.minCoordTimer.stop()
            print "stopMin updating coords"
            self.updateCoordinates()
            print "stopMin logging"
            logging.getLogger(self.__class__.__name__).info("Minimization has stopped.")
        
        self.parent.simRunning = False
        self.ui.minButton.setText("Run")
        self.ui.minButton.setIcon(QtGui.QIcon().fromTheme("media-playback-start"))
        self.ui.minButton.setEnabled(True)
        if self.simRun != None: self.simRun.stop()
    

    @QtCore.pyqtSlot()
    def on_resetButton_pressed(self):
        '''
            Calls the setDefaultValues function
        '''
        self.setDefaultValues()


    @QtCore.pyqtSlot()
    def on_minButton_pressed(self):
        '''
        Checks if there's a simulation running, if not, then the
        simulation starts and the button's text changes to 'pause'
        and the stop button becomes enabled.
        '''
        
        if self.ui.minButton.text() == "Run":
            if (self.parent.simRunning == False):
                if self.checkMD():         
                    self.energyPlot1.reset()
                    self.energyPlot2.reset()
                    self.ui.stopButton.setEnabled(True)
                    self.parent.simRunning = True
                    self.ui.minButton.setText("Pause")
                    self.ui.minButton.setIcon(QtGui.QIcon().fromTheme("media-playback-pause"))
                    self.log.clear()
                    self.runSim()
                    if self.simRun == None: self.stopMin()
                else:   return

            else:
                message = QtGui.QMessageBox(1, "Heyyy!", "There is a simulation running right now, it'd be horrible to run both of them at the same time. \n I'm the only thing that stands between you and disaster!")
                message.exec_()


        elif self.ui.minButton.text() == "Pause":
            self.pauseSim()
            
        else:
            self.continueSim()

    def on_minCoordTimer(self):
        '''
        Updates the mixture viewer at intervals
        '''
        start = time.clock()
        self.minCoordTimer.stop()
        #self.updateCoordinates()
        if self.updateCoordinates():
            elapsedTime = time.clock()-start
            self.minCoordTimer.start(elapsedTime*3000)
        else:
            self.minCoordTimer.start(self._VIEWER_TIMER_TIMEOUT_ * 1.5)
        #print "on_minCoordTimer ", time.clock() - start

    def on_minTimer(self):
		'''
		Gets the output from the MD package and sends it to
		the instance of EnergyPlot class.
		Also checks if the thread is still alive.  
		'''
		
		self.minTimer.stop()
		namdOutput = self.simRun.getOutput()
		if namdOutput != None:
			#print "SimTab on_minTimer", namdOutput
			self.checkError(namdOutput)
			if WOLFFIA_USES_IMD:
			    self.energyPlot1.addValuesFromIMD(self.simRun.getEnergies())
			    self.energyPlot2.addValuesFromIMD(self.simRun.getEnergies())
			else:
			    self.energyPlot1.addValuesFromNamd(namdOutput)
			    self.energyPlot2.addValuesFromNamd(namdOutput)
		
		try:
		    if not self.simRun.isAlive():
		        self.minCoordTimer.stop()
		        self.ui.minButton.setText("Run")
		        self.ui.minButton.setIcon(QtGui.QIcon().fromTheme("media-playback-start"))
		        self.wolffia.simRunning = False
		        self.ui.stopButton.setEnabled(False)
		        message = QtGui.QMessageBox(1, "Message", "Minimization has ended!")
		        message.exec_()
		        #self.minPipe.close()
		        return
		    
		    else:   self.minTimer.start(self._PLOT_TIMER_TIMEOUT_)
		               
		
		except:
			print "SimTab on_minTimer exception occured", sys.exc_info()[0]
			pass

            

    def on_minTree_collapsed(self):
        self.minTree.resizeColumnToContents(0)


    def on_minTree_expanded(self):
        self.minTree.resizeColumnToContents(0)


    #==========================================================================
    def checkCutoff(self):
        '''
        Adjusts pairListDist and switchDist when the cutoff DoubleSpinbox changes.
        (See 4.1.1 of Namd User's Manual)
        '''
        if self.switchDist.value() > self.cutoff.value() - 1:
            self.switchDist.setValues(self.cutoff.value() - 1)
            msgBox = QtGui.QMessageBox ();
            msgBox.setText("switchDist should not be larger than cutoff - 1.\nIt has been reset to "+str(self.switchDist.value())+".");
            msgBox.exec_();
        elif self.pairListDist.value() < self.cutoff.value() + 1:
            self.pairListDist.setValues(self.cutoff.value() + 1)    
            msgBox = QtGui.QMessageBox ();
            msgBox.setText("pairListDist should not be smaller than cutoff + 1.\nIt has been reset to "+str(self.pairListDist.value())+".");
            msgBox.exec_();

    def checkError(self, lineas):
        '''
        Checks the output for errors
        :param lineas: An array of the MD package's output
        '''
        errorMessage = ""
        for lines in lineas:
            if lines[0:5] == "ERROR" or lines[0:11] == "FATAL ERROR":
                self.log.addMessage(lines, "WARNING")
                #errorMessage += lines
                return True
            elif lines[0:4]    == "Info" or lines[0:3] == "LDB" or lines[0:7] == "Warning":
                self.log.addMessage(lines, "INFO")
                #print lines

        #if errorMessage != "":
            #message = QtGui.QMessageBox(1, "ERROR", lines)
            #message.exec_()
            #return True

    def checkMD(self):
        '''
        
        '''
        if self.settings.namdLocation == "":
                message = QtGui.QMessageBox(1, "Message", "NAMD not found!")
                message.exec_()
                return False
        elif not os.path.exists(self.settings.namdLocation):    
                message = QtGui.QMessageBox(1, "Message", self.settings.namdLocation + " not found!")
                message.exec_()
                return False
        else:   return True

    def checkScale(self):
        '''
        Handles changes to the exclusion ComboBox
        '''
        if self.exclusion.currentIndex() > 2:
            self.scaling.setEnabled(True)
        else:
            self.scaling.setEnabled(False)

    def continueSim(self):
        '''
        Continues a simulation by signaling the process.
        '''
        self.minTimer.start(self._PLOT_TIMER_TIMEOUT_)
        self.minCoordTimer.start(self._VIEWER_TIMER_TIMEOUT_)
        self.simRun.resume()
        self.ui.minButton.setText("Pause")
        self.ui.minButton.setIcon(QtGui.QIcon().fromTheme("media-playback-pause",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "media-playback-pause.svg")    ))

    def pauseSim(self):
        '''
        Pauses the simulation by signaling the process.
        '''
        self.minTimer.stop()
        self.minCoordTimer.stop()
        self.simRun.pause()
        self.ui.minButton.setText("Continue")

    def reset(self):
        '''
        Resets the minTab by placing the default values, stopping
        the simulation (if any) and stopping the timers.
        '''
        self.preview.reset()
        try:
            self.setDefaultValues()
            self.stopMin()
            self.minTimer.stop()
            self.minCoordTimer.stop() 
            
        except:
            print "MinTab reset: algo fallo"
            pass    
        
        
    def runSim(self):
        """
         Sets up the configuration, the run thread and the timer for polling the simulation. 
        """
        start = time.clock()

        #print "runSim A", time.clock() - start
        progress      = QtGui.QProgressDialog("Configuring...", QtCore.QString(), 0, 6, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setWindowTitle("Minimization")
        progress.setValue(0)
        QtGui.QApplication.processEvents()

        #print "runSim B", time.clock() - start
        progress.setValue(1)
        progress.setLabelText("Memorizing current state...")
        QtGui.QApplication.processEvents()
        self.history.push(force=True)

        #print "runSim C", time.clock() - start
        progress.setLabelText("Generating configuration...")
        progress.setValue(2)
        QtGui.QApplication.processEvents()
        conf = Configuration(self.__dict__, self.history.currentState().getDrawer(), 
                                self.history.currentState().fixedMolecules.hasFixedMolecules(), 
                                simType=Configuration.MINIMIZATION)
        #print "runSim D", time.clock() - start
        progress.setLabelText("Configuring simulator...")
        try:
			conf.writeSimulationConfig(str(self.settings.currentMixtureLocation()), str(self.history.currentState().getMixture().getMixtureName()))
            #conf.writeSimulationConfig(str(self.settings.currentMixtureLocation()), str(self.settings.currentMixtureName))
        except ConfigurationError, e:
            Error = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Error!", e.message)
            Error.exec_()
            return

        #print "runSim E", time.clock() - start
        progress.setValue(3)
        progress.setLabelText("Writing mixture files...")
        QtGui.qApp.processEvents()
        #print "MinTab runSim", self.history.currentState().getMixture().getMolecule(self.history.currentState().getMixture().molecules()[0]).getForceField()._ANGLES
        try:
            self.history.currentState().writeFiles(self.settings.currentMixtureLocation() + str(self.history.currentState().getMixture().getMixtureName()))
        except Exception,  e:
			Error = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Error!", e.message)
			Error.exec_()
			progress.cancel()
			progress.hide()
			return
			
        
        #print "runSim F", time.clock() - start
        progress.setValue(4)
        progress.setLabelText("Starting the minimization...")
        if WOLFFIA_USES_IMD:
            from lib.communication.namd.SimThread import ImdSimThread
            self.simRun = ImdSimThread(conf, str(self.settings.namdLocation),port=conf.getImdPort())
        else:
            from lib.communication.namd.SimThread import SimThread
            self.simRun = SimThread(conf, str(self.settings.namdLocation))
        self.simRun.start()

        #print "runSim G", time.clock() - start
        progress.setValue(5)
        progress.setLabelText("Starting clocks...")
        self.minTimer.start(self._PLOT_TIMER_TIMEOUT_)
        self.minCoordTimer.start(self._VIEWER_TIMER_TIMEOUT_)

        #print "runSim H", time.clock() - start
        progress.setValue(6)
        progress.hide()

    def updateSimTab(self):
        '''
        Calls the updateSimTab function in simTab
        '''
        self.simTab.updateSimTab(self)


    def useSwitchChanged(self):
        '''
        Handles changes to the switchDist CheckBox
        '''
        self.switchDist.setEnabled(self.useSwitch.isChecked())


    def updateCoordinates(self):
        '''
        Updates the coordinate files calling the updateCoordinates function in history.
        '''

        if self.simRun.coordinatesAreNew():
            self.simRun.updateCoordinates(self.history.currentState().getMixture())
            self.preview.setMixture(self.history.currentState().getMixture())
            return True
        return False


        
        