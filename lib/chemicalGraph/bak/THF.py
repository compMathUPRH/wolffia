from Molecule import *

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from NanoCAD_conf import NANOCAD_PDB_DIR

class THF(Molecule):
   def __init__(self, nombre):
       Molecule.__init__(self, nombre)

       self.load(NANOCAD_PDB_DIR + "/Solvents/THF.pdb" , NANOCAD_PDB_DIR + "/Solvents/THF.psf")
       self.rename(nombre)

#==========================================================================
if __name__ == '__main__':
	print "Probando THF"
	m = THF("THF prueba" )
	print m

