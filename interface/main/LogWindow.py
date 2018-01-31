#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from conf.Wolffia_conf import WOLFFIA_GRAPHICS
from QClasses import *
from PyQt4.QtGui import QToolTip
from PyQt4.QtCore import QPoint
#from ui_LogWindow import Ui_LogWindow

class LogWindow():
	'''
	LogWindow
	'''
	LOGMODE = {"OFF":0, "INFO":1, "WARNING":2}
	
	def __init__(self, ui):
	    '''
	    Constructor
	    '''
	    self.button = ui.FeedbackTabs
	    self.tabIndex = ui.FeedbackTabs.indexOf(ui.logTab)
	    #self.ui_logs = Ui_LogWindow()
	    #self.ui_logs.setupUi(self)
	    self.messages = ui.messages
	    self.messages.setReadOnly(True)
	    self.reset()
	
	def reset(self):
	    self.setLogMode("OFF")
	    self.messages.clear()
	    self.firstMessage = True
	
	def setLogMode(self, logmode):
	    self.mode = logmode
	    if logmode == "OFF":
	        if self.button != None: self.button.setTabIcon(self.tabIndex, QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "logIcon-off.png"))
	    elif logmode == "WARNING":
	        if self.button != None: self.button.setTabIcon(self.tabIndex, QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "logIcon-warning.png"))
	        if self.firstMessage:
	            self.firstMessage = False
	            #mDialog = QtGui.QMessageBox(1, "ERROR", "ERRORS have been added to the log window.")
	            #mDialog.setIconPixmap(QtGui.QPixmap(str(WOLFFIA_GRAPHICS) + "logIcon-warning.png"))
	            #mDialog.exec_()
	
	            QToolTip.showText(self.button.parentWidget ().mapToGlobal(self.button.geometry().bottomLeft()) , "ERRORS have been added to the log window.",self.button)
	            #self.button.setToolTip("ERRORS have been added to the log window.")
	
	
	    elif self.mode != "WARNING":
	        self.mode == "INFO"
	        if self.button != None: self.button.setTabIcon(self.tabIndex, QtGui.QIcon(str(WOLFFIA_GRAPHICS) + "logIcon-info.png"))
	
	
	def addMessage(self, message, mtype=None):
		#print "LogWindow addMessage ",message
		self.messages.appendPlainText(message.rstrip('\n'))
		self.setLogMode(mtype)
	
	def write(self, message): self.addMessage(message)
	
	def clear(self):
	    self.reset()
        
    