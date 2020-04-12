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
import struct
import re, sys
import math

class PRM(dict):
	def __init__(self,molname,filename = None, mass = None,nonb = None,bond = None,angl = None,dihe = None,impr = None,hbon = None):
		self.molname = molname
		self.filename = filename
		self.title = molname

		if mass == None: self["MASS"] = dict()
		else: self["MASS"] = mass
		
		if nonb == None: self["NONB"] = dict()
		else: self["NONB"] = nonb
		
		if bond == None: self["BOND"] = dict()
		else: self["BOND"] = bond
		
		if angl == None: self["ANGL"] = dict()
		else: self["ANGL"] = angl
		
		if dihe == None: self["DIHE"] = dict()
		else: self["DIHE"] = dihe
		
		if impr == None: self["IMPR"] = dict()
		else: self["IMPR"] = impr
		
		if hbon == None: self["HBON"] = dict()
		else: self["HBON"] = hbon
		
		#non implemented sections
		self["NBFI"] = None
		self["CMAP"] = None
		self["END"] = None
		
		self.trad = None

		if filename != None:
			self.load(filename)

		#print  "PRM__init__: ", self["ANGL"]
	#-----------------------------------------------------------------------------------------
	def load(self,filename):
		"""
		Reads force field.  Assumes CHARMM format (same as loadCHARM())

		@type  filename: string
		@param filename: CHARMM filename.
		"""
		self.loadCHARMM(filename)
	#-----------------------------------------------------------------------------------------
	def loadAMBER(self,filename):
		"""
		Reads force field in AMBER format.

		\"Modified  force  field  parameters in file frcmod: This file is
		normally the one that will be changed by the user.  It consists
		of  a 1-card title, followed by a blank line, then keyword sec-
		tions.\" Refer to http://ambermd.org/formats.html#topology for details.

		@type  filename: string
		@param filename: PRM filename.
		"""
		f = open(filename)
		mode = None
		self.title = f.readline()
		f.readline()

		for line in f:
			#print  "linea: ", line[:4]
			if line[:4] in self.keys():
				mode = line[:4]
			elif mode == 'MASS':  #FORMAT(A2,2X,F10.2x,f10.2)unpack("6sx8sx9sx6sx2sx30sx6sx6sx6sx2s", line.strip())
				self['MASS'].append(struct.unpack('2s2x10.2fx10.2f', line))
			elif mode == 'BOND':  #FORMAT(A2,1X,A2,2F10.2)
				self['BOND'].append(struct.unpack('', line))
			elif mode == 'ANGL':  #FORMAT(A2,1X,A2,1X,A2,2F10.2)
				self['ANGL'].append(struct.unpack('', line))
			elif mode == 'DIHE':  #FORMAT(A2,1X,A2,1X,A2,1X,A2,I4,3F15.2)
				self['DIHE'].append(struct.unpack('', line))
			elif mode == 'IMPR':  #FORMAT(A2,1X,A2,1X,A2,1X,A2,I4,3F15.2)
				self['IMPR'].append(struct.unpack('', line))
			elif mode == 'HBON':  #FORMAT(2X,A2,2X,A2,2x,5F10.2,I2)
				self['HBON'].append(struct.unpack('', line))
			elif mode == 'NONB':  #FORMAT(20(A2,2X))
				self['NONB'].append(struct.unpack('', line))




	#-----------------------------------------------------------------------------------------
	def loadCHARMM(self,filename):
		"""
		Reads force field in CHARMM format.

		Refer to http://www.charmm.org/documentation/c32b2/parmfile.html for details.

		@type  filename: string
		@param filename: PRM filename.
		"""

		try:
			f = open(filename)
		except:
			print("Error in PRM.loadCHARMM: could not open \'" + str(filename) + "\'")
			sys.exit(0)

		mode = None
		self.title = f.readline()
		f.readline()

		for line in f:
			#try:
				# join lines ending with '-'
				#print "linea: ", line, ": Cont ", line[-2:-1]
				while line[-2:-1] == '-':
					line = line[:-2]
					line += f.next()

				if len(line.strip()) == 0 or line.strip()[0] == '*' or line.strip()[0] == '!':
					#print " blank line and comments"
					pass # ignore blank lines and comments
				elif line[:3] in self.keys() or line[:4] in self.keys():
					mode = line[:4]
					#print "Cambio modo a ", mode
				elif mode == 'MASS': 
					pass #not implemented
				elif mode == 'BOND': 
					splitLine = re.split( '[^a-z,A-Z,0-9,.,\*,\+,\-]+', line)
					[elttype1, elttype2, K, bondLength] = splitLine[:4]
					#print "sacado: ", splitLine
					if elttype1 <= elttype2:
						self["BOND"][elttype1+' '+elttype2] = [float(K), float(bondLength)]
					else:
						self["BOND"][elttype2+' '+elttype1] = [float(K), float(bondLength)]
				elif mode == 'ANGL': 
					splitLine = re.split( '[^a-z,A-Z,0-9,.,\*,\+,\-]+', line)
					[elttype1, elttype2, elttype3, Kt, angle] = splitLine[:5]
					#print "sacado: ", splitLine
					# lowest elttype first
					if elttype1 <= elttype3:
						self["ANGL"][elttype1+' '+elttype2+' '+elttype3] = [float(Kt), float(angle)]
					else:
						self["ANGL"][elttype3+' '+elttype2+' '+elttype1] = [float(Kt), float(angle)]
				elif mode == 'DIHE': 
					splitLine = re.split( '[^a-z,A-Z,0-9,.,\*,\+,\-]+', line)
					#print "sacado: ", splitLine
					[elttype1, elttype2, elttype3, elttype4, Kchi, n, delta] = splitLine[:7]
					# lowest elttype first or equal edges with lowest second elttype
					if elttype1 < elttype4 or (elttype1 == elttype4 and elttype2 <= elttype3):
						self["DIHE"][elttype1+' '+elttype2+' '+elttype3+' '+elttype4] = [float(Kchi), int(n), float(delta)]
					else:
						self["DIHE"][elttype4+' '+elttype3+' '+elttype2+' '+elttype1] = [float(Kchi), int(n), float(delta)]
				elif mode == 'IMPR': 
					pass #not implemented
				elif mode == 'HBON': 
					pass #not implemented
				elif mode == 'NONB': 
					splitLine = re.split( '[^a-z,A-Z,0-9,.,\*,\+,\-]+', line)
					#print "sacado: ", splitLine
					[element, ignored, rd, epsilon] = splitLine[:4]
					[element]= splitLine[:1]  
					#print " elemento que quiero:", splitLine
					self["NONB"][element] = [float(rd), float(epsilon), 0.]
			#except:
				#print "Problemas leyendo ", mode
				#pass #quite permissive
		#print "PRM.loadCHARMM: ", self["ANGL"]


	#-----------------------------------------------------------------------------------------
	def __tr__(self, elt):
		if self.trad == None or not self.trad.has_key(elt):
			return elt
		else:
			return self.trad[elt]

	#-----------------------------------------------------------------------------------------
	def writeCHARMM(self,filename, mode="w", trad=None):
		#print "TRAD",trad
		#print "PRM writeCHARMM ====", self
		if trad == None  or trad == {}:
			self.trad = None
		else:
			self.trad = trad

		if filename==None:
			f = sys.stdout
		else:
			f = open(filename,mode)

		f.write("*>>>>>> CHARMM parameter file for " + self.molname + " <<<<<<<<<\n")
		f.write("*>>>>>> Produced by Wolfia, wolffia.uprh.edu <<<<<<<<<\n")

		if len(self['NONB'].keys()) > 0:
			f.write("\nNONB     ! " + self.molname + "\n")
			if self.trad == None:
				for elttype in self['NONB'].keys():
					f.write("{:<4} {:10.6f} {:10.6f}   {:10.6f}\n".format(self.__tr__(elttype), 0.0, self['NONB'][elttype][0], self['NONB'][elttype][1])) 
			else:
				for elttype in self.trad.keys():
					if not elttype in self['NONB']:
						raise PRMError("Element type " + elttype + " does not have Lennard-Jones parameter values.")
					f.write("{:<4} {:10.6f} {:10.6f}   {:10.6f}\n".format(self.__tr__(elttype), 0.0, self['NONB'][elttype][0], self['NONB'][elttype][1])) 

		if len(self['BOND'].keys()) > 0:
			f.write("\nBOND   ! " + self.molname + "\n")
			for elts in self['BOND'].keys():
				[elt1, elt2] = elts
				if self.trad == None or (elt1 in self.trad.keys() and elt2 in self.trad.keys()):
					f.write("{:<4} {:<4} {:8.3f}   {:8.4f}\n".format(self.__tr__(elt1), self.__tr__(elt2), self['BOND'][elts][0], self['BOND'][elts][1])) 

		if len(self['ANGL'].keys()) > 0:
			f.write("\nANGL   ! " + self.molname + "\n")

			for elts in self['ANGL'].keys():
				[elt1, elt2, elt3] = elts
				if self.trad == None or (elt1 in self.trad.keys() and elt2 in self.trad.keys() and elt3 in self.trad.keys()):
					f.write("{:<4} {:<4} {:<4} {:8.3f}   {:8.4f}\n".format(self.__tr__(elt1), self.__tr__(elt2), self.__tr__(elt3), self['ANGL'][elts][0], self['ANGL'][elts][1])) 

		if len(self['DIHE'].keys()) > 0:
			f.write("\nDIHE   ! " + self.molname + "\n")
			for elts in self['DIHE'].keys():
				[elt1, elt2, elt3, elt4] = elts
				if self.trad == None or (elt1 in self.trad.keys() and elt2 in self.trad.keys() and elt3 in self.trad.keys() and elt4 in self.trad.keys()):
					f.write("{:<4} {:<4} {:<4} {:<4} {:10.4f}  {:1}  {:7.2f}\n".format(self.__tr__(elt1), self.__tr__(elt2), self.__tr__(elt3), self.__tr__(elt4), self['DIHE'][elts][0], int(self['DIHE'][elts][1]), self['DIHE'][elts][2])) 

	@staticmethod
	def _splitKey_(key):
		return re.split( '[^a-z,A-Z,0-9,.,\*,\+,\-]+', key)

	@staticmethod
	def _splitBond_(key):
		[elt1,elt2,k,a] =  re.split( '[^a-z,A-Z,0-9,.,\*,\+,\-]+', key)
		return [elt1,elt2,float(k),float(a)]

#==========================================================================
class PRMError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


#==========================================================================
if __name__ == '__main__':
	prm = PRM(molname='prueba', filename='../../../data/forceFields/PMMA.prm')
	#prm.load()
	#print  prm
	trad={'HZ': 'HZQ', 'CZ':'CZQ', 'CL':'CLQ'}

	prm.writeCHARMM("/tmp/prueba.prm", trad=trad)


