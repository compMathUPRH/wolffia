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

	"minBabyStep": [0.1, "DoubleSpinBox", " K", 10, 0.1, 1, True, 0.001],
	"minTinyStep": [0.000001, "DoubleSpinBox", "", 10, 0.000000000001, 1, True, 0.0000001],
	"minLineGoal": [0.0001, "DoubleSpinBox", "", 10, 0.0000000001, 1, True, 0.00001],
	"minSteps":  [10000, "SpinBox", "", 0, 99999999, True, 1],
	"exclusion": [0, "ComboBox", "none", "1-2", "1-3", "1-4", "scaled1-4", True], #Same one as exclude from namdSimParm, I just don't want to deal with changing their names now....
	"cutoff":  [12, "DoubleSpinBox", " A", 1, 0, 9999999999, True, 1],
	"useSwitch": [False, "CheckBox", False, True],
	"pairListDist":  [13, "DoubleSpinBox", " A", 1, 0, 9999999999, True, 1],
	"switchDist":  [11, "DoubleSpinBox", " A", 1, 0, 9999999999, False, 1],
	"scaling": [1, "DoubleSpinBox", "", 3, 0, 1, False, 0.1]
}
