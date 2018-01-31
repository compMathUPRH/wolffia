from Molecule import *

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from NanoCAD_conf import NANOCAD_PDB_DIR

class DMF(Molecule):

   def __init__(self,chain):
       Molecule.__init__(self, str(chain))

       print NANOCAD_PDB_DIR + "/Solvents/DMF.pdb" , NANOCAD_PDB_DIR + "/Solvents/DMF.psf" 
       self.load(NANOCAD_PDB_DIR + "/Solvents/DMF.pdb" , NANOCAD_PDB_DIR + "/Solvents/DMF.psf")


#==========================================================================
if __name__ == '__main__':
	print "Probando DMF"
	m = DMF("DMF prueba" )
	print m
