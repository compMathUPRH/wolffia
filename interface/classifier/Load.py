#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------
#  load.py
#  Version 0.1, October, 2011
#
#  Description: load.py creates a QDialog to load psf and pdb files 
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    Melissa  López Serrano, 

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


from PyQt4 import QtCore, QtGui
import sys, os
import random
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import NANOCAD_BASE
from lib.chemicalGraph.Mixture import Mixture
from interface.main.MixtureViewer import MixtureViewer
from interface.main.History import History
from ui_Load import Ui_Load
from interface.main.WFileDialogs import WFileDialog
from interface.main.WWidgets import PreviewButton

class Load(QtGui.QDialog):
    def __init__(self, parent=None, dropedPdb=None):
        super(Load, self).__init__(parent, modal = 1)
        
        print "Load dropedPdb=", dropedPdb
        #Dialog settings
        self.uiLoad         = Ui_Load()
        self.uiLoad.setupUi(self)
        self.history = History()
        self.isAdded = False
        self.history.currentState().reset()
        
        #Viewer
        print "Load setting viewer"
        self.previewArea    = MixtureViewer(self.history, self, None)
        self.previewArea.showHelp(False)
        self.uiLoad.moleculeViewerLayout.addWidget(self.previewArea)
        
        #Mixture
        print "Load setting getting mixture"
        self.myMixture      = self.history.currentState().getMixture()
        self.mixAndRows     = list()
        
        #Table Settings
        self.loadTable      = self.uiLoad.tableWidget
        self.loadTableRows  = 0
        self.equalMolecules = []
        self.saveCheckBox   = None
        
        #Information Button Settings
        self.uiLoad.hint.setFlat(True)
        self.uiLoad.hint.setIcon(QtGui.QIcon().fromTheme("dialog-information", QtGui.QIcon(str(NANOCAD_BASE+"\\interface\\graphics\\") +"dialog-information.png")))    
        self.uiLoad.connectDataBaseButton.setFlat(True)
        self.uiLoad.connectDataBaseButton.setIcon(QtGui.QIcon().fromTheme("network-server", QtGui.QIcon(str(NANOCAD_BASE+"\\interface\\graphics\\") +"dialog-information.png")))    

        #PDB droped from MixtureViewer
        print "Load setting pdbDirectory"
        self.pdbDirectory = dropedPdb
        if self.pdbDirectory != None:
            print "Load setting self.pdbDirectory != None"
            self.uiLoad.lineEdit_1.setText(self.pdbDirectory)
            print "Load animateClick"
            self.uiLoad.loadButton.animateClick()
        print "Load end"
        
    def update(self):
        self.previewArea.update()
        return
        mix = Mixture()
        for i in range(self.loadTable.rowCount()):
            #for j in range(3,6):
            ##print "Load update", self.loadTable.item(i,5).text(),self.loadTable.cellWidget(i,1).show
            if self.loadTable.cellWidget(i,1).show:
                mix.add(self.myMixture.getMolecule(str(self.loadTable.item(i,5).text())))
        self.previewArea.setMixture(mix)
