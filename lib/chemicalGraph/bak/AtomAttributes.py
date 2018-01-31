# -*- coding: utf-8 -*-
# positions of attributes
#
#	Department of Mathematics, University of Puerto Rico at Humacao
#	Humacao, Puerto Rico
#	jse@math.uprh.edu
#
#  Department of Mathematics
#  University of Puerto Rico at Humacao
#
#  Acknowledgements: The main funding source for this project has been provided
#  by the UPR-Penn Partnership for Research and Education in Materials program, 
#  USA National Science Foundation grant number DMR-0934195. 
#---------------------------------------------------------------------------

import math



class AtomAttributes():
	"""Holds the attributes of an atom including coordinates, element, mass, charge
	and other properties found in PDB files.
	"""
	

	def __init__(self, name, elmt, coord, ch, m, bfactor = '',occup = 1,altloc = ' ',fullname = 'X',res='',chain='A',attrs=[]):
		"""Atom Attributes.
		@type	name:	string
		@param	name:	atom name
		@type	elmt:	string
		@param	elmt:	element name
		@type	coord:	list of 3 floats
		@param	coord:	coordinates
		@type	ch:	string
		@param	ch:	
		@type	m:	float
		@param	m:	atom mass
		@type	bfactor:string
		@param	bfactor:	
		@type	occup:	
		@param	occup:	
		@type	altloc:	
		@param	altloc:	
		@type	fullname:string
		@param	fullname:	
		@type	res:	string
		@param	res:	
		@type	chain:	string
		@param	chain:	
		@type	attrs:	list
		@param	attrs:	other attributes not in the class fields list.

		"""
		self._attributes = attrs
		self._element = elmt
		self._coordinates = coord
		self._mass = m
		self._charge = ch
		self._name = name
		self._bfactor = bfactor
		self._occupancy = occupancy
		self._altloc = altloc
		self._fullname = fullname
		self._residue = "XXX"
		self._chain = chain
		self._res_seq = 1
	#-------------------------------------------------------------
	def PSFline(self, ser_num):
		"""ATOM line corresponding to this atom (self) for a PSF file.

		@type ser_num:	int
		@param ser_num:	sequence number to be used.

		@rtype:  string
		@return: ATOM line.
		"""
		return "%8i %4s%2s    %3s%5s   %-5s   %+8.6f %9.4f           0" % (ser_num,"MAIN",self._chain,self._residue,self._element,self._name,self._charge,self._mass)

	#-------------------------------------------------------------
	def PDBline(self, ser_num):
		"""ATOM line corresponding to this atom (self) for a PDB file.

		@type ser_num:	int
		@param ser_num:	sequence number to be used.

		@rtype:  string
		@return: ATOM line.
		"""
		return "%s%4i  %-4s%c%3s %s%4i%c   %8.3f%8.3f%8.3f%6.2f%6.2f        %4s%2s%2s" % ("ATOM  ",ser_num,self._name,' ',self._residue,self._chain,1,' ',self._coordinates[0],self._coordinates[1],self._coordinates[2],self._occupancy,0.0,'    ',self._element,'  ')

	#-------------------------------------------------------------
	def getElement(self):
		"""Element of the atom.

		@rtype:  string
		@return: Element of the atom.
		"""
		return self._element
	#-------------------------------------------------------------
	def getCoord(self):
		"""Coordinates of the atom.

		@rtype:  list
		@return: Coordinates of the atom.
		"""
		return self._coordinates

	#-------------------------------------------------------------
	def distanceTo(self, attr2):
		"""Calculates distance between the coordinates in self and in attr2.

		@type attr2:	list of 3 floats.
		@param attr2:	attributes of second atom.

		@rtype:  float
		@return: distance.
		"""

		dx = self._coordinates[0]-attr2._coordinates[0]
		dy = self._coordinates[1]-attr2._coordinates[1]
		dz = self._coordinates[2]-attr2._coordinates[2]
		return math.sqrt(dx*dx+dy*dy+dz*dz)

	#-------------------------------------------------------------
	def getCharge(self):
		"""Charge of the atom.

		@rtype:  float
		@return: Charge of the atom.
		"""
		return self._charge

	#-------------------------------------------------------------
	def getMass(self):
		"""Mass of the atom.

		@rtype:  float
		@return: Mass of the atom.
		"""
		return self._mass

	#-------------------------------------------------------------
	def moveby(self, displ): # backward compatibility
		self.moveBy(displ)

	#-------------------------------------------------------------
	def moveBy(self, displ):
		"""Moves the atom (self).

		@type displ:	list of three floats
		@param displ:	displacement of the atom.
		"""
		self._coordinates[0] += displ[0]
		self._coordinates[1] += displ[1]
		self._coordinates[2] += displ[2]

	#-------------------------------------------------------------
	def rotate(self, matr):
		"""Rotate the atom (self).

		@type displ:  list of three lists of three floats
		@param displ: rotation matrix.
		"""
		self._coordinates = [sum([matr[i][j] * self._coordinates[j] for j in range(3)]) for i in range(3)]

	#-------------------------------------------------------------
	def setCoord(self, newCoords):
		"""Coordinates of the atom.

		@rtype:  list of 3 floats
		@return: Coordinates of the atom.
		"""
		self._coordinates = newCoords


	#-------------------------------------------------------------
	def __eq__(self, node2):
		"""Determines if two nodes are equal.

		@type	node2: attributes of second atom
		@param	node2: node to be compared to self
		@rtype:  boolean
		@return: true if elements are equal.
		"""
		#print " Determines if two nodes are equal." 
		return self._element == node2._element

	#-------------------------------------------------------------
	def __str__(self):
		"""String representation of attributes.
		@rtype:  string
		@return: String representation of attributes.
		"""
		return "AtomAttributes{" + self._element + ", " + str(self._coordinates) + ", " + str(self._mass) + ", " + str(self._charge) + ", " + str(self._attributes) + "}"


	#-------------------------------------------------------------
	class AtomAttributesError(Exception):
		"""
		"""
		def __init__(self, value):
			"""Initializes AtomAttributesError 
			@type	value: string.
			@param	value: error message.
			"""
			self.value = value

		def __str__(self):
			"""String representation of AtomAttributesError.
			@rtype:  string
			@return: error message.
			"""
			return repr(self.value)


