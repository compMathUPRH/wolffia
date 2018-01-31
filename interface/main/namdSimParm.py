# -*- coding: utf-8 -*-
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
#Some have the range to 0, but will not accept 0, check that.

parmDict = {
	#QtDouble
	#Name : [ Value, object, suffix, decimals , min, max, enabled?, stepSize]
	#QtSpin
	#Name : [ Value, object, suffix, min, max, enabled?, stepsize]
	#QtCheckBox
	#Name : [ value, object, checked?, enabled?]
	#QCombobox
	#Name : [ primary value, object, values,  enabled?]	
	#InputFile
	#Name : ["default", "inputfile", enabled?]
"PStree" : {
	#"Basic Timesteps" : {
	"temperature": [0, "DoubleSpinBox", " K", 1, 0, 9999999999, True, 1],
	"COMmotion": [False, "CheckBox", False, True],
	"dielectric": [1, "DoubleSpinBox", "", 3, 1, 9999999999, True, 1],
	"seed":  [2000, "SpinBox", "", 0, 99999999, True, 1],
	"rigidBonds": [0, "ComboBox", "none", "water", "all", True],
	"rigidTol": [0.00000001, "DoubleSpinBox", " A", 10, 0, 9999999999, True, 0.000000001], #Angstrom#no me acuerdo que valores puede tomar
	"rigidIter":  [100, "SpinBox", "", 0, 99999999, True, 1],
	"settle": [True, "CheckBox", True, True],
	#}
	#"Timestep Parameters" : {
	"numSteps":  [10000, "SpinBox", "", 0, 99999999, True, 1],
	"timeSteps":  [1, "DoubleSpinBox", " fs", 4, 0, 9999999999, True, 1], #change to angstrom
	"startStep": [0, "SpinBox", "", 0, 99999999, True, 1],
	"stepsCycle": [20, "SpinBox", "", 0, 99999999, True, 1],
	#}
	#"Simulation Space Partitioning": { #this one is missing the one for scaled 1-4 interactions
	"exclude": [0, "ComboBox", "none", "1-2", "1-3", "1-4", "scaled1-4", True],
    "scaling": [1, "DoubleSpinBox", "", 3, 0, 1, False, 0.1],
    "cutoff":  [12, "DoubleSpinBox", " A", 1, 0, 9999999999, True, 1],
    "useSwitch": [False, "CheckBox", False, True],
    "pairListDist":  [13, "DoubleSpinBox", " A", 1, 0, 9999999999, True, 1],
    "switchDist":  [11, "DoubleSpinBox", " A", 1, 0, 9999999999, False, 1],
	"splitPatch": [0, "ComboBox", "hydrogen", "position", True],
	"pairCycle":  [2, "SpinBox", "", 1, 99999999, True, 1],
	"hCutoff":  [2.5, "DoubleSpinBox", " A", 1, 0, 9999999999, True, 1],
	"margin": [0, "DoubleSpinBox", " A", 2, 0, 9999999999, True, 1], #change to angstrom
	"pairMin":  [1, "SpinBox", "", 1, 99999999, True, 1],
	"pairOut":  [0, "SpinBox", "", 0, 99999999, True, 1],
	"pairShrink":  [0.01, "DoubleSpinBox", "", 10, 0, 9999999999, True, 0.001],
	"pairGrow":  [0.01, "DoubleSpinBox", "", 10, 0, 9999999999, True, 0.001],
	"pairTrigger":  [0.3, "DoubleSpinBox", "", 10, 0, 9999999999, True, 0.01],
	#}
	#"PME Parameters": {
	"pme": [False, "CheckBox", False, True], #Chekea si PME es necesario para los demas!
	"pmeTol": [0.000001, "DoubleSpinBox", "", 10, 0, 9999999999, False, 0.0000001],
	"pmeIn": [4, "DoubleSpinBox", "", 10, 0, 9999999999, False, 1],
	"pmeGridSp": [1, "DoubleSpinBox", "", 2, 0, 9999999999, False, 1],
	"gridX": [1, "SpinBox", "", 0, 9999999, False, 1],
	"gridY": [1, "SpinBox", "", 0, 9999999, False, 1],
	"gridZ": [1, "SpinBox", "", 0, 9999999, False, 1],
	"FFTOp": [False, "CheckBox", False, True],
	"FFTProc": [0, "SpinBox", "", 1, 99999999, True, 1], #this one depends on the number of procesors! Also check for changes?
	"FFTW": [True, "CheckBox", True, True],
	"FFTFile": ['default', 'InputFile', False],
	#}
	#"Full Direct Parameters" : {
	"elc": [False, "CheckBox", False, True],
	#}
	#"Multiple Timesteps Parameters" : {
	"numElc":  [0, "SpinBox", "", 0, 99999999, True, 1],
	"timeBond":  [1, "SpinBox", "", 1, 99999999, True, 1],
	"MTSalg":  [0, "ComboBox", "impulse", "constant", True],
	"rforce": [0, "ComboBox", "c1", "c2", True],
	"moll": [False, "CheckBox", False, True],
	"molltol": [0.00001, "DoubleSpinBox", "", 10, 0, 9999999999, True, 0.000001],
	"mollitr":  [100, "SpinBox", "", 1, 99999999, True, 1]
	#}
}  ,
"SMtree"  :  {
	#"Constraints and Restraints" : {
		#"Harmonic Constraint Parameters" : {
	"const": [False, "CheckBox", False, True],
	"harExp":  [2, "SpinBox", "", 2, 99999999, False, 2],
	"pdbCons": ['default', 'InputFile', False],
	"pdbForc": ['default', 'InputFile', False],
	"pdbcol1": [0, "ComboBox", "O", "X", "Y", "Z", "B", False],
	"selCons": [False, "CheckBox", False, False],
	"selConsX": [False, "CheckBox", False, False],
	"selConsY": [False, "CheckBox", False, False],
	"selConsZ": [False, "CheckBox", False, False],
		#}
		#"Fixed Atom Parameters" : {
	"fixAtm": [False, "CheckBox", True, False],
	"fixAtmForc": [False, "CheckBox", False, False],
	"fixAtmFile": ['default', 'InputFile', False],
	"fixAtmCol": [0, "ComboBox", "O", "X", "Y", "Z", "B", False],
		#}
	#}
	#"Temperature Control and Equilibration" : {
		#"Langevin Dynamics Parameters" : {
	"useLang": [False, "CheckBox", False, True],
	"langTemp": [0, "DoubleSpinBox", " K", 1, 0, 9999999999, False, 1],
	"langDamp": [1, "DoubleSpinBox", " (1/ps)", 4, 0.0001, 9999999999, False, 1],
	"langHyd": [True, "CheckBox", True, True],
	"pdbLang": ['default', 'InputFile', False],
	"pdbCol": [0, "ComboBox", "O", "X", "Y", "Z", "B", False],
		#}
		#"Temperature Coupling Parameters" : {
	"tempCoup": [False, "CheckBox", False, True],
	"tempBath": [0, "DoubleSpinBox", " (1/ps)", 10, 0, 9999999999, False, 1],
	"pdbTCouple": ['default', 'InputFile', False],
	"pdbTCol": [0, "ComboBox", "O", "X", "Y", "Z", "B", False],
		#}
		#"Temperature Rescaling Parameters" : {
	"timeTRes": [0, "SpinBox", "", 0, 99999999, True, 1],
	"tempEq": [1, "DoubleSpinBox", "", 10, 1, 9999999999, False, 1],
		#}
		#"Temperature Reassignment Parameters" : {
	"useTempRe": [False, "CheckBox", False, True],
	"timeBTemp": [1, "SpinBox", "", 1, 99999999, False, 1],
	"tempResEq": [1, "DoubleSpinBox", " K", 10, 0, 9999999999, False, 1],
	"tempInc": [0, "DoubleSpinBox", " K", 10, -9999999999, 9999999999, False, 1],
	"resHold": [1, "DoubleSpinBox", " K", 10, 0, 9999999999, False, 1],
		#}
	#}
	#"Pressure Control" : {
	"grpPress": [False, "CheckBox", False, True],
	"antiCell": [False, "CheckBox", False, True],
	"consRat": [False, "CheckBox", False, True],
	"consArea": [False, "CheckBox", False, True],
		#"Berendsen Pressure Bath Coupling" : {
	"useBeren": [False, "CheckBox", False, True],
	"targPress": [0, "DoubleSpinBox", "", 10, 1, 9999999999, False, 1],
	"berenComp": [0, "DoubleSpinBox", "", 10, 1, 9999999999, False, 1],
	"berenRelx": [0, "DoubleSpinBox", "", 10, 1, 9999999999, False, 1],
	"berenPress": [0, "SpinBox", "", 1, 99999999, True, 1],
		#}
		#"Nose-Hoover Langevin Piston Pressure Control" : {
	"useLangP": [False, "CheckBox", False, True],
	"langTarg": [1.01325, "DoubleSpinBox", "bar", 4, -999999999, 9999999999, False, 1],
	"oscilPer": [200, "DoubleSpinBox", " fs", 10, 0, 9999999999, False, 1],
	"langDecay": [100, "DoubleSpinBox", " fs", 10, 0, 9999999999, False, 1],
	"langPTemp": [0.0001, "DoubleSpinBox", " K", 4, 0.0001, 9999999999, False, 1],
	"surfTen": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"strainX": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"strainY": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"strainZ": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	#"exclPress": [False, "CheckBox", False, False],
	#"exclPressFile": ['default', 'InputFile', False],
	#"exclPressCol": [0, "ComboBox", "O", "X", "Y", "Z", "B", False],
		#}
		#}
	#"Applied Forces and Analysis : {
	#"Constant Forces" : {
	"constForce": [False, "CheckBox", False, True],
	"consFrcFile": ['default', 'InputFile', False],
	#"External Electric Field" : {
	"useEField": [False, "CheckBox", False, True],
	"efieldX": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"efieldY": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"efieldZ": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	#}
	#"Moving Constraints" : {
	"movConst": [False, "CheckBox", False, True],
	"velMoveX": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"velMoveY": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"velMoveZ": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	#}
	#"Rotating Constraints" : {
	"rotCons": [False, "CheckBox", False, True],
	"rotAxisX": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"rotAxisY": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],	
	"rotAxisZ": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"rotPivX": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1], 	
	"rotPivY": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"rotPivZ": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"rotVel": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	#}
	#"Steered Molecular Dynamics (SMD)" : {
	"smd": [False, "CheckBox", False, True],
	"smdFile": ['default', 'InputFile', False],
	"smdk": [1, "DoubleSpinBox", "", 10, 0.000000001, 9999999999, False, 1],
	"smdVel": [1, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1], #can be anything except 0
	"smdDirX": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"smdDirY": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"smdDirZ": [0, "DoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
	"smdOut": [1, "SpinBox", "", 1, 99999999, True, 1],
	#}
	#}
}
		}
