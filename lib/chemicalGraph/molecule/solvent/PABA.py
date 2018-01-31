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
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../conf')
from conf.Wolffia_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS, WOLFFIA_WFY_DIR

from lib.chemicalGraph.molecule.Molecule import Molecule
from lib.chemicalGraph.Mixture import Mixture
from lib.chemicalGraph.molecule.ForceField import ForceField
from lib.chemicalGraph.molecule.AtomAttributes import AtomAttributes
#=========================================================================
#-----Improve force fields------ Jordan A. Caraballo Vega

class PABA_Tetradecane(Molecule):
    _FORCE_FIELD = None
    def __init__(self):
		mix  = Mixture()
		mix.loadWFM(WOLFFIA_WFY_DIR + "/PABAtetradecane.wfm")
		print mix.molecules()
		Molecule.__init__(self, "PABA-Tetradecane", molecule=mix.getMolecule("PABA-TetradecaneQ_1"))
		self.changeResidues("PAB")
#---------------------------------------------------------------------           
class PABA_Heptane(Molecule):
    _FORCE_FIELD = None
    def __init__(self):
		mix  = Mixture()
		mix.loadWFM(WOLFFIA_WFY_DIR + "/PABAheptane.wfm")
		print mix.molecules()
		Molecule.__init__(self, "PABA-Heptane", molecule=mix.getMolecule("PABA-HeptaneQ_1"))
		self.changeResidues("PAB")
#---------------------------------------------------------------------           
class PABA_Pentane(Molecule):
    _FORCE_FIELD = None
    def __init__(self):
		mix  = Mixture()
		mix.loadWFM(WOLFFIA_WFY_DIR + "/PABApentane.wfm")
		print mix.molecules()
		Molecule.__init__(self, "PABA-Pentane", molecule=mix.getMolecule("PABA-Pentane_1"))
		self.changeResidues("PAB")
#---------------------------------------------------------------------           

#==========================================================================
"""
if __name__ == '__main__':
    print "Probando PABA-Tetradecane"
    m = PABA()
    print m
    m.writePSF("PABA.psf")
    m.writePDB("PABA.pdb")
"""