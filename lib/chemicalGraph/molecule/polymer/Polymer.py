# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva,  Radamés J.  Vega Alfaro, 
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


from lib.chemicalGraph.molecule.Molecule import Molecule
from conf.Wolffia_conf import *

class Polymer(Molecule):
   """
   Polymer is an abstract class.  Should not be directly instantiated.
   It models a linear polymer.
   """
   momomerAtoms = []  # lists of atom counts made by constructPDB()

   def __init__(self, chain, molname=None):
   		print("Polymer")
		if type(self) == Polymer:
		   raise Molecule.MoleculeError("Polymer is an abstract class.  Should not be directly instantiated.")
		
		if molname == None:
			molname = str(chain)
		
		Molecule.__init__(self, molname)
		
		if hasattr(self,'MONOMERS_PDBS'): self.chainOldStyle(chain)
		else: self.chainMolStyle(chain)



   def chainMolStyle(self, chain):
   		#import set
   		#print "chainMolStyle"
   		#print "chainMolStyle ", chain
		for dn in range(len(chain)):
			monomer = self.MONOMERS_MOLS[chain[dn]].copy()
			monomer.rotateRad(0.0, dn * self.ANGLE, 0.0)
			monomer.moveby([0.0, self.DISPL * dn, 0.0])

			if self.order() == 0:
				self.merge(monomer,[])
				lastSegment = set(self.atoms())
			else:
				#atomsToJoin = self.closestAtoms(monomer)
				# self.merge(monomer,[[self.order(), 1]])
				maxAtom = max(self)
				#self.merge(monomer,[self.closestAtoms(monomer,atomsSubset=lastSegment)])
				#print "chainMolStyle", [self.closestAtoms(monomer)]
				self.merge(monomer,[self.closestAtoms(monomer)])
				#lastSegment = [a+maxAtom for a in monomer]
				lastSegment = set(self.atoms()) - lastSegment

   def chainOldStyle(self, chain):
   		print("chainOldStyle")
		if len(chain) == 1:
		   self.load(self.ONE_MONOMER_PDB[chain[0]])
		   return
		
		for dn in range(len(chain)):
		   # print "Polymer(",NANOCAD_PDB_DIR+self.MONOMERS_PDBS[chain[dn]],")"
		   monomer = Molecule(chain[dn])
		   monomer.load(NANOCAD_PDB_DIR+self.MONOMERS_PDBS[chain[dn]], NANOCAD_PDB_DIR+self.MONOMERS_PSFS[chain[dn]])
		   monomer.rotateRad(0.0, dn * self.ANGLE, 0.0)
		   monomer.moveby([0.0, self.DISPL * dn, 0.0])
		   if self.order() == 0:
		      self.merge(monomer,[])
		   elif hasattr(self,'START_ATOM'):
		      self.merge(monomer,[[self.order() - self.NUM_ATOMS_BACKBONE_MONOMER + self.END_ATOM, self.START_ATOM]])
		   else:
		      self.merge(monomer,[[self.order(), 1]])


#==========================================================================
#sustituida
   def constructPDB2(self,chain):
      if len(chain) == 1:
         self.load(self.ONE_MONOMER_PDB[chain[0]])
         return

      tempname = tempfile.mktemp('.pdb')
      ftemp = open(tempname,'w')

      atomcount = 1

      # copy start monomer
      # monomer base PDB info
      # open source files and temp files
      f = open(NANOCAD_PDB_DIR+self.START_MONOMERS_PDBS[chain[0]])
      lines = f.readlines()
      f.close()
      for line in lines:
         if line.find('ATOM') > -1:
            #ftemp.write("ATOM %5d%69s" % (atomcount,line[10:79]))
            ftemp.write("ATOM  %5d %12s%2d%52s" % (atomcount,line[13:24],1,line[28:]))
            atomcount = atomcount+1
      #print atomcount-1, " atoms in start monomer."

      # copy n-2 copies of backbone
      # monomer base PDB info
      # open source files and temp files
      dn = 1  # in case there are two monomers
      for dn in range(1,len(chain)-1):
         f = open(NANOCAD_PDB_DIR+self.BACKBONE_MONOMERS_PDBS[chain[dn]])
         lines = f.readlines()
         f.close()
         for line in lines:
            if line.find('ATOM') > -1:
               #print line[0:80]+"\n"
               numatom = int(line[5:11])  # base atom id

               # coordinates
               x = float(line[31:38])
               z = float(line[47:54])
               #print line[47:56], '  ', z

               # write atom entry displaced DISPL amstrongs rotation ANGLE (rad)
               ftemp.write("ATOM  %5d %12s%2d%3s" % (atomcount,line[13:24],dn+1,line[28:30]))
               # rotated coordinates
               xr = math.cos(dn * self.ANGLE) * x + math.sin(dn * self.ANGLE) * z
               zr = math.cos(dn * self.ANGLE) * z - math.sin(dn * self.ANGLE) * x
               y = float(line[39:46]) + self.DISPL * dn
               ftemp.write("%8.3f" % xr,)
               ftemp.write("%8.3f" % y)
               ftemp.write("%8.3f" % zr)
               ftemp.write("%s" % line[54:])

               atomcount = atomcount + 1
         #print dn+1, " monomers (", atomcount-1, "atoms)"

      # copy end monomer
      # monomer base PDB info
      # open source files and temp files
      f = open(NANOCAD_PDB_DIR+self.END_MONOMERS_PDBS[chain[len(chain)-1]])
      lines = f.readlines()
      f.close()
      for line in lines:
         if line.find('ATOM') > -1:
            numatom = int(line[5:11])  # base atom id

            # coordinates
            x = float(line[31:38])
            z = float(line[47:54])

            # write entries for n atoms  displaced DISPL amstrongs
            dn = len(chain)-1
            # rotated coordinates
            xr = math.cos(dn * self.ANGLE) * x + math.sin(dn * self.ANGLE) * z
            zr = math.cos(dn * self.ANGLE) * z - math.sin(dn * self.ANGLE) * x
            ftemp.write("ATOM  %5d %12s%2d%3s" % (atomcount,line[13:24],dn+1,line[28:30]))
            #ftemp.write("ATOM  %5d %18s" % (atomcount,line[13:30]))
            ftemp.write("%8.3f" % xr,)
            y = float(line[39:46]) + self.DISPL * dn
            ftemp.write("%8.3f" % y)
            ftemp.write("%8.3f" % zr)
            ftemp.write("%s" % line[54:])

            atomcount = atomcount + 1
      #print "end monomer (", atomcount-1, "atoms)"

      # create molecule from temp file and clean up
      #self.mol = Molecule()
      ftemp.close()
      self.load(tempname)
      #os.remove(tempname)


