
from conf.Wolffia_conf import _WOLFFIA_OS, WOLFFIA_USES_IMD
import random

class Configuration(object):
	SIMULATION   = 1
	MINIMIZATION = 2
	
	CURRENT_FOLDER = 0x1
	NO_IMD_WAIT    = 0x2
	
	_CHECKED_BOOL_TO_WORD_    = {True:"yes", False:"no"}
	
	def __init__(self, parameters, drawer, fixedAtoms=False, simType=SIMULATION, confOptions=0x0):
	    #self.__dict__.update(parameters.__dict__)
	    self.__dict__.update(parameters)
	    self.drawer         = drawer
	    self.fixedAtoms     = fixedAtoms
	    self.filename       = None
	    self.buildDirectory = None
	    self.simType        = simType
	    random.seed()
	    self.imdPort        = random.randint(30000,40000)
	    
	    #print "Configuration __init__ ", confOptions
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
	    conf          =    file(self.filename, mode="w")
	
	    return conf
	
	def writeCutOffs(self, conf):
	    conf.write("\n# CutOffs\n")
	    conf.write("   cutoff   " + str(self.cutoff.value()) + "\n")
	    conf.write("   switching   " + str(self._CHECKED_BOOL_TO_WORD_[self.useSwitch.isChecked()]) + "\n")
	    if self.useSwitch.isChecked():
	        conf.write("   switchdist   " + str(self.switchDist.value()) + "\n")
	    conf.write("   pairlistdist   " + str(self.pairListDist.value()) + "\n")
	    conf.write("   exclude   %s\n" % (self.exclude.itemText(self.exclude.currentIndex())))
	    conf.write("   1-4scaling   %.10f" % ( self.scaling.value()))
	    
	    
	def writeMinimizationParameters(self, conf):
	    conf.write("\n\n#Parameters for minimization, some of these will be passed on to the actual simulation configuration file\nminBabyStep   %.10f\nminTinyStep   %.10f\nminLineGoal   %.10f\nnumsteps   %d\n" % 
	               (self.minBabyStep.value(), 
	                self.minTinyStep.value(), 
	                self.minLineGoal.value(), 
	                self.minSteps.value()))
	
	
	def writeConf(self, conf):
	    conf.write("\n#TIMESTEP PARAMETERS\n")
	    conf.write("   timestep   %.4f\n   numsteps   %d\n   firsttimestep   %d\n   stepspercycle   %d\n" % (self.timeSteps.value(), self.numSteps.value(), self.startStep.value(), self.stepsCycle.value()))
	    
	    
	    conf.write("\n#SIMULATION SPACE PARTITIONING\n")
	    conf.write("   splitPatch   %s\n   hgroupCutoff   %.8f\n   margin   %.8f\n   pairlistMinProcs   %d\n   pairlistsPerCycle   %d\n   outputPairlists   %d\n   pairlistShrink   %.8f\n   pairlistGrow   %.8f\n   pairlistTrigger   %.8f" % (self.splitPatch.itemText(self.splitPatch.currentIndex()), self.hCutoff.value(), self.margin.value(), self.pairMin.value(), self.pairCycle.value(), self.pairOut.value(), self.pairShrink.value(), self.pairGrow.value(), self.pairTrigger.value()))
	
	    
	    conf.write("\n\n###Basic Dynamics###\n   temperature   %.10f\n   COMmotion   %s\n   dielectric   %.8f\n   seed   %d\n   rigidBonds   %s\n   rigidTolerance   %.10f\n   rigidIterations   %d\n   useSettle   %s" % 
	               (self.temperature.value(), 
	                (self._CHECKED_BOOL_TO_WORD_[self.COMmotion.isChecked()]), 
	                self.dielectric.value(), 
	                self.seed.value(), 
	                self.rigidBonds.itemText(self.rigidBonds.currentIndex()), 
	                self.rigidTol.value(), 
	                self.rigidIter.value(),
	                (self._CHECKED_BOOL_TO_WORD_[ self.settle.isChecked()])))
	    
	    
	    #PME params
	    if self.pme.isChecked():
	        conf.write("\n\n###PME PARMS###\n   PMEGridSpacing    %s\n   PME   %s\n   PMETolerance   %.8f\n   PMEInterpOrder   %d" % (str(self.pmeGridSp.value()), (self._CHECKED_BOOL_TO_WORD_[self.pme.isChecked()]), self.pmeTol.value(), self.pmeIn.value()))
	        if self.gridX.value() != 0: 
	            conf.write("\n   PMEGridSizeX   " + str(self.gridX.value()))
	        if self.gridY.value() != 0:
	            conf.write("\n   PMEGridSizeY   " + str(self.gridY.value()))
	        if self.gridZ.value() != 0:
	            conf.write("\n   PMEGridSizeZ   " + str(self.gridZ.value()))
	        if self.FFTProc.value() != 0:
	            conf.write("\n   PMEProcessors   " + str(self.FFTProc.value()))
	        conf.write("\n   FFTWEstimate   %s\n   FFTWUseWisdom   %s" % ((self._CHECKED_BOOL_TO_WORD_[self.FFTOp.isChecked()]), (self._CHECKED_BOOL_TO_WORD_[self.FFTW.isChecked()])))
	        if hasattr(self.FFTFile,"text") and  self.FFTFile.text() != "default" and self.FFTFile.text() != '':
	            conf.write("\n   FFTWWisdomFile   " + str(self.FFTFile.text()))
	    
	    #FULL DIRECT PARAMS
	    if self.elc.isChecked():
	        conf.write("\n\n###FULL DIRECT PARAMS###\nFullDirect   yes")
	    
	    #Multiple timesteps # 
	    conf.write("\n\n###Multiple timestep parameters###")
	    if self.numElc.value() != 0:
	        conf.write("\n   fullElectFrequency   " + str(self.numElc.value()))
	    if self.timeBond.value() != 0:
	        conf.write("\n   nonBondedFreq   " + str(self.timeBond.value()))
	    conf.write("\n   MTSAlgorithm   " + str(self.MTSalg.itemText(self.MTSalg.currentIndex())))
	    conf.write("\n   longSplitting   " + str(self.rforce.itemText(self.rforce.currentIndex())))
	    conf.write("\n   molly   " + str((self._CHECKED_BOOL_TO_WORD_[self.moll.isChecked()])))
	    conf.write("\n   mollyTolerance   " + str(self.molltol.value()))
	    conf.write("\n   mollyIterations   " + str(self.mollitr.value()))
	    
	    
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
	    
	    #langevin dynamics 
	    if self.useLang.isChecked():
	        conf.write("\n\n###LANGEVIN DYNAMICS###\n   langevin   on")
	        if self.langTemp == 0:
	            print "You did not set a temperature for langevin calculations!\nTemperature will be set to 1 to avoid error."
	            conf.write("\n   langevinTemp   1")
	        else:
	            conf.write("\n   langevinTemp   " + str(self.langTemp.value()))
	        if self.langDamp.value() != 0:
	            conf.write("\n   langevinDamping   " + str(self.langDamp.value()))
	        conf.write("\n   langevinHydrogen   " + str(self._CHECKED_BOOL_TO_WORD_[self.langHyd.isChecked()]))
	        if  hasattr(self.pdbLang,"text") and  self.pdbLang.text() != "default" and self.pdbLang.text(f) != '':
	            conf.write("\n   langevinFile   " + str(self.pdbLang.text()))
	            conf.write("\n   langevinCol   " + str(self.pdbCol.itemText(self.fixAtmCol.currentIndex())))
	    
	    #temperature coupling
	    if self.tempCoup.isChecked():
	        conf.write("\n\n###Temperature Coupling###\ntCouple   on")
	        if self.tempBath.value() == 0:
	            print "No values given to tCoupleTemp! \nGiving it a default value of 1."
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
	            print "No value given to rescaleTemp! \n Giving it a default value of 1."
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
	            print "No value given to reassignHold! \n Giving it a default value of 1."
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
	            print "No value given to target pressure for Berendsen Pressure Bath coupling \n Giving it a default value of 1."
	            conf.write("\n   BerendsenPressureTarget   1")
	        else:
	            conf.write("\n   BerendsenPressureTarget   " + str(self.targPress.value()))
	        if self.berenComp.value() == 0:
	            print "No value given to compressibility for Berendsen Pressure Bath coupling \n Giving it a default value of 1."
	            conf.write("\n   BerendsenPressureCompressibility   1")
	        else:
	            conf.write("\n   BerendsenPressureCompressibility   " + str(self.berenComp.value()))
	        if self.berenRelx.value() == 0:
	            print "No value given to relaxation time for Berendsen Pressure Bath coupling \n Giving it a default value of 1."
	            conf.write("\n   BerendsenPressureRelaxationTime   1")
	        else:
	            conf.write("\n   BerendsenPressureRelaxationTime   " + str(self.berenRelx.value()))
	        if self.berenPress.value() != 0:
	            conf.write("\n   BerendsenPressureFreq   " + str(self.berenPress.value()))
	
	    #nose hooving something machinka
	    if self.useLangP.isChecked():
	        conf.write("\n\n###Nose-Hoover Langevin Piston Pressure Control###\n   LangevinPiston   on")
	        try:
	            conf.write("\n   LangevinPistonTarget   " + str(self.langTarg.value()))
	            conf.write("\n   LangevinPistonPeriod   " + str(self.oscilPer.value()))
	            conf.write("\n   LangevinPistonDecay   " + str(self.langDecay.value()))
	            conf.write("\n   LangevinPistonTemp   " + str(self.langPTemp.value()))
	            conf.write("\n   SurfaceTensionTarget   " + str(self.surfTen.value()))
	            conf.write("\n   StrainRate   " + str(self.strainX.value()) + " " + str(self.strainY.value()) + " " + str(self.strainZ.value()))
	        except:
	            print("Message from Wolffia:\n \n You did not give a required value to Nose-Hoover Langevin Piston Pressure Control!\n")
	        #if self.exclPress.isChecked():
	        #    conf.write("\nExcludeFromPressure   on")
	         #   if self.exclPressFile.text() != "default" and self.exclPressFile.text() != '':
	         #       conf.write("\nExcludeFromPressureFile   " + str(self.exclPressFile.text()))
	         #   conf.write("\nExcludeFromPressureCol   " + str(self.exclPressCol.itemText(self.exclPressCol.currentIndex())))
	    
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
	            print "Hey, you forgot to name the file for SMD constraints! \nExit"
	            return
	        else:
	            conf.write("\nSMDFile   " + self.smdFile.text())
	        conf.write("\nSMDk   " + str(self.smdk.value())) 
	        conf.write("\nSMDVel   " + str(self.smdVel.value())) 
	        conf.write("\nSMDDir   " + str(self.smdDirX.value()) + " " + str(self.smdDirY.value()) + " " + str(self.smdDirZ.value()))
	        conf.write("\nSMDOutputFreq   " + str(self.smdOut.value()))
	        
	
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
	    #print self.__dict__.keys()
	    conf.write("   restartfreq " + str(self.restartSteps.value()) +  "\n")
	    conf.write("   binaryrestart no\n")
	    conf.write("\n   outputname   \""    +    mixtureName + "\"\n")
	    conf.write("   DCDfile   \"$basedir/%s\"\n   DCDfreq %s\n" % (str(mixtureName + ".dcd"), str(self.trajectorySteps.value())))
	    if WOLFFIA_USES_IMD:
	        conf.write("\n   IMDon on\n   IMDport " + str(self.imdPort)  + "\n   IMDfreq " + str(self.trajectorySteps.value()) +  "\n   IMDwait " + self.imdWait + "\n   IMDignore no\n")
	    else:
	        conf.write("\n   IMDon off\n   IMDport 3000\n   IMDfreq " + str(self.trajectorySteps.value()) +  "\n   IMDwait no\n   IMDignore no\n")
	    conf.write("\n   outputEnergies " + str(self.energySteps.value()) +  "\n")
	    #print "writeIOSection", self.restartSteps.value()
	    conf.write("\n   outputTiming  " + str(self.energySteps.value()) +  "\n")
	
	
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
	    print "Configuration writeSimulationConfig", buildDirectory, mixtureName
	    confFile = self.openFile(buildDirectory, mixtureName)
	    self.writeHeader(confFile)
	    self.writeSimulationType(confFile)
	    self.writeIOSection(confFile, buildDirectory, mixtureName)
	    self.writeCutOffs(confFile)
	    self.writeFixedAtomsParameters(confFile)
	    self.writePBCsection(confFile, self.drawer)
	    
	    if self.simType == Configuration.SIMULATION:
	        self.writeConf(confFile)
	    else:
	        self.writeMinimizationParameters(confFile)
	                    
	    confFile.close()

    
        
class ConfigurationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


