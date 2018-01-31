from Molecule import *
from ForceField import *

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from NanoCAD_conf import NANOCAD_PDB_DIR, NANOCAD_FORCE_FIELDS

class CLF(Molecule):
  _FORCE_FIELD = ForceField(NANOCAD_FORCE_FIELDS + "/CLF.prm")
  def __init__(self, nombre):
       Molecule.__init__(self, nombre)

       self.load(NANOCAD_PDB_DIR + "/Solvents/CLF.pdb" , NANOCAD_PDB_DIR + "/Solvents/CLF.psf")
       self.rename(nombre)

#==========================================================================
if __name__ == '__main__':
	print "Probando CLF"
	m = CLF("CLF prueba" )
	print m
	for node in m:
		print m.getAtomAttributes(node)
	m.writePSF()

