# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  ForceTab.py
#  Version 0.1, December, 2011
#
#  Wolffia: tab for setting force field parameter values.
#
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, Carlos J.  Cortés Martínez, Frances  Martínez Miranda, 
    Radamés J.  Vega Alfaro, 
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
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
from ui_ForceTab import Ui_forceTab
#from PyQt4.QtCore import *
#from PyQt4.QtGui import QFileDialog

import sys,os, time
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import WOLFFIA_GRAPHICS, NANOCAD_BASE
from interface.main.WTimer import WTimer

from interface.main.MixtureViewer import MixtureViewer
from lib.chemicalGraph.molecule.ForceField import ForceField, NonBond

#====================================================================
class ChargesTable(QtGui.QTableWidget):
    def __init__(self, hist, forceTab, parent=None):
        super(ChargesTable, self).__init__(parent=parent)
        #print "ChargesTable init"
        self.history = hist
        self.forceTab = forceTab

        self.setColumnCount(3)
        self.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(2, item)

        item = self.horizontalHeaderItem(0)
        item.setText("Atom")
        item = self.horizontalHeaderItem(1)
        item.setText("Type")
        item = self.horizontalHeaderItem(2)
        item.setText("Charge")

    def update(self):
        #print "ChargesTable update"
        self.insertChargesTable()

    def showEvent(self,e):
        #print "ChargesTable showEvent"
        self.insertChargesTable()

    def updateCharges(self):
		#list all molecules in the Structure Manager
		# count nonb in all molecules
		#print "updateCharges start"
		rows = 0
		displayedMols=list()

		self.blockSignals(True)
		for molName in self.history.currentState().mixture:
			molecule = self.history.currentState().mixture.getMolecule(molName)
			if not molecule.molname() in displayedMols:
				displayedMols.append(molecule.molname() )
				rows += len(molecule.atoms())+2
				#chrow = rows - 1   ELIMINADO TEMPORERAMENTE
				chrow = 1 # SUSTITUIDO TEMPORERAMENTE
				charge = molecule.charge()
				
				totalCharge = QtGui.QTableWidgetItem("{:f}".format(charge))
				totalCharge.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
				#print "updateCharges ",rows,molecule.molname(),molecule.charge()
				self.setItem(chrow, 2, totalCharge)
				
				if charge > 0:
					self.item(chrow, 2).setBackground(QtGui.QBrush(QtGui.QColor(200,200,255)))
				elif charge < 0:
					self.item(chrow, 2).setBackground(QtGui.QBrush(QtGui.QColor(255,200,200)))
				else:
					self.item(chrow, 2).setBackground(QtGui.QBrush(QtGui.QColor(200,255,200)))
		self.blockSignals(False)
		#print "updateCharges end"
			

    def insertChargesTable(self):
        '''
        list all molecules in the Structure Manager
        '''
        # count nonb in all molecules
        print "insertChargesTable start"
        #timer = WTimer("ForceTab.insertChargesTable")
        row = 0
        rows = 0
        molCount=0

        self.setRowCount(0)
        displayedMols=list()
        charges = dict()
        #progress	  = QtGui.QProgressDialog("Updating charges...", QtCore.QString(), 0, len(self.history.currentState().mixture), self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
        #progress.setWindowModality(QtCore.Qt.WindowModal)

        self.blockSignals(True)
        for molName in self.history.currentState().mixture:
            #progress.setValue(molCount)
            molCount +=  1
            charVals = dict()
            molecule = self.history.currentState().mixture.getMolecule(molName)
            if not molecule.molname() in displayedMols:
                print "insertChargesTable ", molecule.molname(), molecule.charge(), self.history.currentState().mixture.countMoleculesNamed(molecule.molname())
                #self.allForceField[molName] = {"nonBonded" : [], "Bonds" : [] , "Angles": [], "Dihedrals": []}
                displayedMols.append(molecule.molname() )
                
                #ff = molecule.getForceField()
                ff = molecule.forceField
                #print "insertChargesTable ", ff._NONBONDED
                types = molecule.atomTypes()
                #print "insertChargesTable types", types
                #rows += len(molecule.atoms())+2        ELIMINADO TEMPORERAMENTE
                rows += 2         # SUSTITUIDO TEMPORERAMENTE
                self.setRowCount(rows) 
                  
                # display molecule name
                nameW = QtGui.QTableWidgetItem(molecule.molname())
                nameW.setTextAlignment(4)
                nameW.setFlags(QtCore.Qt.ItemIsEnabled)
                nameW.setToolTip("Click to select.")
                self.setItem(row, 0, nameW)
                self.setSpan(row, 0, 1, 3)
                self.item(row,0).setBackgroundColor (self.forceTab._selectedColor(molecule.molname()))
                row += 1
                
                '''
                ELIMINADO TEMPORERAMENTE: Debe estar en diálogo popup para que no retrase todo
                for atom in molecule.atoms():
                    aType = molecule.getAtomAttributes(atom).getInfo().getType()


                    charType = QtGui.QTableWidgetItem(aType)
                    charType.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                    self.setItem(row, 0, QtGui.QTableWidgetItem(str(atom)))
                    self.setItem(row, 1, charType)
                    

                    charge = ChargeSpinBox([-10, 10], 6, parent=self.forceTab, molecule=molecule, atom=atom)

                    self.setCellWidget(row, 2, charge)
                    
                    charVals[aType] = [charge] 
                    
                    row += 1
                    
                    for otherMolecule in self.forceTab.equivalences[molecule.molname()]:
							charge.addMolecule(otherMolecule)
                '''

                numMolecules = self.history.currentState().mixture.countMoleculesNamed(molecule.molname())
                totalCharge = QtGui.QTableWidgetItem("{:f}".format(molecule.charge() * numMolecules))
                totalCharge.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                self.setItem(row, 1, QtGui.QTableWidgetItem("net q:"))
                self.setItem(row, 2, totalCharge)

                row += 1
        #self.updateCharges()
        #progress.setValue(len(self.history.currentState().mixture))
        #timer.report()
        self.blockSignals(False)

