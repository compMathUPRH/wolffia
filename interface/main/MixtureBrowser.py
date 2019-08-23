#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------
#  MixtureBrowser.py
#  Original version, June, 2012
#
#  Description: MixtureBrowser.py creates a QDialog to browse mixtures
#
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Carlos J.  Cortés Martínez,

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

from PyQt5 import QtCore, QtGui
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
#from conf.Wolffia_conf import NANOCAD_BASE #@UnresolvedImport
from .MixtureViewer import MixtureViewer
from lib.chemicalGraph.Mixture import Mixture
from ui_MixtureBrowser import Ui_MixtureBrowser
from .WFileDialogs import WFileNameDialog
from conf.Wolffia_conf import WOLFFIA_GRAPHICS

class MixtureBrowser(QtGui.QDialog):
    '''
    Creates a dialog to browse the mixtures
    '''
    def __init__(self, settings, history, parent=None):
        '''
        constructor
        
        :param settings: Settings
        :param history: History
        :param parent: Wolffia, Main Window
        '''
        super(MixtureBrowser, self).__init__(parent,  modal = 1)
        
        #Dialog settings
        self.uiMixtureBrowser         = Ui_MixtureBrowser()
        self.uiMixtureBrowser.setupUi(self)
        self.settings = settings
        self.history = history
        self.wolffia = parent
                
        #self.uiMixtureBrowser.packButton.setIcon(QtGui.QIcon().fromTheme("package-x-generic"))
        self.uiMixtureBrowser.addMixtureButton.setIcon(QtGui.QIcon().fromTheme("list-add"))
        self.uiMixtureBrowser.deleteMixtureButton.setIcon(QtGui.QIcon().fromTheme("list-remove"))    

        #Viewer
        self.previewArea    = MixtureViewer(self.history)#, self, Mixture())
        #self.previewArea.setHighResolution(False)
        self.uiMixtureBrowser.moleculeViewerLayout.addWidget(self.previewArea)
        
        #Mixture
        self.mixtures           =   list()

        #Table Settings
        self.loadTable          =   self.uiMixtureBrowser.tableWidget
        self.loadTableRows      =   0
        self.equalMolecules     =   []
        self.saveCheckBox       =   None
        self.lastSelectedItem   =   None 
        self.lastSelectedItemText   =   None
        #saves the current mixture
        
        #self.wolffia.saveWolffiaState()
        
        self.setTable()


    def generateListOfMixtures(self):
        '''
        Generates the list of mixtures by going inside the working folder and looking inside all the directories
        for a .wfy file. If it finds the .wfy file, then it is considered a mixture.
        '''
        self.mixtures = []
        for x in os.listdir(self.settings.workingFolder):
            if os.path.isdir(self.settings.workingFolder + x):
                #Checks if the .wfy file is accessible and it's not a directory
                if os.access(self.settings.workingFolder + x + "/" + x + ".wfy", os.F_OK) and not os.path.isdir(self.settings.workingFolder + x + "/" + x + ".wfy"):
                    self.mixtures.append(x)

    def setTable(self):      
        '''
        Sets the table and fills it with all the currently available mixtures.
        '''
        #regenerating the list of mixtures
        self.generateListOfMixtures()
        
        self.loadTable.setColumnCount(1)
        self.loadTable.setRowCount(len(self.mixtures))
        
        item = QtGui.QTableWidgetItem()
        self.loadTable.setHorizontalHeaderItem(0, item)
        self.loadTable.horizontalHeaderItem(0).setText("Simulation Name")
        row = 0
        
        self.loadTable.blockSignals(True)

        for mixture in self.mixtures:
            
            newTableWidgetItem = QtGui.QTableWidgetItem(mixture,0)
            newTableWidgetItem.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
            self.loadTable.setItem(row,0,newTableWidgetItem)
            if mixture == self.settings.currentSimulationName():
                self.loadTable.setCurrentCell(row,0)
                newTableWidgetItem.setBackgroundColor(QtGui.QColor("blue"))
                self.lastSelectedItem = newTableWidgetItem            

            self.loadTable.resizeColumnToContents(0)

                
            row += 1

        self.loadTable.sortItems(0)
        self.loadTable.blockSignals(False)

    def on_cancelButton_pressed(self):
        '''
        Closes the window.
        '''
        self.close()

    def on_okButton_pressed(self):
        '''
        Button to confirm changing mixtures.
        Saves the old mixture and sets the last picked mixture as the new one.
        '''
        #Quick check that an item has been selected
        try:
            if self.lastSelectedItem != None:   newMixName = str(self.lastSelectedItem.text())
            else:   newMixName = self.settings.currentSimulationName()
        except RuntimeError:
            pass
        if newMixName == self.settings.currentSimulationName() or newMixName == "":
            self.close()
        else:
            self.settings.setMixtureLocation(newMixName)
            self.history.currentState().load(self.settings.workingFolder + newMixName + "/" + newMixName + ".wfy")

            self.setTable()
            self.wolffia.update()
            self.close()
    
    def isCurrentSelected(self):
        '''
        Checks if the selected mixture is the current mixture
        '''
        if self.lastSelectedItem.text() == self.settings.currentSimulationName():
            return True
        else:   return False
        
        
    def on_deleteMixtureButton_released(self):
        '''
        Deletes the last selected mixture. 
        Currently used Mixture cannot be deleted.
        '''
        index = self.loadTable.indexFromItem(self.lastSelectedItem)
        if self.isCurrentSelected() or self.lastSelectedItem.text() == "":
            info = QtGui.QErrorMessage(self)
            info.setModal(True) # blocks Wolffia
            info.showMessage("The current mixture cannot be deleted.")
        else:
			msg = "Are you sure you want to delete simulation " + self.lastSelectedItem.text() + "?"
			reply = QtGui.QMessageBox.question(self, 'Message', msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes:
			    import shutil
			    shutil.rmtree(self.settings.workingFolder + str(self.lastSelectedItem.text()))
			    self.mixtures.pop(index.row())
			    self.loadTable.removeRow(index.row())
			    self.setTable()
        
    def on_previewButton_pressed(self):
        '''
        Enables the possibility of previewing a mixture before choosing it by loading the mixture onto the viewer.
        '''
        from .History import History
        history = History(None, None, None, self.settings.workingFolder + str(self.lastSelectedItem.text()) + "/" + str(self.lastSelectedItem.text()) + ".wfy")
        #print "loaded mixture from", self.settings.workingFolder + str(self.lastSelectedItem.text()) + "/" + str(self.lastSelectedItem.text()) + ".wfy"
        #print "mixture being sent is: ", history.currentState().getMixture()
        
        #The only way I managed to make it work was by removing the old previewArea and replacing it with a new one that contains
        #what is to be previewed
        self.uiMixtureBrowser.moleculeViewerLayout.removeWidget(self.previewArea)
        self.previewArea = MixtureViewer(history, self) 
        self.uiMixtureBrowser.moleculeViewerLayout.addWidget(self.previewArea)
        
    def on_addMixtureButton_pressed(self):
        '''
        Creates a new, nameless mixture on the QWidgetTree.
        '''
        self.loadTable.blockSignals(True)
        newName, ok = QtGui.QInputDialog.getText(self, 'Renaming a mixture', 'Enter the new name for the mixture:')
        newName = str(newName).strip('\/\\')
        if ok and newName and not newName.isspace():
            for mixName in self.mixtures:
                if mixName == newName: 
                    QtGui.QMessageBox.information(self, "Error", "That mixture name already exists", QtGui.QMessageBox.Ok)
                    
        elif not ok:    return
        else:   
            QtGui.QMessageBox.information(self, "Error", "Bad mixture name", QtGui.QMessageBox.Ok)
            return
            
        from lib.chemicalGraph.Mixture import Mixture #@UnresolvedImport


        self.wolffia.setDefaultTabs()
        row = self.loadTable.rowCount()
        self.loadTable.setRowCount(row+1)
        self.loadTable.setItem(row, 0, QtGui.QTableWidgetItem())
        newTableWidgetItem = QtGui.QTableWidgetItem("")
        self.loadTable.setItem(row,0,newTableWidgetItem)
        newTableWidgetItem.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
        self.settings.setMixtureLocation(newName)
        #print newName
        self.history.currentState().setBuildDirectory(self.settings.currentMixtureLocation())
        self.wolffia.reset()
        newMix = Mixture(mixName = newName)

        for row in range(self.loadTable.rowCount()):
            self.loadTable.item(row,0).setBackgroundColor(QtGui.QColor("white"))
        
        self.lastSelectedItem = newTableWidgetItem
        newTableWidgetItem.setBackgroundColor(QtGui.QColor("blue"))
        self.history.currentState().updateMixture(newMix)
        self.history.currentState().setBuildDirectory(self.settings.currentMixtureLocation())
        self.history.currentState().save(self.settings.currentMixtureLocation() + newMix.mixName + ".wfy")
        self.wolffia.update()
        self.mixtures.append(newName)
        self.setTable()
        self.loadTable.blockSignals(False)
        
    
    def on_tableWidget_itemClicked(self, item):
        '''
        Sets this item as the lastSelected and turns it's background blue.
        :param item: The QTreeWidgetItem that was clicked
        '''
        self.loadTable.blockSignals(True)
        for row in range(self.loadTable.rowCount()):
            self.loadTable.item(row,0).setBackgroundColor(QtGui.QColor("white"))
        self.lastSelectedItem = item
        self.lastSelectedItemText = item.text()
        item.setBackgroundColor(QtGui.QColor("blue"))
        self.loadTable.blockSignals(False)

    def on_tableWidget_itemChanged(self, widEdit):
        '''
        
        :param widEdit: The QTreeWidgetItem who's text is being edited
        '''
        self.loadTable.blockSignals(True)
        mixSet = []
        name = str(widEdit.text()).strip("\/\\")
        print("on_tableWidget_itemChanged" ,self.lastSelectedItemText, name)

        if not name.isspace() and name:
            #print "on_tableWidget_itemChanged : got in, ", bool(name), bool (not name.isspace()), name
            if not os.path.isdir(self.settings.workingFolder + "/" + name):
                for mixture in range(0, self.loadTable.rowCount()):
                    mixSet.append(str(self.loadTable.item(mixture,0).text()))
                #print "on_tableWidget_itemChanged, " , set(mixSet), set(self.mixtures)
                if bool(set(mixSet) - set(self.mixtures)) :
                    #print "on_tableWidget_itemChanged, " , set(self.mixtures) - set(mixSet), set(mixSet) - set(self.mixtures), bool(set(mixSet) - set(self.mixtures))
                    mixture = list(set(self.mixtures) - set(mixSet))[0]
                    self.mixtures.pop(self.mixtures.index(mixture))
                    self.history.currentState().load(self.settings.workingFolder + mixture + "/" + mixture + ".wfy")
                    self.history.currentState().setBuildDirectory(self.settings.workingFolder + "/" + name )
                    self.history.currentState().setMixtureName(name)
                    self.mixtures.append(name)
                    #print "on_tableWidget_itemChanged", mixture, self.settings.currentSimulationName(), name
                    if mixture == self.settings.currentSimulationName():
                        self.settings.setCurrentMixture(name)
                        self.wolffia.update()
                    else:
                        self.history.currentState().save(self.settings.workingFolder + mixture + "/" + mixture + ".wfy")
                        self.history.currentState().load(self.settings.currentMixtureLocation()  + "/" + self.settings.currentSimulationName() + ".wfy" )
                    renamingDir = self.settings.workingFolder + mixture
                    for files in os.listdir(renamingDir):
                        os.rename(renamingDir + "/" + files, renamingDir + "/" + files.replace(mixture, name))
                    os.rename(self.settings.workingFolder + mixture, self.settings.workingFolder + name)
            else:
                widEdit.setText(self.lastSelectedItemText)
                self.loadTable.blockSignals(False)
                return
        
        else:
            widEdit.setText(self.lastSelectedItemText)
        self.loadTable.blockSignals(False)

                



#=====================================================================
if __name__ == '__main__':
        
    app = QtGui.QApplication(sys.argv)
    load_gui = MixtureBrowser()
    load_gui.show()
    sys.exit(app.exec_())
