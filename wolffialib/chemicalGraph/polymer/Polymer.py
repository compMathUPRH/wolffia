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


from wolffialib.chemicalGraph.Molecule import Molecule
#from conf.Wolffia_conf import *

class Polymer(Molecule):
   """
   Polymer is an abstract class.  Should not be directly instantiated.
   It models a linear polymer.
   """
   momomerAtoms = []  # lists of atom counts made by constructPDB()

   def __init__(self, chain, molname=None):
   		#print( "Polymer")
   		if type(self) == Polymer:
   		    Molecule.MoleculeError("Polymer is an abstract class.  Should not be directly instantiated.")
		
   		if molname == None:
   		    molname = str(chain)
		
   		Molecule.__init__(self, molname)
		
   		if hasattr(self,'MONOMERS_PDBS'): self.chainOldStyle(chain)
   		else: self.chainMolStyle(chain)



   def chainMolStyle(self, chain):
   		for dn in range(len(chain)):
   		    monomer = self.MONOMERS_MOLS[chain[dn]].copy()
   		    monomer.rotateRad(0.0, dn * self.ANGLE, 0.0)
   		    monomer.moveby([0.0, self.DISPL * dn, 0.0])

   		    if self.order() == 0:
   		        self.merge(monomer,[])
   		        lastSegment = set(self.atoms())
   		    else:
   		        maxAtom = max(self)
   		        self.merge(monomer,[self.closestAtoms(monomer)])
   		        lastSegment = set(self.atoms()) - lastSegment

   def chainOldStyle(self, chain):
   		print ("chainOldStyle")
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

