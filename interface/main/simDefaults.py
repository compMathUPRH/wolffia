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
"""	
	QtDouble
	Name : [ Value, object, suffix, decimals , min, max, enabled?, stepSize]
	
	QtSpin
	Name : [ Value, object, suffix, min, max, enabled?, stepsize]
	
	QtCheckBox
	Name : [ value, object, checked?, enabled?]
	
	QCombobox
	Name : [ primary value, object, values,  enabled?]	
	
	InputFile
	Name : ["default", "inputfile", enabled?]
	
"""

todos = {
"Basic Simulation Parameters" : {
	"order" : ["Basic Timesteps", "Timestep Parameters", "Simulation Space Partitioning", "PME Parameters", "Full Direct Parameters", "Multiple Timesteps Parameters"],
	"Basic Timesteps" : {
		"temperature": [0, "QDoubleSpinBox", " K", 10, 0, 9999999999, True, 1],
		"COMmotion": [False, "QCheckBox", False, True],
		"dielectric": [1, "QDoubleSpinBox", "", 10, 1, 9999999999, True, 1],
		"seed":  [2000, "QSpinBox", "", 0, 99999999, True, 1],
		"rigidBonds": [0, "QComboBox", "none", "water", "all", True],
		"rigidTol": [0.00000001, "QDoubleSpinBox", " A", 10, 0, 9999999999, True, 0.000000001], #Angstrom#no me acuerdo que valores puede tomar
		"rigidIter":  [100, "QSpinBox", "", 0, 99999999, True, 1],
		"settle": [True, "QCheckBox", True, True],
		"order": ["temperature","COMmotion","dielectric","seed","rigidBonds","rigidTol","rigidIter","settle"]
	} ,
	"Timestep Parameters" : {
		"numSteps":  [10000, "QSpinBox", "", 0, 99999999, True, 1],
		"timeSteps":  [1, "QDoubleSpinBox", " A", 10, 0, 9999999999, True, 1], #change to angstrom
		"startStep": [0, "QSpinBox", "", 0, 99999999, True, 1],
		"stepsCycle": [20, "QSpinBox", "", 0, 99999999, True, 1],
		"order": ["numSteps", "timeSteps", "startStep", "stepsCycle"]
	} ,
	"Simulation Space Partitioning": { #this one is missing the one for scaled 1-4 interactions
		"exclude": [0, "QComboBox", "none", "1-2", "1-3", "1-4", "scaled1-4", True],
		"cutoff":  [12, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 1],
		"useSwitch": [False, "QCheckBox", False, True],
		"switchDist":  [12, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 1],
		"pairListDist":  [13, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 1],
		"splitPatch": [0, "QComboBox", "hydrogen", "position", True],
		"pairCycle":  [2, "QSpinBox", "", 1, 99999999, True, 1],
		"hCutoff":  [2.5, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 1],
		"margin": [0, "QDoubleSpinBox", " A", 10, 0, 9999999999, True, 1], #change to angstrom
		"pairMin":  [1, "QSpinBox", "", 1, 99999999, True, 1],
		"pairOut":  [0, "QSpinBox", "", 1, 99999999, True, 1],
		"pairShrink":  [0.01, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 0.001],
		"pairGrow":  [0.01, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 0.001],
		"pairTrigger":  [0.3, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 0.01],
		"order": ["exclude", "cutoff", "useSwitch", "switchDist", "pairListDist", "splitPatch", "pairCycle", "hCutoff", "margin", "pairMin", "pairOut", "pairShrink", "pairGrow", "pairTrigger"]
	},
	"PME Parameters": {
	"pme": [False, "QCheckBox", False, True], #Chekea si PME es necesario para los demas!
	"pmeTol": [0.000001, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 0.0000001],
	"pmeIn": [4, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 1],
	"gridX": [0, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 1],
	"gridY": [0, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 1],
	"gridZ": [0, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 1],
	"FFTOp": [False, "QCheckBox", False, True],
	"FFTProc": [0, "QSpinBox", "", 1, 99999999, True, 1], #this one depends on the number of procesors! Also check for changes?
	"FFTW": [True, "QCheckBox", True, True],
	"FFTFile": ['default', 'InputFile', True],
	"order" : ["pme", "pmeTol", "pmeIn", "gridX", "gridY", "gridZ", "FFTOp", "FFTProc", "FFTW", "FFTFile"]
	} ,
	"Full Direct Parameters" : {
	"elc": [False, "QCheckBox", False, True],
	"order" : ["elc"]
	} ,
	"Multiple Timesteps Parameters" : {
	"numElc":  [0, "QSpinBox", "", 0, 99999999, True, 1],
	"timeBond":  [1, "QSpinBox", "", 1, 99999999, True, 1],
	"MTSalg":  [0, "QComboBox", "impulse", "constant", True],
	"rforce": [0, "QComboBox", "c1", "c2", True],
	"moll": [False, "QCheckBox", False, True],
	"molltol": [0.00001, "QDoubleSpinBox", "", 10, 0, 9999999999, True, 0.000001],
	"mollitr":  [100, "QSpinBox", "", 1, 99999999, True, 1],
	"order": ["numElc", "timeBond", "MTSalg", "rforce", "moll", "molltol", "mollitr"]
	}
 }  ,
 "Aditional Simulation Parameters"  :  {
	"order" : ["Constraints and Restraints", "Temperature Control and Equilibration", "Pressure Control", "Applied Forces and Analysis"],
	"Constraints and Restraints" : {
		"order": ["Harmonic Constraint Parameters","Fixed Atom Parameters"],
		"Harmonic Constraint Parameters" : {
			"const": [False, "QCheckBox", False, True],
			"harExp":  [2, "QSpinBox", "", 2, 99999999, False, 2],
			"pdbCons": ['default', 'InputFile', False],
			"pdbForc": ['default', 'InputFile', False],
			"pdbcol1": [0, "QComboBox", "O", "X", "Y", "Z", "B", False],
			"selCons": [False, "QCheckBox", False, False],
			"selConsX": [False, "QCheckBox", False, False],
			"selConsY": [False, "QCheckBox", False, False],
			"selConsZ": [False, "QCheckBox", False, False],
			"order": ["const", "harExp", "pdbCons", "pdbForc", "pdbcol1", "selCons", "selConsX", "selConsY", "selConsZ"]
		} , 
		"Fixed Atom Parameters" : {
			"fixAtm": [False, "QCheckBox", False, True],
			"fixAtmForc": [False, "QCheckBox", False, False],
			"fixAtmFile": ['default', 'InputFile', False],
			"fixAtmCol": [0, "QComboBox", "O", "X", "Y", "Z", "B", False],
			"order": ["fixAtm", "fixAtmForc", "fixAtmFile", "fixAtmCol"]
		}
	} ,
	"Temperature Control and Equilibration" : {
		"order": ["Langevin Dynamics Parameters","Temperature Coupling Parameters","Temperature Rescaling Parameters","Temperature Reassignment Parameters"],
		"Langevin Dynamics Parameters" : {
			"useLang": [False, "QCheckBox", False, True],
			"langTemp": [0, "QDoubleSpinBox", " K", 10, 0, 9999999999, False, 1],
			"langDamp": [1, "QDoubleSpinBox", " (1/ps)", 10, 1, 9999999999, False, 1],
			"langHyd": [True, "QCheckBox", True, True],
			"pdbLang": ['default', 'InputFile', False],
			"pdbCol": [0, "QComboBox", "O", "X", "Y", "Z", "B", False],
			"order": ["useLang", "langTemp", "langDamp", "langHyd", "pdbLang", "pdbCol"]
		} ,
		"Temperature Coupling Parameters" : {
			"tempCoup": [False, "QCheckBox", False, True],
			"tempBath": [0, "QDoubleSpinBox", " (1/ps)", 10, 0, 9999999999, False, 1],
			"pdbTCouple": ['default', 'InputFile', False],
			"pdbTCol": [0, "QComboBox", "O", "X", "Y", "Z", "B", False],
			"order": ["tempCoup", "tempBath", "pdbTCouple", "pdbTCol"]
		} ,
		"Temperature Rescaling Parameters" : {
			"timeTRes": [0, "QSpinBox", "", 0, 99999999, True, 1],
			"tempEq": [1, "QDoubleSpinBox", "", 10, 1, 9999999999, False, 1],
			"order": ["timeTRes", "tempEq"]
		} ,
		"Temperature Reassignment Parameters" : {
			"timeBTemp": [1, "QSpinBox", "", 1, 99999999, True, 1],
			"tempResEq": [1, "QDoubleSpinBox", " K", 10, 0, 9999999999, True, 1],
			"tempInc": [0, "QDoubleSpinBox", " K", 10, -9999999999, 9999999999, True, 1],
			"resHold": [1, "QDoubleSpinBox", " K", 10, 0, 9999999999, True, 1],
			"order": ["timeBTemp", "tempResEq", "tempInc", "resHold"]
		}
	} ,
	"Pressure Control" : {
		"order": ["grpPress", "antiCell", "consRat", "consArea","Berendsen Pressure Bath Coupling","Nose-Hoover Langevin Piston Pressure Control"],		
		"grpPress": [False, "QCheckBox", False, True],
		"antiCell": [False, "QCheckBox", False, True],
		"consRat": [False, "QCheckBox", False, True],
		"consArea": [False, "QCheckBox", False, True],
		"Berendsen Pressure Bath Coupling" : {
			"useBeren": [False, "QCheckBox", False, True],
			"targPress": [0, "QDoubleSpinBox", "", 10, 0, 9999999999, False, 1],
			"berenComp": [0, "QDoubleSpinBox", "", 10, 0, 9999999999, False, 1],
			"berenRelx": [0, "QDoubleSpinBox", "", 10, 0, 9999999999, False, 1],
			"berenPress": [0, "QDoubleSpinBox", "", 10, 0, 9999999999, False, 1],
			"order": ["useBeren", "targPress", "berenComp", "berenRelx", "berenPress"]
		} ,
		"Nose-Hoover Langevin Piston Pressure Control" : {
			"useLangP": [False, "QCheckBox", False, True],
			"langTarg": [1.01325, "QDoubleSpinBox", " bar", 5, -999999999, 9999999999, False, 1],
			"oscilPer": [200, "QDoubleSpinBox", " fs", 10, 0, 9999999999, False, 1],
			"langDecay": [100, "QDoubleSpinBox", " fs", 10, 0, 9999999999, False, 1],
			"langPTemp": [0, "QDoubleSpinBox", " K", 10, 0, 9999999999, False, 1],
			"surfTen": [0, "QDoubleSpinBox", " dyn/cm", 10, -999999999, 9999999999, False, 1],
			"strainX": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"strainY": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"strainZ": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			#"exclPress": [False, "QCheckBox", False, False],
			#"exclPressFile": ['default', 'InputFile', False],
			#"exclPressCol": [0, "QComboBox", "O", "X", "Y", "Z", "B", False],
			"order": ["useLangP", "langTarg", "oscilPer", "langDecay", "langPTemp", "surfTen", "strainX", "strainY", "strainZ", "exclPress", "exclPressFile", "exclPressCol"]
		} 
	} ,
	"Applied Forces and Analysis" : {
		"order" : ["Constant Forces","External Electric Field","Moving Constraints","Rotating Constraints","Steered Molecular Dynamics (SMD)"],
		"Constant Forces" : {
			"constForce": [False, "QCheckBox", False, True],
			"consFrcFile": ['default', 'InputFile', False],
			"order": ["constForce", "consFrcFile"]
		} , 
		"External Electric Field" : {
			"useEField": [False, "QCheckBox", False, True],
			"efieldX": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"efieldY": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"efieldZ": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"order": ["useEField", "efieldX", "efieldY", "efieldZ"]
		}, 
		"Moving Constraints" : {
			"movConst": [False, "QCheckBox", False, True],
			"velMoveX": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"velMoveY": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"velMoveZ": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"order": ["movConst", "velMoveX", "velMoveY", "velMoveZ"]
		},
		"Rotating Constraints" : {
			"rotCons": [False, "QCheckBox", False, True],
			"rotAxisX": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"rotAxisY": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],	
			"rotAxisZ": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"rotPivX": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1], 	
			"rotPivY": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"rotPivZ": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"rotVel": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"order" : ["rotCons", "rotAxisX", "rotAxisY", "rotAxisZ", "rotPivX", "rotPivY", "rotPivZ", "rotVel"]
		} ,
		"Steered Molecular Dynamics (SMD)" : {
			"smd": [False, "QCheckBox", False, True],
			"smdFile": ['default', 'InputFile', False],
			"smdk": [1, "QDoubleSpinBox", "", 10, 0.000000001, 9999999999, False, 1],
			"smdVel": [1, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1], #can be anything except 0
			"smdDirX": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"smdDirY": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"smdDirZ": [0, "QDoubleSpinBox", "", 10, -999999999, 9999999999, False, 1],
			"smdOut": [1, "QSpinBox", "", 1, 99999999, True, 1],
			"order" : ["smd", "smdFile", "smdk", "smdVel", "smdDirX", "smdDirY", "smdDirZ", "smdDirZ", "smdOut"]
		}
	}
}
		}