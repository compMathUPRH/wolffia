# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, Carlos J.  Cortés Martínez, Frances  Martínez Miranda, 

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


import math, binascii, inspect
import numpy

class AtomInfo(object):
	"""Holds the attributes of an atom including coordinates, element, mass, charge
	and other properties found in PDB files.
	"""
	

	def __init__(self, name, elmt, elttype, ch, m, bfactor = '',occup = 1,altloc = ' ',fullname = 'X',res='XXX',chain='A', res_seq = 1):
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
		@param	res:	residue
		@type	chain:	string
		@param	chain:	
		@type	res_seq:integer
		@param	res_seq:	
		@type	attrs:	list
		@param	attrs:	other attributes not in the class fields list.
		@type	type:	string
		@param	type:	type of atom (usually obtained from PSF).

		"""
		self._element = elmt
		self._mass = m  # asociar a tipo
		self._charge = ch 
		self._name = name   # eliminar
		self._fullname = fullname  # asociar a tipo
		self._residue = res  # asociar a tipo
		self._chain = chain  # asociar a tipo
		self._res_seq = res_seq   # asociar a tipo
		self._type = elttype
	#-------------------------------------------------------------
	'''
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return  self._type == other._type
		else: return False
	'''
	#-------------------------------------------------------------
	def __lt__(self, other): return self._type < other._type
	def __gt__(self, other): return self._type > other._type
	def __eq__(self, node2):
		"""Determines if two nodes are equal.

		@type	node2: attributes of second atom
		@param	node2: node to be compared to self
		@rtype:  boolean
		@return: true if elements are equal.
		"""
		#print "AtomInfo ", self.__dict__, node2.__dict__, self.__dict__ == node2.__dict__
		return self.__dict__ == node2.__dict__
 
	def __ne__(self, node2):
		return not self == node2

	
	def PSFline(self, ser_num, trad={}):
		"""ATOM line corresponding to this atom (self) for a PSF file.

		@type ser_num:	int
		@param ser_num:	sequence number to be used.

		@rtype:  string
		@return: ATOM line.
		"""
		#print "PSFline: ", trad
		if len(trad) > 0:
		 	#print "PSFline trad:", trad
			typename = trad[self.getType()]
		else:
			typename = self._type

		#return "%8i %4s%2s    %3s%5s  %-5s    %+8.6f %9.4f           0" % (ser_num,"MAIN",self._chain,self._residue,self._name,typename,self._charge,self._mass)
		return "%8i %4s%2s    %3s%5s  %-5s    %+8.6f %9.4f           0" % (ser_num,"MAIN",self._chain,self._residue,self._name,typename,0.0,self._mass)

	#-------------------------------------------------------------
	#-------------------------------------------------------------
	def getElement(self):
		"""Element of the atom.

		@rtype:  string
		@return: Element of the atom.
		"""
		return self._element
	#-------------------------------------------------------------
	def getName(self):
		"""Name of the atom.

		@rtype:  string
		@return: Name of the atom.
		"""
		return self._name
	#-------------------------------------------------------------
	def getCharge(self):
		"""Charge of the atom.

		@rtype:  float
		@return: Charge of the atom.
		"""
		return self._charge

	def setCharge(self, charge):
		"""Set Charge of the atom.

		@rtype:  float
		@return: Charge of the atom.
		"""
		self._charge = charge

	#-------------------------------------------------------------
	def getMass(self):
		"""Mass of the atom.

		@rtype:  float
		@return: Mass of the atom.
		"""
		return self._mass
	#-------------------------------------------------------------
	def __str__(self):
		"""String representation of attributes.
		@rtype:  string
		@return: String representation of attributes.
		"""
		#return "AtomAttributes{" + self._element + ", " + str(self._coordinates) + ", " + str(self._mass) + ", " + str(self._charge) + ", " + str(self._attributes) + "}"
		return "AtomInfo(\"" \
			+ str(self._name)       + "\", \"" + self._element     + "\", "   \
			+ str(self._charge)     + ", "     +  str(self._mass)  + ", "    \
			+ "\', \""  + str(self._fullname)    + "\", \""\
			+ str(self._residue)    + "\", \"" + str(self._chain)  + "\", "    + str(self._res_seq) + ")"

	def typeName(self): return self._type
	def getType(self): return self._type
	def setType(self, t): self._type = t
	def setResidue(self, t): self._residue = t
	

DEPRECATED_CALLS = list()

class AtomAttributes(object):
	"""Holds the attributes of an atom including coordinates, element, mass, charge
	and other properties found in PDB files.
	"""
	
	#def __init__(self, name, elmt, elttype, coord, ch, m, bfactor = '',occup = 1,altloc = ' ',fullname = 'X',res='XXX',chain='A', res_seq = 1, attrs=[]):
	
	#def __init__(self, elttype, coord, attrs=[]):
	def __init__(self, arg1, arg2, arg3=[], coord=[0,0,0], ch=0., m=0., bfactor = '',occup = 1,altloc = ' ',fullname = 'X',res='XXX',chain='A', res_seq = 1, attrs=[]):
		if isinstance(arg1, AtomInfo):
			"""Atom Attributes.
			@type	coord:	list of 3 floats
			@param	coord:	coordinates
			@type	attrs:	list
			@param	attrs:	other attributes not in the class fields list.
			@type	type:	AtomInfo
			@param	type:	type of atom (usually obtained from PSF).
	
			"""
			self._attributes = arg3
			self.setCoord(numpy.array(arg2))
			self._info = arg1
		else:
			import inspect
			global DEPRECATED_CALLS
			if not str(inspect.stack()[1][1:]) in DEPRECATED_CALLS:
				print("WARNING: Deprecated AtomAttributes.__init__ called from "+ str(inspect.stack()[1][1:]) + ".")
			raise Exception


	#-------------------------------------------------------------
	def PDBline(self, ser_num, trad={}, fixedAtom=False):
		"""ATOM line corresponding to this atom (self) for a PDB file.

		@type ser_num:	int
		@param ser_num:	sequence number to be used.

		@rtype:  string
		@return: ATOM line.
		"""
		#print "PDBline ", self
		tObj = self.getInfo()
		if fixedAtom:
			#return "%s%5i %-4s%c%3s %c%4i%c   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%1.4f" % ("ATOM  ",ser_num,self._name,' ',self._residue,self._chain,1,' ',self._coordinates[0],self._coordinates[1],self._coordinates[2],1              ,0.0,self._element,self._charge)
			return "%s%5i %-4s%c%3s %c%4i%c   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s" % ("ATOM  ",ser_num%100000,tObj._name,' ',tObj._residue,tObj._chain,1,' ',self.getCoord()[0],self.getCoord()[1],self.getCoord()[2],1              ,0.0,tObj._element)
		else:
			#return "%s%5i %-4s%c%3s %c%4i%c   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%1.4f" % ("ATOM  ",ser_num,self._name,' ',self._residue,self._chain,1,' ',self._coordinates[0],self._coordinates[1],self._coordinates[2],0,0.0,self._element,self._charge)
			return "%s%5i %-4s%c%3s %c%4i%c   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s" % ("ATOM  ",ser_num%100000,tObj._name,' ',tObj._residue,tObj._chain,1,' ',self.getCoord()[0],self.getCoord()[1],self.getCoord()[2],0,0.0,tObj._element)

	def getType(self):
		print("WARNING: Deprecated call to AtomAttributes.getType() from ", inspect.stack()[1])
		return self.getInfo().getType() 

	def getInfo(self):
		"""Info of the atom.

		@rtype:  string
		@return: Name of the atom.
		"""
		try:
			return self._info
		except:  # compatibility for older versions
			return AtomInfo("X", "X", "X",  0., 0., 0.0, 1.0, ' ', "X   ", "XXX", "X", 1)
		
	def setInfo(self, t):
		#print "AA setInfo", t
		self._info = t

	#-------------------------------------------------------------
	def getCoord(self):
		"""Coordinates of the atom.

		@rtype:  numpy.array
		@return: Coordinates of the atom.
		"""
		return self._coordinates
	
	#-------------------------------------------------------------
	def getAttrs(self):
		"""Attributes of the atom.

		@rtype:  list
		@return: Attributes of the atom.
		"""
		return self._attributes
	#-------------------------------------------------------------
	def copy2(self):
		"""Copy of the atom attributes.

		@rtype:  list
		@return: Copy of the attributes of the atom.
		"""
		newAttr = AtomAttributes(None, None, None, None, None, None)
		newAttr.__dict__ = self.__dict__.copy()
		return newAttr

	#-------------------------------------------------------------
	def distanceTo(self, attr2, box=None):
		"""Calculates distance between the coordinates in self and in attr2.

		@type attr2:	list of 3 floats.
		@param attr2:	attributes of second atom.

		@type box:	Drawer. (new in version 1.136)
		@param box:	periodic boundary conditions.

		@rtype:  float
		@return: distance.
		"""
		if box != None:
			origin  = box.getCellOrigin()
			vectors = box.getCellBasisVectors()
			#boxDims = [vectors[i][i] for i in range(3)]
			#print " distanceTo ", origin,boxDims
			X0, Y0, Z0 = list(self.getCoord())
			X1, Y1, Z1 = list(attr2.getCoord())
			#print "----------------> ", X0, Y0, Z0, list(attr2.getCoord())
			
			box = [origin, [origin[0]+vectors[0][0], origin[1]+vectors[1][1], origin[2]+vectors[2][2]]]
			#-----------------------------------------------------------------
			dx = box[1][0]-box[0][0]
			dy = box[1][1]-box[0][1]
			dz = box[1][2]-box[0][2]
			#print "box=", box
			#print "dx:", dx,"dy:", dy,"dz:", dz
			
			dmin = float("inf")
			Xmin = box[0][0]
			Ymin = box[0][1]
			Zmin = box[0][2]
			
			
			X0 = X0 - (math.floor((X0-Xmin)/dx)) * dx
			Y0 = Y0 - (math.floor((Y0-Ymin)/dy)) * dy
			Z0 = Z0 - (math.floor((Z0-Zmin)/dz)) * dz
			X1 = X1 - (math.floor((X1-Xmin)/dx)) * dx
			Y1 = Y1 - (math.floor((Y1-Ymin)/dy)) * dy
			Z1 = Z1 - (math.floor((Z1-Zmin)/dz)) * dz
			#print "Atom1:", (X0,Y0,Z0), "Atom2:", (X1,Y1,Z1)
			
			#print "Xmin=", Xmin, "   X0=", X0, "X1:", X1, "  dx=", dx
			#print "Ymin=", Ymin, "   Y0=", Y0, "Y1:", Y1, "  dy=", dy
			#print "Zmin=", Zmin, "   Z0=", Z0, "Z1:", Z1, "  dz=", dz
			#d = []
			# traer los puntos a la caja central
			for sigX in [-dx,0,dx]:
				for sigY in [-dy,0,dy]:
					for sigZ in [-dz,0,dz]:
						#print (X1+sigX-X0), (Y1+sigY-Y0), (Z1+sigZ-Z0)
						#d.append(  math.sqrt ((X1+sigX-X0)**2 + (Y1+sigY-Y0)**2 + (Z1+sigZ-Z0)**2))
						dmin = min(dmin, math.sqrt (((X1+(sigX))-X0)**2 + ((Y1+(sigY))-Y0)**2 + ((Z1+(sigZ))-Z0)**2))
			#print "Distances:", d
			#print "Minimum Distance:", dmin
			return dmin
		else:
			#print "distanceTo ", self.getCoord(), attr2._coordinates
			dx = self.getCoord()[0]-attr2.getCoord()[0]
			dy = self.getCoord()[1]-attr2.getCoord()[1]
			dz = self.getCoord()[2]-attr2.getCoord()[2]

		return math.sqrt(dx*dx+dy*dy+dz*dz)

	
	def distanceToLine(self, pts):
		"""
		Distance between the line defined by 2 points in pts and the atom.
		"""
		P0 = numpy.array(pts[0])
		P1 = numpy.array(pts[1])
		P  = numpy.array(self.getCoord())
		#print "distanceToLine", P0,P1,P

		v = P1 - P0
		w = P - P0
		c1 = numpy.dot(w,v)
		if c1  <= 0:
			return numpy.linalg.norm(P-P0)
		c2 = numpy.dot(v,v)
		if c2 <= c1:
			return numpy.linalg.norm(P-P1)
		b = c1 / c2
		Pb = P0 + b * v
		#print "distanceToLine numpy.linalg.norm", P, Pb
		return numpy.linalg.norm(P - Pb)


	#-------------------------------------------------------------
	def moveby(self, displ): # backward compatibility
		self.moveBy(displ)

	#-------------------------------------------------------------
	def moveBy(self, displ):
		"""Moves the atom (self).

		@type displ:	list of three floats
		@param displ:	displacement of the atom.
		self._coordinates[0] += displ[0]
		self._coordinates[1] += displ[1]
		self._coordinates[2] += displ[2]
		"""
		self.setCoord(self.getCoord() + displ)
	#-------------------------------------------------------------
	def rotate(self, matr):
		"""Rotate the atom (self).

		@type matr:  numpy.matrix
		@param matr: rotation matrix.
		"""
		#self.setCoord([sum([matr[i][j] * self._coordinates[j] for j in range(3)]) for i in range(3)])
		#m = numpy.matrix(matr)
		#print "rotate", m,self._coordinates, numpy.asarray(m.dot(self._coordinates))[0]
		self.setCoord(numpy.asarray(matr.dot(self.getCoord()))[0])

	#-------------------------------------------------------------
	def setCoord(self, newCoords):
		"""Coordinates of the atom.

		@rtype:  list of 3 floats
		"""
		self._coordinates = numpy.array(newCoords)


	#-------------------------------------------------------------
	def __eq__(self, node2):
		"""Determines if two nodes are equal.

		@type	node2: attributes of second atom
		@param	node2: node to be compared to self
		@rtype:  boolean
		@return: true if elements are equal.
		"""
		#print "AtomAtributes " , self.getInfo(), node2.getInfo()
		#return self._element == node2._element and self._name == node2._name
		return self.getInfo() == node2.getInfo()
 
	#-------------------------------------------------------------
	def __ne__(self, node2):
		"""Determines if two nodes are not equal.

		@type	node2: attributes of second atom
		@param	node2: node to be compared to self
		@rtype:  boolean
		@return: true if elements are equal.
		"""
		#return self._element == node2._element and self._name == node2._name
		return not self == node2
 
	#-------------------------------------------------------------
	def __str__(self):
		"""String representation of attributes.
		@rtype:  string
		@return: String representation of attributes.
		"""
		#return "AtomAttributes{" + self._element + ", " + str(self.getCoord()) + ", " + str(self._mass) + ", " + str(self._charge) + ", " + str(self._attributes) + "}"
		try:
			return "AtomAttributes(\"" \
				+ str(self._info)       + "\", "    + str(self.getCoord()) + ", "    \
				+ str(self._attributes) + ")"
		except:
			return "AtomAttributes(\"" \
				+ str(self._info._type)       + "\", "    + str(self.getCoord()) + ", "    \
				+ str(self._attributes) + ")"
			

	def crc32(self, val):
		"""
		Computes the crc32 value of the attributes.  Used to determine
		if attributes have changed. (see documentation on binascii.crc32)
		"""
		return binascii.crc32(str(self)+str(self.getCoord()), val)

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


