# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Brnardo A. Roque Carrión, 
    Lemuel I. Rivera Cantú
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

from wolffialib.chemicalGraph.polymer.Homopolymer import Homopolymer
from wolffialib.chemicalGraph.Molecule import Particle
from wolffialib.chemicalGraph.ForceField import NonBond

        
class ParticleChain(Homopolymer):
    ''' ParticleChain is aHomopolymer in which the monomers are single particles.
        Usefull for coarse grain simulations.
    '''
    END_ATOM                   = 1
    START_ATOM                 = 1
    DISPL                      = NonBond._SIGMA
    ANGLE                      = 0

    def __init__(self,n, name="ParticleChain", atomType='PCH', atomElement='Xx', bondLength=NonBond._SIGMA, mass=1, charge=0):
        ''' int n: number of particles in the chain.
        string name: name of the chain (defaults to "ParticleChain")
        string atomType: name given to atom types (defaults to 'PCH')
        '''
        
        self.DISPL = bondLength
        bead = Particle(atomType, atomType, atomElement, mass=mass, charge=charge)
        self.BACKBONE_MONOMER_MOL = bead
        self.START_MONOMER_MOL    = bead
        self.END_MONOMER_MOL      = bead
        self.ONE_MONOMER_MOL      = bead

        super().__init__(n, "{:s}({:d})".format(name, n))
        
        # add FF parameters for monomer junctions
        ff = self.getForceField()
        ff.setBond((atomType,atomType),  305., NonBond._EPSILON)
        ff.setAngle((atomType,atomType,atomType),  0.,  0)
        ff.setDihedral((atomType,atomType,atomType,atomType), 0, 0)
        
        self.setForceField(ff)
        self.copyChargesToForceField()

#==========================================================================
if __name__ == '__main__':
    print("Testing ParticleChain")
    
    p = Particle()
    assert(len(p) == 1)
    
    pc = ParticleChain(10, name='NewChain', atomType='BEA')
    print(len(pc))
    assert(len(pc) == 10)
    
    print("Particle and ParticleChain passed all tests.")