#====================================================================
class NonBondTable(QtGui.QTableWidget):
    def __init__(self, hist, forceTab, parent=None):
        super(NonBondTable, self).__init__(parent=parent)
        #print "NonBondTable init"
        self.history = hist
        self.forceTab = forceTab

        self.setObjectName("nonBondTable")
        self.setColumnCount(3)
        self.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(2, item)

        item = self.horizontalHeaderItem(0)
        item.setText("Type")
        item = self.horizontalHeaderItem(1)
        item.setText("e")
        item = self.horizontalHeaderItem(2)
        item.setText("Rmin/2")

        # https://stackoverflow.com/questions/38098763/pyside-pyqt-how-to-make-set-qtablewidget-column-width-as-proportion-of-the-a#38129829
        header = self.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

    def update(self):
        #print "NonBondTable update"
        self.insertAllToNonBondTable()

    def showEvent(self,e):
        #print "NonBondTable showEvent"
        self.insertAllToNonBondTable()

    def insertAllToNonBondTable(self):
		#list all molecules in the Structure Manager
		# count nonb in all molecules
		#print "insertAllToNonBondTable start"
		row = 0
		rows = 0
		self.setRowCount(0)
		displayedMols=list()

		self.blockSignals(True)
		self.clearContents ()
		for molName in self.history.currentState().mixture:
			#nombVals = dict()
			molecule = self.history.currentState().mixture.getMolecule(molName)
			if not molecule.molname() in displayedMols:
				#print "insertAllToNonBondTable ", molecule.molname(),molecule.atomTypes(),molecule.getForceField().getTypes()
				#self.allForceField[molName] = {"nonBonded" : [], "Bonds" : [] , "Angles": [], "Dihedrals": []}
				displayedMols.append(molecule.molname() )
				
				ff = molecule.getForceField()
				types = molecule.atomTypes()
				types.sort()  # to search for changed types in on_nonBondTable_itemChanged
				rows += len(types)+1
				self.setRowCount(rows)
				  
				# display molecule name
				nameW = QtGui.QTableWidgetItem(molecule.molname())
				nameW.setTextAlignment(4)
				nameW.setFlags(QtCore.Qt.ItemIsEnabled)
				nameW.setToolTip("Click to select.")
				self.setItem(row, 0, nameW)
				self.setSpan(row, 0, 1, 4)
				self.item(row,0).setBackgroundColor (self.forceTab._selectedColor(molecule.molname()))
				
				row += 1
				
				for aType in types:
					#print "insertAllToNonBondTable", aType, ff.nonBond(aType),ff.charge(aType)
					atomType = QtGui.QTableWidgetItem(aType)
					atomType.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
					atomType.setToolTip("Double click to edit the name type.")
					self.setItem(row, 0, atomType)
					#atomType = QtGui.QLineEdit(aType)
					#self.setCellWidget(row, 0, atomType)
					
					#print "insertAllToNonBondTable A"
					epsilon = ForceSpinBox([-5, 0], 6, parent=self.forceTab, fl=ff, type=aType, \
										method= ff.setNonBond, pos=0)
					self.setCellWidget(row, 1, epsilon)
					epsilon.setValue(ff.nonBond(aType)[NonBond._EPSILON])
					#print "insertAllToNonBondTable epsilon", aType, ff.nonBond(aType)[NonBond._EPSILON]
					
					rmin = ForceSpinBox([0.000000, 20], 6, parent=self.forceTab, fl=ff, type=aType, \
									method= ff.setNonBond, pos=1)
					self.setCellWidget(row, 2, rmin)
					rmin.setValue(ff.nonBond(aType)[NonBond._SIGMA])
					#print "insertAllToNonBondTable sigma", aType, ff.nonBond(aType)[NonBond._SIGMA]
					
					
					'''
					for otherMolName in self.history.currentState().mixture:
						otherMolecule = self.history.currentState().mixture.getMolecule(otherMolName)
						#print "insertAllToNonBondTable ", otherMolecule.molname(), molecule.molname(),otherMolecule.molname() == molecule.molname()
						if otherMolecule.molname() == molecule.molname():
							otherMolecule = self.history.currentState().mixture.getMolecule(otherMolName)
							epsilon.addForceField(otherMolecule.getForceField())
							rmin.addForceField(otherMolecule.getForceField())
							charge.addForceField(otherMolecule.getForceField())
					'''
					for otherMolecule in self.forceTab.equivalences[molecule.molname()]:
							epsilon.addForceField(otherMolecule.getForceField())
							rmin.addForceField(otherMolecule.getForceField())
						
					row += 1
				
		self.blockSignals(False)
			


