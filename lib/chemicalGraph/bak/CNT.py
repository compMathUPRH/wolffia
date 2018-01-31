# CNT.py

from Molecule import *

class  CNT(Molecule):
	def __init__(self,length,n,m):
		# initialize base class
		Molecule.__init__(self)
		self.rename(str( self.__class__)+"("+str(n)+","+str(m)+")")

		# call nanotubegen
		#os.system("cd " + MOSDAS_OO_PDB_DIR + " ;echo \" " + str(length) + " " + str(n) + " "+str(m)+" \" | " + MOSDAS_OO_BASE_DIR + "/nanotubegen ; cd ..")
		os.system("cd " + MOSDAS_OO_TEMP_DIR + " ;echo \" " + str(length) + " " + str(n) + " "+str(m)+" \" | " + MOSDAS_OO_BIN_DIR + "/nanotubegen ; cd ..")
		#tempMol=MergableMolecule()
		tempMol = self
		tempMol.load(MOSDAS_OO_TEMP_DIR + "/nanotube.pdb")


	#============================================================================
	class Dialog:
		"""
		Class fields: 
			_molecules
			_top
			_length
			_n
			_m
		"""
		def __init__(self, parent, molecules, classname):
			self.parent = parent
			self._top = top = Toplevel(parent)
			#self._classname = classname
			
			Label(top, text="Single-wall Carbon nanotube specifications: ").grid(row=0,column=0, columnspan=4)
			
			Label(top, text="Length in angstroms: ").grid(row=1,column=0, columnspan=1)
			self._length = Entry(top)
			self._length.grid(row=1,column=1, columnspan=1)

			Label(top, text="Chirality: (").grid(row=2,column=0, columnspan=1)
			self._n = Entry(top)
			self._n.grid(row=2,column=1, columnspan=1)
			Label(top, text=" , ").grid(row=2,column=2, columnspan=1)
			self._m = Entry(top)
			self._m.grid(row=2,column=3, columnspan=1)
			Label(top, text=")").grid(row=2,column=4, columnspan=1)

			b = Button(top, text="OK", command=self.ok)
			b.grid(row=3,column=1, columnspan=1)
			Button(top, text="Cancel", command=self.cancel).grid(row=3,column=2, columnspan=1)

		def ok(self):
			#print "value is", self.Input.get()
			l = int(self._length.get())
			n = int(self._n.get())
			m = int(self._m.get())
			_molecules.append(CNT(l,n,m))
			
			#turn on edit options
			#editObject.updateMenuEntires()
			
			self._top.destroy()

		def cancel(self):
			self._top.destroy()
				

