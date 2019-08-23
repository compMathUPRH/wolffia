if __name__ == '__main__':
	import sys, os
	sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../')
	print os.path.dirname(os.path.realpath(__file__))+'/../../'
	
from lib.chemicalGraph.Mixture import Mixture
from lib.chemicalGraph.molecule.AtomAttributes import *
from lib.chemicalGraph.ChemicalGraph import ChemicalGraph

def readfile(filename):
	import re
	f = open(filename, "r")
	N = int(f.readline().strip("\n"))
	chemicalGraphMixed = ChemicalGraph()
	adjLists = dict()
	
	for i in range(N):
		line = re.findall(r"[\w']+", f.readline())
		elt, atomNum, x, y, z, ignored = line[:6]
		atomNum = int(atomNum)
		
		atomType = elt  # Hay que revisar esto, aqui debe ir otra cosa
		symbol   = elt
		coords   = [float(x), float(y), float(z)]
		name	 = elt
		residue  = elt
		psfType  = elt
		charge   = 0.0
		mass	 = 12.
		
		ai  = AtomInfo(atomType, symbol, psfType, charge, mass, 1, 1, 1, name, residue)
		atr = AtomAttributes(ai, coords, [])
		print atr
		chemicalGraphMixed.add_node(i + 1, attrs=[atr])
		adjLists[i+1] = list()
		for e in line[9:]:
			adjLists[i+1].append(e)
	print adjLists
	for n in adjLists:
		for e in adjLists[n]:
			chemicalGraphMixed.add_edge([n,e])
			
	return chemicalGraphMixed




#==========================================================================
if __name__ == '__main__':
	import sys, os
	sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../')
	print os.path.dirname(os.path.realpath(__file__))+'/../../'
	
	r = readfile("/home/jse/inv/Cuchifritos/bazaar/Wolffia/data/coordinates/Fullerenes/C60-Ih.cc1")
	print r
