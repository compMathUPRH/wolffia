# -*- coding: utf-8 -*-
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
from polymer.PMMA import PMMA
from allotrope.Tube import Tube
from allotrope.Graphene import Graphene

#----------------------------------------------------------------------
# Molecules data structure
MOLECULE_CLASS_NAME=1
MOLECULE_SUBMENU=1
MOLECULE_UNDERLINE=0
MDCONF_MOLECUES = {
	'Polymer': [0, {
		'Homopolymer': [0, {
#			'Polyaniline': [0, Polyaniline],
#			"PolyCYT": [0, PolyCYT],
#			"PolyADE": [0, PolyADE],
#			"PolyGUA": [0, PolyGUA],
#			"PolyTHY": [0, PolyTHY],
			'PMMA': [1, PMMA]
		}],
		'Comopolymer': [0, {
#			"SsDNA": [0, makeDNA]
		}],
	}],
	'Fiber': [0, {
	}],
	'Allotropes': [0, {
		"swCNT": [0, Tube],
		"Graphene": [0, Graphene]
#		"HOPG": [0, makeHOPG]
	}],
	'Droplet': [0, {
#		"Argon": [0, makeArgon]
	}]
}

