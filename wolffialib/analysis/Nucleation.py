#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  {Sotero Esteva}, Frances J. Martínez-Miranda
    Computational Science Group, Department of Mathematics, 
    University of Puerto Rico at Humacao 
    <jse@math.uprh.edu>.

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
from PyQt4 import QtGui, QtCore, uic
from ui_nucleation import Ui_nucleation

import sys, os
import numpy

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../')

from wolffialib.chemicalGraph.Mixture import Mixture
from interface.main.History import NanoCADState
from wolffialib.io.CoordinateFile import CoordinatesUpdateFile
from interface.main.WFileDialogs import WFileDialog


class Nucleation():

	def __init__(self, mixture, box, resolution=5, threshold=0):
	    #super(Nucleation, self).__init__()
	    self.mixture = mixture
	    self.maxint = mixture.order() + 1
	    self.resolution = resolution
	    self.threshold = threshold
	    self.faces = faces = box.getFaces()
	    self.dims = [int((faces[1] - faces[0])/resolution) , 
	     			 int((faces[3] - faces[2])/resolution) ,
	     			 int((faces[5] - faces[4])/resolution) ]
	    self.widths = [faces[1] - faces[0], 
	     			   faces[3] - faces[2], 
	     			   faces[5] - faces[4]]
	    self.deltas = [self.widths[0]/self.dims[0],self.widths[1]/self.dims[1],self.widths[2]/self.dims[2]]
	    #print "deltas ", self.deltas
	    ##print "prticiones ", self.dims
	    #print "tamano caja ", self.widths
	     
	    self._scanBox()
	    self._classify()
	
	def _scanBox(self):
	    self.occupied = numpy.zeros(self.dims,numpy.int32)
	    self.tags = numpy.zeros(self.dims,numpy.int8)
	    walls = [self.faces[0],self.faces[2],self.faces[4]]
	    #1
	    for mol in self.mixture:
	        molecule = self.mixture.getMolecule(mol)
	        #if molecule.molname() <> "SOLVENT(WATER)": print "molecule ", molecule.molname()
	        
	        for atom in molecule:
	            attr = molecule.getAttributes(atom)
	            #---------------------------2
	            Pos = numpy.divide(
	                            numpy.mod(
	                                      numpy.subtract(attr.getCoord(),walls), 
	                                      self.widths), 
	                            self.deltas)
	            #c = attr.getCoord()
	            #Pos = [(c[0]-walls[0])%self.widths[0]/self.deltas[0], 
	            #       (c[1]-walls[1])%self.widths[1]/self.deltas[1], 
	            #       (c[2]-walls[2])%self.widths[2]/self.deltas[2]]
	            #if molecule.molname() == "C_Tube(10,10)": print "coor ", attr.getCoord(),"  Pos ", Pos, " type=", attr.getType()
	            self.occupied[Pos[0]%self.dims[0],Pos[1]%self.dims[1],Pos[2]%self.dims[2]] += 1
	
	def _mark(self, i,j,k,tag):
	    #print "tag", i,j,k,self.occupied[i,j,k], "->",tag
	    self.tags[i,j,k] = tag
	    self.occupied[i,j,k] = self.maxint
	    for ii in [i-1, i, i+1]:
	        for jj in [j-1, j, j+1]:
	            for kk in [k-1, k, k+1]:
	                iii = ii % self.dims[0]
	                jjj = jj % self.dims[1]
	                kkk = kk % self.dims[2]
	                if self.occupied[iii,jjj,kkk] <= self.threshold:
	                    self._mark(iii,jjj,kkk,tag)
	
	def _classify(self): #3
	    '''
	    Classify connected components of voids.
	    Alters self.occupied.
	    returns number of disconnected void regions
	    '''
	    tag = 1
	    for i in range(self.dims[0]):
	        for j in range(self.dims[1]):
	            for k in range(self.dims[2]):
	                if self.occupied[i,j,k] <= self.threshold:
	                    tag += 1
	                    self._mark(i,j,k,tag)
	    return tag-1
	
	def voidsCells(self):
		'''
		Returns a list with the numbers of cells in each of the disconnected voids.
		'''
		totals = list()
		i      = 2
		subTotal = numpy.sum(numpy.equal(self.tags,i))
		while subTotal <> 0:
			totals.append(subTotal)
			i += 1
			subTotal = numpy.sum(numpy.equal(self.tags,i))
		return totals
	
	def voidsVolumes(self): 
		v = self.deltas[0]*self.deltas[1]*self.deltas[2]
		return  [n * v for n in self.voidsCells()]
	
	def filledVoids(self):
		'''
		Returns a LJ fluid that fills the voids
		'''
		from wolffialib.chemicalGraph.Mixture import Mixture
		from wolffialib.chemicalGraph.Molecule import Molecule
		from wolffialib.chemicalGraph.AtomAttributes import AtomAttributes
		mix = Mixture()
		for i in range(self.dims[0]):
			for j in range(self.dims[1]):
				for k in range(self.dims[2]):
					if self.tags[i,j,k] > 1:
						liquid = Molecule()
						atr = AtomAttributes(str(self.tags[i,j,k]), "AR", "AR", 
											[ self.faces[0]+i*self.deltas[0], self.faces[2]+j*self.deltas[1], self.faces[4]+k*self.deltas[2]], 
											0.0, 39.9500, 0.0, 1.0, ' ', "OT  ", "WAT", "A", 1)
						liquid.add_atom(atr,[])
						mix.add(liquid)
		return mix

