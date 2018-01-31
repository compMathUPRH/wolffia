# -*- coding: utf-8 -*-
# Authors: José O. Sotero Esteva
#	Department of Mathematics, University of Puerto Rico at Humacao
#	Humacao, Puerto Rico
#	jse@math.uprh.edu


SOLVENT_BOX_SOLVENTS = ['WAT']


class SolventBox(Mixture):	

	def __init__(self, solvent='WAT'):
		"""
		Box of Solvent.

		@type  attributes: list
		@param attributes: other attributes not in the class fields list.

		"""
		Mixture.__init__(self)