#====================================================================
class BondsTable(QtGui.QTableWidget):
    def __init__(self, hist, forceTab, parent=None):
        super(BondsTable, self).__init__(parent=parent)
        #print "BondsTable init"
        self.history = hist
        self.forceTab = forceTab

        self.setColumnCount(3)
        self.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(2, item)

        item = self.horizontalHeaderItem(0)
        item.setText("Type")
        item = self.horizontalHeaderItem(1)
        item.setText("Kb")
        item = self.horizontalHeaderItem(2)
        item.setText("b0")

        # https://stackoverflow.com/questions/38098763/pyside-pyqt-how-to-make-set-qtablewidget-column-width-as-proportion-of-the-a#38129829
        header = self.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
		

    def update(self):
        #print "BondsTable update"
        self.insertAllBondTable()

    def showEvent(self,e):
        #print "BondsTable showEvent"
        self.insertAllBondTable()

    def insertAllBondTable(self):
        #list all molecules in the Structure Manager
    
        row = 0
        rows = 0
        self.setRowCount(0)
        displayedMols=list()
        self.blockSignals(True)
        for molName in self.history.currentState().mixture:
            bonds = dict()
            molecule = self.history.currentState().mixture.getMolecule(molName)
            #print "insertAllBondTable", molecule.molname(),molecule.atomTypes()
            if not molecule.molname() in displayedMols:
				displayedMols.append(molecule.molname())
				
				ff = molecule.getForceField()
				bondTypes = molecule.bondTypes()
				rows += len(bondTypes)+1
				self.setRowCount(rows)
				
				# display molecule name
				nameW = QtGui.QTableWidgetItem(molecule.molname())
				nameW.setTextAlignment(4)
				self.setItem(row, 0, nameW)
				self.setSpan(row, 0, 1, 3)
				self.item(row,0).setBackgroundColor (self.forceTab._selectedColor(molecule.molname()))
				row += 1
				
				#print "insertAllToBondTable bonds", [(t1, t2) for [t1,t2] in bondTypes]
				for (t1,t2) in bondTypes:
					atomType = QtGui.QTableWidgetItem(t1+"-"+t2)
					atomType.setFlags(QtCore.Qt.ItemIsEnabled)
					self.setItem(row, 0, atomType)
					
					Kb = ForceSpinBox([000.000, 9999.99], 3, parent=self.forceTab, fl=ff, type=(t1,t2),\
										method= ff.setBond, pos=0)
					self.setCellWidget(row, 1, Kb)
					Kb.setValue(ff.bond(t1,t2)[0])
					#print "insertAllToBondTable K", t1, t2, ff.bond(t1,t2)[0],ff.__dict__
					
					b0 = ForceSpinBox([0.0000, 5], 4, parent=self.forceTab, fl=ff, type=(t1,t2),\
										method= ff.setBond, pos=1)
					self.setCellWidget(row, 2, b0)
					b0.setValue(ff.bond(t1,t2)[1])
					#print "insertAllToBondTable b0", t1, t2, ff.bond(t1,t2)[1]
					 
					bonds[t1,t2] = [Kb, b0] 
					
					for otherMolecule in self.forceTab.equivalences[molecule.molname()]:
					        Kb.addForceField(otherMolecule.getForceField())
					        b0.addForceField(otherMolecule.getForceField())
					
					row += 1
				#self.allForceField[molName]["Bonds"]=bonds
        #---------------------------------------------------------------
        #list all molecules in the Structure Manager
        self.blockSignals(False)
        #print "insertAllBondTable fin"

    
#====================================================================
class AnglesTable(QtGui.QTableWidget):
    def __init__(self, hist, forceTab, parent=None):
        super(AnglesTable, self).__init__(parent=parent)
        #print "AnglesTable init"
        self.history = hist
        self.forceTab = forceTab

        self.setObjectName("anglesTable")
        self.setColumnCount(3)
        self.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(2, item)

        item = self.horizontalHeaderItem(0)
        item.setText("Type")
        item = self.horizontalHeaderItem(1)
        item.setText("Ktheta")
        item = self.horizontalHeaderItem(2)
        item.setText(u"Ⲑ0")

        # https://stackoverflow.com/questions/38098763/pyside-pyqt-how-to-make-set-qtablewidget-column-width-as-proportion-of-the-a#38129829
        header = self.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

    def update(self):
        #print "AnglesTable update"
        self.insertAllAngleTable()

    def showEvent(self,e):
        #print "AnglesTable showEvent"
        self.insertAllAngleTable()

    def insertAllAngleTable(self):
    
        row = 0
        rows = 0
        self.setRowCount(0)
        displayedMols=list()
        self.blockSignals(True)
        for molName in self.history.currentState().mixture:
            angles = dict()
            molecule = self.history.currentState().mixture.getMolecule(molName)
            if not molecule.molname() in displayedMols:
                displayedMols.append(molecule.molname())
                
                ff = molecule.getForceField()
                angleTypes = molecule.angleTypes()
                rows += len(angleTypes)+1
                self.setRowCount(rows)
                
                # display molecule name
                nameW = QtGui.QTableWidgetItem(molecule.molname())
                nameW.setTextAlignment(4)
                self.setItem(row, 0, nameW)
                self.setSpan(row, 0, 1, 3)
                self.item(row,0).setBackgroundColor (self.forceTab._selectedColor(molecule.molname()))
                row += 1
               
                for (t1,t2,t3) in angleTypes:
                    atomType = QtGui.QTableWidgetItem(t1+"-"+t2+"-"+t3)
                    atomType.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.setItem(row, 0, atomType)
                    
                    Kth = ForceSpinBox([000.000, 999.999], 3,  parent=self.forceTab, fl=ff, type=(t1,t2,t3),\
										method= ff.setAngle, pos=0)
                    self.setCellWidget(row, 1, Kth)
                    Kth.setValue(ff.angle(t1,t2,t3)[0])
                    
                    a0 = ForceSpinBox([0.0000, 180], 4,   parent=self.forceTab, fl=ff, type=(t1,t2,t3),\
										method= ff.setAngle, pos=1)
                    self.setCellWidget(row, 2, a0)
                    a0.setValue(ff.angle(t1,t2,t3)[1])
            
                    angles[t1,t2,t3] = [Kth, a0] 
                    
                    for otherMolecule in self.forceTab.equivalences[molecule.molname()]:
                            Kth.addForceField(otherMolecule.getForceField())
                            a0.addForceField(otherMolecule.getForceField())
            
                    row += 1
        
                #self.allForceField[molName]["Angles"]=angles
        self.blockSignals(False)

    

