# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  WATER.py
#
#  Authors:
#  Frances Martínez Miranda
#  José O. Sotero Esteva  (jse@mate.uprh.edu)
#
#  Department of Mathematics
#  University of Puerto Rico at Humacao
#
#  Acknowledgements: The main funding source for this project has been provided
#  by the UPR-Penn Partnership for Research and Education in Materials program, 
#  USA National Science Foundation grant number DMR-0934195. 
#---------------------------------------------------------------------------

from Molecule import *
from ForceField import *

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from NanoCAD_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS

class WATER(Molecule):
   _FORCE_FIELD = ForceField(NANOCAD_FORCE_FIELDS + "/WATER.prm")
   def __init__(self,chain):
       Molecule.__init__(self, str(chain))

       print NANOCAD_PDB_DIR + "/Solvents/WATER.pdb" , NANOCAD_PDB_DIR + "/Solvents/WATER.psf" 
       self.load(NANOCAD_PDB_DIR + "/Solvents/WATER.pdb" , NANOCAD_PDB_DIR + "/Solvents/WATER.psf")


#==========================================================================
if __name__ == '__main__':
	print "Probando WATER"
	m = WATER("WATER prueba" )
	print m
	for node in m:
		print m.getAtomAttributes(node)
	m.writePSF()
