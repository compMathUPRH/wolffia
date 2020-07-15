# -*- coding: utf-8 -*-
'''
Created on May 10, 2012

@author: jse
'''
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Carlos J.  Cortés Martínez, Giovanni Casanova

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
from multiprocessing import Queue

import threading, sys, os, time, tempfile
import select
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../')
from subprocess import signal, Popen, PIPE

from conf.Wolffia_conf import _WOLFFIA_OS
import wolffialib.communication.imd.imd as imd

class SimThread(threading.Thread):
	'''
	classdocs
	'''
	
	
	def __init__(self, conf, namdLocation=None, remoteHost=None, remoteLocation=None, useLogFile=False):
		'''
		Constructor
		'''
		threading.Thread.__init__(self)
		self.configuration = conf
		
		if remoteHost == None or remoteHost == 'localhost':
		    if _WOLFFIA_OS == "Windows":
		        self.pipe = Popen(str(namdLocation + " " + conf.getFilename()), stdout=PIPE, shell=True)
		        self.coordinateFileName = conf.getBuildDirectory() + "\\" + conf.getMixtureName() + ".coor"
		    else:
		    	if useLogFile:
		    		print "SimThread.__init__ executing \"", str(namdLocation + " " + conf.getFilename() + " > " + conf.getMixtureName() + ".log"
), "\""
		        	self.pipe = Popen(str(namdLocation + " " + conf.getFilename() + " > " + conf.getMixtureName() + ".log"
), stdout=PIPE, bufsize=0, shell=True , preexec_fn=os.setsid)
		        else:
		        	self.pipe = Popen(str(namdLocation + " " + conf.getFilename()), stdout=PIPE, bufsize=0, shell=True , preexec_fn=os.setsid)
		        self.coordinateFileName = conf.getBuildDirectory() + "/" + conf.getMixtureName() + ".coor"
		        self.cellFileName = conf.getBuildDirectory() + "/" + conf.getMixtureName() + ".xsc"
		else:
			#print "SimThread.__init__ executing remotely "
			self.remoteHost = remoteHost
			self.pipe = self.remoteHost.startSimulation(conf.getMixtureName(), useLogFile)
			#self.pipe = Popen(['/usr/bin/sshpass', '-p',  password, '/usr/bin/ssh' , '-T',  username + '@' +  remoteHost] + command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
			#self.pipe = self.connect(remoteHost, username, password, conf, processors, gpus, remoteLocation)
			self.cellFileName = conf.getMixtureName() + ".xsc"
		
		self.bufferAccess = threading.Semaphore()
		self.namdOutput    = list()
		self.cell          = NAMDcell(self.cellFileName, remoteHost)
		self.ready         = False
		self.modTime       = time.time()
		self.remoteHost    = remoteHost
	    
	    
	def cancel(self):
	    '''
	    Stop the simulation by killing the simulation process, stopping all 
	    the timers, killing the pipe(?) and stopping the simRun thread
	    
	    '''
	    print "SimThread cancel"
	    try: 
	        self.pipe.poll()
	    except AttributeError:
	        print "cancel: No pipe"   
	
	    try: 
	        os.killpg(self.pipe.pid,signal.SIGKILL)
	    except:
	        print "cancel: Nothing to kill"            

		threading.Thread.cancel(self)
	
	def coordinatesAreNew(self):
	    #print "coordinatesAreNew ", self.modTime
	    try:            
	        newModTime = (os.stat(self.coordinateFileName).st_mtime)                
	    except:
	        newModTime = self.modTime
	    
	    if self.modTime < newModTime:
	        self.modTime = newModTime
	        return True
	    return False
	
	def resume(self):
	    '''
	    Continues a simulation by signaling the process.
	    '''
	    if _WOLFFIA_OS == "Windows":
	        os.kill(self.pipe.pid,signal.CTRL_BREAK_EVENT) #@UndefinedVariable
	    else:    
	        os.killpg(self.pipe.pid,signal.SIGCONT)
	        
	    #self.wolffia.lightbulb('on')
	
	
	def pause(self):
	    '''
	    Pauses the simulation by signaling the process.
	    '''
	    if _WOLFFIA_OS == "Windows":
	        os.kill(self.pipe.pid,signal.CTRL_BREAK_EVENT) #@UndefinedVariable
	    else:    
	        os.killpg(self.pipe.pid,signal.SIGSTOP)
	
	        
	def getOutput(self):
	    """
	    Returns output from the simulation
	    """
	    if self.ready:
	    	#print "SimThread.getOutput pidiendo permiso"
	        self.bufferAccess.acquire()
	    	#print "SimThread.getOutput permiso concedido"
	        result = self.namdOutput
	        self.namdOutput = list()
	        self.ready = False
	        self.bufferAccess.release()
	        return result
	    return None
	
	
	def resetModifiationTime(self):
	    '''
	    Sets the modification time to current time.  Avoids loading coordinates from an old
	    run into a new one.
	    '''
	    self.modTime = time.time()
	
	
	def run(self):
		"""
		Runs the thread. Called by self.start.
		"""
		#print "SimThread.run corriendo ", self.getName()
		pipePoll = select.poll()
		pipePoll.register(self.pipe.stdout, select.POLLIN) 
		self.pipe.poll()
		while self.pipe.returncode == None:
			if pipePoll.poll(0):
			#if True:
				#print "SimThread.run leyendo"
				self.bufferAccess.acquire()
				#print "SimThread.run permiso concedido"
				#self.namdOutput += self.pipe.stdout.readlines(1)
				line = self.pipe.stdout.readline()
				if len(line) > 0:
					self.namdOutput.append(line)
					self.ready = True
					#print "SimThread.run lines received: ", len(self.namdOutput)
				self.bufferAccess.release()
			#print "SimThread.run self.pipe.returncode = ", self.pipe.returncode
			self.pipe.poll()
		self.resetModifiationTime()
		print "SimThread.run termino"
	
	
	def stop(self):
		#self.pipe.kill()
		self._Thread__stop()
	
	
	def updateCoordinates(self, mixture):
	    #print "SimThread updateCoordinates "
	    mixture.updateCoordinates(self.coordinateFileName)
	    	    
        
              
