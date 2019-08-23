# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#   ConnectioDialog.py
#  Version 0.1, October, 2013
#
#  Set default settings.
#
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

from PyQt4 import QtGui
from interface.main.ui_ConnectionDialog import Ui_ConnectionDialog
from lib.communication.RemoteHost import *
import time

class ConnectionDialog(QtGui.QDialog):
	def __init__(self, parent, connection=None, logWidget=None):
	
		super(ConnectionDialog, self).__init__(parent, modal = 1)
		
		self.log               = logWidget
		self.connection        = connection
		self.ui                = Ui_ConnectionDialog()
		self.ui.setupUi        (self)
		self.ui.okButton.setIcon(QtGui.QIcon().fromTheme("network-wireless"	))
		self.ui.okButton.setEnabled(False)
		self.ui.processorsBox.setEnabled(False)
		self.ui.gpusBox.setEnabled(False)
		self.ui.cancelButton.setFlat(False)
		self.ui.cancelButton.setIcon(QtGui.QIcon().fromTheme("computer"	))
		
		if self.connection != None:
			self.ui.hostnameEdit.setText(self.connection.getHostName())
			self.ui.usernameEdit.setText(self.connection.getUserName())
			self.ui.passwordEdit.setText("***")
	    
	def on_hostnameEdit_textChanged(self,t):
		self.ui.okButton.setEnabled(False)
		
	def on_usernameEdit_textChanged(self,t):
		self.ui.okButton.setEnabled(False)
		
	def on_passwordEdit_textChanged(self,t):
		self.ui.okButton.setEnabled(False)
		
	def on_probeButton_pressed(self):		
		time.sleep(1)
		try:
			if self.connection == None:
			    self.connection = RemoteHost(str(self.ui.hostnameEdit.text()), 
			                                str(self.ui.usernameEdit.text()), 
			                                password=str(self.ui.passwordEdit.text()),
			                                workingDir="home_inv/",
			                                logArea=self.log)
			else:
				self.ui.statusLabel.setText("Connecting to remote host...")
				self.ui.namdLabel.setText("Connecting to remote host...")
				self.ui.probeButton.setEnabled(False)
				self.connection.setUserName(str(self.ui.usernameEdit.text()))
				self.connection.setHostName(str(self.ui.hostnameEdit.text()))
				#self.connection.setPassword(str(self.ui.passwordEdit.text()))
				self.connection.probe()
				
		except Exception as e:
		    self.ui.statusLabel.setText("Connection failed."+str(e))
		    self.ui.okButton.setEnabled(False)
		    self.connection = None
		    print("on_probeButton_pressed exception", e)
		    return
		
		if self.connection.isConnected():
			self.ui.statusLabel.setText("Connection confirmed.")
			self.ui.okButton.   setEnabled (True)
			self.ui.okButton.   setFlat    (False)
			self.ui.okButton.   setDefault (True)
			self.ui.probeButton.setEnabled (True)
			self.ui.probeButton.setDefault (False)
		else:
			self.ui.statusLabel.setText("Connection could not be established.")
			self.ui.okButton.setEnabled(False)
			self.ui.cancelButton.setDefault (True)
			self.ui.probeButton.setEnabled (True)
			return
		   
		self.ui.processorsBox.setEnabled(True)
		self.ui.processorsBox.setMaximum(self.connection.getMaxProcessors())
		self.ui.processorsBox.setValue(self.connection.getChosenProcessors())
		self.ui.gpusBox.setEnabled(True)
		self.ui.gpusBox.setMaximum(self.connection.getMaxGpus())
		self.ui.gpusBox.setValue(self.connection.getChosenGpus())
		self.ui.namdLabel.setText(str(len(self.connection.getMDSUsers())) + " users: " + str(self.connection.getMDSUsers()))
		   
	    
	def on_cancelButton_pressed(self):
	    self.connection = None
	    self.close()
	
	
	def on_okButton_pressed(self):
		self.connection.setChosenProcessors(self.ui.processorsBox.value())
		self.connection.setChosenGpus(self.ui.gpusBox.value())
		self.close()
	
	
	    
	    
        