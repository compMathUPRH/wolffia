# Graphene.py
# -*- coding: utf-8 -*-
#
# Author: José O. Sotero Esteva
#	Department of Mathematics, University of Puerto Rico at Humacao
#	Humacao, Puerto Rico
#	jse@math.uprh.edu
#

print "Instalando Graphene"

from Hexagonal2D import Hexagonal2D

class  Graphene(Hexagonal2D):
	def __init__(self,n,m,length):
		Hexagonal2D.__init__(self,n,m,length, element="C", bondLength=1.4201, mass=12)

if __name__ == "__main__":
	gr = Graphene(0,10, 50)
	gr.writePDB()
	#gr.printXYZ()