import PyQt4.Qwt5 as Qwt

class NucleationDialog(QtGui.QDialog):
	def __init__(self):
	    super(NucleationDialog, self).__init__()
	    self.ui = Ui_nucleation()
	    self.ui.setupUi(self)
	    
	    self.ui.defaultCheckBox.setChecked(True)
	    self.ui.cellSizeSpinBox.setValue(10)
	    self.ui.cellSizeSpinBox.setEnabled(False)
	    self.ui.cellSizeSpinBox.setMinimum(3)
	    
	    self.maxCurve	= Qwt.QwtPlotCurve("Maximum")
	    self.maxCurve.attach(self.ui.maximosQwtPlot)
	    self.ui.maximosQwtPlot.setTitle("Maxima")
	    self.maxCurve.setData(range(100), range(100))
	    
	    self.sumCurve = Qwt.QwtPlotCurve("Sum")
	    self.sumCurve.attach(self.ui.SumasQwtPlot)
	    self.ui.SumasQwtPlot.setTitle("Sumas")
	    self.sumCurve.setData(range(100),range(100))

	    
	    
	def on_lineEdit1Button_pressed(self):
		d = WFileDialog(self, 'Browse File','','')
		if d.accepted():
			filename1 = d.fullFilename()
			if not os.path.exists(str(filename1)):
				QtGui.QMessageBox.information(self, "Wolffia's message", "Did not find file " + filename + ". File not loaded.", QtGui.QMessageBox.Ok)
				return
			self.ui.lineEdit1.setText(str(filename1))

	def on_lineEdit2Button_pressed(self):
		d = WFileDialog(self, 'Browse File','','')
		if d.accepted():
			filename2 = d.fullFilename()
			if not os.path.exists(str(filename2)):
				QtGui.QMessageBox.information(self, "Wolffia's message", "Did not find file " + filename + ". File not loaded.", QtGui.QMessageBox.Ok)
				return
			self.ui.lineEdit2.setText(str(filename2))

	def getPaths(self):
		corridaFile = str(self.ui.lineEdit1.displayText())
		self.ui.lineEdit1.clear()
		wfyFile = str(self.ui.lineEdit2.displayText())
		self.ui.lineEdit2.clear()
		return [wfyFile, corridaFile]
	
	def on_runButton_pressed(self):#4
		wfyFile, corridaFile = self.getPaths()
		self.cellValue = self.ui.cellSizeSpinBox.value()
		print "self.cellValur = " + str(self.cellValue)
		#print "runButton_pressed" + "wfyFile:"+wfyFile + "corridaFile:"+corridaFile
		
		#prueba= ["/home/kaori/Investigacion/PruebaNucleationGui/DispersionCNTclf.wfy",
		#		   "/home/kaori/Investigacion/PruebaNucleationGui/corrida.pdb",
		#		   None,
		#		   "/home/kaori/Investigacion/PruebaNucleationGui/liquido.pdb"]
		prueba= [wfyFile,corridaFile,None,
				 "/home/kaori/Investigacion/PruebaNucleationGui/liquido.pdb"]

		print "Void Volumes ", prueba
		state = NanoCADState(filename=prueba[0])
		#if prueba[2] <> None: state.getDrawer().readNAMD(prueba[2])
		ufile = CoordinatesUpdateFile(prueba[1],state.getMixture())
		i=1
		maximos = list()
		sumas = list()
		while ufile.next():
			n = Nucleation(state.getMixture(), state.getDrawer(),self.cellValue,0)
			cells = n.voidsCells()