class ImdSimThread(SimThread):
	def __init__(self, conf, namdLocation=None, remoteHost=None, port=3000, remoteLocation=None, useLogFile=False):
		'''
		Constructor
		'''
		print "ImdSimThread __init__", namdLocation, remoteHost, port, remoteLocation
		super(ImdSimThread,self).__init__(conf, namdLocation, remoteHost, remoteLocation, useLogFile)
		if remoteHost == None:
			self.imdProc = imd.IMDThread(port=port)
		else:
			self.imdProc = imd.IMDThread(remoteHost=remoteHost.getHostName(), port=port)
	
	def cancel(self):
		'''
		Stops the simulation 
		'''
		print "ImdSimThread cancel"
		self.imdProc.cancel()
		super(ImdSimThread,self).cancel()
		
	def coordinatesAreNew(self):
	    return self.imdProc.coordinatesAreNew()
	
	def getCoordinates(self):
	    return self.imdProc.getCootdinates()
	
	def getCoordinatesQ(self):
		from collections import deque
		Q = self.imdProc.getCoordinatesQ()
		q = deque()
		while not Q.empty():
			frame = Q.get()
			#self.imdProc.getCoordinatesQ().get_nowait()
			q.append(frame.coordinates())
			Q.task_done()
			
		return q
	
	def getEnergies(self):
	    return self.imdProc.getEnergies()
	
	def getEnergiesQ(self):
	    return self.imdProc.getEnergiesQ()
	
	def setCoordinatesCallback(self, f):
		self.imdProc.setCallback(f, imd.IMDType.IMD_FCOORDS)
		
	def setEnergiesCallback(self, f):
		self.imdProc.setCallback(f, imd.IMDType.IMD_ENERGIES)
		
	def run(self):
		print "ImdSimThread run"
		self.imdProc.start()
		SimThread.run(self)
		#self.imdProc.join()
	'''
	
	def run(self):
	    self.imd = imd.IMDConnection('localhost', 3000)
	    self.imd.go()
	    
	    en = self.imd.recv()
	    while True:
	        p = self.imd.recv()
	        print "ImdSimThread run packet received"
	        if p.header.type == imd.IMDType.IMD_DISCONNECT: break
	        elif p.header.type == imd.IMDType.IMD_FCOORDS:
	            self.coordArray = p.data.rawCoords
	            self.updateCoordsMethod()
	        elif p.header.type == imd.IMDType.IMD_ENERGIES:
	            pass
	   
	    self.imd.close()
	'''
	
	def close(self):
	    self.imdProc.close()
	    super(ImdSimThread,self).close()
	
	def updateCoordinates(self, mixture):
		'''
		# empty queue
		while not self.imdProc.getCoordinatesQ().empty():
			self.imdProc.getCoordinatesQ().get_nowait()
		'''
		
		coords = self.imdProc.getCoordinatesArray()
		mixture.updateCoordinatesFromArray(coords)
		return coords

 
