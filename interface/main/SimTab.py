# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  SimTab.py
#  Version 0.6, October, 2011
#
#  Wolffia's tab for running and monitoring simulations.
#
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Carlos J.  Cortés Martínez, , Giovanni Casanova

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


import sys, os, math, time, queue
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import NANOCAD_BASE,WOLFFIA_GRAPHICS, WOLFFIA_USES_IMD
from .QClasses import *
from PyQt4 import QtCore
from ui_SimTab import Ui_simTab 
from .namdSimParm import parmDict
from subprocess import signal, Popen, PIPE #@UnusedImport 
from lib.communication.namd.Configuration import Configuration, ConfigurationError
from lib.communication.namd.SimThread import SimThread, ImdSimThread
#import lib.communication.imd.imd as imd


class SimTab(QtGui.QFrame):
	'''
	Wolffia's tab for running and monitoring simulations.
	'''
	_PLOT_TIMER_TIMEOUT_      = 500
	_VIEWER_TIMER_TIMEOUT_    = 500
	_CHECKED_BOOL_TO_WORD_    = {True:"yes", False:"no"}
	
	def __init__(self, hist, settings, parent, preview):
		'''
		Constructor for SimTab
		
		:param hist: History
		:param settings: Settings
		:param parent: Wolffia, Main Window
		:param preview: MixtureViewer
		'''
		super(SimTab, self).__init__(parent)
		self.history            =   hist
		self.wolffia            =   parent
		self.log                =   parent.logWindow
		self.allowUpdate        =   True
		self.preview = preview
		#self.analysis = parent.analysis
		self.wolffia.simRunning =   False
		self.settings           =   settings
		self.remoteHost         =   None
		self.simRun         =   None
		
		self.modTime            =   0
		#if not WOLFFIA_USES_IMD:
		self.simCoordTimer      =   QtCore.QTimer()
		self.connect(self.simCoordTimer, QtCore.SIGNAL('timeout()'), self.on_simCoordTimer)
		
		self.simTimer           =   QtCore.QTimer()
		self.connect(self.simTimer, QtCore.SIGNAL('timeout()'), self.on_simTimer)
		
		#energyplot
		self.energyPlot1        =   parent.energyPlot1
		self.energyPlot2        =   parent.energyPlot2
		
		
		#kinetic plot
		self.kineticsPlot1      =   parent.kineticsPlot1
		self.kineticsPlot2      =   parent.kineticsPlot2
		
		
		#widgets import
		self.ui                 =   Ui_simTab()
		self.ui.setupUi(self)
		
		#self.ui.Thermo.setFillColor(QtGui.QColor("Red"))
		#self.ui.saveButton.setIcon(QtGui.QIcon().fromTheme("media-floppy",	QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "media-floppy.png")	))
		#self.ui.loadButton.setIcon(QtGui.QIcon().fromTheme("document-open",	QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "document-open.png")	))
		self.ui.runButton.setIcon(QtGui.QIcon().fromTheme("media-playback-start",	QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "media-playback-start.svg")	))
		self.ui.cancelButton.setIcon(QtGui.QIcon().fromTheme("media-playback-stop",	QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "media-playback-stop.svg")	))
		self.ui.packButton.setIcon(QtGui.QIcon().fromTheme("package-x-generic"))
		self.ui.resetButton.setIcon(QtGui.QIcon().fromTheme("emblem-default",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "emblem-default.png")    ))
		self.ui.remoteButton.setIcon(QtGui.QIcon().fromTheme("computer"))
		
		self.ui.toolBox.setItemText(0,"Configuration Parameters")
		self.ui.toolBox.setItemText(1,"Basic Simulation Parameters*")
		self.ui.toolBox.setItemText(2,"Additional Simulation Parameters")
		
		
		self.IOtree = self.ui.IOtreeWidget
		
		#input, output files
		self.baseDir            =    QtGui.QLabel(self.IOtree)
		baseDirAt               =    self.IOtree.topLevelItem(0).child(0)
		self.coordinatesFile    =    QtGui.QLabel(self.IOtree)
		self.coordinatesFile.setFrameStyle(QtGui.QFrame.Box)
		coordinatesFileAt       =    self.IOtree.topLevelItem(0).child(1)
		self.structuresFile     =    QtGui.QLabel(self.IOtree)
		structuresFileAt        =    self.IOtree.topLevelItem(0).child(2)
		self.parametersFile     =    QtGui.QLabel(self.IOtree)
		parametersFileAt        =    self.IOtree.topLevelItem(0).child(3)
		self.outputFile         =    OutputFileLabel(self.IOtree)
		outputFileAt            =    self.IOtree.topLevelItem(1).child(0)
		
		self.energySteps        =    QtGui.QSpinBox(self.IOtree)
		self.trajectorySteps    =    QtGui.QSpinBox(self.IOtree)
		self.restartSteps       =    QtGui.QSpinBox(self.IOtree)
		
		self.energySteps.    setMaximum (9999999)
		self.trajectorySteps.setMaximum (9999999)
		self.restartSteps.   setMaximum (9999999)
		self.energySteps.    setMinimum (1)
		self.trajectorySteps.setMinimum (1)
		self.restartSteps.   setMinimum (1)
		self.energySteps.    setValue (1000)
		self.trajectorySteps.setValue (1000)
		self.restartSteps.   setValue (1000)
		
		#adds widgets to IOtree 
		self.IOtree.setItemWidget(baseDirAt, 0, self.baseDir)
		self.IOtree.setItemWidget(coordinatesFileAt, 0, self.coordinatesFile)
		self.IOtree.setItemWidget(structuresFileAt, 0, self.structuresFile)
		self.IOtree.setItemWidget(parametersFileAt, 0, self.parametersFile)
		self.IOtree.setItemWidget(outputFileAt, 0, self.outputFile)
		self.IOtree.setItemWidget(self.IOtree.topLevelItem(2).child(0), 0, self.energySteps)
		self.IOtree.setItemWidget(self.IOtree.topLevelItem(2).child(1), 0, self.trajectorySteps)
		self.IOtree.setItemWidget(self.IOtree.topLevelItem(2).child(2), 0, self.restartSteps)
		self.IOtree.resizeColumnToContents(0)
		
		self.PStree             =    self.ui.BasicTree
		
		#Basic Dynamics
		temperatureAt           =    self.PStree.topLevelItem(1).child(0) 
		COMmotionAt             =    self.PStree.topLevelItem(1).child(1) 
		dielectricAt            =    self.PStree.topLevelItem(1).child(2) 
		seedAt                  =    self.PStree.topLevelItem(1).child(3) 
		rigidBondsAt            =    self.PStree.topLevelItem(1).child(4) 
		rigidTolAt              =    self.PStree.topLevelItem(1).child(5) 
		rigidIterAt             =    self.PStree.topLevelItem(1).child(6)
		settleAt                =    self.PStree.topLevelItem(1).child(7)
		
		#Timestep parameters
		numStepsAt              =    self.PStree.topLevelItem(0).child(0)
		timeStepsAt             =    self.PStree.topLevelItem(0).child(1)
		startStepAt             =    self.PStree.topLevelItem(0).child(2)
		stepsCycleAt            =    self.PStree.topLevelItem(0).child(3)
		
		#Simulation space partitioning
		excludeAt               =    self.PStree.topLevelItem(2).child(0)
		scalingAt               =    self.PStree.topLevelItem(2).child(1)
		cutoffAt                =    self.PStree.topLevelItem(2).child(2)
		useSwitchAt             =    self.PStree.topLevelItem(2).child(3)
		switchDistAt            =    self.PStree.topLevelItem(2).child(4)
		pairListDistAt          =    self.PStree.topLevelItem(2).child(5)
		splitPatchAt            =    self.PStree.topLevelItem(2).child(6)
		hCutoffAt               =    self.PStree.topLevelItem(2).child(7)
		marginAt                =    self.PStree.topLevelItem(2).child(8)
		pairMinAt               =    self.PStree.topLevelItem(2).child(9)
		pairCycleAt             =    self.PStree.topLevelItem(2).child(10)
		pairOutAt               =    self.PStree.topLevelItem(2).child(11)
		pairShrinkAt            =    self.PStree.topLevelItem(2).child(12)
		pairGrowAt              =    self.PStree.topLevelItem(2).child(13)
		pairTriggerAt           =    self.PStree.topLevelItem(2).child(14)
		
		#PME PARAMETERS
		pmeAt                   =    self.PStree.topLevelItem(3).child(0)
		pmeGridSpAt				=	 self.PStree.topLevelItem(3).child(1)
		pmeTolAt				=	 self.PStree.topLevelItem(3).child(5)
		pmeInAt                 =    self.PStree.topLevelItem(3).child(6)
		gridXAt                 =    self.PStree.topLevelItem(3).child(2)
		gridYAt                 =    self.PStree.topLevelItem(3).child(3)
		gridZAt                 =    self.PStree.topLevelItem(3).child(4)
		FFTProcAt               =    self.PStree.topLevelItem(3).child(7)
		FFTOpAt                 =    self.PStree.topLevelItem(3).child(8)
		FFTWAt                  =    self.PStree.topLevelItem(3).child(9)
		FFTFileAt               =    self.PStree.topLevelItem(3).child(10)
		
		#Full direct parameters
		elcAt                   =    self.PStree.topLevelItem(4).child(0)
		
		#Multiple timestep parameters
		numElcAt                =    self.PStree.topLevelItem(5).child(0)
		timeBondAt              =    self.PStree.topLevelItem(5).child(1)
		MTSalgAt                =    self.PStree.topLevelItem(5).child(2)
		rforceAt                =    self.PStree.topLevelItem(5).child(3)
		mollAt                  =    self.PStree.topLevelItem(5).child(4)
		molltolAt               =    self.PStree.topLevelItem(5).child(5)
		mollitrAt               =    self.PStree.topLevelItem(5).child(6)
		
		self.SMtree             =    self.ui.AddTree
		
		#harmonic constraint parameters
		constAt                 =    self.SMtree.topLevelItem(0).child(0).child(0)
		harExpAt                =    self.SMtree.topLevelItem(0).child(0).child(1)
		pdbConsAt               =    self.SMtree.topLevelItem(0).child(0).child(2)
		pdbForcAt               =    self.SMtree.topLevelItem(0).child(0).child(3)
		pdbcol1At               =    self.SMtree.topLevelItem(0).child(0).child(4)
		selConsAt               =    self.SMtree.topLevelItem(0).child(0).child(5)
		selConsXAt              =    self.SMtree.topLevelItem(0).child(0).child(6)
		selConsYAt              =    self.SMtree.topLevelItem(0).child(0).child(7)
		selConsZAt              =    self.SMtree.topLevelItem(0).child(0).child(8)
		
		
		#fixed atom parameters
		fixAtmAt                =    self.SMtree.topLevelItem(0).child(1).child(0)
		fixAtmForcAt            =    self.SMtree.topLevelItem(0).child(1).child(1)
		fixAtmFileAt            =    self.SMtree.topLevelItem(0).child(1).child(2)
		fixAtmColAt             =    self.SMtree.topLevelItem(0).child(1).child(3)
		
		#Langevin Dynamics
		useLangAt               =    self.SMtree.topLevelItem(1).child(0).child(0)
		langTempAt              =    self.SMtree.topLevelItem(1).child(0).child(1)
		langDampAt              =    self.SMtree.topLevelItem(1).child(0).child(2)
		langHydAt               =    self.SMtree.topLevelItem(1).child(0).child(3)
		pdbLangAt               =    self.SMtree.topLevelItem(1).child(0).child(4)
		pdbColAt                =    self.SMtree.topLevelItem(1).child(0).child(5)
		
		#Temperature couplin
		tempCoupAt              =    self.SMtree.topLevelItem(1).child(1).child(0)
		tempBathAt              =    self.SMtree.topLevelItem(1).child(1).child(1)
		pdbTCoupleAt            =    self.SMtree.topLevelItem(1).child(1).child(2)
		pdbTColAt               =    self.SMtree.topLevelItem(1).child(1).child(3)
		
		#Temperature rescaling
		timeTResAt              =    self.SMtree.topLevelItem(1).child(2).child(0)
		tempEqAt                =    self.SMtree.topLevelItem(1).child(2).child(1)
		
		#Temperature reassignment
		useTempReAt             =    self.SMtree.topLevelItem(1).child(3).child(0)
		timeBTempAt             =    self.SMtree.topLevelItem(1).child(3).child(1)
		tempResEqAt             =    self.SMtree.topLevelItem(1).child(3).child(2)
		tempIncAt               =    self.SMtree.topLevelItem(1).child(3).child(3)
		resHoldAt               =    self.SMtree.topLevelItem(1).child(3).child(4)
		
		#Pressure control
		grpPressAt              =    self.SMtree.topLevelItem(2).child(0)
		antiCellAt              =    self.SMtree.topLevelItem(2).child(1)
		consRatAt               =    self.SMtree.topLevelItem(2).child(2)
		consAreaAt              =    self.SMtree.topLevelItem(2).child(3)
		
		#Berendsen pressure bath 
		useBerenAt              =    self.SMtree.topLevelItem(2).child(4).child(0)
		targPressAt             =    self.SMtree.topLevelItem(2).child(4).child(1)
		berenCompAt             =    self.SMtree.topLevelItem(2).child(4).child(2)
		berenRelxAt             =    self.SMtree.topLevelItem(2).child(4).child(3)
		berenPressAt            =    self.SMtree.topLevelItem(2).child(4).child(4)
		
		#NOSE-HOOVer LANGEVIN PISTON
		useLangPAt              =    self.SMtree.topLevelItem(2).child(5).child(0)
		langTargAt              =    self.SMtree.topLevelItem(2).child(5).child(1)
		oscilPerAt              =    self.SMtree.topLevelItem(2).child(5).child(2)
		langDecayAt             =    self.SMtree.topLevelItem(2).child(5).child(3)
		langPTempAt             =    self.SMtree.topLevelItem(2).child(5).child(4)
		surfTenAt               =    self.SMtree.topLevelItem(2).child(5).child(5)
		strainXAt               =    self.SMtree.topLevelItem(2).child(5).child(6)
		strainYAt               =    self.SMtree.topLevelItem(2).child(5).child(7)
		strainZAt               =    self.SMtree.topLevelItem(2).child(5).child(8)
		exclPressAt             =    self.SMtree.topLevelItem(2).child(5).child(9)
		exclPressFileAt         =    self.SMtree.topLevelItem(2).child(5).child(10)
		exclPressColAt          =    self.SMtree.topLevelItem(2).child(5).child(11)
		
		
		#constant forces
		constForceAt            =    self.SMtree.topLevelItem(3).child(0).child(0)
		consFrcFileAt           =    self.SMtree.topLevelItem(3).child(0).child(1)
		
		#external electric field
		useEFieldAt             =    self.SMtree.topLevelItem(3).child(1).child(0)
		efieldXAt               =    self.SMtree.topLevelItem(3).child(1).child(1)
		efieldYAt               =    self.SMtree.topLevelItem(3).child(1).child(2)
		efieldZAt               =    self.SMtree.topLevelItem(3).child(1).child(3)
		
		#moving constraints
		movConstAt              =    self.SMtree.topLevelItem(3).child(2).child(0)
		velMoveXAt              =    self.SMtree.topLevelItem(3).child(2).child(1)
		velMoveYAt              =    self.SMtree.topLevelItem(3).child(2).child(2)
		velMoveZAt              =    self.SMtree.topLevelItem(3).child(2).child(3)
		
		
		#rotating constraints
		rotConsAt               =    self.SMtree.topLevelItem(3).child(3).child(0)
		rotAxisXAt              =    self.SMtree.topLevelItem(3).child(3).child(1)
		rotAxisYAt              =    self.SMtree.topLevelItem(3).child(3).child(2)
		rotAxisZAt              =    self.SMtree.topLevelItem(3).child(3).child(3)
		rotPivXAt               =    self.SMtree.topLevelItem(3).child(3).child(4)
		rotPivYAt               =    self.SMtree.topLevelItem(3).child(3).child(5)
		rotPivZAt               =    self.SMtree.topLevelItem(3).child(3).child(6)
		rotVelAt                =    self.SMtree.topLevelItem(3).child(3).child(7)
		
		#SMD parameters
		smdAt                   =    self.SMtree.topLevelItem(3).child(4).child(0)
		smdFileAt               =    self.SMtree.topLevelItem(3).child(4).child(1)
		smdkAt                  =    self.SMtree.topLevelItem(3).child(4).child(2)
		smdVelAt                =    self.SMtree.topLevelItem(3).child(4).child(3)
		smdDirXAt               =    self.SMtree.topLevelItem(3).child(4).child(4)
		smdDirYAt               =    self.SMtree.topLevelItem(3).child(4).child(5)
		smdDirZAt               =    self.SMtree.topLevelItem(3).child(4).child(6)
		smdOutAt                =    self.SMtree.topLevelItem(3).child(4).child(7)
		
		#utilizes the dictionary NAMDParmDict to initialize all the parameter variables and add them to the tree
		for trees in list(parmDict.keys()):
		    if trees == "PStree": tree = "PStree"
		    else:    tree = "SMtree"
		    for defaults in    parmDict[trees].keys():
		        if parmDict[trees][defaults][1] == "InputFile":
		            vars(self)[defaults] = InputFile(tree)
		            vars(self)[defaults].setEnabled(parmDict[trees][defaults][2])
		        elif parmDict[trees][defaults][1] == "CheckBox":
		            vars(self)[defaults] = CheckBox(tree)
		            vars(self)[defaults].setChecked(parmDict[trees][defaults][2])
		            vars(self)[defaults].setEnabled(parmDict[trees][defaults][3])
		            vars(self)[defaults].stateChanged.connect(self.storeValuesInState)
		        elif parmDict[trees][defaults][1] == "SpinBox":
		            vars(self)[defaults] = SpinBox(tree)
		            vars(self)[defaults].setSuffix(parmDict[trees][defaults][2])
		            vars(self)[defaults].setRange(parmDict[trees][defaults][3], parmDict[trees][defaults][4])
		            vars(self)[defaults].setEnabled(parmDict[trees][defaults][5])
		            vars(self)[defaults].setSingleStep(parmDict[trees][defaults][6])
		            vars(self)[defaults].setValues(parmDict[trees][defaults][0])
		            vars(self)[defaults].editingFinished.connect(self.storeValuesInState)
		        elif parmDict[trees][defaults][1] == "DoubleSpinBox":
		            vars(self)[defaults] = DoubleSpinBox(tree)
		            vars(self)[defaults].setSuffix(parmDict[trees][defaults][2])
		            vars(self)[defaults].setDecimals(parmDict[trees][defaults][3])
		            vars(self)[defaults].setRange(parmDict[trees][defaults][4], parmDict[trees][defaults][5])
		            vars(self)[defaults].setEnabled(parmDict[trees][defaults][6])
		            vars(self)[defaults].setSingleStep(parmDict[trees][defaults][7])
		            vars(self)[defaults].setValues(parmDict[trees][defaults][0])
		            vars(self)[defaults].editingFinished.connect(self.storeValuesInState)
		        elif parmDict[trees][defaults][1] == "ComboBox":
		            vars(self)[defaults] = ComboBox(tree)
		            cLen = len(parmDict[trees][defaults])
		            vars(self)[defaults].setEnabled(parmDict[trees][defaults][cLen - 1])
		            vars(self)[defaults].setCurrentIndex(parmDict[trees][defaults][0])
		            for y in range(2, cLen - 1):
		                vars(self)[defaults].addItem(parmDict[trees][defaults][y])
		            vars(self)[defaults].currentIndexChanged.connect(self.storeValuesInState)
		        vars(self)[tree].setItemWidget(vars()[defaults + "At"], 0, vars(self)[defaults]) #adds them all to the tree
		
		
		#sets the connections that need to be set before initilization
		self.pme.stateChanged.connect(self.pmeChanged)
		
		self.setValues(self.history.currentState().getSimTabValues())
		
		#sets the connections between parameters
		self.SMtree.resizeColumnToContents(0)
		self.cutoff.editingFinished.connect(self.checkCutoff)
		self.pairListDist.editingFinished.connect(self.checkCutoff)
		self.useSwitch.stateChanged.connect(self.useSwitchChanged)
		self.switchDist.editingFinished.connect(self.checkCutoff)
		self.const.stateChanged.connect(self.constChanged)
		self.selCons.stateChanged.connect(self.selConsChanged)
		self.fixAtm.stateChanged.connect(self.fixAtmChanged)
		self.useLang.stateChanged.connect(self.useLangChanged)
		self.timeBTemp.valueChanged.connect(self.tempResChanged)
		self.antiCell.stateChanged.connect(self.antiCellChanged)
		self.consRat.stateChanged.connect(self.consRatChanged)
		self.consArea.stateChanged.connect(self.consAreaChanged)
		#self.consArea.stateChanged.connect(self.pressureCons)
		#self.consRat.stateChanged.connect(self.pressureCons)
		self.useBeren.stateChanged.connect(self.berenState)
		self.useLangP.stateChanged.connect(self.useLangPChanged)
		self.constForce.stateChanged.connect(self.constFrcChanged)
		self.rotCons.stateChanged.connect(self.rotConsChanged)
		self.movConst.stateChanged.connect(self.movConstChanged)
		
		self.pmeGridSp.valueChanged.connect(self.pmeGridChanged)
		self.gridX.editingFinished.connect(self.pmeGridChanged)
		self.gridY.editingFinished.connect(self.pmeGridChanged)
		self.gridZ.editingFinished.connect(self.pmeGridChanged)
		self.FFTW.stateChanged.connect(self.pmeChanged)
		
		self.exclude.currentIndexChanged.connect(self.checkScale)
		self.useTempRe.stateChanged.connect(self.useTempReChanged)
		self.useEField.stateChanged.connect(self.eFieldChanged)
		
		self.SMtree.resizeColumnToContents(0)
		self.PStree.resizeColumnToContents(0)
		
		self.useTempReChanged()
	
		#================================ = QtGui.QProgressDialog("Configuring...", QtCore.QString(), 0, 8, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
		self.progressBar  = QtGui.QProgressDialog("Configuring...", QtCore.QString(), 0, 100, self,QtCore.Qt.Dialog|QtCore.Qt.FramelessWindowHint)
		self.progressBar.setWindowModality(QtCore.Qt.WindowModal)
		self.progressBar.setAutoClose(False)

		#self.progressBar.setRange(0,8)

		self.myLongTask = RunThread(self)
		self.myLongTask.notifyProgress.connect(self.onProgress)
		self.myLongTask.notifyFinishedProgress.connect(self.onFinishedProgress)

	
	def storeValuesInState(self, dummy=None):
		self.history.currentState().setSimTabValues(self.getValues())
	    
	def getValues(self):
	    '''
	    Returns a dictionary containing values of all the 
	    input widgets in the QTreeWidget
	    [inputWidgetObjectName] [value]
	    '''
	    picklesan = dict()
	    for elements in list(parmDict.keys()):
	        for defaults in    parmDict[elements].keys():
	            picklesan[defaults] = vars(self)[defaults].value()
	    return picklesan
	
	def setValues(self, initVal):
	    '''
	    Restores the values the input widgets in the QTreeWidget 
	    had before being closed.
	    :param initVal: dictionary that contains the values of all the inputWidgets in SimTab
	    '''
	    #print "SimTab setValues"
	    if initVal != None:
	        for elements in list(parmDict.keys()):
	            for defaults in    parmDict[elements].keys():
	                vars(self)[defaults].setValues(initVal[defaults])
	
	def setDefaultValues(self):
	    '''
	    Sets the default values in the input widgets 
	    using the default parameter dictionary
	    '''
	    for elements in list(parmDict.keys()):
	        for defaults in    parmDict[elements].keys():
	            vars(self)[defaults].setValues(parmDict[elements][defaults][0])
	
	def checkScale(self):
	    '''
	    Handles changes to the scaling QComboBox
	    '''
	    if self.exclude.currentIndex() > 2:
	        self.scaling.setEnabled(True)
	    else:
	        self.scaling.setEnabled(False)
	
	def eFieldChanged(self):
	    '''
	    Handles changes to the efield QCheckBox
	    '''
	    
	    self.efieldX.setEnabled(self.useEField.isChecked())
	    self.efieldY.setEnabled(self.useEField.isChecked())
	    self.efieldZ.setEnabled(self.useEField.isChecked())
	
	        
	        
	def constChanged(self):
	    '''
	    Handles changes to the const QCheckBox
	    '''
	        
	    self.harExp.setEnabled(self.const.isChecked())
	    self.pdbCons.setEnabled(self.const.isChecked())
	    self.pdbForc.setEnabled(self.const.isChecked())
	    self.pdbcol1.setEnabled(self.const.isChecked())
	    self.selCons.setEnabled(self.const.isChecked())    
	    self.selConsX.setEnabled(self.const.isChecked())
	    self.selConsY.setEnabled(self.const.isChecked())
	    self.selConsZ.setEnabled(self.const.isChecked())    
	
	
	def selConsChanged(self):
	    '''
	    Handles the changes in the selCons QCheckBox
	    '''
	    self.selConsX.setEnabled(self.selCons.isChecked())
	    self.selConsY.setEnabled(self.selCons.isChecked())
	    self.selConsZ.setEnabled(self.selCons.isChecked())
	    
	def tempRes(self):
	    '''
	    Handles the changes in the timeTRes SpinBox
	    '''
	    if self.timeTRes.value() != 0:
	        self.tempEq.setEnabled(True)
	    else:
	        self.tempEq.setEnabled(False)
	
	def constFrcChanged(self):
	    '''
	    Handles the changes in the constForce QCheckBox
	    '''
	    self.consFrcFile.setEnabled(self.constForce.isChecked())
	    
	def tempCoupChanged(self):
	    '''
	    Handles the changes in the tempCoup QCheckBox
	    '''
	    
	    self.tempBath.setEnabled(self.tempCoup.isChecked())
	    self.pdbTCol.setEnabled(self.tempCoup.isChecked())
	    self.pdbTCouple.setEnabled(self.tempCoup.isChecked())
	
	def berenState(self):
	    '''
	    Handles the changes in the berenState QCheckBox
	    '''
	    self.targPress.setEnabled(self.useBeren.isChecked())
	    self.berenComp.setEnabled(self.useBeren.isChecked())
	    self.berenRelx.setEnabled(self.useBeren.isChecked())
	    self.berenPress.setEnabled(self.useBeren.isChecked())
	
	def movConstChanged(self):
	    '''
	    Handles the changes in the movConst QCheckbox
	    '''
	    self.velMoveX.setEnabled(self.movConst.isChecked())
	    self.velMoveY.setEnabled(self.movConst.isChecked())
	    self.velMoveZ.setEnabled(self.movConst.isChecked())
	    
	def useLangPChanged(self):
	    '''
	    Handles the changes in the useLangP QCheckbox
	    '''
	    self.langTarg.setEnabled(self.useLangP.isChecked())
	    self.oscilPer.setEnabled(self.useLangP.isChecked())
	    self.langDecay.setEnabled(self.useLangP.isChecked())
	    self.langPTemp.setEnabled(self.useLangP.isChecked())
	    self.surfTen.setEnabled(self.useLangP.isChecked())
	    self.strainX.setEnabled(self.useLangP.isChecked())
	    self.strainY.setEnabled(self.useLangP.isChecked())
	    self.strainZ.setEnabled(self.useLangP.isChecked())
	    if self.useLangP.isChecked() and self.useLang.isChecked():
	    	self.langPTemp.setValue(self.langTemp.value())

	    #self.exclPress.setEnabled(self.useLangP.isChecked())
	    #if self.useLangP.isChecked() == False:
	    #    self.exclPressCol.setEnabled(self.exclPress.isChecked())
	    #    self.exclPressFile.setEnabled(self.exclPress.isChecked())
	
	def useTempReChanged(self):
	    '''
	    Handles the changes in the useTempRe QCheckbox
	    '''
	    self.timeBTemp.setEnabled(self.useTempRe.isChecked())
	    self.tempResEq.setEnabled(self.useTempRe.isChecked())
	    self.tempInc.setEnabled(self.useTempRe.isChecked())
	    self.resHold.setEnabled(self.useTempRe.isChecked())
	
	
	def antiCellChanged(self):
	    '''
	    Handles the changes in the antiCell QCheckbox
	    '''
	    #if self.consArea.isChecked() == 0:
	    #    self.consRat.setEnabled(self.antiCell.isChecked())
	    if not self.antiCell.isChecked():
	        self.consRat.setChecked(False)
	        self.consArea.setChecked(False)
	
	def consAreaChanged(self):
		'''
		Handles the changes in the antiCell QCheckbox
		'''
		if self.consArea.isChecked():
		    self.consRat.setChecked(False)
		    self.antiCell.setChecked(True)
	
	def consRatChanged(self):
		'''
		Handles the changes in the antiCell QCheckbox
		'''
		if self.consRat.isChecked():
			self.consArea.setChecked(False)
			self.antiCell.setChecked(True)
	
	def fixAtmChanged(self):
	    '''
	    Handles the changes in the fixAtm QCheckbox
	    '''
	    self.fixAtmCol.setEnabled(self.fixAtm.isChecked())
	    self.fixAtmForc.setEnabled(self.fixAtm.isChecked())
	    self.fixAtmFile.setEnabled(self.fixAtm.isChecked())
	
	def exclPressChanged(self):
	    '''
	    Handles the changes in the exclPress QCheckbox
	    '''
	    self.exclPressCol.setEnabled(self.exclPress.isChecked())
	    self.exclPressFile.setEnabled(self.exclPress.isChecked())
	
	def useLangChanged(self):
	    '''
	    Handles the changes in the useLang QCheckbox
	    '''
	    self.langTemp.setEnabled(self.useLang.isChecked())
	    self.langDamp.setEnabled(self.useLang.isChecked())
	    self.langHyd.setEnabled(self.useLang.isChecked())
	    self.pdbLang.setEnabled(self.useLang.isChecked())
	    self.pdbCol.setEnabled(self.useLang.isChecked())
	
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
	
	def pressureCons(self):
	    '''
	    Handles the changes in the consArea QCheckbox
	    '''
	    if self.consArea.isChecked():
	        self.consRat.setEnabled(False)
	        self.consRat.setChecked(False)
	    elif self.antiCell.isChecked():
	        self.consRat.setEnabled(True)
	    
	    if self.consRat.isChecked():
	        self.consArea.setEnabled(False)
	    else:
	        self.consArea.setEnabled(True)
	
	def useSwitchChanged(self):
	    '''
	    Handles the changes in the useSwitch QCheckbox
	    '''
	    self.switchDist.setEnabled(self.useSwitch.isChecked())    
	
	def stepsChanged(self):
	    '''
	    Handles the changes in the stepsCycle QSpinbox
	    '''
	    self.startStep.setSingleStep(self.stepsCycle.value())
	    if (self.startStep.value() % self.stepsCycle.value()) != 0:
	        self.startStep.setValues(0)
	
	def tempResChanged(self):
	    '''
	    Handles the changes in the timeBTemp QDoubleSpinbox
	    '''
	    if self.timeBTemp.value() != 0:
	        self.tempInc.setEnabled(True)
	        self.resHold.setEnabled(True)
	        self.tempResEq.setEnabled(True)
	    else:
	        self.tempInc.setEnabled(False)
	        self.resHold.setEnabled(False)
	        self.tempResEq.setEnabled(False)
	
	def rotConsChanged(self):
	    '''
	    Handles the changes in the rotCons QCheckbox
	    '''
	    self.rotAxisX.setEnabled(self.rotCons.isChecked())
	    self.rotAxisX.setEnabled(self.rotCons.isChecked())
	    self.rotAxisX.setEnabled(self.rotCons.isChecked())
	    self.rotPivX.setEnabled(self.rotCons.isChecked())
	    self.rotPivY.setEnabled(self.rotCons.isChecked())
	    self.rotPivZ.setEnabled(self.rotCons.isChecked())
	    self.rotVel.setEnabled(self.rotCons.isChecked())
	
	def pmeChanged(self):
	    '''
	    Handles the changes in the pme QCheckbox
	    '''
	    if self.pme.isChecked() and not self.history.currentState().drawer.hasCell():
	        message = QtGui.QMessageBox(1, "Help", "Particle Mesh Edwald cannot be used\nwithout periodic boundary conditions.\nUse the Setup tab to define them.")
	        message.exec_()
	        self.pme.nextCheckState()
	    self.pmeTol.setEnabled(self.pme.isChecked())
	    self.pmeGridSp.setEnabled(self.pme.isChecked())
	    self.pmeIn.setEnabled(self.pme.isChecked())
	    self.gridX.setEnabled(self.pme.isChecked())
	    self.gridY.setEnabled(self.pme.isChecked())
	    self.gridZ.setEnabled(self.pme.isChecked())
	    self.FFTFile.setEnabled(self.FFTW.isChecked())
	    
	    self.pmeGridChanged(silence=False)
	    
	    
	def pmeGridChanged(self, silence=False):
	    changed = False
	    gridSp = self.pmeGridSp.value()
	    cell = self.history.currentState().drawer.getCellBasisVectors()
	    #print "pmeGridChanged X",self.gridX.value(), math.ceil(cell[0][0]/gridSp)
	    #print "pmeGridChanged Y",self.gridY.value(), math.ceil(cell[1][1]/gridSp)
	    #print "pmeGridChanged Z",self.gridZ.value(), math.ceil(cell[2][2]/gridSp)
	    if self.pme.isChecked() and cell != None:
	        if self.gridX.value() < math.ceil(cell[0][0]/gridSp):
	            self.gridX.setValue(math.ceil(cell[0][0]/gridSp))
	            changed = True
	        if self.gridY.value() < math.ceil(cell[1][1]/gridSp):
	            self.gridY.setValue(math.ceil(cell[1][1]/gridSp))
	            changed = True
	        if self.gridZ.value() < math.ceil(cell[2][2]/gridSp):
	            self.gridZ.setValue(math.ceil(cell[2][2]/gridSp))
	            changed = True
	        if changed and not silence:
	            QtGui.QMessageBox(1, "Information", "A grid point number was changed to the minimum allowed value corresponding to the grid spacing and box dimensions.").exec_()
	
	def updateSimTab(self, minTab):
	    '''
	    Updates the simtab with the values the mintab has in some of it's objects
	    :param minTab: MinTab
	    '''
	
	    self.cutoff.setValues(minTab.cutoff.value()) 
	    self.pairListDist.setValues(minTab.pairListDist.value()) 
	    self.switchDist.setValues(minTab.switchDist.value())
	    self.useSwitch.setChecked(minTab.useSwitch.isChecked())
	    self.exclude.setCurrentIndex(minTab.exclusion.currentIndex())
	    self.scaling.setValues(minTab.scaling.value())
	    self.checkScale()    
	
	
	@QtCore.pyqtSlot()
	def on_saveButton_pressed(self):
	    '''
	    Calls the save function
	    '''
	    self.save()
	
	
	def save(self):
		'''
		Saves the current parameters in a .para (parameters) file the following way:
		[parm name] [value]
		'''
	
		from interface.main.WFileDialogs import WFileNameDialog
		d = WFileNameDialog(self, 'Save parameters', self.settings.currentMixtureLocation())
		if d.isReady():
		    confFile            =    self.wolffia.configurationFilesBasename() + ".para"
		    conf                =    open(confFile, mode="w")
		
		    for elements in list(parmDict.keys()):
		        for defaults in    parmDict[elements].keys():
		            conf.write(str(defaults) + " " + str(vars(self)[defaults].value()) + "\n") 
	
	@QtCore.pyqtSlot()
	def on_loadButton_pressed(self):
	    '''
	    Calls the load function
	    '''
	    self.load()
	
	def load(self):
	    '''
	    Loads the .para (parameters) file and uses it to re-assign the values to all the input widgets 
	    '''
	    import csv
	    parmFile = QtGui.QFileDialog.getOpenFileName(self, "Choose an .para file", self.settings.currentMixtureLocation())
	    if parmFile != '' and parmFile != ' ':
	        try:
	            csvread = csv.reader(open(parmFile, 'r'), delimiter=' ')
	            for line in csvread:
	                vars(self)[line[0]].setValues(line[1])
	        except:
	            info = QtGui.QErrorMessage(self)
	            info.setModal(True) # blocks Wolffia
	            info.showMessage("There's something evil in that file!")
	        
	@QtCore.pyqtSlot()
	def on_resetButton_pressed(self):
	    '''
	    Calls the setDefaultValues function
	    '''
	    self.setDefaultValues()
	
	
	def on_remoteButton_pressed(self):
	    from .ConnectionDialog import ConnectionDialog
	    connectDialog = ConnectionDialog(self, connection=self.remoteHost, logWidget=self.log)
	    connectDialog.exec_()
	    self.remoteHost = connectDialog.connection
	    if self.remoteHost == None:
	    	self.ui.remoteButton.setIcon(QtGui.QIcon().fromTheme("computer"))
	    else:
	    	self.ui.remoteButton.setIcon(QtGui.QIcon().fromTheme("network-wireless"))

	    
	def on_runButton_pressed(self):
	    '''
	    Checks if there's a simulation running, if not, then the
	    simulation starts and the button's text changes to 'pause'
	    and the stop button becomes enabled.
	    '''
	    
	    if self.ui.runButton.text() == "Run":
	        if (self.wolffia.simRunning == False):
	            #print self.__dict__   
	            if self.checkMD():
	                self.wolffia.simRunning = True
	            	self.pmeGridChanged()  # tests PME parameters
	                self.energyPlot1.reset()
	                self.energyPlot2.reset()
	                self.kineticsPlot1.reset()
	                self.kineticsPlot2.reset()
	                self.ui.runButton.setText("Pause")      
	                self.ui.runButton.setIcon(QtGui.QIcon().fromTheme("media-playback-pause",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "media-playback-pause.svg")    ))
	                self.ui.cancelButton.setEnabled(True)
	                #self.log.setLogMode("OFF")
	                self.log.clear()
	                self.runSim()
	                if self.simRun == None: self.cancelSim()
	            else:   return
	        else:
	            message = QtGui.QMessageBox(1, "Attention!"
	                , "There is a minimization or simulation running right now, it'd be horrible to run both of them at the same time!\n\n Just horrible...")
	            message.exec_()
	    elif self.ui.runButton.text() == "Pause":
	        self.pauseSim()
	
	    else:
	        self.continueSim()
	        
	def on_IOtreeWidget_expanded(self):
	    self.baseDir.setText(self.settings.currentMixtureLocation());
	    self.coordinatesFile.setText(self.wolffia.configurationFilesBasename() + ".coor");
	    self.structuresFile.setText (self.wolffia.configurationFilesBasename() + ".psf" );
	    self.parametersFile.setText (self.wolffia.configurationFilesBasename() + ".prm" );
	    self.outputFile.setText     (self.wolffia.configurationFilesBasename() + ".conf");
	    self.IOtree.resizeColumnToContents(0)
	
	def on_BasicTree_expanded(self):
	    self.PStree.resizeColumnToContents(0)
	
	def on_BasicTree_collapsed(self):
	    self.PStree.resizeColumnToContents(0)
	
	def on_AddTree_expanded(self):
	    self.SMtree.resizeColumnToContents(0)
	
	def on_AddTree_collapsed(self):
	    self.SMtree.resizeColumnToContents(0)
	
	def on_IOtreeWidget_collapsed(self):
	    self.IOtree.resizeColumnToContents(0)
	
	def on_simTimer(self):
		'''
		Gets the output from the MD package and sends it to
		the instances of EnergyPlot and KineticPlot class.
		Also checks if the thread is still alive.  
		'''
		#print "on_simTimer A"
		self.simTimer.stop()
		#print "on_simTimer B"
		currentTimeout = self.simTimer.interval()
		#print "on_simTimer C"
		namdOutput = self.simRun.getOutput()
		#print "on_simTimer D"
		#print "on_simTimer namdOutput", namdOutput, currentTimeout
		
		# with queue
		if WOLFFIA_USES_IMD:
			eQ = self.simRun.getEnergiesQ()
			while True:
				try:
					e = eQ.get_nowait()
					self.energyPlot1.addValuesFromIMD(e)
					self.energyPlot2.addValuesFromIMD(e)
				except queue.Empty:
					break
			
			# without queue
			#self.energyPlot1.addValuesFromIMD(self.simRun.getEnergies())
			#self.energyPlot2.addValuesFromIMD(self.simRun.getEnergies())
		
		#print "on_simTimer E"
		if namdOutput != None:
			#print "on_simTimer E0"
			self.checkError(namdOutput)
			#print "on_simTimer E1"
			if not WOLFFIA_USES_IMD:
			    self.energyPlot1.addValuesFromNamd(namdOutput)
			    self.energyPlot2.addValuesFromNamd(namdOutput)
			#print "on_simTimer E2"
			self.kineticsPlot1.addValuesFromNamd(namdOutput)
			#print "on_simTimer E3"
			self.kineticsPlot2.addValuesFromNamd(namdOutput)
			#print "on_simTimer E4"
			currentTimeout -= 10
		else:
			currentTimeout += 100
		#print "on_simTimer F"
		
		try:
		    if not self.simRun.isAlive():
		        self.simCoordTimer.stop()
		        self.ui.runButton.setText("Run")
		        self.ui.runButton.setIcon(QtGui.QIcon().fromTheme("media-playback-start",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "media-playback-start.svg")    ))
		        self.ui.resetButton.setIcon(QtGui.QIcon().fromTheme("emblem-default",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "emblem-default.png")    ))
		        self.wolffia.simRunning = False
		        self.ui.cancelButton.setEnabled(False)
		        #message = QtGui.QMessageBox(1, "Message", "Simulation has ended!")
		        self.wolffia.analysis.update()
		        #message.exec_()
		        return
		except:
		    print("on_simTimer problemas para detener")
		    pass
		#print "on_simTimer G"
		
		if currentTimeout > 0:
			self.simTimer.start(currentTimeout)
		else:
			self.simTimer.start(1)
		#print "on_simTimer fin"
	        
	def checkError(self, lineas):
	    '''
	    Checks the output for errors
	    :param lineas: An array of the MD package's output
	    '''
	    for lines in lineas:
	        if lines[0:5] == "ERROR" or lines[0:11] == "FATAL ERROR":
	            self.log.addMessage(lines, "WARNING")
	            return True
	        elif lines[0:4]    == "Info" or lines[0:3] == "LDB" or lines[0:7] == "Warning":
	            #print lines
	            self.log.addMessage(lines, "INFO")
	
	    #if errorMessage != "":
	        #message = QtGui.QMessageBox(1, "ERROR", lines)
	        #message.exec_()
	
	@QtCore.pyqtSlot()
	def on_cancelButton_pressed(self):
	    '''
	    Calls the cancelSim function
	    '''
	    self.cancelSim()
	
	        
	#--------------------------------------------------------------------------------
	def on_packButton_pressed(self):
	    '''
	    Compresses the whole mixture folder to whatever location the user specifies
	    '''
	    from .WFileDialogs import WFileNameDialog
	
	    d = WFileNameDialog(self, 'Save Zipped Files', self.settings.workingFolder, "Zip File (*.zip)")
	    if d.isReady():
			self.history.currentState().save()
						
			filename = str(d.fullFilename())
			if not filename.endswith(".zip"):
			    filename +=  ".zip"
			
			
			progress      = QtGui.QProgressDialog("Packing...", "Cancel", 
			                0, 2, 
			                self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
			progress.setWindowModality(QtCore.Qt.WindowModal)
			progress.setValue(0)
			progress.forceShow()
			
			# update files
			#print "packing options ", Configuration.CURRENT_FOLDER|Configuration.NO_IMD_WAIT
			conf = Configuration(self.__dict__, self.history.currentState().getDrawer(), self.history.currentState().fixedMolecules.hasFixedMolecules(), confOptions=Configuration.CURRENT_FOLDER|Configuration.NO_IMD_WAIT)
			conf.writeSimulationConfig(str(self.settings.currentMixtureLocation()), self.history.currentState().getMixture().getMixtureName())
			progress.setValue(1)
			
			extensionsNotPacked = self.history.currentState().packFiles(self.wolffia.configurationFilesBasename(),filename)
			
			progress.hide()
			if not progress.wasCanceled():
			    if extensionsNotPacked == "":
			        reply = QtGui.QMessageBox.information(self, "Success", 
			                "The " + self.history.currentState().getMixtureName() + " files have been successfully packed in " + filename + ".",)
			    else:
			        reply = QtGui.QMessageBox.warning(self, "Files not found", 
			                "The files with extensions " + extensionsNotPacked + " were not found in mixture "
			                + self.history.currentState().getMixtureName() + ".  Other files have been successfully packed in " + filename + ".\nOnly the extensions .conf, .pdb, .prm and .psf are strictly necessary.",)
	
	
	
	def cancelSim(self):
	    if self.simRun != None:
	    	try: self.simRun.cancel()
	    	except:
				print("SimTab.cancelSim: Problem cancelling simulation. Communications lost?")
	    self.simTimer.stop()
	    self.simCoordTimer.stop()
	    self.wolffia.simRunning = False
	    self.ui.cancelButton.setEnabled(False)
	    self.ui.runButton.setEnabled(False)
	    if self.simRun != None: self.updateCoordinates()
	    print("cancelSim Simulation has been canceled.")
	    self.ui.runButton.setText("Run")
	    self.ui.runButton.setIcon(QtGui.QIcon().fromTheme("media-playback-start",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "media-playback-start.svg")    ))
	    self.ui.runButton.setEnabled(True)
	    if self.simRun != None: self.simRun.stop()
	
	def pauseSim(self):
	    self.simTimer.stop()
	    self.simCoordTimer.stop()
	    self.simRun.pause()
	    self.ui.runButton.setText("Continue")
	    #self.wolffia.lightbulb('pause')
	
	def continueSim(self):
	    '''
	    Continues a simulation by signaling the process.
	    '''
	    self.simTimer.start(self._PLOT_TIMER_TIMEOUT_)
	    self.simCoordTimer.start(self._VIEWER_TIMER_TIMEOUT_)
	    self.simRun.resume()
	        
	    self.ui.runButton.setText("Pause")
	    #self.wolffia.lightbulb('on')
	
	def on_simCoordTimer(self):
	    """
	        Gets called by simCoordTimer to call updateCoordinates.
	        Takes no parameters
	        
	    """
	  
	    start = time.clock()
	    self.simCoordTimer.stop()
	    #self.updateCoordinates()
	    if self.updateCoordinates():
	        elapsedTime = time.clock()-start
	        self.simCoordTimer.start(elapsedTime*3000)
	        #print "on_simCoordTimer elapsedTime", elapsedTime
	    else:
	        self.simCoordTimer.start(self._VIEWER_TIMER_TIMEOUT_ * 1.5)
	    #print "on_simCoordTimer termino"
	
	def update(self):
	    self.setValues(self.history.currentState().getSimTabValues())
	    
	    	
	def updateCoordinates(self):
	    
	    """
	        Updates the coordinates on the mixtureViewer.
	        state -- The current wolffia state
	    """
	    #print "SimTab updateCoordinates in", self.preview.isVisible()
	    if self.simRun.coordinatesAreNew():
	        #print "SimTab updateCoordinates coordinatesAreNew"
	        self.simRun.updateCoordinates(self.history.currentState().getMixture())
	        q = self.simRun.getCoordinatesQ()  # empty coords queue
	        if self.history.currentState().hasBox():
		        box = self.simRun.cell.getBox()
		        if box != None:
		            self.history.currentState().getDrawer().setCellBasisVectors(box[0])
		            self.history.currentState().getDrawer().setCellOrigin(box[1])
		            self.wolffia.setupTab.update()
	
	        #print "updateCoordinates simRun.updateCoordinates"
	        self.preview.update(adjustViewingVolume=False)
	        self.wolffia.analysis.update()
	        #print "updateCoordinates out true"
	        return True
	    #print "SimTab updateCoordinates out false"
	    return False
	
	def updateEnergyPlots(self, e):	
		self.energyPlot1.addValuesFromIMD(e)
		self.energyPlot2.addValuesFromIMD(e)
	
	def runSim2(self):
		self.progressBar.open()
		self.progressBar.setAutoClose(True)
		self.myLongTask.start()

	def onProgress(self, i):
		self.progressBar.setValue(i)
		
	def onFinishedProgress(self):
		self.progressBar.close()
		
	def runSim(self):
		"""
		 Sets up the configuration, the run thread and the timer for polling the simulation. 
		"""
		progress      = QtGui.QProgressDialog("Configuring...", QtCore.QString(), 0, 8, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
		progress.setWindowModality(QtCore.Qt.WindowModal)
		progress.setWindowTitle("Simulation")
		progress.setValue(0)
		QtGui.QApplication.processEvents()
		
		QtGui.QApplication.processEvents()
		self.history.push(force=True)
		
		progress.setValue(1)
		QtGui.QApplication.processEvents()
		
		if self.remoteHost != None:
			conf = Configuration(self.__dict__, self.history.currentState().getDrawer(), self.history.currentState().fixedMolecules.hasFixedMolecules(), Configuration.CURRENT_FOLDER)
		else:
			conf = Configuration(self.__dict__, self.history.currentState().getDrawer(), self.history.currentState().fixedMolecules.hasFixedMolecules())

		try:
			conf.writeSimulationConfig(str(self.settings.currentMixtureLocation()), self.history.currentState().getMixture().getMixtureName())
		except ConfigurationError as e:
		    Error = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Error!", e.message)
		    Error.exec_()
		    return
		
		progress.setValue(2)
		QtGui.QApplication.processEvents()
		progress.setLabelText("Writing files...")
		try:
		    self.history.currentState().writeFiles(self.wolffia.configurationFilesBasename())
		except Exception as  e:
			Error = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Error!", e.message)
			Error.exec_()
			progress.cancel()
			progress.hide()
			return
		#self.history.currentState().save()
		
		progress.setValue(3)
		progress.setLabelText("Starting namd...")
		if WOLFFIA_USES_IMD:
			if self.remoteHost != None: 
				#conf.setBuildDirectory(self.remoteHost.getWorkingDir())
				print("SimTab runSim", self.wolffia.configurationFilesBasename())
				zipName = self.wolffia.configurationFilesBasename() + ".zip"
				self.history.currentState().packFiles(self.wolffia.configurationFilesBasename(), zipName)
				progress.setValue(4)
				self.remoteHost.sendFile(zipName, unzip=True)
				progress.setValue(5)
				self.simRun = ImdSimThread(conf, remoteHost=self.remoteHost,port=conf.getImdPort())
			else:
				self.simRun = ImdSimThread(conf, namdLocation=str(self.settings.namdLocation),port=conf.getImdPort())
			#self.simRun.setEnergiesCallback(self.updateEnergyPlots)
		else:
		    self.simRun = SimThread(conf, str(self.settings.namdLocation))
		
		progress.setValue(6)
		self.wolffia.saveWolffiaState()
		self.simRun.start()
		
		progress.setValue(7)
		progress.setLabelText("Starting clocks...")
		#starts up the clocks again
		self.simTimer.start(self._PLOT_TIMER_TIMEOUT_)
		
		self.simCoordTimer.start(self._VIEWER_TIMER_TIMEOUT_)
		progress.setValue(8)
		progress.hide()
	
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
	
	def reset(self):
	    '''
	    Resets the minTab by placing the default values, stopping
	    the simulation (if any) and stopping the timers.
	    '''
	    self.setDefaultValues()
	    self.preview.reset()
	    try:
	        self.cancelSim()       
	        self.simTimer.stop()
	        self.simCoordTimer.stop()
	        
	    except:
	        
	        print ("SimTab_ reset_ Failed")
        
class RunThread(QtCore.QThread):
	notifyProgress = QtCore.pyqtSignal(int)
	notifyFinishedProgress = QtCore.pyqtSignal()
	def __init__(self, simRun):
		super(RunThread, self).__init__()
		self.sim = simRun
		
	def run(self):
		"""
		 Sets up the configuration, the run thread and the timer for polling the simulation. 
		"""
		self.sim.progressBar.setLabelText("Configuring...")
		self.notifyProgress.emit(10)
		
		self.sim.history.push(force=True)
		
		self.notifyProgress.emit(20)
		
		if self.sim.remoteHost != None:
			conf = Configuration(self.sim.__dict__, self.sim.history.currentState().getDrawer(), self.sim.history.currentState().fixedMolecules.hasFixedMolecules(), Configuration.CURRENT_FOLDER)
		else:
			conf = Configuration(self.sim.__dict__, self.sim.history.currentState().getDrawer(), self.sim.history.currentState().fixedMolecules.hasFixedMolecules())
	
		try:
			conf.writeSimulationConfig(str(self.sim.settings.currentMixtureLocation()), self.sim.history.currentState().getMixture().getMixtureName())
		except ConfigurationError as e:
		    Error = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Error!", e.message)
		    Error.exec_()
		    return
		
		self.notifyProgress.emit(30)
		self.sim.progressBar.setLabelText("Writing files...")
		self.sim.history.currentState().writeFiles(self.sim.wolffia.configurationFilesBasename())
		self.notifyProgress.emit(40)
		#self.sim.history.currentState().save()
		
		#progress.setLabelText("Starting namd...")
		if WOLFFIA_USES_IMD:
			if self.sim.remoteHost != None: 
				#conf.setBuildDirectory(self.remoteHost.getWorkingDir())
				print("SimTab runSim", self.sim.wolffia.configurationFilesBasename())
				zipName = self.sim.wolffia.configurationFilesBasename() + ".zip"
	
				self.sim.progressBar.setLabelText("Packing files...")
				self.sim.history.currentState().packFiles(self.sim.wolffia.configurationFilesBasename(), zipName, progressSignal=self.notifyProgress)
	
				self.sim.progressBar.setLabelText("Starting remote simulation...")
				self.notifyProgress.emit(10)
				self.sim.remoteHost.sendFile(zipName, unzip=True)
				self.notifyProgress.emit(50)
				self.sim.simRun = ImdSimThread(conf, remoteHost=self.sim.remoteHost,port=conf.getImdPort())
			else:
				self.sim.simRun = ImdSimThread(conf, namdLocation=str(self.sim.settings.namdLocation),port=conf.getImdPort())
				self.notifyProgress.emit(50)
			#self.simRun.setEnergiesCallback(self.updateEnergyPlots)
		else:
			self.sim.simRun = SimThread(conf, str(self.sim.settings.namdLocation))
		
		self.sim.progressBar.setLabelText("Saving state...")
		#self.notifyProgress.emit(10)
		self.sim.wolffia.saveWolffiaState()
		self.notifyProgress.emit(70)
		self.sim.simRun.start()
		
		self.notifyProgress.emit(80)
		#progress.setLabelText("Starting clocks...")
		#starts up the clocks again
		self.sim.simTimer.start(self.sim._PLOT_TIMER_TIMEOUT_)
		
		self.sim.simCoordTimer.start(self.sim._VIEWER_TIMER_TIMEOUT_)
		self.notifyProgress.emit(90)
		self.notifyFinishedProgress.emit()
		#progress.hide()

#================================================================================================

if __name__ == '__main__':
    
    app            =    QtGui.QApplication(sys.argv)
    editor            =    SimTab()
    editor.show()
    sys.exit(app.exec_())
