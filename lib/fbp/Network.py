

from PyQt4 import QtCore
import libraryComponents
import sys
from lib.fbp.libraryComponents import FBP_NO_WRAP_FUNCTIONS

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from interface.main.History import NanoCADState
from lib.io.dcd import DCDReader

#import matplotlib.pyplot as plt
import numpy
import time

def bondLengthsFromState(state):
	return  bondLengthsFromMixture(state.getMixture())
	
	
def bondLengthsFromMixture(mix):
	lengths = list()
	for molname in mix:
		mol = mix.getMolecule(molname)
		for (a1, a2) in mol.bonds():
			lengths.append(mol.getAtomAttributes(a1).distanceTo(mol.getAtomAttributes(a2)))

	print "RESULTADO DEL NETWORK ===========================" 
	print max(lengths)
	print "=================================================" 
	return lengths
	
	
def longBonds(mix):
	maxBondLength = 2.428683298
	longBonds     = dict()
	for molname in mix:
		mol = mix.getMolecule(molname)
		for (a1, a2) in mol.bonds():
			if mol.getAtomAttributes(a1).distanceTo(mol.getAtomAttributes(a2)) > maxBondLength:
				if not longBonds.has_key(molname): longBonds[molname] = list()
				longBonds[molname].append( (a1,a2) )
	return longBonds


def produceGraph(vals):
	import pylab
	bins = 50
	dmin, dmax = 1.0, 3.0
	barWidth = (dmax - dmin) / bins
	r = pylab.arange(dmin, dmax, (dmax-dmin)/bins)

	freqs, edges = numpy.histogram(vals, bins=bins, range=(dmin, dmax))

	pylab.clf()
	pylab.bar(r, freqs, barWidth, linewidth=1)
	pylab.xlabel(r"distance $r$ in $\AA$")
	pylab.ylabel(r"radial distribution function $g(r)$")
	pylab.savefig("/home/jse/Desktop/rdf.pdf")

def test():
	state = NanoCADState()
	state.load("/home/jse/inv/Simulaciones/CarbonActivado/diamondTest/diamondTest.wfy")
	mixture = state.getMixture()
	dcd = DCDReader("/home/jse/inv/Simulaciones/CarbonActivado/diamondTest/diamondTest.dcd")
	
	for X,Y,Z in dcd:
		print "DCDLoader updating frame"
		mixture.updateCoordinatesFromArray([item for tuples in zip(X,Y,Z) for item in tuples])
		produceGraph(  bondLengthsFromMixture(mixture)  )
		time.sleep(2)
	

def bondHistogramComponent(state):
	mixture = state.getMixture()
	produceGraph(  bondLengthsFromMixture(mixture)  )

def removeEdgesAndRestart(state, wolffia,shownMolecules):
	mix = state.getMixture()
	molBonds = longBonds(mix)
	print "removeEdgesAndRestart rompera enlaces en ", len(molBonds), " moleculas"
	if len(molBonds) > 0:
		wolffia.simTab.on_cancelButton_pressed()
		#while wolffia.simRunning == True:
			#print "removeEdgesAndRestart esperando por namd ... "
			#wolffia.simTab.on_cancelButton_pressed()
			#time.sleep(1)
		for mol in molBonds:
			print "removeEdgesAndRestart rompiendo ", len(molBonds[mol]) , "enlaces ", molBonds[mol], " en ", mol
			state.getMixture().removeBonds(mol,molBonds[mol],shownMolecules)
		wolffia.simTab.on_runButton_pressed()
	
	
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#------------------------------------------------------
def addInOutWrapperToFunction(procName):
	return 	"\ndef " + procName + "WRAPPER(inQ, outQ):\n" + \
		"\timport sys\n\tsys.path.append(\"/tmp\")\n" + \
		"\tfrom lib.fbp.libraryComponents import *\n" + \
		"\tfrom customComponents import *\n" + \
		"\tinItem = inQ.get()\n" + \
		"\twhile inItem != FBP_CONSTANTS.END_TOKEN:\n" + \
		"\t\tprint \"" + procName + " recibio\"\n" + \
		"\t\t#outQ.put([" + procName + "(*inItem)])\n" + \
		"\t\tfor resultado in " + procName + "(*inItem):\n" + \
		"\t\t\toutQ.put([resultado])\n" + \
		"\t\tinItem = inQ.get()\n" + \
		"\tprint \"" + procName + " termino\"\n" + \
		"\toutQ.put(FBP_CONSTANTS.END_TOKEN)\n"   + \
		"\toutQ.close()\n"

#------------------------------------------------------
def addInWrapperToFunction(procName):
	return 	"\ndef " + procName + "WRAPPER(inQ):\n" + \
		"\timport sys\n\tsys.path.append(\"/tmp\")\n" + \
		"\tfrom lib.fbp.libraryComponents import *\n" + \
		"\tfrom customComponents import *\n" + \
		"\tinItem = inQ.get()\n" + \
		"\twhile inItem != FBP_CONSTANTS.END_TOKEN:\n" + \
		"\t\tprint \"" + procName + " recibio\"\n" + \
		"\t\t" + procName + "(*inItem)\n" + \
		"\t\tinItem = inQ.get()\n" + \
		"\tprint \"" + procName + " termino\"\n"

