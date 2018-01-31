# PolyCYT.py

#import sys
#sys.path.append('/usr/local/lib/vmd/scripts/python/')

print "Instalando PolyCYT"


from Homopolymer import *
import math


class  PolyCYT(Homopolymer):
   BACKBONE_MONOMER_PDB='/Polymers/CYT/backbone_CYT.pdb'
   START_MONOMER_PDB='/Polymers/CYT/start_CYT.pdb'
   END_MONOMER_PDB='/Polymers/CYT/end_CYT.pdb'
   ONE_MONOMER_PDB='/Polymers/CYT/one_CYT.pdb'
   BACKBONE_MONOMER_PSF='/Polymers/CYT/backbone_CYT.psf'
   START_MONOMER_PSF='/Polymers/CYT/start_CYT.psf'
   END_MONOMER_PSF='/Polymers/CYT/end_CYT.psf'
   ONE_MONOMER_PSF='/Polymers/CYT/one_CYT.psf'
   NUM_ATOMS_START_MONOMER=32
   #NUM_ATOMS_BACKBONE_MONOMER=
   #NUM_ATOMS_LAST_MONOMER=
   DISPL = 6.0
   ANGLE = math.pi / 6.0
   #ANGLE = 0.0

   def __init__(self,n):
	# initialize base class
	Homopolymer.__init__(self, n, "PolyCYT(" + str(n) +")")

