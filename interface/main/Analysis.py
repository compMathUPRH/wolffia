#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 
    #Melissa  López Serrano, Carlos J.  Cortés Martínez, Frances  Martínez Miranda, 
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

import sys,os
import logging

from PyQt4			import QtCore, QtGui, uic, Qt
#from pyf.manager.network	import Network
wolfiadir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(wolfiadir+'/../../')
from ui_Analysis import Ui_Analysis
from lib.fbp.Network import Network, NetworkThread
from multiprocessing import Queue

class TextField(QtGui.QTextEdit):

	def __init__(self, title, parent):

		super(TextField, self).__init__(title, parent)
		#print "Abre pantalla"
		
		self.setAcceptDrops(True)
		self.setWordWrapMode(QtGui.QTextOption.NoWrap)
		self.setFontFamily("Courier")

#-----------------------------------------------------

	def dragEnterEvent(self, e):
		print("PRIMERdrag")
		dropUrl = e.mimeData().urls()[0]
		if not dropUrl.isLocalFile():
			return 

		if e.mimeData().hasFormat('text/plain'):
			print("mimeData.hasFormat (text Plain)")
			fileName    = str(dropUrl.toLocalFile())
			extension   = os.path.splitext(fileName)
			print("filename:" + fileName)
			print("extension:" + str(extension[1]))
				
			e.accept()
			print("aceptado")
			print("PRIMERif")

	def dropEvent(self, e):
		text = open(str(e.mimeData().urls()[0].toLocalFile())).read()
		print("PRIMERdrop")
		
		self.setText(text)

class RunScriptThread(QtCore.QThread):
	consoleConnection = QtCore.pyqtSignal(str)
	updateConnection  = QtCore.pyqtSignal()
	def __init__(self, parent, script, state, console):
		QtCore.QThread.__init__(self)
		self.script = script
		self.console = console
		self.state = state
	
	def run(self):
		state = self.state
		exec( str(self.script.toPlainText()))


class Analysis(QtGui.QFrame):

	def __init__(self, hist, parent=None, previewer=None, settings=None ):
		super(Analysis, self).__init__(parent)

		self.ui = Ui_Analysis()
		self.ui.setupUi(self)

#		print "Dialog(", self.ui.__dict__.keys()
#		self.setAcceptDrops(True)
		
		#self.FBP1 = Analysis("test", self.ui.layoutWidget2)
		#self.ui.Network.removeWidget(self.textEdit)
		#self.textEdit.setObjectName("textEdit")
		#self.ui.Network.addWidget(self.FBP1)

		self.network = TextField("", self.ui.scriptWidget)
		self.ui.scriptLayout.addWidget(self.network)
		
		self.components = TextField("", self.ui.consoleWidget)
		self.ui.consoleLayout.addWidget(self.components)
		
		#print "Abre pantalla"
		self.history		= hist
		self.wolffia		= parent
		self.buildPreview	= previewer
		self.settings		= settings
		self.analysisClass  = None
		self.currentDir     = self.history.currentState().getBuildDirectory()
		
		self.stateQueue = Queue()
		#self.netwokRunner = Network(self.stateQueue)
		#self.netwokThread = NetworkThread(self.netwokRunner)

	
		#self.setAcceptDrops(True)
		#self.setWordWrapMode(QtGui.QTextOption.NoWrap)
		#self.setFontFamily("Courier")