#------------------------------------------------------
def addOutWrapperToFunction(procName):
	return 	"\ndef " + procName + "WRAPPER(outQ):\n" + \
		"\timport sys, time\n\tsys.path.append(\"/tmp\")\n" + \
		"\tfrom lib.fbp.libraryComponents import *\n" + \
		"\tfrom time import sleep\n" + \
		"\tfrom customComponents import *\n" + \
		"\tprint \"" + procName + " entro\"\n" + \
		"\t#outQ.put([" + procName + "()])\n" + \
		"\tfor resultado in " + procName + "():\n" + \
		"\t\t#while not outQ.empty(): sleep(1)\n" + \
		"\t\toutQ.put([resultado])\n" + \
		"\tprint \"" + procName + " termino\"\n" + \
		"\toutQ.put(FBP_CONSTANTS.END_TOKEN)\n"  + \
		"\toutQ.close()\n"

#------------------------------------------------------
'''
def storeComponents(code):
	f = open("customComponents.py","w")
	f.write(code)
	f.close()
'''


#------------------------------------------------------
class NetworkThread(QtCore.QThread):
	def __init__(self, state,wolffia):
		super(NetworkThread, self).__init__()
		self.state   = state
		self.wolffia = wolffia
		
	def run(self):
		removeEdgesAndRestart(self.state,self.wolffia)
		#bondHistogramComponent(self.state)
		
#------------------------------------------------------
class NetworkThread2(QtCore.QThread):
	def __init__(self, netObj):
		super(NetworkThread, self).__init__()
		netObj.moveToThread(self)
		self.started.connect(netObj.run)
		netObj.finishSignal.connect(self.quit)
		self.finished.connect(netObj.quit)

			
#------------------------------------------------------
class Network(QtCore.QObject):
	finishSignal = QtCore.pyqtSignal()
	def __init__(self, connectionQueue=None):
		super(Network, self).__init__()
		self.adjTable = dict()
		self.procNames = dict()
		self.components = None
		self.wolffiaStateQ = connectionQueue

	def setCode(self, code):
		self.code = str(code)

	def run(self):
		if self.components != None:
			# flush the input queue
			while not self.wolffiaStateQ.empty():
				self.wolffiaStateQ.get(True,1)
				
			print "Network run components ======================\n", self.components,"components end ======================\n"
			print "Network run wrapperFunctions ======================\n", self.wrapperFunctions(),"wrapperFunctions end ======================\n"
			print "Network run networkCode ======================\n", self.networkCode(),"networkCode end ======================\n"


			#exec self.components + self.networkCode()
			self.storeComponents()
			exec self.wrapperFunctions()
			#from multiprocessing import Process, Queue
			#from lib.fbp.libraryComponents import *
			exec self.networkCode()
			print "Network run  Llego de exec"
			#runNetwork()
			#print "Network run  Llego de runNetwork"
			
			try:
				self.processes = lp
			except:
				self.processes = None
				
			# restore stdout and stderr
			#sys.stdout = sys.__stdout__
			#sys.stderr = sys.__stderr__
			
	@QtCore.pyqtSlot()
	def quit(self):
		self.wolffiaStateQ.put(libraryComponents.FBP_CONSTANTS.END_TOKEN)
		if self.processes != None:
			print "Network.quit() terminating ", len(self.processes), " processes."
			for p in self.processes: 
				print "Network.quit() terminating process ", p.pid
				p.terminate()
		else:
			print "Network.quit() no process to terminate"
			
		super(Network, self).quit()
		
	def setAdjacenciesTable(self,network):
		#print "\n\nadjacenciesTable network ", network
		self.adjTable = dict()
		self.procNames = dict()
		lines = str(network).split("\n")
		i = 1
		#print "\n\nadjacenciesTable lines ", lines
		for line in lines:
			if not (line.isspace() or line == ''):
				#print "networkCode", line
				try:
					node, adj = line.split(":")
					name, function = node.split(",")
					adjacencies = adj.split(',')
					if adjacencies != ['']:
						self.adjTable[name] = [a.strip(' ') for a in adjacencies]
					self.procNames[name] = function
				except:
					print "Warning: line " + str(i) + " of the network could not be understood in adjacenciesTable."
					print sys.exc_info()[0]
			i += 1
		#print "\n\nadjacenciesTable table ", table
		self.procNames["wolffiaState"] = "wolffiaState"
		return [self.adjTable,self.procNames]
	
	def getAdjacenciesTable(self):
		return self.adjTable
	
	def setComponents(self, compText):
		self.components = str(compText)
#------------------------------------------------------

