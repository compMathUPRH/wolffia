
from conf.Wolffia_conf import _WOLFFIA_OS, WOLFFIA_USES_IMD
from wolffialib.Container import Container

import random


class Configuration(object):
	SIMULATION   = 1
	MINIMIZATION = 2
	
	CURRENT_FOLDER = 0x1
	NO_IMD_WAIT    = True
	
	_CHECKED_BOOL_TO_WORD_    = {True:"yes", False:"no"}
	MINIMIZATION_DEFAULT_PARAMETERS = {'restartSteps':1000, 'trajectorySteps':1000,'energySteps':20,'cutoff':12.0, 'useSwitch':True, 'switchDist':11.0, 'pairListDist':13.0, 'exclude':'1-2', 'scaling':1.0,'minTinyStep':1.0e-6,'minBabyStep':1.0e-2,'minLineGoal':1.0e-4,'minSteps':10000, 'DCDfreq':1000,'outputEnergies':1000, 'switching':True,'exclude':'1-2', 'pairlistdist':13,'switchdist':9,'IMDon':'off'}
	SIMULATION_DEFAULT_PARAMETERS = {'langevin':'on','langevinTemp':295, 'langevinDamping':1.0, 'langevinHydrogen':'yes', 'LangevinPiston':'off', 'LangevinPistonDecay':100,'LangevinPistonPeriod':200,'LangevinPistonTarget':1.01325, 'DCDfreq':1000,'seed':random.randint(1,40000), 'temperature':295.0, 'pairlistsPerCycle':2,'pairlistMinProcs':1,'margin':0,'hgroupCutoff':2.5,'splitPatch':'hydrogen','scaling':1,'exclude':'1-2', 'pairlistdist':13,'switchdist':9, 'switching':True, 'timeSteps':1.0, 'numSteps':10000, 'startStep':0, 'stepsCycle':1,'restartSteps':1000,'outputEnergies':1000,'cutoff':12,'IMDon':'off'}
    
	def __init__(self, parameters=None, container=Container(), fixedAtoms=False, simType=SIMULATION, confOptions=0x0):
		#self.__dict__.update(parameters.__dict__)

		if parameters == None:
		    if simType == self.MINIMIZATION:
		        self.__dict__.update(self.MINIMIZATION_DEFAULT_PARAMETERS)
		    else:
		        self.__dict__.update(self.SIMULATION_DEFAULT_PARAMETERS)
        
		self.container         = container
		self.fixedAtoms     = fixedAtoms
		self.filename       = None
		self.buildDirectory = None
		self.simType        = simType
		random.seed()
		self.imdPort        = random.randint(30000,40000)
	    
		#print("Configuration __init__ ", confOptions)
		if confOptions & self.NO_IMD_WAIT: self.imdWait = "no"
		else: self.imdWait = "yes"
	    
	
	
	def getImdPort(self): return self.imdPort
	
	
	def getBuildDirectory(self):  return self.buildDirectory
	def setBuildDirectory(self, d):  self.buildDirectory = d
	
	
	def getFilename(self):  return self.filename
	
	
	def getMixtureName(self): return self.mixtureName
	
	
	def openFile(self, buildDirectory, mixtureName):
	    self.buildDirectory = buildDirectory
	    if _WOLFFIA_OS == "Windows":
	        if self.buildDirectory[-1] != "\\": self.buildDirectory.append("\\")
	        self.buildDirectory = str(buildDirectory.replace('\\' , "\\\\"))
	    else:
	        if self.buildDirectory[-1] != "/": self.buildDirectory += "/"

	    self.mixtureName = mixtureName
	    self.filename =    self.buildDirectory  + mixtureName + ".conf"
	    conf          =    open(self.filename, mode="w")
	
	    return conf
	
	def writeCutOffs(self, conf):
	    conf.write("\n# CutOffs\n")
	    conf.write("   cutoff   " + str(self.cutoff) + "\n")
	    conf.write("   switching   " + str(self._CHECKED_BOOL_TO_WORD_[self.switching]) + "\n")
	    if self.switching:
	        conf.write("   switchdist   " + str(self.switchdist) + "\n")
	    conf.write("   pairlistdist   " + str(self.pairlistdist) + "\n")
	    conf.write("   exclude   %s\n" % (self.exclude))
	    conf.write("   1-4scaling   %.2f" % ( self.scaling))
	    
	    
	def writeMinimizationParameters(self, conf):
	    conf.write("\n\n#Parameters for minimization, some of these will be passed on to the actual simulation configuration file\nminBabyStep   %.10f\nminTinyStep   %.10f\nminLineGoal   %.10f\nnumsteps   %d\n" % 
	               (self.minBabyStep, 
	                self.minTinyStep, 
	                self.minLineGoal, 
	                self.minSteps))
	
	def _writeIfDefined(self, conf, pars):
	    for k in pars:
	        try: conf.write('   ' + str(k) + '   ' + str(self.__dict__[k]) + '\n')
	        except KeyError:  pass

	def writeConf(self, conf):
	    conf.write("\n#TIMESTEP PARAMETERS\n")
	    conf.write("   timestep   %.4f\n   numsteps   %d\n   firsttimestep   %d\n   stepspercycle   %d\n" % (self.timeSteps, self.numSteps, self.startStep, self.stepsCycle))
	    
	    
	    conf.write("\n#SIMULATION SPACE PARTITIONING\n")
	    # all of these have default values
	    self._writeIfDefined(conf, ['splitPatch', 'hgroupCutoff', 'margin', 'pairlistMinProcs', 'pairlistsPerCycle', 'outputPairlists', 'pairShrink', 'pairGrow', 'pairTrigger'])

	    conf.write("\n\n###Basic Dynamics###\n   temperature   %.10f\n   seed   %d\n" % (self.temperature, self.seed))
	    self._writeIfDefined(conf, ['COMmotion', 'dielectric','rigidBonds','rigidTolerance','rigidIterations','useSettle'])
    
	    #PME params
	    if 'PME' in self.__dict__ and self.PME == 'yes':
	        conf.write("\n\n###PME PARMS###\n   PME   yes\n")
	        self._writeIfDefined(conf, ['PMEGridSpacing','PMETolerance','PMEInterpOrder','PMEGridSizeX','PMEGridSizeY','PMEGridSizeZ','PMEProcessors','FFTWEstimate','FFTWUseWisdom','FFTWWisdomFile'])
	    
	    #FULL DIRECT PARAMS
	    self._writeIfDefined(conf, ['FullDirect'])
	    
	    #Multiple timesteps # 
	    conf.write("\n\n###Multiple timestep parameters###")
	    self._writeIfDefined(conf, ['fullElectFrequency','nonBondedFreq','MTSAlgorithm','longSplitting','molly','mollyTolerance','mollyIterations'])
	    
	    ''' TO BE CHANGED............
	    #Harmonic constraint params
	    if self.const.isChecked():
	        conf.write("\n\n####HARMONIC CONSTRAINT PARAMETERS###\nconstraints   on\nconsexp   " + str(self.harExp.value()))
	        if self.pdbCons.text() != "default" and self.pdbCons.text() != '':
	            conf.write("\nconsref   " + str(self.pdbCons.text()))
	        else:
	            raise ConfigurationError("You did not specify a PDB file containing the constraint reference positions! \n Exit.")
	            #Error = QtGui.QMessageBox(3, "Error!", )
	            #Error.exec_()
	            #return
	        if self.pdbForc.text() != "default" and self.pdbForc.text() != '':
	            conf.write("\nconskfile   " + str(self.pdbForc.text()))
	        else:
	            raise ConfigurationError("You did not specify a PDB file containing the force constant values! \n Exit.")
	            #Error = QtGui.QMessageBox(3, "Error!", 
	            #Error.exec_()
	            #return
	        conf.write("\nconskcol   " + str(self.pdbcol1.itemText(self.pdbcol1.currentIndex()))) 
	        if self.selCons.isChecked():
	            conf.write("\nselectConstraints   %s\nselectConstrX   %s\nselectConstrY   %s\nselectConstrZ   %s" % ((self._CHECKED_BOOL_TO_WORD_[self.selCons.isChecked()]), (self._CHECKED_BOOL_TO_WORD_[self.selConsX.isChecked()]), (self._CHECKED_BOOL_TO_WORD_[self.selConsY.isChecked()]), (self._CHECKED_BOOL_TO_WORD_[self.selConsZ.isChecked()])))
	    '''
        
	    #langevin dynamics 
	    if 'langevin' in self.__dict__ and self.langevin == 'on':
	        conf.write("\n\n###LANGEVIN DYNAMICS###\n   langevin   on")
	        if 'langevinTemp' not in  self.__dict__:
	            print("You did not set a temperature for langevin calculations!\nTemperature will be set to 295.")
	            conf.write("\n   langevinTemp   295")
	            self.langevinTemp = 295
	        else:
	            conf.write("\n   langevinTemp   " + str(self.langevinTemp)+"\n")
	        self._writeIfDefined(conf, ['langevinDamping','langevinHydrogen','langevinFile','langevinCol'])
                


	    ''' TO BE CHANGED............ 
	    #temperature coupling
	    if self.tempCoup.isChecked():
	        conf.write("\n\n###Temperature Coupling###\ntCouple   on")
	        if self.tempBath.value() == 0:
	            print("No values given to tCoupleTemp! \nGiving it a default value of 1.")
	            conf.write("\ntCoupleTemp   1.00")
	        else:
	            conf.write("\ntCoupleTemp   " + str(self.tempBath.value()))
	        if self.pdbTCouple.text() != "default" and self.pdbTCouple.text() != '':
	            conf.write("\ntCoupleFile   " + str(self.pdbTCol.text()))
	        conf.write("\ntCoupleCol   " + str(self.pdbTCol.itemText(self.pdbTCol.currentIndex())))
	        
	    #temp rescaling
	    if self.timeTRes.value() != 0:
	        conf.write("\n\n###Temperature Rescaling###\nrescaleFreq   " + str(self.timeTRes.value()))
	        if self.tempEq.value() == 0:
	            print("No value given to rescaleTemp! \n Giving it a default value of 1.")
	            conf.write("\nrescaleTemp   1")
	        else:
	            conf.write("\nrescaleTemp   " + str(self.tempEq.value()))
	    
	    
	    #temperature reassignment
	    if self.useTempRe.isChecked():
	        conf.write("\n\n###temperature reassignment###\nreassignFreq   " + str(self.timeBTemp.value()))
	        if self.tempResEq.value() != 0:            
	            conf.write("\nreassignTemp   " + str(self.tempResEq.value()))
	        conf.write("\nreassignIncr   " + str(self.tempInc.value()))
	        if self.resHold.value() == 0:
	            print("No value given to reassignHold! \n Giving it a default value of 1.")
	            conf.write("\nreassignHold   1")
	        else:
	            conf.write("\nreassignHold   " + str(self.resHold.value()))
	    
	    #pressure control up the wazhoozy
	    if self.grpPress.isChecked() or self.antiCell.isChecked():
	        conf.write("\n\n###Pressure Control Parameters###")
	    if self.grpPress.isChecked():
	        conf.write("\n\n###Pressure Control Parameters###\n   useGroupPressure   on")
	    if self.antiCell.isChecked():
	        conf.write("\n   useFlexibleCell   " + str((self._CHECKED_BOOL_TO_WORD_[self.antiCell.isChecked()])))
	        conf.write("\n   useConstantRatio   " + str((self._CHECKED_BOOL_TO_WORD_[self.consRat.isChecked()]))) 
	        conf.write("\n   useConstantArea   " + str((self._CHECKED_BOOL_TO_WORD_[self.consArea.isChecked()]))) 
	    
	    #berendsen pressara bath
	    if self.useBeren.isChecked() != False:
	        conf.write("\n\n###Berendsen Pressure Bath Coupling###\n   BerendsenPressure   on")
	        if self.targPress.value() == 0:
	            print("No value given to target pressure for Berendsen Pressure Bath coupling \n Giving it a default value of 1.")
	            conf.write("\n   BerendsenPressureTarget   1")
	        else:
	            conf.write("\n   BerendsenPressureTarget   " + str(self.targPress.value()))
	        if self.berenComp.value() == 0:
	            print("No value given to compressibility for Berendsen Pressure Bath coupling \n Giving it a default value of 1.")
	            conf.write("\n   BerendsenPressureCompressibility   1")
	        else:
	            conf.write("\n   BerendsenPressureCompressibility   " + str(self.berenComp.value()))
	        if self.berenRelx.value() == 0:
	            print("No value given to relaxation time for Berendsen Pressure Bath coupling \n Giving it a default value of 1.")
	            conf.write("\n   BerendsenPressureRelaxationTime   1")
	        else:
	            conf.write("\n   BerendsenPressureRelaxationTime   " + str(self.berenRelx.value()))
	        if self.berenPress.value() != 0:
	            conf.write("\n   BerendsenPressureFreq   " + str(self.berenPress.value()))
        '''
        
	    #nose hooving something machinka
	    if 'LangevinPiston' in self.__dict__ and self.LangevinPiston == 'on':
	        conf.write("\n\n###Nose-Hoover Langevin Piston Pressure Control###\n   LangevinPiston   on\n")
	        try:
	            conf.write("   LangevinPistonTarget   " + str(self.LangevinPistonTarget))
	            conf.write("\n   LangevinPistonPeriod   " + str(self.LangevinPistonPeriod))
	            conf.write("\n   LangevinPistonDecay   " + str(self.LangevinPistonDecay))
                
	            try: conf.write("\n   LangevinPistonTemp   " + str(self.LangevinPistonTemp))
	            except:
	                try: conf.write("\n   LangevinPistonTemp   " + str(self.langevinTemp))
	                except: conf.write("\n   LangevinPistonTemp   295")
                    
	        except:
	            print("Message from Wolffia:\n \n You did not give a required value to Nose-Hoover Langevin Piston Pressure Control!\n")
	    if 'sasa' in self.__dict__ and self.sasa == 'on':
	            self._writeIfDefined(conf, ['sasa','SurfaceTension'])
	        #if self.exclPress.isChecked():
	        #    conf.write("\nExcludeFromPressure   on")
	         #   if self.exclPressFile.text() != "default" and self.exclPressFile.text() != '':
	         #       conf.write("\nExcludeFromPressureFile   " + str(self.exclPressFile.text()))
	         #   conf.write("\nExcludeFromPressureCol   " + str(self.exclPressCol.itemText(self.exclPressCol.currentIndex())))
	    
	    ''' TO BE CHANGED............
	    #External electric field
	    if self.useEField.isChecked():
	        conf.write("\n\n###External Electric Field###\neFieldOn   yes")
	        conf.write("\neField   " + str(self.efieldX.value()) + " " + str(self.efieldY.value()) + " " + str(self.efieldZ.value()))
	    
	    #Moving constraints
	    if self.movConst.isChecked():
	        conf.write("\n\n###Moving Constraints###\nmovingConstraints   on")
	        conf.write("\nmovingConsVel   " + str(self.velMoveX.value()) + " " + str(self.velMoveY.value()) + " " + str(self.velMoveZ.value()))
	        
	    
	    #rotating constraints
	    if self.rotCons.isChecked():
	        conf.write("\n\n###Rotating Constraints###\nrotConstraints   on")
	        conf.write("\nrotConsAxis   " + str(self.rotAxisX.value()) + " " + str(self.rotAxisY.value()) + " " + str(self.rotAxisZ.value()))
	        conf.write("\nrotConsPivot   " + str(self.rotPivX.value()) + " " + str(self.rotPivY.value()) + " " + str(self.rotPivZ.value()))
	        conf.write("\nrotConsVel   " + str(self.rotVel.value()))
	    
	    #SMD parameters
	    if self.smd.isChecked():
	        conf.write("\n\n###Steered molecular dynamics###\nSMD   on")
	        if self.smdFile.text() == "default":
	            print("Hey, you forgot to name the file for SMD constraints! \nExit")
	            return
	        else:
	            conf.write("\nSMDFile   " + self.smdFile.text())
	        conf.write("\nSMDk   " + str(self.smdk.value())) 
	        conf.write("\nSMDVel   " + str(self.smdVel.value())) 
	        conf.write("\nSMDDir   " + str(self.smdDirX.value()) + " " + str(self.smdDirY.value()) + " " + str(self.smdDirZ.value()))
	        conf.write("\nSMDOutputFreq   " + str(self.smdOut.value()))
        '''
	       
	
	def writeFixedAtomsParameters(self, conf):
	    #fixed atoms parameters
	    if self.fixedAtoms:
	        conf.write("\n\n###FIXED ATOMS PARAMETERS###\n   fixedAtoms   on\n   fixedAtomsForces   off" )
	        conf.write("\n   fixedAtomsCol   O\n")
	    
	            
	def writeHeader(self, conf):
	    conf.write("#Configuration file created by Wolffia\n\n#Configuration Parameters\n")
	
	
	def writeIOSection(self, conf, buildDirectory, mixtureName):
	    conf.write("\n#Input/Output section\n   #Working directory.  (change for manual run)\n")
	    conf.write("   #set basedir    \""    +    buildDirectory  + "\"\n")
	    conf.write("   set basedir   ./\n")
	    conf.write("\n   #File names, types and update frequencies.\n")
	    conf.write("   structure     \"$basedir/"  +    mixtureName + ".psf\"\n")
	    conf.write("   coordinates   \"$basedir/"  + mixtureName + ".pdb\"\n")
	    conf.write("   #extendedSystem   \"$basedir/"  + mixtureName + ".xsc\"\n")
	    conf.write("   binaryoutput no\n") #Needs to be off to be able to read the coordinates
	    conf.write("\n   parameters    \"$basedir/"  + mixtureName + ".prm\"\n")
	    conf.write("   paraTypeCharmm on\n")
	    conf.write("\n   restartname \"$basedir/" + mixtureName  + "\"\n")
	    #print(self.__dict__.keys())
	    conf.write("   restartfreq " + str(self.restartSteps) +  "\n")
	    conf.write("   binaryrestart no\n")
	    conf.write("\n   outputname   \""    +    mixtureName + "\"\n")
	    conf.write("   DCDfile   \"$basedir/%s\"\n   DCDfreq %s\n" % (str(mixtureName + ".dcd"), str(self.DCDfreq)))
	    try:
	        conf.write("\n   IMDon " + self.IMDon + "\n   IMDport " + str(self.imdPort)  + "\n   IMDfreq " + str(self.DCDfreq) +  "\n   IMDwait " + self.imdWait + "\n   IMDignore no\n")
	    except:
	        conf.write("\n   IMDon off\n")
	    conf.write("\n   outputEnergies " + str(self.outputEnergies) +  "\n")
	    #print("writeIOSection", self.restartSteps.value())
	    conf.write("\n   outputTiming  " + str(self.outputEnergies) +  "\n")
	
	
	def writePBCsection(self, conf, boudary):
	    '''
	    PERIODIC BOUNDARY CNDITIONS (MIRGERY & SOTERO)
	    '''
	    
	    if boudary.hasCell():
	        conf.write("\n#Periodic Boundary Conditions section\n")
	        [v1,v2,v3] = boudary.getCellBasisVectors()
	        origin = boudary.getCellOrigin()
	        conf.write("   cellBasisVector1 " + str(v1[0]) + "  "  + str(v1[1]) + "  "  + str(v1[2]) + "\n")
	        conf.write("   cellBasisVector2 " + str(v2[0]) + "  "  + str(v2[1]) + "  "  + str(v2[2]) + "\n")
	        conf.write("   cellBasisVector3 " + str(v3[0]) + "  "  + str(v3[1]) + "  "  + str(v3[2]) + "\n")
	        conf.write("   cellOrigin "       + str(origin[0]) + "  "  + str(origin[1]) + "  "  + str(origin[2]) + "\n")
	        conf.write("   wrapWater "        + self._CHECKED_BOOL_TO_WORD_[boudary.getWrapWater()] + "\n")
	        conf.write("   wrapAll "        + self._CHECKED_BOOL_TO_WORD_[boudary.getWrapAllMolecules()] + "\n")
	
	
	def writeSimulationType(self, conf):
	    if self.simType == Configuration.MINIMIZATION:
	        conf.write("\nminimization   on      # minimization enabled\n")
	    else:
	        conf.write("\n# This is an MD simulation\n")
	    
	    
	def writeSimulationConfig(self, buildDirectory, mixtureName):
	    """
	     Writes the configuration file for the MD simulation. 
	    """
	    #print("Configuration writeSimulationConfig", buildDirectory, mixtureName)
	    confFile = self.openFile(buildDirectory, mixtureName)
	    self.writeHeader(confFile)
	    self.writeSimulationType(confFile)
	    self.writeIOSection(confFile, buildDirectory, mixtureName)
	    self.writeCutOffs(confFile)
	    self.writeFixedAtomsParameters(confFile)
	    self.writePBCsection(confFile, self.container)
	    
	    if self.simType == Configuration.SIMULATION:
	        self.writeConf(confFile)
	    else:
	        self.writeMinimizationParameters(confFile)
	                    
	    confFile.close()

    
        
class ConfigurationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


