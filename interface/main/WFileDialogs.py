# -*- coding: utf-8 -*-
'''
Created on Mar 13, 2012

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
from PyQt5 import QtGui, QtCore, QtWidgets


#class WDirectoryDialog(QtGui.QFileDialog):
class WDirectoryDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None, caption ='Specify Directory', directory = None):
        #QtGui.QFileDialog.__init__(self,parent, caption, directory)
        QtWidgets.QFileDialog.__init__(self,parent, caption, directory)
        #print "WDirectoryDialog", directory
        #self.setFileMode(QtGui.QFileDialog.Directory)
        self.setFileMode(QtWidgets.QFileDialog.Directory)
        #self.setOption(QtGui.QFileDialog.ShowDirsOnly,True)
        self.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        self.setFilter(QtCore.QDir.Hidden | QtCore.QDir.AllDirs)
        self.show()
        self.response = self.exec_()

    def accepted(self): return self.response == QtWidgets.QDialog.Accepted
        
    def path(self):
        return self.directory().absolutePath()


#class WFileDialog(QtGui.QFileDialog):
class WFileDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None, caption ='Specify File', directory = None, filter = ""):
        QtWidgets.QFileDialog.__init__(self,parent, caption, directory, filter)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.show()
        self.response = self.exec_()
    
    def fullFilename(self):
        return self.selectedFiles()[0]

    def accepted(self): return self.response == QtWidgets.QDialog.Accepted

#class WFilesDialog(QtGui.QFileDialog):
class WFilesDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None, caption ='Specify Files', directory = None, filter = ""):
        QtWidgets.QFileDialog.__init__(self,parent, caption, directory, filter)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.show()
        self.response = self.exec_()
    
    def fullFilename(self):
        return self.selectedFiles()
    
    def accepted(self): return self.response == QtWidgets.QDialog.Accepted

#class WFileNameDialog(QtGui.QFileDialog):
class WFileNameDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None, caption ='Specify File', directory = None, filter = ""):
        QtWidgets.QFileDialog.__init__(self,parent, caption, directory, filter)
        self.setModal(True)
        self.setFileMode(QtWidgets.QFileDialog.AnyFile)
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        self.show()
        self.exec_()

        self.ans = True
        if self.result() == QtWidgets.QDialog.Rejected:
            self.setReady(False)			
    
    def fullFilename(self):
        return str(self.selectedFiles()[0])

    def path(self):
        return str(self.directory().absolutePath())

    def mixname(self):
        return str(self.fullFilename()[self.fullFilename().rfind('/')+1:])

    def setReady(self, flag): 
        self.ans = flag

    def isReady(self):
        return self.ans


