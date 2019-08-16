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

import os, sys, platform

WOLFFIA_VERSION = "1.4"

NANOCAD_BASE            = os.path.realpath(os.path.dirname(os.path.realpath(__file__))+"/..").replace("\\","/")
NANOCAD_PDB_DIR         = NANOCAD_BASE		   +"/data/coordinates/"
NANOCAD_MOLECULES       = NANOCAD_BASE		   +"/lib/"
NANOCAD_INTERFACE       = NANOCAD_BASE		   +"/interface/main"
NANOCAD_CLASSIFIER      = NANOCAD_BASE		   +"/interface/classifier"
NANOCAD_NANOTUBE_EDITOR = NANOCAD_BASE		   +"/interface/nanotubeEditor"
NANOCAD_GRAPHENE_EDITOR = NANOCAD_BASE		   +"/interface/grapheneEditor"
NANOCAD_PANI_EDITOR     = NANOCAD_BASE		   +"/interface/PANI"
NANOCAD_HOMOPOLY_EDITOR = NANOCAD_BASE		   +"/interface/homopolyEditor"
NANOCAD_FORCE_FIELDS    = NANOCAD_BASE         +"/data/forceFields"
CHARMM_FORCE_FIELDS     = NANOCAD_FORCE_FIELDS +"/CHARMM/"

WOLFFIA_WFY_DIR		    = NANOCAD_BASE		   +"/data/wfm/"

WOLFFIA_STYLESHEET      = NANOCAD_BASE         +"/conf/Wolffia.css"
C_MOLECULE_CATALOG      = os.path.expanduser(".cMolecule")  

sys.path.append(NANOCAD_MOLECULES)
sys.path.append(NANOCAD_INTERFACE)
sys.path.append(NANOCAD_CLASSIFIER)
sys.path.append(NANOCAD_NANOTUBE_EDITOR)
sys.path.append(NANOCAD_GRAPHENE_EDITOR)
sys.path.append(NANOCAD_PANI_EDITOR)
sys.path.append(NANOCAD_HOMOPOLY_EDITOR)
sys.path.append(NANOCAD_FORCE_FIELDS)

#==== System-dependent configurations ===================
#print "OS: '" + platform.system() + "'<"
_WOLFFIA_OS = platform.system()

if _WOLFFIA_OS == "Windows":
	WOLFFIA_DIR = os.path.expanduser("~\\Wolffia\\")
	WOLFFIA_GRAPHICS = os.path.realpath(os.path.dirname(os.path.realpath(__file__))+"\\..")+"\\interface\\graphics\\"
elif _WOLFFIA_OS == "Linux":
	WOLFFIA_DIR = os.path.expanduser("~/.wolffia/")
	WOLFFIA_GRAPHICS = os.path.realpath(os.path.dirname(os.path.realpath(__file__))+"/..")+"/interface/graphics/"

# other
WOLFFIA_DEFAULT_MIXTURE_NAME = "Unnamed"
WOLFFIA_DEFAULT_MIXTURE_LOCATION = WOLFFIA_DIR + WOLFFIA_DEFAULT_MIXTURE_NAME


WOLFFIA_USES_IMD = True