class NAMDcell: 
    def __init__(self,nombreArchivo, remoteHost=None):
		self.archivo = nombreArchivo 
		self.remoteHost = remoteHost
		if self.remoteHost <> None:
			self.remoteHostFile = nombreArchivo
		self.readNext()
    
    
    def readNext(self):
		if self.remoteHost <> None:
			self.fh, tempFileName = tempfile.mkstemp()
			(resp, err) = self.remoteHost.getFile(self.remoteHostFile, tempFileName)
			#print "NAMDcell readNext", resp, err
			self.archivo = tempFileName
		
		self.dx = self.dy = self.dz = self.ox = self.oy = self.oz = None
		try:
		    f = open(self.archivo, 'r')
		    lines = f.readlines()
		    f.close()
		    if self.remoteHost <> None: 
		    	os.close(self.fh)
		    	os.remove(self.archivo)
		except:
			print "Warning. NAMDcell could not open or read cell file ", self.archivo
		    
		try:
		    valores = lines[2].split(' ')
		    #print "NAMDcellvalores ", valores
		    self.dx = [float(valores[1]), float(valores[2]), float(valores[3])]
		    self.dy = [float(valores[4]), float(valores[5]), float(valores[6])]
		    self.dz = [float(valores[7]), float(valores[8]), float(valores[9])]
		    self.ox = float(valores[10])
		    self.oy = float(valores[11])
		    self.oz = float(valores[12])
		except:
		    print "Warning. NAMDcell could not process cell in ", self.archivo
		    self.dx = self.dy = self.dz = self.ox = self.oy = self.oz = None
            
     
    def getBox(self):
        self.readNext()
        if self.dx != None: return [[self.dx, self.dy,self.dz], [self.ox, self.oy, self.oz]]
        else: return None
        
        
#=====================================================================
class dummy:
	pass

if __name__ == '__main__':
	sys.path.append("/home/jse/inv/Cuchifritos/bazaar/Wolffia")
	from  interface.main.History import NanoCADState
	from wolffialib.communication.RemoteHost import RemoteHost
	from wolffialib.communication.namd.Configuration import Configuration
	simulatorLocation = "home_inv/inv/namd/"
	hostnameEdit = "yagrumo.uprh.edu"
	usernameEdit = "jse"
	passwordEdit = ""

	prueba = ["/home/jse/inv/Frances/5temp400/", "DispersionCLFdensidad5temp400"]

	
	state = NanoCADState(filename=prueba[0]+prueba[1]+".wfy")
	state.setBuildDirectory(prueba[0])
	
	nada = dummy()
	nada.__dict__ = state.simTabValues
	conf = Configuration(nada, state.getDrawer(), state.fixedMolecules.hasFixedMolecules())
	
	conf.buildDirectory = prueba[0]
	conf.mixtureName =  prueba[1]
	conf.writeSimulationConfig(prueba[0], prueba[1])
	
	state.packFiles(conf.buildDirectory + conf.mixtureName + ".zip")

	remote = RemoteHost(hostnameEdit,usernameEdit, passwordEdit)

 	proc = ImdSimThread( conf, state,
								remote, 
								3000,
								simulatorLocation)