#====================================================================
class DihedralsTable(QtGui.QTableWidget):
    def __init__(self, hist, forceTab, parent=None):
        super(DihedralsTable, self).__init__(parent=parent)
        #print "DihedralsTable init"
        self.history = hist
        self.forceTab = forceTab

        self.setObjectName("dihedralTable")
        self.setColumnCount(4)
        self.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(3, item)

        item = self.horizontalHeaderItem(0)
        item.setText("Type")
        item = self.horizontalHeaderItem(1)
        item.setText("Kchi")
        item = self.horizontalHeaderItem(2)
        item.setText("n")
        item = self.horizontalHeaderItem(3)
        item.setText("Delta")

        # https://stackoverflow.com/questions/38098763/pyside-pyqt-how-to-make-set-qtablewidget-column-width-as-proportion-of-the-a#38129829
        header = self.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

    def update(self):
        #print "DihedralsTable update"
        self.insertAllAngleTable()

    def showEvent(self,e):
        #print "DihedralsTable showEvent"
        self.insertAllAngleTable()

    def insertAllDihedralTable(self):
        #list all molecules in the Structure Manager
    
        row = 0
        rows = 0
        self.setRowCount(0)
        displayedMols=list()
        self.blockSignals(True)
        self.clearContents ()
        for molName in self.history.currentState().mixture:
            dihedrals = dict()
            molecule = self.history.currentState().mixture.getMolecule(molName)
            if not molecule.molname() in displayedMols:
                displayedMols.append(molecule.molname())

                ff = molecule.getForceField()
                dihedralTypes = molecule.dihedralTypes()
                rows += len(dihedralTypes)+1
                self.setRowCount(rows)
                
                # display molecule name
                nameW = QtGui.QTableWidgetItem(molecule.molname())
                nameW.setTextAlignment(4)
                self.setItem(row, 0, nameW)
                self.setSpan(row, 0, 1, 4)
                self.item(row,0).setBackgroundColor (self._selectedColor(molecule.molname()))
                row += 1
               
                for [t1,t2,t3,t4] in dihedralTypes:
                    atomType = QtGui.QTableWidgetItem(t1+"-"+t2+"-"+t3+"-"+t4)
                    atomType.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.setItem(row, 0, atomType)
                    
                    Kchi = ForceSpinBox([0.0000, 99.9999], 4, parent=self.forceTab, fl=ff, type=(t1,t2,t3,t4),\
										method= ff.setDihedral, pos=0)
                    self.setCellWidget(row, 1, Kchi)
                    Kchi.setValue(ff.dihedral(t1,t2,t3,t4)[0])
                    
                    
                    n = ForceSpinBox([0, 9], 0, parent=self.forceTab, fl=ff, type=(t1,t2,t3,t4),\
										method= ff.setDihedral, pos=1)
                    self.setCellWidget(row, 2, n)
                    n.setValue(ff.dihedral(t1,t2,t3,t4)[1])
                        
                    Delta = ForceSpinBox([000.00, 999.99], 2, parent=self.forceTab, fl=ff, type=(t1,t2,t3,t4),\
										method= ff.setDihedral, pos=2)
                    self.setCellWidget(row, 3, Delta)
                    Delta.setValue(ff.dihedral(t1,t2,t3,t4)[2])
            
                    dihedrals[t1,t2,t3,t4] = [Kchi,Delta,n] 
            
                    for otherMolecule in self.forceTab.equivalences[molecule.molname()]:
                            n.addForceField(otherMolecule.getForceField())
                            Delta.addForceField(otherMolecule.getForceField())
                            Kchi.addForceField(otherMolecule.getForceField())
                        
                    row += 1
                #self.allForceField[molName]["Dihedrals"]=dihedrals
        self.blockSignals(False)



#====================================================================
#====================================================================