#----------------------------------------------------------------
			if cells == []: 
				print i,0,0
				maximos.append(0)
				sumas.append(0)
			else: 
				print i,max(cells), sum(cells)
				maximos.append(max(cells))
				sumas.append(sum(cells))
			self.maxCurve.setData(range(i), maximos)
			self.sumCurve.setData(range(i), sumas)
			self.ui.maximosQwtPlot.setAxisScale(Qwt.QwtPlot.xBottom, 0, i, 0)
			self.ui.SumasQwtPlot.setAxisScale(Qwt.QwtPlot.xBottom, 0, i, 0)
			self.ui.maximosQwtPlot.replot()
			self.ui.SumasQwtPlot.replot()

			liquid = n.filledVoids()
			
			#liquid.writePDB(prueba[3])
			#os.system("vmd -m -pdb "+ prueba[1] + " -pdb "+ prueba[3])
			#print "termine"
			#if cells <> [] and max(cells) > 12: break
			i += 1
	
		#liquid = n.filledVoids()
		print "Termine ciclo"
		liquid.writePDB(prueba[3])
		print "Termine escribir"
		
		os.system("vmd -m -pdb "+ prueba[1] + " -pdb "+ prueba[3])
		print "Termine "

	def on_cancelButton_pressed(self):
		self.close()
	
	def on_defaultCheckBox_toggled(self,checked):
		
		if checked:
			self.ui.cellSizeSpinBox.setValue(10)
			self.ui.cellSizeSpinBox.setEnabled(False)
		
		else:
			self.ui.cellSizeSpinBox.setEnabled(True)


	

#=====================================================================
'''
if __name__ == '__main__':
	sys.path.append("/home/frances/Investigacion/bazaar/Wolffia")
	#from wolffialib.io.CoordinateFile import CoordinatesUpdateFile
	
	#from  interface.main.History import NanoCADState

	prueba1 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/30/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/30/DispersionCNTclf.dcd",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/30/liquido.pdb"]
	
	prueba2 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/5temp400/DispersionCLFdensidad5temp400.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/5temp400/DispersionCLFdensidad5temp400.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/5temp400/liquido.pdb"]
	
	
	prueba3 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/2temp400/DispersionCLFdensidad2temp400.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/2temp400/DispersionCLFdensidad2temp400.coor",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/2temp400/liquido.pdb"]

	prueba4 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/Original/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/Original/Corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/Original/liquido.pdb"]
	
	prueba5 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/22/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/22/corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/22/liquido.pdb"]
	
	prueba6 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/20/DispersionCLFdensidad1_25.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/20/corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/20/liquido.pdb"]
	
	prueba7 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/15/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/15/corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/15/liquido.pdb"]
	
	prueba8 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/6.5/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/6.5/corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/6.5/liquido.pdb"]
	
	prueba9 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/13/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/13/corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/13/liquido.pdb"]
	
	prueba10 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/7/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/7/corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/7/liquido.pdb"]

	prueba11 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/8.5/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/8.5/corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/8.5/liquido.pdb"]

	prueba12 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/10/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/10/corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/10/liquido.pdb"]
	
	prueba13 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/jordan/mixfulerinesArgonremoving.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/jordan/mixfulerinesArgonremoving.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/jordan/liquido.pdb"]

	prueba14 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/jordan/pruebanucleation.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/jordan/pruebanucleation.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/jordan/liquido1.pdb"]
	
	prueba15 = ["/home/frances/.wolffia/9.25/9.25b.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/9.25/corrida.pdb",
			   None,
			    "/home/frances/Investigacion/2013/SimulacionesNuclation/9.25/liquido.pdb"]

	prueba16 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/9.5/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/9.5/corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/9.5/liquido.pdb"]	
	
	prueba17 = ["/home/frances/Investigacion/2013/SimulacionesNuclation/9/DispersionCNTclf.wfy",
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/9/corrida.pdb",
			   None,
			   "/home/frances/Investigacion/2013/SimulacionesNuclation/9/liquido.pdb"]
	
	prueba = prueba5
	
	
	
	
	
	print "Void Volumes "
	state = NanoCADState(filename=prueba[0])
	if prueba[2] <> None: state.getDrawer().readNAMD(prueba[2])
	ufile = CoordinatesUpdateFile(prueba[1],state.getMixture())
	i=1
	while ufile.next():
		n = Nucleation(state.getMixture(), state.getDrawer(),10,0)
		cells = n.voidsCells()
		if cells == []: print i,0,0
		else: print i,max(cells), sum(cells)
		
		liquid = n.filledVoids()
		
		#liquid.writePDB(prueba[3])
		#os.system("vmd -m -pdb "+ prueba[1] + " -pdb "+ prueba[3])
		#print "termine"
		#if cells <> [] and max(cells) > 12: break
		i += 1

	#liquid = n.filledVoids()
	print "Termine ciclo"
	liquid.writePDB(prueba[3])
	print "Termine escribir"
	
	os.system("vmd -m -pdb "+ prueba[1] + " -pdb "+ prueba[3])
	print "Termine "
	'''    

	
#---------------------------------------------------------------------------
def main():
	from History import NanoCADState
	gui = QtGui.QApplication([])

	from wolffialib.io.CoordinateFile import CoordinatesUpdateFile
	
	from  interface.main.History import NanoCADState
	
	
	load_gui = NucleationDialog()
	load_gui.show()
	gui.exec_()
	
   



if __name__ == '__main__' :
	main()
	
	sys.path.append("/home/kaori/Investigacion/bazaar/Wolffia")
	