#-----------------------------------------------------

	'''
	def dragEnterEvent(self, e):
		print "PRIMERdrag"
		dropUrl = e.mimeData().urls()[0]
		if not dropUrl.isLocalFile():
			return 

		if e.mimeData().hasFormat('text/plain'):
			print "mimeData.hasFormat (text Plain)"
			fileName    = str(dropUrl.toLocalFile())
			extension   = os.path.splitext(fileName)
			print "filename:" + fileName
			print "extension:" + str(extension[1])
				
			e.accept()
			print "aceptado"
			print "PRIMERif"

	def dropEvent(self, e):
		text = open(str(e.mimeData().urls()[0].toLocalFile())).read()
		print "PRIMERdrop"
		
		self.network.setText(text)
	'''

	def networkGraph(self):
		import networkx as nx
		self.netwokRunner.setAdjacenciesTable(self.network.toPlainText())
		#print "networkGraph ", self.network.toPlainText()
		table = self.netwokRunner.getAdjacenciesTable()
		#nodes = []
		edges = []
		#lines = str(network).split("\n")
		i = 1
		for proc in table:
			#nodes.append(name + ":" + function)
			edges += [(a,proc) for a in table[proc]]
			i += 1
	
		graph = nx.MultiDiGraph()
		#graph.add_nodes_from(nodes)
		graph.add_edges_from(edges)
		diagram = nx.to_agraph(graph)
		diagram.layout('dot')
		#diagram.graph_attr.update(rankdir='LR')
		diagram.draw("/tmp/g.png")
		return diagram.draw(format='png')

	def on_processNetworkButton_pressed(self):
		KeepAspectRatio = 1
		self.networkGraph()
		netPixmap = QtGui.QPixmap(QtCore.QString.fromUtf8("/tmp/g.png")).scaledToHeight(self.ui.graphicsView.height())
		self.ui.graphicsView.setPixmap(netPixmap)
		#.scaled(self.ui.graphicsView.size(), KeepAspectRatio)
		
	def on_loadButton_pressed(self):
		scriptFile = QtGui.QFileDialog.getOpenFileName(self, "Load a script file", self.currentDir, "Python script (*.py)")
		self.currentDir =  QtCore.QFileInfo(scriptFile).absolutePath()
		self.ui.scriptFileName.setText(scriptFile)
		self.network.setText(open(self.ui.scriptFileName.text(),"r").read())
	
	def on_reloadButton_pressed(self):
		self.network.setText(open(self.ui.scriptFileName.text(),"r").read())
		
	def on_runButton_pressed(self):
		
		#print "on_runButton_pressed", str(self.components.toPlainText() + self.networkCode(self.network.toPlainText()))
		#self.netwokRunner.setComponents(self.components.toPlainText())
		#self.netwokRunner.run()
		self.history.push()
		self.components.clear()
		
		#prepare local variables
		state = self.history.currentState()
		
		
		# redirect stdout, execute, display result and restore stdout
		from io import StringIO
		old_stdout = sys.stdout
		redirected_output = sys.stdout = StringIO()
		thr = RunScriptThread(self,self.network,state, self.components)
		thr.finished.connect(self.update)
		thr.finished.connect(self.buildPreview.update)
		thr.consoleConnection.connect(self.writeConsole)
		thr.updateConnection.connect(self.update)
		thr.updateConnection.connect(self.buildPreview.update)
		thr.start()
		sys.stdout = old_stdout
		self.components.setText(redirected_output.getvalue())
		
		#self.update()
		#self.buildPreview.update()
		pass
		
	def writeConsole(self,m):
		self.components.append(m)
		
		
	def exit(self):
		pass

	def update(self):
		print("Analysis.update")
		if self.analysisClass != None:
			self.analysisClass.update()
		#from lib.fbp.Network import removeEdgesAndRestart
		#self.netwokThread = NetworkThread(self.history.getCurrentState(), self.wolffia)
		#self.netwokThread.start()
		
		'''
		removeEdgesAndRestart(self.history.getCurrentState(), self.wolffia,self.history.getCurrentState().shownMolecules)
		print "Analysis.update received ", len(self.history.getCurrentState().getMixture().molecules()), " molecules"
		self.history.getCurrentState().shownMolecules.addMolecules(self.history.currentState().getMixture())
		self.wolffia.buildTab.update()
		self.wolffia.previewer.update()
		'''
			
	def reset(self): 
		self.ui.scriptFileName.clear()
		self.components.clear()
		self.network.clear()
		self.update()
		self.buildPreview.update()
		

#def main():
#	app = QtGui.QApplication([])
#	myDialog = Ui_Dialog()
#	myDialog.setupUi(Dialog)
#	myDialog.show()
#	ex = Dialog()
#	ex.show() #--------------- muestra pantalla
#	app.exec_() #-------------ejecuta 


#if __name__ == '__main__':
#	main()
