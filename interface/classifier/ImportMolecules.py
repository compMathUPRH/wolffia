# -*- coding: utf-8 -*-
#-----------------------------------------------
#  ImportMolecules.py
#  Version 0.1, June, 2012
#
#  Description: ImportMolecules.py creates a QDialog to import molecules from the Protein Data Bank.
"""
    Copyright 2011, 2012: Melissa  López Serrano, 
    
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

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../conf')
from conf.Wolffia_conf import WOLFFIA_STYLESHEET

from ui_ImportMolecules import Ui_ImportMolecules

class ImportMolecules(QtGui.QDialog):
    #------------------------------ Constructor ------------------------------
    def __init__(self, parent=None):
            super(ImportMolecules, self).__init__(parent, modal = 1)

            self.uiImportMolecules = Ui_ImportMolecules()
            self.uiImportMolecules.setupUi(self)
            
            self.moleculeFile      = None
            self.fileType          = None
            self.proceedValue           = False
            try:
                self.setStyleSheet(open(WOLFFIA_STYLESHEET,'r').read())
            except:
                print("WARNING: Could not read style specifications")

    #--------------------------------- Methods ------------------------------------------
    
    #---------------------------------
    # inputName is a function that gets the input filename
    def inputName(self):

        if self.uiImportMolecules.IDlineEdit.text() == '': return None

        else: return str(self.uiImportMolecules.IDlineEdit.text())

    #---------------------------------
    # getPDB is a function that return the pdb
    def getMoleculeFile(self):
        return self.moleculeFile
    #---------------------------------
    # getPDB is a function that return the pdb
    def getFileType(self):
        return self.fileType
    def proceed(self):
        return self.proceedValue
    #------------------------------ Signals ------------------------------------------

    @QtCore.pyqtSlot()
    def on_ok_pressed(self):
        print("pdb Is checked?",self.uiImportMolecules.pdbRButton.isChecked())
        #Specifies the user that has to write a valid filename
        moleculeName = self.uiImportMolecules.IDlineEdit.text()
        fileCode = str(moleculeName.replace(' ','-'))
        if  fileCode == '':
            QtGui.QMessageBox.critical(self, 'Error','ERROR: Invalid entry!!')
        else:
            if self.uiImportMolecules.pdbRButton.isChecked():
                host          = "www.rcsb.org"
                url           = "/pdb/files/"
                ext           = ".pdb"
                self.fileType = "pdb"
            else:
                host          = "cactus.nci.nih.gov"
                url           =  "/chemical/structure/"    
                ext           =  "/sdf"    
                self.fileType = "sdf"
                
            import http.client
            print("on_ok_pressed", host+url+fileCode+ext)
            conn = http.client.HTTPSConnection(host,timeout=10)
            conn.request("GET", url+fileCode+ext)
            r1 = conn.getresponse()
            if r1.reason == 'OK':
                self.moleculeFile = r1.read()
                self.proceedValue = True
                self.close()
            else: 
                print("ERRORRR!!!!!")
                QtGui.QMessageBox.warning(self, 'Error '+str(r1.status), r1.reason)
                
            print(r1.status, r1.reason)
            conn.close()

                

    @QtCore.pyqtSlot()
    def on_cancel_pressed(self):
        self.proceedValue = False
        self.close()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    add_gui = ImportMolecules()
    add_gui.show()
    sys.exit(app.exec_())
