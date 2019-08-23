# -*- coding: utf-8 -*-
'''
Created on Jul 15, 2012

@author: jse
'''
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

from PyQt4 import QtGui, QtCore
from ui_CHARMMParameterFinderDialog import Ui_CHARMMParameterFinderDialog
from lib.chemicalGraph.molecule.Molecule import Molecule
import threading, time

class CHARMMParameterFinderDialog(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent, molecule=None):
        '''
        Constructor
        '''
        super(CHARMMParameterFinderDialog, self).__init__(parent, modal = 1)
        self.ui                = Ui_CHARMMParameterFinderDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.forceField = None
        self.pairing = None
        self.thread = None
        self.molecule = Molecule(molecule.molname(), molecule)
        self.originalMolecule = molecule
        self.ui.timeLeftClock.setValue(self.ui.timeLimitSlider.value())
        
        self.timer           =   QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.on_timer)
        
        self.ui.acceptButton.setEnabled(False)
        self.ui.reportTextEdit.setReadOnly(True)
        self.ui.startButton.setEnabled(False)

        
    def getForceField(self): return self.forceField
    
    def getPairing(self): return self.pairing

    def on_timeLimitSlider_valueChanged(self,pos):
        self.ui.timeLeftClock.setValue(pos)
        self.ui.timeLimitSlider.setToolTip (str(pos))
        cursorPos = self.mapToParent (self.ui.timeLimitSlider.pos()) + QtCore.QPoint(pos,15)
        QtGui.QToolTip.showText (cursorPos, \
                                 str(pos), self.ui.timeLimitSlider)

    def on_collectionsListWidget_itemClicked(self, qlwi):
        itemActive = False
        for i in range(self.ui.collectionsListWidget.count()):
            item = self.ui.collectionsListWidget.item(i)
            itemActive = itemActive or self.ui.collectionsListWidget.isItemSelected (item)
        self.ui.startButton.setEnabled(itemActive)
        
    def on_startButton_released(self):
        #print "on_startButton_pressed ", self.ui.timeLimitSlider.value()
        if self.thread != None and self.thread.is_alive():
            self.ui.reportTextEdit.appendPlainText ("Please wait...")
        elif self.molecule != None:
            selections = list()
            for i in range(self.ui.collectionsListWidget.count()):
                item = self.ui.collectionsListWidget.item(i)
                if self.ui.collectionsListWidget.isItemSelected (item):
                    selections.append(str(item.text()))
            """
            self.pairing = self.molecule.guessForceField(self.ui.timeLimitSlider.value(), selections)
            """
            if len(selections) > 0:
                self.thread = CHARMMParameterFinderThread(self.molecule,self.ui.timeLimitSlider.value(), selections, includeHydrogens=self.ui.hydrogensCheckBox.isChecked())
                self.thread.start()
                self.startTime     = time.clock()
                self.timeLimit = self.ui.timeLimitSlider.value()
                
                self.timer.start(1000)
                #print "on_startButton_pressed timeLimit", self.timeLimit
                
                self.ui.reportTextEdit.clear()
                self.ui.reportTextEdit.appendPlainText ("Searching...")
                self.ui.acceptButton.setEnabled(False)
                self.ui.startButton.setText("Wait")
                

    def on_timer(self):
        if self.thread.is_alive():
            if self.thread.getPairing() != None:
                print("on_startButton_pressed matches", self.thread.getPairing().getMatches())
            #print "on_startButton_pressed  timer ", self.timeLimit - (time.clock() - self.startTime)
            self.ui.timeLeftClock.setValue(max(0,int(self.timeLimit - (time.clock() - self.startTime))))
            self.ui.timeLeftClock.step()
            self.ui.timeLeftClock.updateScale ()
        else:
            self.timer.stop()
            self.ui.timeLeftClock.setValue(0)
            self.ui.startButton.setText("Start")
            self.pairing = self.thread.getPairing()
            self.ui.reportTextEdit.clear()
            if self.pairing == None:
                self.ui.reportTextEdit.appendPlainText ("No match found")
                self.ui.acceptButton.setEnabled(False)
            else:
                #print "on_startButton_pressed result", self.pairing.getMatches()
                self.ui.reportTextEdit.appendPlainText ( \
                        "Matches found: %d\nMinimum Potential: %f\nSelected Matches: %s" \
                        % (self.pairing.getMatches(), self.pairing.minPot, self.pairing.getPairing()))
                self.ui.acceptButton.setEnabled(True)

    def on_acceptButton_released(self):
        #if self.pairing.getForceField() != None:
            #print "on_acceptButton_released result", self.pairing.getForceField()._BONDS
            #self.originalMolecule.renameTypes(self.pairing.getPairing())
            #self.originalMolecule.getForceField().merge(self.forceField)
            #self.originalMolecule = self.molecule
        self.close()

    def on_rejectButton_released(self):
        self.forceField = None
        self.pairing = None
        self.close()

class CHARMMParameterFinderThread(threading.Thread):
    def __init__(self, molecule, timeLimit, FFSeletion, includeHydrogens=True):
        threading.Thread.__init__(self)
        self.molecule = molecule
        self.timeLimit = timeLimit
        self.FFSeletion = FFSeletion
        self.pairing = None
        self.includeHydrogens=includeHydrogens
        
    def run(self):
        self.pairing = self.molecule.guessForceField(self.timeLimit, self.FFSeletion, self.includeHydrogens)
    
    def getPairing(self):
        return self.pairing