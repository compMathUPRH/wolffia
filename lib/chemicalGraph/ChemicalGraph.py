# ChemicalGraph.py
# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, Frances  Martínez Miranda, 
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

from math import *

from networkx.classes.graph import Graph
from networkx.algorithms.components.connected import connected_components
from networkx.algorithms.components.connected import connected_component_subgraphs
from networkx.algorithms import isomorphism, could_be_isomorphic, fast_could_be_isomorphic
import numpy

class ChemicalGraph(Graph):
    """
    """

    def __init__(self, oldCG=None):
        """
        """
        Graph.__init__(self, oldCG)
        self.matrix = [[1,0,0,0],[0,1,0,0],[0,0,1,0], [0,0,0,1]]
    #-------------------------------------------------------------
    def add_edge(self,bond): # overwrites Graph add_edge to receive one list instead of two parameters
        """
        """
        super(ChemicalGraph, self).add_edge(bond[0], bond[1])
        
    #-------------------------------------------------------------
    def loadFiles(self, pdbFile, psfFile):
        """Loads and parses PDB coordinate file and PSF topology file containing molecules.

        @type  pdbFile: string
        @param pdbFile: PDB filename.

        @type  psfFile: string
        @param psfFile: PDB filename.
        """
        from Bio.PDB.PDBParser import PDBParser
        from PSF import PSF

        atomsGen=PDBParser(PERMISSIVE=1).get_structure("ChemicalGraph", pdbFile).get_atoms()
        atoms = [a for a in atomsGen]
        psf=PSF(psfFile)
        if len(atoms) != len(psf.atoms):
            raise self.MoleculeError("Ammount of atoms in PDF and PSF files are different.")

        # add nodes
        elements = psf.get_elements()
        charges = psf.get_charges()
        print("ChemicalGraph loadFiles charges", charges[:30])
        masses = psf.get_masses()
        for n in range(len(atoms)):
            atom=atoms[n]
            atr = AtomAttributes(atom.get_name(), elements[n], atom.get_coord(), charges[n], masses[n], residue=atom.get_parent().get_resname())
            self.add_node(n+1, attrs=[atr])

        # add edges
        for bond in psf.bonds:
            self.add_edge(bond)

        # add everything else
        #_angles = psf.get_angles()
        #_dihedrals = psf.get_dihedrals()

    #-------------------------------------------------------------
    def connectedComponents(self):
        """Finds connected components of the graph (the molecules).

        @rtype:  list of instances of ChemicalGraph
        @return: List of connected components.
        """
        #print "connectedComponents ",self.__class__
        return connected_component_subgraphs(self)

    #-------------------------------------------------------------
    def connectedComponents3(self):
        """Finds connected components of the graph (the molecules).

        @rtype:  list of instances of ChemicalGraph
        @return: List of connected components.
        """
        result = []
        comp_conexos = connected_components(self)
        quedan=self.nodes()
        edges = self.edges()
    
        for comp in comp_conexos:
            result_graph = ChemicalGraph()
            result_graph.add_nodes(comp)

            for atom in result_graph.nodes():
                result_graph.add_node_attribute(atom, self.getAtomAttributes(atom))
        
            for index in edges:
                if (index[0] in pre_ordering) and (index[1] in pre_ordering) and not(index in result_graph.edges()) :     
                    result_graph.add_edge(index) 
                    #print result_graph

            # copy corresponding angles and dihedrars
            for atom in result_graph.nodes():
                for angle in result_graph._angles:
                    try:
                        pos = angle.index(atom)
                        result_graph._angles.append(angle)
                        break
                    except ValueError:
                        pass 
                for dihedral in result_graph._dihedrals:
                    try:
                        pos = dihedral.index(atom)
                        result_graph._dihedrals.append(dihedral)
                        break
                    except ValueError:
                        pass 

            result.append(result_graph)
        
            for v in pre_ordering:
                quedan.remove(v)
        
    
        return result

    #-------------------------------------------------------------
    def connectedComponents2(self):
        """Finds connected components of the graph (the molecules).

        @rtype:  list of instances of ChemicalGraph
        @return: List of connected components.
        """
        result = []
        quedan=self.nodes()
        edges = self.edges()
    
        while quedan != []:
            result_graph = ChemicalGraph()
            raiz=quedan[0]
            spanningTree, pre_ordering, post_ordering = depth_first_search(self, root=raiz)        
            result_graph.add_nodes(pre_ordering)

            for atom in result_graph.nodes():
                result_graph.add_node_attribute(atom, self.getAtomAttributes(atom))
        
            for index in edges:
                if (index[0] in pre_ordering) and (index[1] in pre_ordering) and not(index in result_graph.edges()) :     
                    result_graph.add_edge(index) 
                    #print result_graph

            # copy corresponding angles and dihedrars
            for atom in result_graph.nodes():
                for angle in result_graph._angles:
                    try:
                        pos = angle.index(atom)
                        result_graph._angles.append(angle)
                        break
                    except ValueError:
                        pass 
                for dihedral in result_graph._dihedrals:
                    try:
                        pos = dihedral.index(atom)
                        result_graph._dihedrals.append(dihedral)
                        break
                    except ValueError:
                        pass 

            result.append(result_graph)
        
            for v in pre_ordering:
                quedan.remove(v)
        
    
        return result

    #-------------------------------------------------------------
    def add_angles(self, angles):
        """
        """
        self._angles += angles
    #-------------------------------------------------------------
    def add_dihedrals(self, dihedrals):
        """
        """
        self._dihedrals += dihedrals

    #-------------------------------------------------------------
    def equalNodes(self, node1, node2):
        """
        """
        return self.node[node1]['attrs'][0] == self.node[node2]['attrs'][0]

    #-------------------------------------------------------------
    def is_isomorphic(graph1, graph2):
        """Determines if two graphs are isomorphic.

        @graph2:  graph to be compared to self
        @return: true if they are isomorphic.
        """

        if graph1.order() != graph2.order(): return False
        
        # select method to be used to determine isomorphism
        if graph1.order() > 5000:
            return fast_could_be_isomorphic(graph1,graph2)
        elif graph1.order() > 1000:
            return could_be_isomorphic(graph1,graph2)
        else:

            matcher = isomorphism.GraphMatcher(graph1,graph2)
    
            try:

                match_iter = matcher.isomorphisms_iter()
                for iso in match_iter:
                    sameAttributes = True
                    for atom in iso:
                        if not(graph1.getAttributes(atom).getInfo().getType() == graph2.getAttributes(iso[atom]).getInfo().getType()):
                            #print "is_isomorphic atributos diferentes",graph1.getAttributes(atom), graph2.getAttributes(iso[atom])
                            sameAttributes =  False
                            break    
                    if sameAttributes: return True
                return False
            except StopIteration: return False    

    
    #-------------------------------------------------------------
    def is_isomorphic3(graph1, graph2):
        """Determines if two graphs are isomorphic.

        @graph2:  graph to be compared to self
        @return: true if they are isomorphic.
        """
        print("graph1: " , graph1.order())
        print("graph2: " , graph2.order())
        matcher = isomorphism.GraphMatcher(graph1,graph2)

        if graph1.order() == graph2.order():
            print("order is the same")
            try:
                match_iter = next(matcher.isomorphisms_iter())
                for atom in match_iter:
                    if not(graph1.getAttributes(atom) == graph2.getAttributes(match_iter[atom])):
                        return False
                        break
    
    
                return True
            except StopIteration: return False    
        else: return False
    #-------------------------------------------------------------
    def is_isomorphic2(graph1, graph2):
        """Determines if two graphs are isomorphic.

        @graph2:  graph to be compared to self
        @return: true if they are isomorphic.
        """
        matcher = isomorphism.GraphMatcher(graph1,graph2)
        match_iter = matcher.isomorphisms_iter()
        print("is_isomorphic(graph1, graph2)")
        print("graph1: " , graph1.order())
        print("graph2: " , graph2.order())
        print("match_iter + ",match_iter)
        for iso in match_iter:
            print("iso = ",iso)
            for atom in iso:
                print("pair = ",atom, iso[atom])
                if not(graph1.getAttributes(atom) == graph2.getAttributes(iso[atom])):
                    print("is_isomorphic: False")
                    return False
                    break
                print("is_isomorphic: True")
            
            
        return True
                
    #-------------------------------------------------------------
    '''
    def __eq__(self, graph2):
        """Determines if two graphs are equal (more than isomorphic).

        @graph2:  graph to be compared to self
        @return: true if they are equal.
        """
        print "ChemicalGraph __eq__"
        if isinstance(graph2, ChemicalGraph):
            return ChemicalGraph.is_isomorphic(self, graph2)
        else:
            return False
    '''
    #-------------------------------------------------------------
    def getAtomAttributes(self, node):
        """
        """
        return self.node[node]['attrs'][0]

    #-------------------------------------------------------------
    def atoms_attributes(self):
        """
        """
        result = ""
        for atom in self.nodes():
            #result += str(atom) + ": " + str(self.node[atom]['attrs'][0]) + "\n"
            result += str(atom) + ": " + str(self.getAttributes(atom)) + "\n"
        return result

    #-------------------------------------------------------------
    def add_atom(self, atom, attribute):
        """
        """
        raise MoleculeError("Molcule.add_atom() not implemented yet.")

    #-------------------------------------------------------------
    def add_bond(self, bond):
        """
        """
        self.add_edge(bond)

    #-------------------------------------------------------------
    def merge(self, chGr, newBonds=[]):
        """Merges chGr into self.  Atom labels of chGr are modified to avoid name collisions
        with existing atoms.

        @type  chGr: ChemicalGraph.
        @param chGr: Graph to be merged into self.

        @type  newBonds: list of pairs of integers.
        @param newBonds: Bonds to be added between the two molecules to form a new molecule.  For each pair, the first integer is an atom (int) of the first molecule and the second an atom of the second.
        """

        try:
            base = max(self.atoms())
        except ValueError:
            base = 0  # merging into an empty graph

        for atom in chGr.atoms():
            self.add_node(atom+base, attrs=[chGr.getAtomAttributes(atom)])
        for edge in chGr.edges():
            try:  # avoids adding an edge twice
                self.add_edge([edge[0]+base, edge[1] + base])
            except AdditionError:
                pass

        for edge in newBonds:
            self.add_edge([edge[0], edge[1] + base])
            #print "LINK ", [edge[0], edge[1] + base]

    #-------------------------------------------------------------
    def copy(self):
        """
        """
        newCG = ChemicalGraph()
        newCG = Graph.copy(self)
        
        return newCG
        
    #-------------------------------------------------------------
    def moveby(self, displ): # backward compatibility
        """
        """
        self.moveBy(displ)


    #-------------------------------------------------------------
    def moveBy(self, displ):
        """Moves the atoms in the graph (self).

        @type displ: list of three floats
        @param displ: displacement of the atoms in the graph.
        """

        if len(displ) != 3:
            raise self.MoleculeError("Argument \"displ\" in Molecule.moveby(self, displ) should a list of 3 numbers.")
        for atom in self.nodes():
            self.getAtomAttributes(atom).moveby(displ)
        
        
        #=======================================================================
        # Rotational matrix
        # self.matrix[3][0] += displ[0]
        # self.matrix[3][1] += displ[1]
        # self.matrix[3][2] += displ[2]
        # print "moveBy ", self.matrix
        #=======================================================================
    
    #-------------------------------------------------------------
    def rotate(self, matr):
        
        """Rotate the atoms in the graph (self).

        @type matr: list of three lists of three floats
        @param matr: rotation matrix.
        """
        #=======================================================================
        # Rotational Matrix thing
        # new_matrix = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,1]]
        # for i in range(3):
        #    for j in range(3):
        #        for k in range(3):
        #            new_matrix[i][j] += self.matrix[i][k]*matr[k][j]        
        # self.matrix = new_matrix
        # print "rotate ", self.matrix
        #=======================================================================

        for atom in self.nodes():
            self.getAtomAttributes(atom).rotate(matr)


    #-------------------------------------------------------------
    def angles(self):
        """Returns angles.

        @rtype:  list of integers.
        @return: Atoms of the molecules.
        """
        return self._angles
    #-------------------------------------------------------------
    def numberOfNodes(self):
        """Returns amount of nodes in the graph.

        @rtype:  an integer.
        @return: 
        """        
        return self.number_of_nodes()
    
     #-------------------------------------------------------------
    def numberOfEdges(self):
        """Returns amount of nodes in the graph.

        @rtype:  an integer.
        @return: 
        """        
        return self.number_of_edges()   

    #-------------------------------------------------------------
    def rotateDeg(self, angleX, angleY, angleZ):
        """
        """
        #print "rotateDeg ", angleX, angleY, angleZ, 
        angleX = angleX * pi / 180
        angleY = angleY * pi / 180
        angleZ = angleZ * pi / 180
        #print " -> ", angleX, angleY, angleZ
        self.rotateRad(angleX, angleY, angleZ)

    #-------------------------------------------------------------
    def rotateRad(self, angleX, angleY, angleZ):
        """
        Constructs rotation matrix (column-major)
        """
        #row-major one here
        rmatr = [[cos(angleY) * cos(angleZ), -cos(angleX) * sin(angleZ) + sin(angleX) * sin(angleY) * cos(angleZ), sin(angleX) * sin(angleZ) + cos(angleX) * sin(angleY) * cos(angleZ)], [cos(angleY) * sin(angleZ), cos(angleX)* cos(angleZ) + sin(angleX) * sin(angleY) * sin(angleZ), -sin(angleX) * cos(angleZ) + cos(angleX) * sin(angleY)* sin(angleZ)], [-sin(angleY), sin(angleX) * cos(angleY), cos(angleX) * cos(angleY)]]
        #print "rotateRad ", rmatr
        #This is the column-major one
        #rmatr = [[cos(angleY) * cos(angleZ), cos(angleY) * sin(angleZ), -sin(angleY), sin(angleX) * cos(angleY)], [-cos(angleX) * sin(angleZ) + sin(angleX) * sin(angleY) * cos(angleZ), cos(angleX)* cos(angleZ) + sin(angleX) * sin(angleY) * sin(angleZ), sin(angleX) * cos(angleY)], [sin(angleX) * sin(angleZ) + cos(angleX) * sin(angleY) * cos(angleZ), -sin(angleX) * cos(angleZ) + cos(angleX) * sin(angleY)* sin(angleZ), cos(angleX) * cos(angleY)]]
        self.rotate(numpy.matrix(rmatr))

    #-------------------------------------------------------------
    class ChemicalGraphError(Exception):
        """
        """
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
    #-------------------------------------------------------------




