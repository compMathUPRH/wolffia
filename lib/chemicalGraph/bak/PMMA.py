# PMMA.py

#import sys
#sys.path.append('/usr/local/lib/vmd/scripts/python/')

print "Instalando PMMA"


# import string
# import tempfile
# import os
from Homopolymer import *
import math

class  PMMA(Homopolymer):
   BACKBONE_MONOMER_PDB='/Polymers/PMMA/backbonePMMA.pdb'
   START_MONOMER_PDB='/Polymers/PMMA/startPMMA.pdb'
   END_MONOMER_PDB='/Polymers/PMMA/endPMMA.pdb'
   ONE_MONOMER_PDB='/Polymers/PMMA/onePMMA.pdb'
   BACKBONE_MONOMER_PSF='/Polymers/PMMA/backbonePMMA.psf'
   START_MONOMER_PSF='/Polymers/PMMA/startPMMA.psf'
   END_MONOMER_PSF='/Polymers/PMMA/endPMMA.psf'
   ONE_MONOMER_PSF='/Polymers/PMMA/endPMMA.psf'
   NUM_ATOMS_START_MONOMER=16
   NUM_ATOMS_BACKBONE_MONOMER=15
   NUM_ATOMS_LAST_MONOMER=4
   DISPL = 3.7
   ANGLE = 3 * math.pi / 4

   def __init__(self,n):
	# initialize base class
	Homopolymer.__init__(self, n, "PMMA(" + str(n) +")")