#-------------------------------------- Methods ------------------------------------
#loadPsfOrNot(): Asks the user if wants to change all the names of the molecules that are the same 

    def loadPsfOrNot(self,filename):
        
        msg = QtGui.QMessageBox.question(self, 'Loading Fi\les...',
         'Would you like to load the psf file associated with: '+filename+'?\n'+'\n NO, will imply to only read the pdb file.', 
         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        
        return msg == QtGui.QMessageBox.Yes

#-------------------------------------- 
#changeNameOrNotMessage(): Asks the user if wants to change all the names of the molecules that are the same 

    def changeNameOrNotMessage(self):
        
        msg = QtGui.QMessageBox.question(self, 'Change all Names...',
         'Would you like to change all the names of the molecules with that color?', 
         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        
        return msg == QtGui.QMessageBox.Yes


#--------------------------------------
#getLineEditInfo(): Gets the paths and constructs the Mixture
    def getLineEditInfo(self):
    
        # Gets paths
        path_1 = str(self.uiLoad.lineEdit_1.displayText())
        print "Load getLineEditInfo",path_1
        self.uiLoad.lineEdit_1.clear()
        path_2 = str(self.uiLoad.lineEdit_2.displayText())
        print "Load getLineEditInfo",path_2
        self.uiLoad.lineEdit_2.clear()
        print "Load getLineEditInfo loadInfo"
        self.loadInfo(path_1, path_2)
        print "Load getLineEditInfo end"
 
#--------------------------------------
    def loadInfo(self,path_1='',path_2= ''):       
        if path_1 <> '' and path_2 == '':
            try:
                self.history.currentState().getMixture().load(path_1)
            except:
                QtGui.QMessageBox.warning(self,"Error 1 !!!","There is a problem loading the file " + path_1 + " in box 1.")
                print sys.exc_info()
        elif not(path_2 == '') and path_1 == '':
            try:
                self.history.currentState().getMixture().load(path_2)
            except:
                QtGui.QMessageBox.warning(self,"Error 2 !!!","There is a problem loading the file " + path_2 + " in box 2.")
        elif not(path_1 == '') and not(path_2 == ''):
            if (path_1[len(path_1)-3]+path_1[len(path_1)-2]+path_1[len(path_1)-1]) == 'pdb' and (path_2[len(path_2)-3]+path_2[len(path_2)-2]+path_2[len(path_2)-1]) == 'psf':
                try: 
                    self.history.currentState().getMixture().load(path_1,path_2)
                except Exception  as e:
                    QtGui.QMessageBox.warning(self,"Error 3 !!!","There is a problem with the file."+str(e))
            elif (path_1[len(path_1)-3]+path_1[len(path_1)-2]+path_1[len(path_1)-1]) == 'psf' and (path_2[len(path_2)-3]+path_2[len(path_2)-2]+path_2[len(path_2)-1]) == 'pdb':
                try:
                    self.history.currentState().getMixture().load(path_2,path_1)
                except Exception  as e:
                    QtGui.QMessageBox.warning(self,"Error 4 !!!","There is a problem with the file."+str(e))
            else:QtGui.QMessageBox.warning(self,"Error 5 !!!","There is a problem with the file.")  
            
        elif not(path_1 == '') and (path_1[len(path_1)-3]+path_1[len(path_1)-2]+path_1[len(path_1)-1]) == 'pdb':
            filePath = None
            
            #Search if the *.psf file associated with the *.pdb file exists in the same folder
            for f in os.listdir(os.path.dirname(path_1)) :
                path1 = os.path.basename(path_1)
                if f == path1[0:len(path1)-2]+'s'+'f':
                    filePath = os.path.dirname(path_1)+'/'+f
                    #print "filePath",filePath
                    
            if not(filePath == None):
                if self.loadPsfOrNot(f):
                    try:
                        self.history.currentState().getMixture().load(path_1,filePath)
                    except:
                        QtGui.QMessageBox.warning(self,"Error 6 !!!","There is a problem with the file.")
                else:
                    try:
                        self.history.currentState().getMixture().load(path_1,None)
                    except:
                        QtGui.QMessageBox.warning(self,"Error 7 !!!","There is a problem with the file.")
            else:
                try:
                    self.history.currentState().getMixture().load(path_1,None)
                except:
                    QtGui.QMessageBox.warning(self,"Error 8 !!!","There is a problem with the file.")
                
                            
        elif not(path_1 == '') and (path_1[len(path_1)-3]+path_1[len(path_1)-2]+path_1[len(path_1)-1]) == 'psf':
            for f in os.listdir(os.path.dirname(path_1)) :
                path1 = os.path.basename(path_1)
                if f == path1[0:len(path1)-2]+'d'+'b':
                    filePath = os.path.dirname(path_1)+'/'+f
                    try:
                        self.history.currentState().getMixture().load(filePath,path_1)
                    except:
                        QtGui.QMessageBox.warning(self,"Error 9 !!!","There is a problem with the file.")

        elif path_1 == '' and not(path_2 == '') and (path_2[len(path_2)-3]+path_2[len(path_2)-2]+path_2[len(path_2)-1]) == 'pdb':
            filePath = None
            for f in os.listdir(os.path.dirname(path_2)) :
                path2 = os.path.basename(path_2)
                if f == path2[0:len(path2)-2]+'s'+'f':
                    filePath = os.path.dirname(path_2)+'/'+f
            if not(filePath == None):
                if self.loadPsfOrNot(f):
                    try:
                        self.history.currentState().getMixture().load(path_2,filePath)
                    except:
                        QtGui.QMessageBox.warning(self,"Error 10 !!!","There is a problem with the file.")
                else:
                    try:
                        self.history.currentState().getMixture().load(path_2,None)
                    except:
                        QtGui.QMessageBox.warning(self,"Error 11 !!!","There is a problem with the file.")
            else:
                try:
                        self.history.currentState().getMixture().load(path_2,None)
                except:
                    QtGui.QMessageBox.warning(self,"Error 12 !!!","There is a problem with the file.")                            
                            
        elif path_1 == '' and not(path_2 == '') and (path_2[len(path_2)-3]+path_2[len(path_2)-2]+path_2[len(path_2)-1]) == 'psf':
            for f in os.listdir(os.path.dirname(path_2)) :
                path2 = os.path.basename(path_2)
                if f == path2[0:len(path2)-2]+'d'+'b':
                    filePath = os.path.dirname(path_2)+'/'+f
                    try:
                        self.history.currentState().getMixture().load(filePath,path_2)
                    except:
                        QtGui.QMessageBox.warning(self,"Error 13 !!!","There is a problem with the file.")
                        
        else:QtGui.QMessageBox.warning(self,"Error 14 !!!","There is a problem with the file.**")
           
        #This is how we can obtain the atoms...
        #for m in self.history.currentState().getMixture().nodes():
            #print "@Load:mixture",self.history.currentState().getMixture().getMolecule(m).nodes()
        #print "myMixture",self.myMixture.order()
                
 
#--------------------------------------
#addCheckBox(): Adds a CheckBox into the column's cell to select the molecules that would be loaded


    def addCheckBox(self,row,name):
    
        #---CheckBox---
    
        self.saveCheckBox = CheckBox(self,row,self.loadTable)
        self.saveCheckBox.setObjectName(str(name+str(row)))
        
        self.saveCheckBox.setCheckState(QtCore.Qt.Checked)
        self.saveCheckBox.setFixedSize(25,25)
            
        #---Cell---
        self.loadTable.setCellWidget(row,0,self.saveCheckBox)

#--------------------------------------
#addButtonintoCell(): Adds a button into the column's cell to preview the molecules


    def addButtonintoCell(self,row,name):
        self.viewToolButton = PreviewButton(self.history.currentState(),
                                        self.previewArea,parent=self.loadTable, molname=str(name),
                                        initState=True)
                                        #initState=self.history.currentState().shownMolecules.isShown(str(name)))
        
        self.history.currentState().shownMolecules.show(str(name))
        #QtCore.QObject.connect(self.viewToolButton, QtCore.SIGNAL('clicked()'), self.on_viewToolButton_clicked())
        #self.viewToolButton.clicked.connect(self.on_viewToolButton_clicked)
        self.viewToolButton.setObjectName(str(name))
        self.viewToolButton.setFixedSize(25,25)
        
        #---Cell---
        self.loadTable.setCellWidget(row,1,self.viewToolButton)

    #--------------------------------------
    #showHideAllMessage(): Asks the user if wants to show/hide all the molecules painted with the same color  

    def loadMessage(self):

        msg = QtGui.QMessageBox.information(self, 'Information...',
        'This may take a while. Please be patient ... ', 
        QtGui.QMessageBox.Ok)
    #--------------------------------------
    #showHideAllMessage(): Asks the user if wants to show/hide all the molecules painted with the same color  

    def showHideAllMessage(self):

        msg = QtGui.QMessageBox.question(self, 'Show or Hide...',
        'Would you like to show/hide all the molecules with that color?', 
        QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        
        
        return msg == QtGui.QMessageBox.Yes 
 

#--------------------------------------
#reviewIsomorphisms(): Verify graph's isomorphism between two graphs
    
    def reviewIsomorphisms(self):
        tempList            = []
        theColors           = []
        self.equalMolecules = []
        row                 = -1
        
        for c in range(0,self.myMixture.order()):
            color = createColors()
            theColors.append(color)
        
        
        #Check equal molecules    
        remainingMols      =  list(self.myMixture)
        
        for each in self.myMixture:
            row        = row + 1
            searchList = list(remainingMols)
        
            for theMol in searchList:
                if self.myMixture.getMolecule(each) == self.myMixture.getMolecule(theMol):
                    tempList.append(theMol)
                    remainingMols.remove(theMol)
                
            if len(tempList) > 0:
                self.equalMolecules.append([tempList, None])
            tempList   = []
        
        #creating colors    
        for c in range(0,len(self.equalMolecules)):
            color = createColors()
            self.equalMolecules[c][1] = color
            #for molecule in self.equalMolecules[c][0]:
                #self.myMixture.getMolecule(molecule).rename(molecule + str(c))
        
                

#************************************************
#addSelectAllCheckBox(): Create a checkBox to select all the molecules in the table

    def addSelectAllCheckBox(self):    
        self.selectAllCheckBox = QtGui.QCheckBox()
        self.deSelectAll       = True
        font                   = QtGui.QFont()
        font.setPointSize(9)
        self.selectAllCheckBox.setFont(font)
        self.selectAllCheckBox.setText(QtGui.QApplication.translate("Load", "Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.selectAllCheckBox.setObjectName("selectAllCheckBox")
        self.selectAllCheckBox.setCheckState(QtCore.Qt.Checked)
        self.selectAllCheckBox.setTristate(on = False)
        self.uiLoad.SelectAllLayout.addWidget(self.selectAllCheckBox)
        self.connect(self.selectAllCheckBox, QtCore.SIGNAL('stateChanged(int)'), self.checkBoxState)
  
    def checkBoxState(self, value):
        if self.selectAllCheckBox.checkState() == QtCore.Qt.Checked:
            for row in range(0,self.loadTableRows):
                self.loadTable.cellWidget(row,0).setCheckState(QtCore.Qt.Checked)
        
        elif self.selectAllCheckBox.checkState() == QtCore.Qt.Unchecked and self.deSelectAll == True:
            for row in range(0,self.loadTableRows):
                self.loadTable.cellWidget(row,0).setCheckState(QtCore.Qt.Unchecked)
        elif self.selectAllCheckBox.checkState() == QtCore.Qt.Unchecked and self.deSelectAll == False:
            self.deSelectAll         = True 

#************************************************
#addSelectAllCheckBox(): Create a checkBox to select all the molecules in the table

    def addShowHideAllCheckBox(self):    
        self.showHideAllCheckBox = QtGui.QCheckBox()
        #print "Entre aqui"
        self.showAll       = True
        font                   = QtGui.QFont()
        font.setPointSize(9)
        self.showHideAllCheckBox.setFont(font)
        self.showHideAllCheckBox.setText(QtGui.QApplication.translate("Load", "Show All", None, QtGui.QApplication.UnicodeUTF8))
        self.showHideAllCheckBox.setObjectName("showHideAllCheckBox")
        self.showHideAllCheckBox.setCheckState(QtCore.Qt.Checked)
        self.showHideAllCheckBox.setTristate(on = False)
        self.uiLoad.ShowAllLayout.addWidget(self.showHideAllCheckBox)
        self.connect(self.showHideAllCheckBox, QtCore.SIGNAL('stateChanged(int)'), self.showHideAllState)
  
    def showHideAllState(self, value):
        if self.showHideAllCheckBox.checkState() == QtCore.Qt.Checked:
            for row in range(0,self.loadTableRows):
                self.loadTable.cellWidget(row,1).setShown()
                #self.loadTable.cellWidget(row,1).click()
        elif self.showHideAllCheckBox.checkState() == QtCore.Qt.Unchecked and self.showAll == True:
            for row in range(0,self.loadTableRows):
                self.loadTable.cellWidget(row,1).setHidden()
        elif  self.showHideAllCheckBox.checkState() == QtCore.Qt.Unchecked  and self.showAll == False:
            self.showAll         = True
   
#*************************************************
#setTable(): Creates and show the table

    def setTable(self):
        
        self.reviewIsomorphisms()
        
        #creates rows and columns
        self.loadTable.setColumnCount(6)
        self.loadTableRows = self.myMixture._len()
        self.loadTable.setRowCount(self.loadTableRows)
        
        
        item = QtGui.QTableWidgetItem()
        self.loadTable.setHorizontalHeaderItem(0, item)
        self.loadTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Load", "Save", None, QtGui.QApplication.UnicodeUTF8))
        
        item = QtGui.QTableWidgetItem()
        self.loadTable.setHorizontalHeaderItem(1, item)
        self.loadTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Load", "Prev", None, QtGui.QApplication.UnicodeUTF8))
        
        item = QtGui.QTableWidgetItem()
        self.loadTable.setHorizontalHeaderItem(2, item)
        self.loadTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Load", "Molecule Name", None, QtGui.QApplication.UnicodeUTF8))
        
        item = QtGui.QTableWidgetItem()
        self.loadTable.setHorizontalHeaderItem(3, item)
        self.loadTable.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Load", "No. of Atoms", None, QtGui.QApplication.UnicodeUTF8))
        
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(0x0001)
        self.loadTable.setHorizontalHeaderItem(4, item)
        self.loadTable.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("Load", "Atoms Found", None, QtGui.QApplication.UnicodeUTF8))
        
        item = QtGui.QTableWidgetItem()
        self.loadTable.setHorizontalHeaderItem(5, item)
        self.loadTable.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("Load", "Atom_ID", None, QtGui.QApplication.UnicodeUTF8))
        
        row = 0
        temp =[]
        
        #Adding the molecule information into the rows
        for eqCassInd in range(len(self.equalMolecules)):
            for molName in self.equalMolecules[eqCassInd][0]:                               
                for column in range(0,6):
                    item = QtGui.QTableWidgetItem()
                    self.loadTable.setItem(row, column, item)
            
                    if column == 0:
                        self.addCheckBox(row,molName)
                        self.loadTable.resizeColumnToContents(column)
                        
                    elif column == 1:
                        self.addButtonintoCell(row,molName)
                        self.loadTable.resizeColumnToContents(column)
                        temp.append(molName)
                        temp.append(row)
                        self.mixAndRows.append(temp)
                        temp = []
            
                    elif column == 2:
                        newTableWidgetItem = myTableWidgetItem(self, self.myMixture.getMolecule(molName)._name, molName)
                        newTableWidgetItem.setBackgroundColor(self.equalMolecules[eqCassInd][1])
                        self.loadTable.setItem(row,column,newTableWidgetItem)
                        self.loadTable.resizeColumnToContents(column)
            
                    elif column == 3:
                        newitem = myTableWidgetItem(self,str(self.myMixture.getMolecule(molName).order()))
                        newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.loadTable.setItem(row, column, newitem)
                        self.loadTable.resizeColumnToContents(column)
                    
                    elif column == 4:                    
                        molecule = self.myMixture.getMolecule(molName)
                        newitem = myTableWidgetItem(self,str(molecule.getElements()))
                        newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.loadTable.setItem(row, column, newitem)
                        self.loadTable.resizeColumnToContents(column)
                    
                    elif column == 5:                    
                        newitem = QtGui.QTableWidgetItem(str(molName))
                        newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.loadTable.setItem(row, column, newitem)
                        self.loadTable.resizeColumnToContents(column)                                      
                row += 1
        self.update()       

#---------------- Dialog's signals -------------------
    def on_Browse_1_pressed(self):
        d = WFileDialog(self, 'Browse File','','')
        if d.accepted():
            filename = d.fullFilename()
            if not os.path.exists(str(filename)):
                QtGui.QMessageBox.information(self, "Wolffia's message", "Did not find file " + filename + ". File not loaded.", QtGui.QMessageBox.Ok)
                return
            self.uiLoad.lineEdit_1.setText(str(d.fullFilename()))
            
    def on_Browse_2_pressed(self):
        d = WFileDialog(self, 'Browse File','','')
        if d.accepted():
            filename = d.fullFilename()
            if not os.path.exists(str(filename)):
                QtGui.QMessageBox.information(self, "Wolffia's message", "Did not find file " + filename + ". File not loaded.", QtGui.QMessageBox.Ok)
                return
            self.uiLoad.lineEdit_2.setText(str(d.fullFilename()))
            
    def on_hint_pressed(self):
        from AboutLoad import AboutLoad
        about = AboutLoad(self)
        about.show()
        about.exec_()
            
    def on_connectDataBaseButton_pressed(self):
        #print"on_connectDataBaseButton_pressed"
        
        from ImportMolecules import ImportMolecules
        
        importMoleculeDialog = ImportMolecules()
        importMoleculeDialog.show()
        importMoleculeDialog.exec_()
        
        #print "PDB \n",importMoleculeDialog.getFileType()
        if importMoleculeDialog.proceed():
            try:
                #print importMoleculeDialog.getMoleculeFile()
                self.history.currentState().getMixture().load(None,None,importMoleculeDialog.getMoleculeFile(),importMoleculeDialog.getFileType(),importMoleculeDialog.inputName())
            except Exception, err:
            	#print "Load on_connectDataBaseButton_pressed: There is a problem with the file ", importMoleculeDialog.getMoleculeFile()
                QtGui.QMessageBox.warning(self,"Error 15 !!!","There is a problem with the file."+ err)
            
            self.loadTable.clear()
            self.loadTableRows = 0
            self.mixAndRows    = []
            self.setTable()
        
            if self.uiLoad.SelectAllLayout.isEmpty() and self.uiLoad.ShowAllLayout.isEmpty():
                self.addSelectAllCheckBox()
                self.addShowHideAllCheckBox()
            
            self.previewArea.setMixture(self.history.currentState().getMixture())    

    def on_cancelButton_pressed(self):
        #print "Load: Cancel Button: history",self.history.currentState()
        self.close()

    def on_loadButton_pressed(self,dropedPdb=None):
    	print "Load on_loadButton_pressed",dropedPdb
        if dropedPdb == None:
            print "Load on_loadButton_pressed getLineEditInfo"
            self.getLineEditInfo()           
        print "Load on_loadButton_pressed loadTable.clear"
        self.loadTable.clear()
        self.loadTableRows = 0
        self.mixAndRows    = []
        print "Load on_loadButton_pressed setTable"
        self.setTable()
    
        if self.uiLoad.SelectAllLayout.isEmpty():
            self.addSelectAllCheckBox()
            self.addShowHideAllCheckBox()
        print "Load on_loadButton_pressed previewArea.setMixture"
        self.previewArea.setMixture(self.history.currentState().getMixture())    
        print "Load on_loadButton_pressed end"

    def on_okButton_pressed(self):
        if self.myMixture._len() == 0:
            msg = QtGui.QMessageBox.warning(self, 'Warning',
            'No molecule has been loaded!',QtGui.QMessageBox.Ok)
                
        else:
            progressMax   = self.myMixture._len()
            progressCount = 0
            progress      = QtGui.QProgressDialog("Loading mixture...", "Abort", 0, progressMax, self,QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
            progress.setWindowModality(QtCore.Qt.WindowModal)        
               
            for row in range(0,self.myMixture._len()):
                if progress.wasCanceled():
                    progress.hide()
                    self.history.currentState().reset()  
                    self.myMixture      = self.history.currentState().getMixture()           
                    self.update()
                    self.close()
                    return
                else:
                    #Delete unchecked molecules 
                    if (self.loadTable.cellWidget(row,0).checkState()) == QtCore.Qt.Unchecked: 
                        self.myMixture.remove(str(self.loadTable.item(row,5).text()))
                    #Add remaining molecules to the state
                progressCount += 1
                progress.setValue(progressCount)  
            self.isAdded = True
            self.close()

    def closeEvent(self, e):
        if not self.isAdded:
            self.myMixture = Mixture()

                            
    def getMixture(self):  return self.myMixture

#------------- Table's signals ---------
    def on_tableWidget_itemChanged(self, wi):
        
        if isinstance(wi, myTableWidgetItem) and wi.name != "(no name)" and wi.isSelected():
            self.loadTable.setItemSelected (wi, False)
            multipleMolecules = False
            
            for row in range(0,self.loadTable.rowCount()):
                if not(self.loadTable.currentRow() == row) \
                and self.loadTable.item(self.loadTable.currentRow(),2).backgroundColor() == self.loadTable.item(row,2).backgroundColor():
                    multipleMolecules = True
                    break
            if multipleMolecules and self.changeNameOrNotMessage():
                # changes names of all isomorphic molecules
                selColor = wi.backgroundColor()
                for eqClass in range(0,len(self.equalMolecules)):
                    if selColor == self.equalMolecules[eqClass][1]:
                        for mol in self.equalMolecules[eqClass][0]:
                            self.myMixture.getMolecule(mol)._name = str(wi.text())
                self.setTable()                                    
            else:
                mol = self.myMixture.getMolecule(wi.name)
                mol._name = str(wi.text())

    #--------------------------------------
    #on_viewToolButton_clicked(): When a viewToolButton is clicked, the user can show/hide all the molecules painted with the same color  
    def on_viewToolButton_clicked(self):
        #print "_mySignal"
        value = self.viewToolButton.show
        #print "@WWidget _mySignal value",value
        multipleMolecules = False
        #print "self.loaded.rowCount()",self.loadTable.rowCount()
        for row in range(0,self.loadTable.rowCount()):
            if not(self.viewToolButton.row == row) and self.loadTable.item(self.viewToolButton.row,2).backgroundColor() == self.loadTable.item(row,2).backgroundColor():
                multipleMolecules = True
                #print "multipleMolecules = True"
                break
        
        if isinstance(self, PreviewButton) and multipleMolecules and self.showHideAllMessage() :
            selColor = self.loadTable.item(self.viewToolButton.row,2).backgroundColor()

            for row in range(0,self.loadTable.rowCount()):
                if selColor == self.loadTable.item(row,2).backgroundColor():
                    if value == True:
                        self.loadTable.cellWidget(row,1).setShown()
                    else:
                        self.loadTable.cellWidget(row,1).setHidden()
                        self.loadTable.showAll = False
                        self.loadTable.showHideAllCheckBox.setCheckState(QtCore.Qt.Unchecked)
                        
        else:
            if value == False: 
                self.loadTable.showAll = False
                self.loadTable.showHideAllCheckBox.setCheckState(QtCore.Qt.Unchecked)
#-------------------------------------------
#createColors(): Creates QtColors

def createColors():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    alpha = random.randint(0, 255)
    qcolor = QtGui.QColor()
    qcolor.setRgb(r, g, b, alpha)
    return     qcolor

#=====================================================================
class myTableWidgetItem(QtGui.QTableWidgetItem):
    def __init__(self, loader,content, name="(no name)"):
        super(myTableWidgetItem,self).__init__(content)
        self.loader = loader
        self.name = name

    def  sizeHint (self):
        return QtCore.QSize(len(self.name), -1)

    
    

#=====================================================================
class CheckBox(QtGui.QCheckBox):
    def __init__(self,loaded, r, parent=None):
        super(CheckBox, self).__init__(parent)
        self.row = r
        self.loaded = loaded
        
        if parent == self.loaded.loadTable:
            QtCore.QObject.connect(self, QtCore.SIGNAL("clicked(bool)"), self._mySignal)

    #***************************** Methods ************************************
    
    #--------------------------------------
    #selectAllMessage(): Asks the user if wants to select/deselect all the molecules painted with the same color  

    def selectAllMessage(self):

            msg = QtGui.QMessageBox.question(self, 'Select...',
            'Would you like to select/deselect all the molecules with that color?', 
            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
       
   
            return msg == QtGui.QMessageBox.Yes 
 
    #--------------------------------------
    #_mySignal(): When a CheckBoxState is changed, the user can select/deselect all the molecules painted with the same color  
    def _mySignal(self, value):
        #print "@Load _mySignal",value
        multipleMolecules = False
        
        for row in range(0,self.loaded.loadTable.rowCount()):
            if not(self.row == row) and self.loaded.loadTable.item(self.row,2).backgroundColor() == self.loaded.loadTable.item(row,2).backgroundColor():
                multipleMolecules = True
                break
        
        if isinstance(self, CheckBox) and multipleMolecules and self.selectAllMessage() :
            selColor = self.loaded.loadTable.item(self.row,2).backgroundColor()

            for row in range(0,self.loaded.loadTable.rowCount()):
                if selColor == self.loaded.loadTable.item(row,2).backgroundColor():
                    if value == True:
                        self.loaded.loadTable.cellWidget(row,0).setCheckState(QtCore.Qt.Checked)
                    else:
                        self.loaded.loadTable.cellWidget(row,0).setCheckState(QtCore.Qt.Unchecked)
                        self.loaded.deSelectAll = False
                        self.loaded.selectAllCheckBox.setCheckState(QtCore.Qt.Unchecked)
                        
        else:
            if value == False: 
                self.loaded.deSelectAll = False
                self.loaded.selectAllCheckBox.setCheckState(QtCore.Qt.Unchecked)
                
                
                                
            
#=====================================================================
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    load_gui = Load()
    load_gui.show()
    sys.exit(app.exec_())