#------------------------------------------------------
	def storeComponents(self):
		f = open("/tmp/customComponents.py","w")
		f.write(self.components)
		f.close()


	def adjacenciesTable(self,network):
		print "\n\nadjacenciesTable network ", network
		table = dict()
		procNames = dict()
		lines = str(network).split("\n")
		i = 1
		print "\n\nadjacenciesTable lines ", lines
		for line in lines:
			if not (line.isspace() or line == ''):
				print "networkCode", line
				try:
					node, adj = line.split(":")
					name, function = node.split(",")
					adjacencies = adj.split(',')
					if adjacencies != ['']:
						table[name] = [a.strip(' ') for a in adjacencies]
					procNames[name] = function
				except:
					print "Warning: line " + str(i) + " of the network could not be understood in adjacenciesTable."
					print sys.exc_info()[0]
			i += 1
		#print "\n\nadjacenciesTable table ", table
		return [table,procNames]


	def wrapperFunctions(self):
		# add WRAPPERs
		invTable = self.__inverseAdjTable()
		allProc = set(self.adjTable.keys()).union(set(invTable.keys()))
		codeString = "# warapper functions generated by Network.wrapperFunctions()\n\n"
		for proc in allProc:
			codeString += "print \'Adding wrapper to " + str(proc)+"'"
			if proc in invTable and proc in self.adjTable:
				codeString += addInOutWrapperToFunction(self.procNames[proc])
			elif proc in self.adjTable:
				codeString += addInWrapperToFunction(self.procNames[proc])
			else:
				codeString += addOutWrapperToFunction(self.procNames[proc])
		return codeString
	
	
	def __inverseAdjTable(self):
		invTable = dict()
		for proc in self.adjTable:
			for next in self.adjTable[proc]:
				if next in invTable: invTable[next].append(proc)
				else: invTable[next] = [proc]
		return invTable


	def networkCode(self):
		print "# entro a networkCode" 
		table = self.adjTable
		procNames = self.procNames
		#print "networkCode table ", table
		#pass
		
		codeString = "END_TOKEN = \"FBP_END_TOKEN\"\n"

		invTable = self.__inverseAdjTable()
		allProc = set(table.keys()).union(set(invTable.keys()))

		codeString +=  "print 'importa multiprocessing'\n"
		codeString +=  "from multiprocessing import Process, Queue\n"
		codeString +=  "print 'importa libraryComponents'\n"
		codeString +=  "from lib.fbp.libraryComponents import *\n"

		codeString +=  "print 'crea colas'\n"
		codeString +=  "lq=[]\n"
		qc = 0
		arrows = dict()
		for p in table:
			for p2 in table[p]:
				arrows[(p,p2)] = qc
				qc += 1

		#print arrows

		codeString +=  "for i in range("+str(qc)+"): lq.append(Queue())\n"


		codeString +=  "lp = []\n"
		codeString +=  "print 'prepara'\n"
		for proc in allProc:
			codeString +=  "lp.append(Process(target=" + procNames[proc]
			if procNames[proc] in FBP_NO_WRAP_FUNCTIONS:   codeString += ", args=["
			else:                                          codeString += "WRAPPER, args=["

			#codeString +=  ","


			if proc in table:
				if len(table[proc]) > 1:
					codeString +=  "["
					for receiver in table[proc][:-1]:
						codeString +=  "lq[" + str(arrows[(proc,receiver)]) + "],"
					codeString +=  "lq[" + str(arrows[(proc,table[proc][-1])]) + "]]"
				elif len(table[proc]) == 1:
						codeString +=  "lq[" + str(arrows[(proc,table[proc][0])]) + "]"
			elif proc == "wolffiaState": 
					codeString +=  "self.wolffiaStateQ,"
			#else: codeString +=  "None"

			if proc in table and proc in invTable: codeString +=  ","

			if proc in invTable:
				if len(invTable[proc]) > 1:
					codeString +=  "["
					for sender in invTable[proc][:-1]:
						codeString +=  "lq[" + str(arrows[(sender,proc)]) + "],"
					codeString +=  "lq[" + str(arrows[(invTable[proc][-1],proc)]) + "]]"
				else: codeString +=  "lq[" + str(arrows[(invTable[proc][0],proc)]) + "]"
			#else: codeString +=  "None"

			codeString +=  "]))\n"
			codeString +=  "print 'ccc'\n"


		codeString +=  "for p in lp: p.start()\n"
		codeString +=  "#for p in lp: p.join()\n"

		#print codeString
		return codeString


	def exit(self):
		pass


#==========================================================================
if __name__ == '__main__':
	import sys
	net = Network()
	print "# Network file: ", sys.argv[1]
	net.setAdjacenciesTable(open(sys.argv[1], "r").read())
	print "# Components file: ", sys.argv[2]
	net.setComponents(open(sys.argv[2], "r").read())
	net.storeComponents()
	print net.wrapperFunctions()
	print net.networkCode()
	print "for p in lp: p.join()"
