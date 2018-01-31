# -*- coding: utf-8 -*-
"""
    Copyright 2011, 2012: José O.  {Sotero Esteva}
    Computational Science Group, Department of Mathematics, 
    University of Puerto Rico at Humacao 
    <jse@math.uprh.edu>.

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
from subprocess import signal, Popen, PIPE
import sys, os, time

CONNECTED    = 0
DISCONNECTED = 1
FAILED       = 2
NO_MDS       = 4
NO_DIR       = 8

class RemoteHost:
	def __init__(self, remoteHost, username, password=None, workingDir="", logArea=sys.stdout):
		self.username    = username
		self.remoteHost  = remoteHost
		self.password    = password
		self.logArea     = logArea
		self.maxProcessors  = 1
		self.maxGpus        = 0
		self.workingDir  = workingDir
		self.probe()
		
		
	def killAllNamd(self):
		'''
		kill all namd processes own by self.username.
		Returns True if a process was killed.
		'''
		self.logArea.write("RemoteHost.killAllNamd killing processes ...\n")
		(resp, err) = RemoteHost._sendCommand(self.remoteHost, self.username, self.password, ['killall namd2'])
		#print "retrieveNamdUsers ", resp
		return not (len(resp) > 1 and resp.split('\n')[-2] <> "namd2: no process found")
	
	def probe(self):
		self.status      = RemoteHost.testConnection(self.remoteHost, self.username, self.password,logArea=self.logArea)
		if not self.status:
			self.retrieveProcessors()
			self.retrieveGPUs()
			self.retrieveNamdUsers()
		else:
			self.maxProcessors  = 1
			self.maxGpus        = 0
		
		self.chosenProcessors = self.maxProcessors
		self.chosenGpus = self.maxGpus
		
	@staticmethod
	def _sendCommand(remoteHost, username, password, command):
		#print "sending command: ", ['/usr/bin/sshpass', '-p',  password, '/usr/bin/ssh' , '-T',  username + '@' +  remoteHost] + command
		remoteConnection = Popen(['/usr/bin/sshpass', '-p',  password, '/usr/bin/ssh' , '-T',  username + '@' +  remoteHost] + command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		return remoteConnection.communicate()


	@staticmethod
	def testConnection(remoteHost, username, password, workingDir="./", logArea=sys.stdout):
		#print "RemoteHost.testConnection ", workingDir
		logArea.write("RemoteHost.testConnection Attempting connection: host=" + remoteHost + ", user=" + username + ", workingDir=" + workingDir + "\n")
		#remoteConnection = Popen(['/usr/bin/sshpass', '-p',  password, '/usr/bin/ssh' , '-T',  username + '@' +  remoteHost], stdin=PIPE, stdout=PIPE)
		#(resp, err) = remoteConnection.communicate(input='hostname ')
		(resp, err) = RemoteHost._sendCommand(remoteHost, username, password, ['hostname '])
		logArea.write("RemoteHost.testConnection RESPONSE " + resp + "\n")
		if len(resp) == 0 or len(err) > 0:
			return FAILED

		returnCode = CONNECTED
		logArea.write("RemoteHost.testConnection Checking namd ...\n")
		(resp, err) = RemoteHost._sendCommand(remoteHost, username, password, ['whereis', 'namd2'])
		if len(resp) > 1 and resp.split('\n')[-2] <> "namd2:":
			logArea.write("RemoteHost.testConnection NAMD confirmed: " + resp.split('\n')[-2] + "\n")
		else:
			logArea.write("RemoteHost.testConnection ERROR: namd2 is not in the remote host's search path. \n")
			returnCode = returnCode | NO_MDS

		logArea.write("RemoteHost.testConnection Checking working directory \"" + workingDir + "\" ...\n")
		(resp, err) = RemoteHost._sendCommand(remoteHost, username, password, ['ls', '-la',  workingDir])
		if len(resp) > 1 and err.find("No such file or directory") == -1 and resp.split('\n')[1][:4] == 'drwx':
			logArea.write("RemoteHost.testConnection working directory confirmed: " + resp.split('\n')[1] + "\n")
		else:
			logArea.write("RemoteHost.testConnection ERROR: working directory is not present or access permissions are wrong. \n")
			returnCode = returnCode | NO_DIR

		return returnCode
	
	
	def retrieveProcessors(self):
		self.logArea.write("RemoteHost.retrieveProcessors Checking number of cpu cores ...\n")
		(resp, err) = RemoteHost._sendCommand(self.remoteHost, self.username, self.password, ['cat /proc/cpuinfo | awk \'/^processor/{print $3}\' | tail -1'])
		try:
			self.maxProcessors = int(resp) + 1
			self.logArea.write("RemoteHost.retrieveProcessors number of cores: " + str(self.maxProcessors) + "\n")
		except:
			self.logArea.write( "RemoteHost.retrieveProcessors ERROR: did not find number of cores. Setting to 1.\n ")
			self.maxProcessors = 1
		return self.maxProcessors
	
	
	def retrieveNamdUsers(self):
		self.logArea.write("RemoteHost.retrieveNamdUsers Checking namd users ...\n")
		(resp, err) = RemoteHost._sendCommand(self.remoteHost, self.username, self.password, ['ps -A u | grep namd2 | grep -v grep | cut -d\' \' -f1'])
		#print "retrieveNamdUsers ", resp
		try:
			self.namdUsers = resp.split('\n')[:-1]
			self.logArea.write("RemoteHost.retrieveNamdUsers users: " + str(self.namdUsers) + "\n")
		except:
			self.logArea.write( "RemoteHost.retrieveNamdUsers ERROR: did not find namd users. Setting to [].\n ")
			self.namdUsers = []
		return self.namdUsers
	
	
	def retrieveGPUs(self):
		self.maxGpus = 0
		self.logArea.write( "RemoteHost.retrieveGPUs Checking number of cpu cores ...\n")
		(resp, err) = RemoteHost._sendCommand(self.remoteHost, self.username, self.password, ['cat /proc/driver/nvidia/version'])
		if err.find("No such file or directory") <> -1:
			self.logArea.write( "RemoteHost.retrieveGPUs did not find NVIDIA drivers\n")
		else:
			(resp, err) = RemoteHost._sendCommand(self.remoteHost, self.username, self.password, ['lspci | grep -i nvidia | grep VGA | wc -l'])
			self.maxGpus = int(resp)
			self.logArea.write( "RemoteHost.retrieveGPUs number of GPU devices: " + str(self.maxGpus) + "\n")

		return self.maxGpus

	def disconnect(self):
		self.status = DISCONNECTED

	@staticmethod
	def _getFile(remoteHost, username, password, remoteName, localTarget):
		#print "RemoteHost getting file: ", remoteHost, username, remoteName, localTarget
		remoteConnection = Popen(['/usr/bin/sshpass', '-p',  password, '/usr/bin/scp' , username + '@' +  remoteHost + ":" + remoteName, localTarget], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		return remoteConnection.communicate()

	def getFile(self, remoteName, localTarget):
		(resp, err) = RemoteHost._getFile(self.remoteHost, self.username, self.password, self.workingDir + remoteName, localTarget)
		#if err.find("No such file or directory") == -1 and resp.split('\n')[1][:4] == 'drwx':
		return (resp, err)
	
	@staticmethod
	def _sendFile(remoteHost, username, password, source, target):
		#print "RemoteHost sending file: ", remoteHost, username, source, target
		#print "RemoteHost sending file command: ", ['/usr/bin/sshpass', '-C -p',  password, '/usr/bin/scp' , source, username + '@' +  remoteHost + ":" + target]
		remoteConnection = Popen(['/usr/bin/sshpass', '-p',  password, '/usr/bin/scp', '-C' , source, username + '@' +  remoteHost + ":" + target], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		return remoteConnection.communicate()

	def sendFile(self, source, target=None, unzip=False, backup=True):
		'''
		Assumes files have been packed already.
		Revisar movimientos de archivos a reescribirse.
		'''
		#print "RemoteHost.sendFile checking if \"" + self.workingDir + "\" exists ..."
		(resp, err) = RemoteHost._sendCommand(self.remoteHost, self.username, self.password, ['ls', '-la', self.workingDir])
		if err.find("No such file or directory") > -1 or len(resp) < 2 or resp.split('\n')[1][:4] <> 'drwx':
			print "ERROR RemoteHost.sendFile: folder \"" + self.workingDir + "\" does not exists or has incorrect permissions ..."
			return
		
		#print "RemoteHost.sendFile detecting files that are about to be overwritten in \"" + self.workingDir + "\" ..."
		copyExtensions = "*.conf,*.pdb,*.prm,*.dcd,*.xsc,*.coor,*.psf,*.vel"
		#print 'ls', '-1a', self.workingDir+"/{"+copyExtensions+"}"
		(resp, err) = RemoteHost._sendCommand(self.remoteHost, self.username, self.password, ['ls', '-la', self.workingDir+"/{"+copyExtensions+"}"])
		if backup and err.find("No such file or directory") == -1:
			copyDir = self.workingDir+"/"+time.strftime("%Y%m%d-%H%M%S")
			#print "RemoteHost.sendFile moving files that are about to be overwritten to  \"", copyDir
			(resp, err) = RemoteHost._sendCommand(self.remoteHost, self.username, self.password, ['mkdir',  copyDir])
			(resp, err) = RemoteHost._sendCommand(self.remoteHost, self.username, self.password, ['mv', '-u',  self.workingDir+"/{"+copyExtensions+"}", copyDir])
		#else:
			#print "RemoteHost.sendFile did not find simulation files in ", self.workingDir

		#print "RemoteHost.sendFile sending ", source, " to ", self.remoteHost
		if target == None: target = self.workingDir + "/" + os.path.basename(source)
		(resp, err) = RemoteHost._sendFile(self.remoteHost, self.username, self.password, source, target)
		#print "RemoteHost.sendFile sending response ",(resp, err)
		 
		if unzip:
			#print "RemoteHost.sendFile uncompress ", target
			(resp, err) = RemoteHost._sendCommand(self.remoteHost, self.username, self.password, ['unzip', '-o -u', '-d', self.workingDir, target])
			#print "RemoteHost.sendFile uncompress result ", resp, err

		
	def getMaxGpus(self):          return self.maxGpus
	def getMaxProcessors(self):    return self.maxProcessors
	def getChosenGpus(self):       return self.chosenGpus
	def getChosenProcessors(self): return self.chosenProcessors
	def getHostName(self):         return self.remoteHost
	def getUserName(self):         return self.username
	def getMDSUsers(self):		   return self.namdUsers
	def getWorkingDir(self):       return self.workingDir

	def isConnected(self): return self.status == CONNECTED

	def setChosenGpus(self, n):       self.chosenGpus       = n
	def setChosenProcessors(self, n): self.chosenProcessors = n
	def setHostName(self, t):         self.remoteHost       = t
	def setUserName(self, t):         self.username         = t
	def setPassword(self, t):         self.password         = t

	def startSimulation(self, mixtureName, useLogFile=False):
		if useLogFile:
			#print "RemoteHost startSimulation", ['/usr/bin/sshpass', '-p xxx /usr/bin/ssh' , '-T',  self.username + '@' +  self.remoteHost, "charmrun +p " + str(self.getChosenProcessors()) + " namd2 +idlepoll " + self.workingDir + "/" + mixtureName + ".conf > " + self.workingDir + "/" + mixtureName + ".log"]
			return Popen(['/usr/bin/sshpass', '-p',  self.password, '/usr/bin/ssh' , '-T',  self.username + '@' +  self.remoteHost, "charmrun +p " + str(self.getChosenProcessors()) + " namd2 +idlepoll " + self.workingDir + "/" + mixtureName + ".conf > " + self.workingDir + "/" + mixtureName + ".log"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		else:
			#print "RemoteHost startSimulation", ['/usr/bin/sshpass', '-p xxx /usr/bin/ssh' , '-T',  self.username + '@' +  self.remoteHost, "charmrun +p " + str(self.getChosenProcessors()) + " namd2 +idlepoll " + self.workingDir + "/" + mixtureName + ".conf" ]
			return Popen(['/usr/bin/sshpass', '-p',  self.password, '/usr/bin/ssh' , '-T',  self.username + '@' +  self.remoteHost, "charmrun +p " + str(self.getChosenProcessors()) + " namd2 +idlepoll " + self.workingDir + "/" + mixtureName + ".conf" ], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		
#=====================================================================
if __name__ == '__main__':
	hostnameEdit = "molecula.uprh.edu"
	usernameEdit = "jse"
	passwordEdit = ""

	rc = RemoteHost(hostnameEdit,usernameEdit,passwordEdit)