class ForceTab(QtGui.QFrame):   
    def __init__(self, hist, parent, previewer):
        super(ForceTab, self).__init__(parent)


        self.history                            =   hist
        self.parent                             = parent
        self.allForceField                      =   {}
        self.generated                          =   time.clock()
        self.allowUpdate                        =   True
        self.selectedMolecule                   =   None
        self.forcePreview = previewer
        #print "ForceTab, self.forcePreview ", self.forcePreview
        #widgets import 
        self.ui = Ui_forceTab()
        self.ui.setupUi(self)
        self.doRestore                           =   True
        self.valueChanged                       = False
        
        #activates the previewer
        #self.forcePreview = MixtureViewer(hist, parent=self)
        #self.ui.forcePreviewLayout.addWidget(self.forcePreview)

        #Buttons
        self.ui.typesButton.setIcon(QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "icon_topology.png"))
        self.ui.saveButton.setIcon(QtGui.QIcon().fromTheme("media-floppy",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "media-floppy.png")))
        self.ui.loadButton.setIcon(QtGui.QIcon().fromTheme("document-open",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "document-open.png")))
        self.ui.findCHARMMButton.setIcon(QtGui.QIcon().fromTheme("system-search",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "system-search.png")))
        self.ui.aboutTab  .setIcon(QtGui.QIcon().fromTheme("help-faq",    QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "help-about.png")    ))
        #Lables
        #splash_pix = QtGui.QPixmap(WOLFFIA_GRAPHICS+'/Wolffialogo.png')
        #self.ui.FBonds.setPixmap(splash_pix);
        #self.ui.FBonds.setMask(splash_pix.mask());



        #self.restoreForceField(self.history.currentState().forceFieldStorage)
        #self.history.push(force=True)

        #TABLES
        self.ui.bondsTable = BondsTable(hist, self, self.ui.bondBox)
        self.ui.gridLayout_2.addWidget(self.ui.bondsTable, 0, 0, 1, 1)
        self.ui.bondsTable.itemClicked.connect(self.on_bondsTable_itemClicked)

        self.ui.chargesTable = ChargesTable(hist, self, self.ui.chargesBox)
        self.ui.gridLayout_33.addWidget(self.ui.chargesTable, 0, 0, 1, 1)
        self.ui.chargesTable.itemClicked.connect(self.on_chargesTable_itemClicked)

        self.ui.nonBondTable = NonBondTable(hist, self, self.ui.nonbondedBox)
        self.ui.gridLayout_3.addWidget(self.ui.nonBondTable, 0, 0, 1, 1)
        self.ui.nonBondTable.itemClicked.connect(self.on_nonBondTable_itemClicked)

        self.ui.anglesTable = AnglesTable(hist, self, self.ui.anglesBox)
        self.ui.gridLayout_4.addWidget(self.ui.anglesTable, 0, 0, 1, 1)
        self.ui.anglesTable.itemClicked.connect(self.on_anglesTable_itemClicked)

        self.ui.dihedralTable = AnglesTable(hist, self, self.ui.dihedralsBox)
        self.ui.gridLayout_5.addWidget(self.ui.dihedralTable, 0, 0, 1, 1)
        self.ui.dihedralTable.itemClicked.connect(self.on_dihedralTable_itemClicked)


        self._updateEquivalences()


    #def paintEvent (self,  event):
    #    QtGui.QFrame.paintEvent(self, event)
    #    self.updateTAB()

    @QtCore.pyqtSlot()
    def on_aboutTab_pressed(self):
        #self.messageAboutTab()
        from AboutFT import AboutFT
        about = AboutFT(self)
        about.show()
        about.exec_()


    def on_anglesTable_itemClicked(self, item):
        self._selectMolecule(item)

    
    def on_bondsTable_itemClicked(self, item):
        self._selectMolecule(item)

    
    def on_chargesTable_itemClicked(self, item):
        self._selectMolecule(item)

    
    def on_chargesTable_itemChanged(self, wi):
    	print "on_chargesTable_itemChanged"
        self.history.push()
        self._changeAtomType(wi)
        self.update()
        self.forcePreview.update()


    def on_defaultForField_cellClicked(self, row, col): #Change this
        count = 0
        for mol in self.history.currentState().getMixture().molecules():
            if count == row:
                self.editor.setMolecule(self.history.currentState())
                break
            count += 1


    def on_dihedralTable_itemClicked(self, item):
        self._selectMolecule(item)

    def on_bondButton_pressed(self):
		'''
		Sets bond lenghts if force field to the current lengths of bonds in the selected molecule.
		If there are more than one bond of certain type, the average bond length is set.
		'''
 		selected = self.parent.buildTab.editor.selectedMolecules()
		print "on_bondButton_pressed ", selected
		if len(selected) != 1 or selected[0].molname() != self.selectedMolecule:
			errorgui = QtGui.QErrorMessage(self)
			errorgui.setModal(True) 
			errorgui.showMessage( "Please select ONE molecule with the same name as the one selected here using the Build tab.")
			return
		refMol = selected[0]
		refMol.getBondsAnglesFrom()
		ff     = refMol.getForceField()
			
		currentMixture = self.history.currentState().mixture
		for molName in currentMixture:
			mol = currentMixture.getMolecule(molName) 
			if mol.molname() == self.selectedMolecule: 
				mol.setForceField(ff)
		self.update()

   
    def on_findCHARMMButton_pressed(self):
        if self.selectedMolecule == None:
            errorgui = QtGui.QErrorMessage(self)
            errorgui.setModal(True) 
            errorgui.showMessage( "Please select a molecule by clicking on its name in the NONBONDED section.")
            return
    
        self.history.push()
        from CHARMMParameterFinderDialog import CHARMMParameterFinderDialog
        #print "on_findCHARMMButton_pressed ", self.selectedMolecule

        #  find first molecule with name as self.selectedMolecule
        molecule = None
        currentMixture = self.history.currentState().mixture
        for molName in currentMixture:
            molecule = currentMixture.getMolecule(molName)
            #print "on_findCHARMMButton_pressed changing ff of " , self.selectedMolecule , " ... checking ", molecule.molname()
            if molecule.molname() == self.selectedMolecule: break

        if molecule != None:
            charmm = CHARMMParameterFinderDialog(self, molecule)
            charmm.show()
            charmm.exec_()
            pairing = charmm.getPairing()
            ff = charmm.getForceField()
            if pairing != None:
                print "on_findCHARMMButton_pressed obtained  " , pairing.getPairing()
                for molName in currentMixture:
                    mol = currentMixture.getMolecule(molName) 
                    if mol.molname() == self.selectedMolecule: 
						#print "on_findCHARMMButton_pressed changing ff of " , molName
						#print "on_findCHARMMButton_pressed mol.atomTypes()", molName , mol.atomTypes()
						#print  "on_findCHARMMButton_pressed mol.atomTypes()", molName, mol.atomTypes()
						mol.getForceField().addZeroParameters(mol)  # ensures bonds, angles, dihedrals get values in next statement
						#mol.setForceField(pairing.getPairedForceField(mol.getForceField(),keepCharges=True))   # FF ya no guarda cargas
						mol.setForceField(pairing.getPairedForceField(mol.getForceField()))
						mol.renameTypes(pairing.getPairing())
						#print  "on_findCHARMMButton_pressed result", molName, mol.forceField._NONBONDED
            self.update()

    
    def on_loadButton_pressed(self):
        if self.selectedMolecule == None:
            errorgui = QtGui.QErrorMessage(self)
            errorgui.setModal(True) # blocks Wolffia
            errorgui.showMessage( "Please select a molecule by clicking on its name in the NONBONDED section.")
            return
    
        file1 = QtGui.QFileDialog.getOpenFileName(self, "Load a force field file", self.history.currentState().getBuildDirectory(), "*.prm")
        #print file +"***file***"
        if len(file1) > 0:
            self.history.push()
            for molName in self.history.currentState().mixture:
                molecule = self.history.currentState().mixture.getMolecule(molName)
                #print "on_loadButton_pressed changing ff of " , self.selectedMolecule , " ... checking ", molecule.molname()
                if molecule.molname() == self.selectedMolecule:
                    #print "       on_loadButton_pressed YES, changing ff of " , self.selectedMolecule
                    #molecule.getForceField().loadCHARMM(file1)
                    ff = ForceField()
                    ff.loadCHARMM(file1)
                    molecule.setForceField(ff)
                    #print "       on_loadButton_pressed ", molecule.getForceField(),molecule.getForceField()._NONBONDED
            self.update()


    def on_nonBondTable_itemChanged(self, wi):
    	print "on_nonBondTable_itemChanged"
        if len(str(wi.text())) > 0:
            self.history.push()
            self._changeType(wi)
        self.update()
        self.forcePreview.update()


    def on_nonBondTable_itemClicked(self, item):
        print "on_nonBondTable_itemClicked ", item.text()
        self._selectMolecule(item)

    def on_saveButton_pressed(self):     
        print "on_saveButton_pressed self.selectedMolecule =", self.selectedMolecule
        if self.selectedMolecule == None:
            errorgui = QtGui.QErrorMessage(self)
            errorgui.setModal(True) # blocks Wolffia
            errorgui.showMessage( "Please select a molecule by clicking on its name.")
            return
    
        mesg = 'Save ' + self.history.currentState().getMixtureName()
        file1 = str(QtGui.QFileDialog.getSaveFileName(self, mesg, self.history.currentState().getBuildDirectory(), "*.prm"))
        if len(file1) > 0:
            if file1[-4:] != ".prm": file1 += ".prm"
            for molName in self.history.currentState().mixture:
                molecule = self.history.currentState().mixture.getMolecule(molName)
                #print "on_loadButton_pressed changing ff of " , self.selectedMolecule , " ... checking ", molecule.molname()
                if molecule.molname() == self.selectedMolecule:
                    #print "       on_loadButton_pressed YES, changing ff of " , self.selectedMolecule
                    molecule.getForceField().writeCHARMM(file1)
                    #print "       on_loadButton_pressed ", molecule.getForceField(),molecule.getForceField()._NONBONDED
            self.update()


    def on_typesButton_pressed(self):
    	print "on_typesButton_pressed ", self.selectedMolecule
        if self.selectedMolecule == None:
            errorgui = QtGui.QErrorMessage(self)
            errorgui.setModal(True) 
            errorgui.showMessage( "Please select a molecule by clicking on its name in the NONBONDED section.")
            return
    
        self.history.push()
        #  find first molecule with name as self.selectedMolecule
        molecule = None
        currentMixture = self.history.currentState().mixture
        for molName in currentMixture:
        	if currentMixture.getMolecule(molName).molname() == self.selectedMolecule:
        		molecule = currentMixture.getMolecule(molName)
        		break
            #molecule = currentMixture.getMolecule(molName)
            #print "on_findCHARMMButton_pressed changing ff of " , self.selectedMolecule , " ... checking ", molecule.molname()
            #if molecule.molname() == self.selectedMolecule: break

        if molecule != None:
            typeAssignments = molecule.redefineTypes()
            if typeAssignments != None:
                report = "The following types were defined:\n\ttype\tatoms\n"
                for type in typeAssignments.keys():
                    report += "\t" + type + "\t" + str(len(typeAssignments[type])) + "\n"
                
                msgBox = QtGui.QMessageBox.information (self, "Detect Atom Type", report, buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.Cancel)
                    
                self.update()
                self.forcePreview.update()
                    
                # finally set this force field to all copies of the molecule
                newFF = molecule.getForceField()
                newFF.addZeroParameters(molecule)
                #print "on_typesButton_pressed newFF", newFF._NONBONDED.keys()
                #print "on_typesButton_pressed newFF", newFF._BONDS.keys()
                for molName in currentMixture:
                    molecule2 = currentMixture.getMolecule(molName)
                    if molecule.molname() == molecule2.molname() and molecule != molecule2:
                        molecule2.redefineTypes()
                        #print "on_typesButton_pressed changed ff of ", molName
            else:
                QtGui.QErrorMessage(self).showMessage("Unable to detect atom types.")
        else:
            QtGui.QErrorMessage(self).showMessage("Please select a molecule by clicking on its name in the NONBONDED section.")
                

    def on_nonBondTable_cellClicked(self, row,col):
        prRow = row
        prCol = col
        
    '''
    def on_nonBondTable_currentCellChanged(self,row,col,prRow,prCol):
        if row >= 0:
            self.ui.nonBondTable.item(row,col).setBackgroundColor (QtCore.Qt.green)
        if prRow >= 0:
            self.ui.nonBondTable.item(prRow,prCol).setBackgroundColor (QtCore.Qt.white)
    '''
    
    def change(self):
        #self.history.push()  # moved to hideEvent
        self.valueChanged = True
        #self.insertAllToNonBondTable()  # marronazo para actualizar carga total
        self.ui.chargesTable.updateCharges()
        pass
        

    def chosenForField(self):
        count = self.ui.defaultForField.topLevelItemCount()
        for i in range(count):
            item = self.ui.defaultForField.itemAt(i,1)

    
    def hideEvent(self,e):
        if self.valueChanged:
            self.history.push()
        print "ForceTab hideEvent"
    #    self.wolffia.update()
        

    def on_anglesTable_showEvent(self,e):
        print "ForceTab on_anglesTable_showEvent"


    def setChargesInMolecule(self, molname, aType, charge):
        #if molname[:8] != "SOLVENT(":

        #print "setChargesInMolecule " , molname, aType, charge
        for mol in self.history.currentState().mixture:
            molecule = self.history.currentState().mixture.getMolecule(mol)
            #print "setChargesInMolecule molecule = " , molecule.molname()
            if molecule.molname() == molname:
                #print "setChargesInMolecule " , molecule, aType, charge
                for atom in molecule.atoms():
                    if molecule.getAttributes(atom).getType() == aType:
                        molecule.getAttributes(atom).setCharge(charge)

    
    def showEvent(self, e):
        #print "ForceTab.showEvent " 
        self.update()
        super(ForceTab, self).showEvent(e)
        #self.update()

    def reset(self):
        self.forcePreview.reset()

    def _updateEquivalences(self):
        self.equivalences =  self.history.currentState().getMixture().equivalenceClasses()

    def update(self):
        print "ForceTab.update "
        timer = WTimer("ForceTab")
        self._updateEquivalences()

        if self.ui.chargesTable.isVisible(): self.ui.chargesTable.update()

        if self.ui.nonBondTable.isVisible(): self.ui.nonBondTable.update()

        if self.ui.bondsTable.isVisible(): self.ui.bondsTable.update()

        if self.ui.anglesTable.isVisible(): self.ui.anglesTable.update()

        if self.ui.dihedralTable.isVisible(): self.ui.dihedralTable.update()


        self.generated = time.clock()
        
        selecteed = self.selectedMolecule != None
        self.ui.bondButton.setEnabled(selecteed)
        self.ui.findCHARMMButton.setEnabled(selecteed)
        self.ui.loadButton.setEnabled(selecteed)
        self.ui.saveButton.setEnabled(selecteed)
        self.ui.typesButton.setEnabled(selecteed)
        timer.report()
        print "ForceTab.update fin"


    def updateTAB(self):
        self.forcePreview.setMixture(self.history.currentState().getMixture())


    def _changeAtomType(self, wi):
        print "ForceTab _changeAtomType  row-col ", wi.row(), wi.column()
        if wi.column() == 1:
			row = wi.row()
			nameRow = row
			print "ForceTab _changeAtomType  ", wi.row(),self.ui.chargesTable.rowSpan(wi.row(),2)
			while self.ui.chargesTable.item(nameRow,0).toolTip() != "Click to select.":
				nameRow -= 1
				
			print "ForceTab _changeAtomType  ", nameRow, row
			if nameRow == row: return
			
			molName = self.ui.chargesTable.item(nameRow,0).text()
			atom    = int(self.ui.chargesTable.item(row,0).text())
			print "ForceTab _changeAtomType  ", nameRow,molName
			molecules = self.history.currentState().getMixture().molecules()
			for mol in molecules:
				molecule = self.history.currentState().getMixture().getMolecule(mol)
				if molName == molecule.molname():
					types = molecule.atomTypes()
					oldType = types[row - nameRow - 1]
					print "ForceTab _changeAtomType  ", mol,oldType
					if len(wi.text()) == 0 or len(wi.text()) > 3:  # check if new name is good (write a method for this)
						wi.setText(oldType)
						return
					if wi.text() != oldType:
						molecule.getAtomAttributes(atom).getInfo().setType(str(wi.text()))

              
    def _changeType(self, wi):
        if wi.column() == 0:
            row = wi.row()
            #print "on_nonBondTable_itemChanged ", wi.row(),self.ui.nonBondTable.rowSpan(wi.row(),2)
            nameRow = row
            while self.ui.nonBondTable.item(nameRow,0).flags() == (QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled):
                #if nameRow == 0: return
                nameRow -= 1
                
            if nameRow == row: return
            
            molName = self.ui.nonBondTable.item(nameRow,0).text()
            #print "on_nonBondTable_itemChanged ", nameRow,molName
            molecules = self.history.currentState().getMixture().molecules()
            for mol in molecules:
                molecule = self.history.currentState().getMixture().getMolecule(mol)
                if molName == molecule.molname():
                    types = molecule.atomTypes()
                    oldType = types[row - nameRow - 1]
                    #print "on_nonBondTable_itemChanged oldType ", mol,oldType
                    if len(wi.text()) == 0 or len(wi.text()) > 3:  # check if new name is good (write a method for this)
                        wi.setText(oldType)
                        return
                    if wi.text() != oldType:
                        molecule.renameTypes({oldType: str(wi.text())})


    def _selectMolecule(self, item):
        print "_selectMolecule ", item.text(),item.flags() != (QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
        
        # act only when item has a molecule name
        if item.flags() != (QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled):
            nextText = item.text()
            if nextText == self.selectedMolecule:
                self.selectedMolecule = None
            else:
                self.selectedMolecule = nextText
            self.update()

    def _selectedColor(self, molname):
        #print "_selectedColor ", molname,self.selectedMolecule , molname == self.selectedMolecule
        if molname == self.selectedMolecule:
            return QtCore.Qt.green
        return QtCore.Qt.white
    



class ForceSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, spinRange=[0,1000], decimals=4, colorIfZero="Yellow", parent=None, fl=None, method=None, type=None, pos=0):
        QtGui.QDoubleSpinBox.__init__(self,parent)
        QtCore.QObject.connect(self, QtCore.SIGNAL("editingFinished()"), self.change)
        if parent != None: QtCore.QObject.connect(self, QtCore.SIGNAL("editingFinished()"), parent.change)
        self.setDecimals(decimals)
        self.setRange(spinRange[0], spinRange[1])
        self.color = colorIfZero
        self.parent = parent
        self.ff = set()
        if fl != None:
            self.ff.add(fl)
        self.method = method
        self.pos = pos
        self.type = type
        #print "ForceSpinBox ", fl
        
    def setValue(self, x):
		#print "ForceSpinBox setValue " , x
		QtGui.QDoubleSpinBox.setValue(self, x)
		if x == 0 :
			self.setStyleSheet('background: '+self.color)
		#self.change()

    def addForceField(self, fl):
        #if not fl in self.ff:
        #print "addForceField ",fl
        self.ff.add(fl)
        
    def change(self):
        import inspect
        if self.ff != None:
            print 'ForceSpinBox self.value(): ', self.value()
            for force in self.ff:
				#print 'ForceSpinBox change changecaller name:', inspect.stack()
				print "ForceSpinBox valueChanged  " , "force.", self.method, self.value(), force
				self.method(self.type,self.value(),self.pos)
            if self.value() == 0 :
               self.setStyleSheet('background: '+self.color)
            else:
               self.setStyleSheet('background: white')
               


class ChargeSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, spinRange=[0,1000], decimals=4, parent=None, molecule=None, atom=None):
        QtGui.QDoubleSpinBox.__init__(self,parent)
        QtCore.QObject.connect(self, QtCore.SIGNAL("editingFinished()"), self.change)
        if parent != None: QtCore.QObject.connect(self, QtCore.SIGNAL("editingFinished()"), parent.change)
        self.setDecimals(decimals)
        self.setRange(spinRange[0], spinRange[1])
        self.parent = parent
        self.molecules=set()
        self.atom = atom
        if molecule != None:
            self.molecules.add(molecule)
            QtGui.QDoubleSpinBox.setValue(self, molecule.getAtomAttributes(self.atom).getInfo().getCharge())
        self.paint()
        
	def setValue(self, x):
		#print "setValue " , x
		QtGui.QDoubleSpinBox.setValue(self, x)
		self.paint()

    def addMolecule(self, molecule):
        #if not fl in self.ff:
        #print "addForceField ",fl
        self.molecules.add(molecule)
        
    def change(self):
        import inspect
        if self.molecules != None:
            for molecule in self.molecules:
				print "ChargeSpinBox valueChanged  " , self.value(), molecule
				molecule.getAtomAttributes(self.atom).getInfo().setCharge(self.value())
            self.paint()
               
    def paint(self):
		if self.value() < 0 :
			self.setStyleSheet('background: #FFAAAA')
		elif self.value() > 0 :
			self.setStyleSheet('background: #AAAAFF')
		else :
			self.setStyleSheet('background: white')
