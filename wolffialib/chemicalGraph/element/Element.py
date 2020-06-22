# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, 

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
import sys, os, copy
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../conf')
#print sys.path
from conf.Wolffia_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS

from wolfialib.chemicalGraph.Molecule import Molecule
from wolfialib.chemicalGraph.ForceField import ForceField, NonBond
from wolfialib.chemicalGraph.AtomAttributes import AtomInfo,AtomAttributes

'''
References: 
1. Reference: program QUANTA, Molecular Simulations Inc., http://www.msg.ucsf.edu/local/programs/xplor/tutorial.dir/toppar/parameter.elements
'''
#=========================================================================
class Element(Molecule):
    _FORCE_FIELD_PARAMETERS = {  # reference
        "H":[-0.03,1.3582],
        "B":[-.0100,2.085],     # (1)
        "HE":[-.0100,2.495],     # (1)
        "KR":[-.0100,3.599],     # (1)
        "RN":[-.0100,4.009],     # (1)
        "SE":[-.0430,3.510],     # (1)
        "AT":[-.3200,3.884],     # (1)
        "BR":[-.3200,3.884],     # (1)
        "XE":[-.0100,3.849],     # (1)
        "I":[-.8000,3.635],     # (1)
        "AL":[-.2500,4.740],     # (1)
        "AS":[-.0600,3.564],     # (1)
        "BA":[-.1600 ,3.385],     # (1)
        "BE":[-.0030,1.960],     # (1)
        "CA":[-.0600,3.107],     # (1)
        "CS":[-.0045,5.183],     # (1)
        "CU":[-.0600,2.459],     # (1)
        "FE":[-.0200,2.610],     # (1)
        "GE":[-.0450,3.029],     # (1)
        "K":[-.0100,4.187],     # (1)
        "LI":[-.0070,2.202],     # (1)
        "MG":[-.0450,2.564],     # (1)
        "MN":[-.7000,2.851],     # (1)
        "NI":[-.0500,1.782],     # (1)
        "PD":[-.0100,2.388],     # (1)
        "PT":[-.0100,2.370],     # (1)
        "RB":[-.0065,4.741],     # (1)
        "RH":[-.0250,2.797],     # (1)
        "RU":[-.0250,2.940],     # (1)
        "SI":[-.3100,4.455],     # (1)
        "SN":[-.0450,3.385],     # (1)
        "SR":[-.1719,3.523],     # (1)
        "YB":[-.0600,3.127],     # (1)
        "ZN":[-.2500,1.942],     # (1)
        "ZR":[-.0100,3.617],     # (1)
        "C":[-0.032, 2.0],
        "N":[-0.18, 1.79],
        "O":[-0.12,1.7],
        "F":[-.1000,2.029],      # (1)
        "NA":[-0.1153, 2.275],
        "P":[-0.585, 2.15],
        "S":[-0.565,2.05],
        "CL":[-0.3002,1.735],
		"AR":[-.01, 3.35],
		"AU":[-0.53537, 3.2]
    }
    
    _ATTRIBUTES = {
        "H" : AtomAttributes(AtomInfo("H",  "H",  "H",  0.417,    1.00794, 0.0, 1.0, ' ', "H",  "ELT", "A", 1),[0.,0.,0.]),
        "O" : AtomAttributes(AtomInfo("O",  "O",  "O",  -0.834,    15.9994, 0.0, 1.0, ' ', "O",  "ELT", "A", 1),[0.,0.,0.]),
        "C" : AtomAttributes(AtomInfo("C",  "C",  "C",  0.147156, 12.0107, 1.0, 1.0, ' ', "C",  "ELT", "A", 1),[0.,0.,0.]),
        "F" : AtomAttributes(AtomInfo("F",  "F",  "F",  -1,    18.9984032, 1.0, 1.0, ' ', "F",  "ELT", "A", 1),[0.,0.,0.]),
        "N" : AtomAttributes(AtomInfo("N",  "N",  "N",  -0.341313, 14.0067, 1.0, 1.0, ' ', "N",  "ELT", "A", 1),[0.,0.,0.]),
        "NA": AtomAttributes(AtomInfo("NA", "NA", "NA", 1.0,      22.98977,1.0, 1.0, ' ', "NA", "ELT", "A", 1),[0.,0.,0.]),
        "P" : AtomAttributes(AtomInfo("P",  "P",  "P",  0.39354,  30.9738, 1.0, 1.0, ' ', "P",  "ELT", "A", 1),[0.,0.,0.]),
        "S" : AtomAttributes(AtomInfo("S",  "S",  "S",  0.0,      32.065,  1.0, 1.0, ' ', "S",  "ELT", "A", 1),[0.,0.,0.]),
        "CL": AtomAttributes(AtomInfo("CL", "CL", "CL", -1,     35.453,  0.0, 1.0, ' ', "CL", "ELT", "A", 1),[0.,0.,0.]),
		"AR": AtomAttributes(AtomInfo("AR", "AR", "AR", 0.0,	  39.9500, 0.0, 1.0, ' ', "O",  "ELT", "A", 1),[0.,0.,0.]),
		"AU": AtomAttributes(AtomInfo("AU", "AU", "AU", 0.0,	 96.96657, 0.0, 1.0, ' ', "AU",  "ELT", "A", 1),[0.,0.,0.])
    }
    _ENAME_TO_SYMBOL = {
        "Argon"      :"AR",
        "Carbon"     :"C",
        "Chlorine"   :"CL",
        "Hydrogen"   :"H",
        "Fluorine"   :"F",
        "Gold"       :"AU",
        "Nitrogen"   :"N",
        "Oxygen"     :"O",
        "Phosphorous":"P",
        "Sodium"     :"NA",
        "Sulfur"     :"S"
    }
    
    def __init__(self,symbol):
        try:
            symbol       = symbol.upper()
            nbParameters = Element._FORCE_FIELD_PARAMETERS[symbol]
        except :
            import logging
            logger = logging.getLogger(self.__class__.__name__)
            logger.error("Invalid element symbol \"" + str(symbol) + "\"")
            print("Invalid element symbol \"" + str(symbol) + "\"")
            return

        Molecule.__init__(self, symbol)

        self.add_node(1, attrs=[copy.deepcopy(Element._ATTRIBUTES[symbol])])

        ff = ForceField(self)
        ff.setNonBond(symbol, nbParameters[NonBond._EPSILON], NonBond._EPSILON)
        ff.setNonBond(symbol, nbParameters[NonBond._SIGMA]/2.,   NonBond._SIGMA)  # VDw DISTANCE DIVIDED BY 2!!!!!

        self.setForceField(ff)
        #self.copyChargesToForceField()

    @staticmethod
    def nameToSymbol(ename):
        return Element._ENAME_TO_SYMBOL[ename]

class H(Element):
    def __init__(self):
        Element.__init__(self, "H")

class O(Element):
    def __init__(self):
        Element.__init__(self, "O")

class C(Element):
    def __init__(self):
        Element.__init__(self, "C")

class P(Element):
    def __init__(self):
        Element.__init__(self, "P")

class S(Element):
    def __init__(self):
        Element.__init__(self, "S")

class Ar(Element):
    def __init__(self):
        Element.__init__(self, "AR")

class Na(Element):
    def __init__(self):
        Element.__init__(self, "NA")

class Au(Element):
    def __init__(self):
        Element.__init__(self, "AU")
