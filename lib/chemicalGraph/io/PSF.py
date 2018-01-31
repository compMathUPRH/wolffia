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
import sys
class PSF(object):
	def __init__(self, filename ):
	      # open source file
	      f = open(filename)

	      atomcount = 1
	      self.atoms = []
	      self._elements = []
	      self._charges = []
	      self._masses = []
	      self.bonds = []
	      self.angles = []
	      self.dihedrals = []
	      self.types = []
	      self.elements = []
	      self.charges = []
	      self.masses = []
	      self.types = []

	      for line in f:
		 if line.find('!NATOM') > -1:
		    atomBase = atomcount - 1
		    natoms = int(line[:8])
		    for i in range(0, natoms):
		       line = f.next()
		       self.atoms.append("%8d" % (atomcount) + line[8:])
		       #print "%8d" % (atomcount) + line[8:]
		       atomcount = atomcount+1

		 if line.find('!NBOND') > -1:
		    nbonds = int(line[:8])
		    for i in range(0, nbonds/4):
		       line = f.next()
		       self.bonds.append([int(line[:8])+atomBase, int(line[9:16])+atomBase])
		       self.bonds.append([int(line[17:24])+atomBase, int(line[25:32])+atomBase])
		       self.bonds.append([int(line[33:40])+atomBase, int(line[41:48])+atomBase])
		       self.bonds.append([int(line[49:56])+atomBase, int(line[57:64])+atomBase])
		    line = f.next()
		    for i in range(0, nbonds % 4):
		       self.bonds.append([int(line[i*16+1: i*16+8])+atomBase, int(line[i*16+9: i*16+16])+atomBase])

		 if line.find('!NTHETA') > -1:
		    nangles = int(line[:8])
		    for i in range(0, nangles/3):
		       line = f.next()
		       self.angles.append([int(line[:8])+atomBase, int(line[9:16])+atomBase,int(line[17:24])+atomBase])
		       self.angles.append([int(line[25:32])+atomBase, int(line[33:40])+atomBase, int(line[41:48])+atomBase])
		       self.angles.append([int(line[49:56])+atomBase, int(line[57:64])+atomBase, int(line[65:72])+atomBase])
		    line = f.next()
		    for i in range(0, nangles % 3):
		       self.angles.append([int(line[i*24+1: i*24+8])+atomBase, int(line[i*24+9: i*24+16])+atomBase, int(line[i*24+17: i*24+24])+atomBase])

		 if line.find('!NPHI') > -1:
		    ndihedrals = int(line[:8])
		    for i in range(0, ndihedrals/2):
		       line = f.next()
		       self.dihedrals.append([int(line[:8])+atomBase, int(line[9:16])+atomBase,int(line[17:24])+atomBase,int(line[25:32])+atomBase])
		       self.dihedrals.append([int(line[33:40])+atomBase, int(line[41:48])+atomBase,int(line[49:56])+atomBase, int(line[57:64])+atomBase])
		    line = f.next()
		    for i in range(0, ndihedrals % 2):
		       self.dihedrals.append([int(line[i*32+1: i*32+8])+atomBase, int(line[i*32+9: i*32+16])+atomBase, int(line[i*32+17: i*32+24])+atomBase, int(line[i*32+25: i*32+32])+atomBase])
	      f.close()

              # print [atom[23:26] for atom in self.atoms]
              self._elements = [atom[24:29].strip() for atom in self.atoms]
              self._charges = [float(atom[36:48]) for atom in self.atoms]
              self._masses = [float(atom[50:58]) for atom in self.atoms]
              self._types = [atom[29:34].strip() for atom in self.atoms]

	#-------------------------------------------------------------
	def inferAngles(self, molecule):
		#from chemicalGraph import Mixture
		#print "molecula: '", molecule, "'"
		angles = list()
		for atom in molecule:
			if atom <= 28:
				neigh = molecule.neighbors(atom)
				#print "Neighbours: ", atom, ", ", neigh
				for n1 in neigh:
					for n2 in neigh:
						if n1 < n2 and n2 < 28 and atom < 10:
							#print (n1, atom, n2)
							awesome = self._types[n1] + " " + self._types[atom] + " " + self._types[n2]
							#print awesome, (n1, atom, n2), "awesome"
							radical = self._types[n2] + " " + self._types[atom] + " " + self._types[n1]
							#print radical, (n2, atom, n1), "radical"
							#print ff._ANGLES
							if awesome in ff._ANGLES:
								print "Append: '" + awesome + "' <<< awesome", ([n1,atom,n2])
								angles.append([n1,atom,n2])
								#print ff._ANGLES[awesome]
							elif radical in ff._ANGLES:
								print "Append: '" + radical + "' <<< radical", ([n1,atom,n2])
								angles.append([n1,atom,n2])
								#print ff._ANGLES[radical]
							else:
								print "NoAppd:", ([n1,atom,n2]), awesome, ";", radical
				#print "This.Type: ", self._types[atom]
		#print "Angles:", angles
		#print "Tipos:", self._types
		
		for angle in angles:
			if not self.hasAngle(angle):
				self.angles.append(angle)

	#-------------------------------------------------------------
	@staticmethod
	def write(mixture, psfFile=None):
		"""
		Writes a PSF topology file.

		@type  psfFile: string
		@param psfFile: PSF filename.  If None it will write to sys.stdout.
		"""

		if psfFile==None:
			fd = sys.stdout
			#print  "writePSF imprimiendo stdout"
		else:
			fd = open(psfFile, 'w')
			#print  "writePSF(",psfFile,")"

		# write ATOM section
		fd.write("PSF\n\n       1 !NTITLE\n REMARKS \n\n%8i !NATOM\n" % mixture.order())
		count = 1
		renumbering = dict()  # atoms labels may not be [1..n]
		for molecule in mixture:
			renumbering[molecule] = dict()
			mol = mixture.getMolecule(molecule)
			#print "PSF write " , molecule, mixture.trad[molecule]
			for atom in mol:
				atr     = mol.atom_attributes(atom)
				#charge = mol.getForceField().charge(atr.getInfo().getType())
				charge  = atr.getInfo().getCharge()
				#print "PSF.write", atr.getInfo().getType(),charge
				psfline = atr.getInfo().PSFline(count, mixture.trad[molecule])
				psfline = "%s%+8.6f%s\n" % (psfline[:38], charge, psfline[47:]) 
				fd.write(psfline)
				#fd.write(atr.PSFline(count)+"\n")
				renumbering[molecule][atom] = count

				count += 1
			
		# write BOND section
		fd.write("\n%8i !NBOND\n" % mixture.bonds())
		count = 0
		bondCount = 0
		for molecule in mixture:
			mol = mixture.getMolecule(molecule)
			bondsT = mol.bonds()
			nbonds = len(bondsT)
			#bonds = list()
			for bond in bondsT:
				#bonds.append([bond[0]+count, bond[1]+count])
				fd.write("%8d%8d" % (renumbering[molecule][bond[0]], renumbering[molecule][bond[1]]))
				bondCount += 1
				if bondCount % 4 == 0:
					fd.write("\n")
			#for i in range(0, nbonds - nbonds % 4, 4):
				#fd.write("%8d%8d" % (bonds[i][0], bonds[i][1]))
			count += mol.order()

		# write angles
		fd.write("\n\n%8d !NTHETA: angles\n" % mixture.angleCount())
		count = 0
		angleCount = 0
		for molecule in mixture:
			mol = mixture.getMolecule(molecule)
			anglesT = mol.angles()
			nangles = len(anglesT)
			#angles = list()
			for angle in anglesT:
				#angles.append([angle[0]+count, angle[1]+count])
				fd.write("%8d%8d%8d" % \
						(renumbering[molecule][angle[0]], \
						 renumbering[molecule][angle[1]], \
						 renumbering[molecule][angle[2]]))
				angleCount += 1
				if angleCount % 3 == 0:
					fd.write("\n")
			#for i in range(0, nangles - nangles % 4, 4):
				#fd.write("%8d%8d" % (angles[i][0], angles[i][1]))
			count += mol.order()


		# write dihedrals
		fd.write("\n\n%8d !NPHI: dihedrals\n" % (0))

		# write other stuff
		fd.write("\n\n%8d !NIMPHI: impropers\n" % (0))
		fd.write("\n\n%8d !NDON: donors\n" % (0))
		fd.write("\n\n%8d !NACC: acceptors\n" % (0))
		fd.write("\n\n%8d !NNB\n" % (0))
		fd.write("\n\n%8d !NGRP\n" % (0))

		fd.close()
			

	#-------------------------------------------------------------
	def getAngles(self):
		return self.angles

	def getDihedrals(self):
		return self.dihedrals

	def getElement(self, i):
		return self._elements[i]

	def getCharge(self, i):
		return self._charges[i]

	def getMass(self, i):
		return self._masses[i]

	def getType(self, i):
		return self._types[i]

	def len(self):
		return len(self.atoms)
	
	def hasAngle(self, angle):
		return angle in self.angles or angle.reverse() in self.angles

if __name__ == '__main__':
	import os
	sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../conf')
	from Wolffia_conf import *
	from chemicalGraph.molecule.ForceField import ForceField
	from chemicalGraph.molecule.polymer.PolyCYT import PolyCYT
	#ff = ForceField("pruebaCYT", "../../../data/forceFields/PolyCYT.prm")
	m = PSF("../../../data/coordinates/Polymers/CYT/start_CYT.psf")

	assert(m.getMass(5) == 12.011)

	mol = PolyCYT(1)
	ff = mol.getForceField()
	print mol.__dict__.keys()
	m.inferAngles(mol)
	print "FF Angles:\n", ff._ANGLES, "\n======================================"
	assert(m.hasAngle([1, 2, 3]))
	
	assert(True)
