
from abc import ABCMeta, abstractmethod
import socket
import struct
from array import array
import threading

IMDVERSION = 2

#IMDSemaphore = threading.Semaphore()


def readn(sock, n):
	'''
	Reads n bytes from the socket.  C to Python adaptation
	of the function imd_readn() in imdapi/imd.c
	'''
	
	nleft = n
	recvdData = ""
	#print "IMDPacket readn reading ",n 
	#currTimeout = sock.gettimeout()
	#sock.settimeout(None)
	while nleft > 0:
		try: # if IMD is killed in the middle of a read this recv will fail
		    buffer = sock.recv(nleft)
		except: return recvdData
		nread = len(buffer)
		#print "IMDPacket readn received ",nread
		if nread == 0: break
		recvdData += buffer
		nleft -= nread
	#sock.settimeout(currTimeout)
	return recvdData

class IMDType:
    IMD_DISCONNECT = 0    #/**< close IMD connection, leaving sim running */
    IMD_ENERGIES   = 1    #/**< energy data block                         */
    IMD_FCOORDS    = 2    #/**< atom coordinates                          */
    IMD_GO         = 3    #/**< start the simulation                      */
    IMD_HANDSHAKE  = 4    #/**< endianism and version check message       */
    IMD_KILL       = 5    #/**< kill the simulation job, shutdown IMD     */
    IMD_MDCOMM     = 6    #/**< MDComm style force data                   */
    IMD_PAUSE      = 7    #/**< pause the running simulation              */
    IMD_TRATE      = 8    #/**< set IMD update transmission rate          */
    IMD_IOERROR    = 9     #/**< indicate an I/O error                     */

class IMDHeader:
	IMDHeaderFormat = 'II'
	IMDHeaderSize = struct.calcsize(IMDHeaderFormat)
	
	def __init__(self, rawHeader, packetType=IMDType.IMD_DISCONNECT):
	    self.ptype          = packetType
	    if rawHeader == None or len(rawHeader) == 0:
	        self.sizeOrVersion = 0
	    else:
	        #print "IMDHeader __init__ ", len(rawHeader), IMDHeader.IMDHeaderSize, len(rawHeader[:IMDHeader.IMDHeaderSize])
	        t = struct.unpack('I', rawHeader[:4])[0]
	        pair          = struct.unpack(IMDHeader.IMDHeaderFormat, rawHeader[:IMDHeader.IMDHeaderSize])
	        self.ptype       = socket.ntohl(pair[0])
	        #print "IMDHeader __init__ self.type       = ", self.ptype
	        try:
	            self.sizeOrVersion = socket.ntohl(pair[1])
	        except:
	            #print "IMDHeader __init__ except", self.type,pair[1]
	            self.sizeOrVersion = 0
	        #print "IMDHeader __init__ pair", self.type,self.sizeOrVersion
	
	def format(self): return IMDHeader.IMDHeaderFormat
	
	def pack(self):
		
		p = struct.pack(
				self.format(),
				socket.htonl(self.ptype), 
				socket.htonl(self.sizeOrVersion)
		)
		#print "IMDHeader pack", len(p)
		return p
	
	def setSize(self, s): self.sizeOrVersion = s
	
	def size(self): return self.sizeOrVersion
	
	def packetType(self): return self.ptype

class IMDData(metaclass=ABCMeta):
	@abstractmethod
	def __init__(self):
	    pass
	
	#def format(self): return "ii"
	
	@abstractmethod
	def pack(self):
		'''
		So far only meant to send signals, not data.  Should be overridden by extending classes.
		'''
		return self.format()
	
	@abstractmethod
	def unpack(self):
	    pass


#class IMDGo(IMDData):
#    pass


class IMDEnergies(IMDData):
	IMDEnergiesFormat = 'ifffffffff'
	IMDEnergiesSize = struct.calcsize(IMDEnergiesFormat)
	
	def __init__(self):
	    IMDData.__init__(self)
	    self.reset()
	
	def energies(self): 
		return (self.tstep,self.T,self.Etot,self.Epot,self.Evdw,
	    self.Eelec,self.Ebond,self.Eangle,self.Edihe,self.Eimpr)
	
	def format(self): return IMDEnergies.IMDEnergiesFormat
	
	def reset(self):
		self.tstep  = 0       #/**< integer timestep index                    */
		self.T      = 0.0     #/**< Temperature in degrees Kelvin             */
		self.Etot   = 0.0     #/**< Total energy, in Kcal/mol                 */
		self.Epot   = 0.0     #/**< Potential energy, in Kcal/mol             */
		self.Evdw   = 0.0     #/**< Van der Waals energy, in Kcal/mol         */
		self.Eelec  = 0.0     #/**< Electrostatic energy, in Kcal/mol         */
		self.Ebond  = 0.0     #/**< Bond energy, Kcal/mol                     */
		self.Eangle = 0.0     #/**< Angle energy, Kcal/mol                    */
		self.Edihe  = 0.0     #/**< Dihedral energy, Kcal/mol                 */
		self.Eimpr  = 0.0     #/**< Improper energy, Kcal/mol                 */
		return self
	
	def pack(self):
		p = struct.pack(
				self.format(),
				socket.htonl(self.tstep), 
				self.T,
				self.Etot, 
				self.Epot, 
				self.Evdw, 
				self.Eelec, 
				self.Ebond, 
				self.Eangle, 
				self.Edihe, 
				self.Eimpr
		)
		#print "IMDEnergies pack" , len(p)
		return p
		
	def unpack(self, imdData):
		#print "IMDEnergies unpack ", len(self.data)
		(self.tstep,self.T,self.Etot,self.Epot,self.Evdw,
		self.Eelec,self.Ebond,self.Eangle,self.Edihe,self.Eimpr) = struct.unpack(
		    self.format(), 
		    imdData)
		return self
	


class IMDCoords(IMDData):
	IMDcoordsFormat = 'fff'
	IMDcoordsSize = struct.calcsize(IMDcoordsFormat)
	
	def __init__(self):
	    IMDData.__init__(self)
	    self.reset()
	
	def coordinates(self):  return self.rawCoords
	
	def format(self): return IMDCoords.IMDcoordsFormat
	
	def setFromIterable(self, it):
		self.rawCoords = array('f', it)
		return self
		
	def numAtoms(self): return int(len(self.rawCoords) / 3)
		
	def reset(self):
		self.rawCoords = array('f')
		return self
	
	def pack(self):
		return self.rawCoords.tostring()
	
	def unpack(self, imdData):
		self.reset()
		self.rawCoords.fromstring(imdData)
		if len(self.rawCoords) % 3 != 0:
		    print("ERROR: Ammount of coordinates in data (", len(self.rawCoords), ")not divisible by 3.")
		    raise ValueError
		return self

class IMDTrate(IMDData):
    IMDTrateFormat = 'i'
    IMDTrateSize = struct.calcsize(IMDTrateFormat)
    
    def __init__(self, recvData=None):
        IMDData.__init__(self,recvData)

	def pack(self): pass # to be implemented
	
	def unpack(self, imdData=None): pass # to be implemented

	def transmitRate(self): pass# to be implemented
	
#===================================================================================
class IMDPacket(metaclass=ABCMeta):
	@abstractmethod
	def __init__(self, sock=None, header=None):
		#print "IMDPacket __init__"
		self.header = header
		
		self.sock   = sock   # not part of the payload
		if sock != None: self.recv()

	def header(self): return self.header
	
	def packetType(self): 
		#print "IMDPacket type self.header.", self.header
		return self.header.packetType()

	@staticmethod
	def recv(sock):
		#print " IMDPacket recv ", sock
		
		#IMDSemaphore.acquire()
		repeat = True
		while repeat:
			repeat = False
			try:
				header = IMDHeader(sock.recv(IMDHeader.IMDHeaderSize))
			except socket.timeout:
				repeat = True
				
		#print " IMDPacket recv type", header.packetType(), header.size()
		if header.packetType() == IMDType.IMD_FCOORDS:
		    size      = header.size() * IMDCoords.IMDcoordsSize
		    c = IMDCoords()
		    c.unpack(readn(sock, size))
		    return IMDCoordPacket( c )
		    
		elif header.packetType() == IMDType.IMD_ENERGIES:
			size      = header.size()  * IMDEnergies.IMDEnergiesSize
			e = IMDEnergies()
			e.unpack( readn(sock, size) )
			return IMDEnergiesPacket( e )
		
		elif header.packetType() == IMDType.IMD_TRATE:
			size      = header.size() * IMDTrate.IMDTrateSize
			return IMDEnergiesPacket(IMDEnergies(readn(sock, size)))
		
		#IMDSemaphore.release()
		#print " IMDPacket recv: normal return", header.packetType()
		try: return IMDTypeToClass[header.packetType()]()
		except: return None
	
	def send(self, sock):
		#print "IMDPacket send", self.__class__.__name__
		#if self.header == None or self.data == None:
		#	print "IMDPacket send: Nothing to send"
		#else:
		data = self.pack()
		#print "IMDPacket send sending ", len(data), " bytes"
		return sock.send(data)
		

class IMDDataPacket(IMDPacket, metaclass=ABCMeta):
	@abstractmethod
	def __init__(self, sock=None, header=None, data=None):
		IMDPacket.__init__(self,header=IMDHeader(None, packetType=None))
		self.data = data
		#print "IMDDataPacket __init__"

	def pack(self):
		return self.header.pack() + self.data.pack()

	'''
	@staticmethod
	def recv(sock):
		#print " IMDDataPacket recv ", sock
		
		#IMDSemaphore.acquire()
		repeat = True
		while repeat:
			repeat = False
			try:
				header = IMDHeader(sock.recv(IMDHeader.IMDHeaderSize))
			except socket.timeout:
				repeat = True
				
		print " IMDDataPacket recv type", header.packetType(), header.size()
		if header.packetType() == IMDType.IMD_FCOORDS:
		    size      = header.size() * IMDCoords.IMDcoordsSize
		    return IMDCoordPacket(IMDCoords(readn(sock, size)))
		    
		elif header.packetType() == IMDType.IMD_ENERGIES:
			size      = header.size() * IMDEnergies.IMDEnergiesSize
			return IMDEnergiesPacket(IMDEnergies(readn(sock, size)))
		
		elif header.packetType() == IMDType.IMD_TRATE:
			size      = header.size() * IMDTrate.IMDTrateSize
			return IMDEnergiesPacket(IMDEnergies(readn(sock, size)))
		
		return None
	'''
	
class IMDControlPacket(IMDPacket, metaclass=ABCMeta):
	@abstractmethod
	def __init__(self, sock=None, header=None):
		pass
		IMDPacket.__init__(self,header=IMDHeader(None, packetType=None))
		#print "IMDControlPacket __init__"

	def pack(self):
		return self.header.pack()

	@staticmethod
	def recv(sock):
		#print " IMDControlPacket recv ", sock
		
		#IMDSemaphore.acquire()
		repeat = True
		while repeat:
			repeat = False
			try:
				header = IMDHeader(sock.recv(IMDHeader.IMDHeaderSize))
			except socket.timeout:
				repeat = True
				
		#print " IMDControlPacket recv type", header.packetType(), header.size()
		
		#IMDSemaphore.release()
		#print " IMDControlPacket recv: normal return", header.packetType()
		return IMDTypeToClass[header.packetType()]()
	


class IMDDisconnectPacket(IMDControlPacket):
    def __init__(self):
    	IMDPacket.__init__(self,header=IMDHeader(None, packetType=IMDType.IMD_DISCONNECT))
    	#print "IMDDisconnectPacket __init__"

class IMDEnergiesPacket(IMDDataPacket):
    def __init__(self, energies):
    	IMDPacket.__init__(self,header=IMDHeader(None, packetType=IMDType.IMD_ENERGIES))
    	self.header.setSize(1)
    	self.data = energies
    	#print "IMDEnergiesPacket __init__"
    	
    def getEnergies(self):
    	return self.data

	def setT(self, temperature):
		self.data.T = temperature
		
class IMDCoordPacket(IMDDataPacket):
    def __init__(self, coordinates):
		IMDPacket.__init__(self,header=IMDHeader(None, packetType=IMDType.IMD_FCOORDS))
		self.header.setSize(coordinates.numAtoms())
		self.data = coordinates
		#print "IMDCoordPacket __init__", self.header.size()
    	
    def getCoordinates(self):
    	return self.data

class IMDKillPacket(IMDControlPacket):
    def __init__(self):
    	IMDPacket.__init__(self,header=IMDHeader(None, packetType=IMDType.IMD_KILL))
    	#print "IMDKillPacket __init__"

class IMDGoPacket(IMDControlPacket):
    def __init__(self):
    	IMDPacket.__init__(self,header=IMDHeader(None, packetType=IMDType.IMD_GO))
    	#print "IMDGoPacket __init__"

class IMDHandshakePacket(IMDControlPacket):
    def __init__(self):
    	IMDPacket.__init__(self,header=IMDHeader(None, packetType=IMDType.IMD_HANDSHAKE))
    	#print "IMDHandshakePacket __init__"

class IMDMDcommPacket(IMDControlPacket):
    def __init__(self):
    	raise NotImplementedError
    	#print "IMDMDcommPacket __init__"

class IMDPausePacket(IMDControlPacket):
    def __init__(self):
    	IMDPacket.__init__(self,header=IMDHeader(None, packetType=IMDType.IMD_PAUSE))
    	#print "IMDPausePacket __init__"

class IMDTratePacket(IMDDataPacket):
    def __init__(self, rate):
		IMDPacket.__init__(self,header=IMDHeader(None, packetType=IMDType.IMD_TRATE))
		self.header.setSize(struct.calcsize(IMDTrate.IMDTrateFormat))
		self.data = rate
		#print "IMDTratePacket __init__"
    	
    def getRate(self):
    	return self.data

class IMDIOerrorPacket(IMDControlPacket):
	def __init__(self):
		IMDPacket.__init__(self,header=IMDHeader(None, packetType=IMDType.IMD_IOERROR),data=None)
    	#print "IMDIOerrorPacket __init__"

IMDTypeToClass = {
	0:IMDDisconnectPacket,
	1:IMDEnergiesPacket,
	2:IMDCoordPacket,
	3:IMDGoPacket,
	4:IMDHandshakePacket,
	5:IMDKillPacket,
	6:IMDMDcommPacket,
	7:IMDPausePacket,
	8:IMDTratePacket,
	9:IMDIOerrorPacket
				}


#===================================================================================
class IMDConnection(metaclass=ABCMeta):
	_TIMEOUT = 30
	def __init__(self, host, port):
		#print "IMDConnection __init__", host, port
		self.sock           = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.            setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.            settimeout(IMDConnection._TIMEOUT)
		self.server_address = (host, port)
		self.connected      = False
		self.packet         = None
		
		#print "IMDConnection __init__ termino", self.server_address

	def __iter__(self):
		return self
		
	def close(self):
		# busy wait until connection is verified
		print("IMDConnection close: waiting for connection to be established", self.connected , self.packet, self.__class__.__name__)
		for i in range(int(IMDConnection._TIMEOUT)):
			if self.connected or self.sock == None: break
			time.sleep(1)  
			 
		if self.connected: 
			print("IMDConnection close: connection established. Now it will be closed!",self.connected , self.packet, self.__class__.__name__)
			self.sock.shutdown(socket.SHUT_RDWR)
			#try: self.sock.shutdown(socket.SHUT_RDWR)
			#except: pass
			self.sock.close()
			self.sock = None
		self.connected = False
	
	@abstractmethod
	def connect(self):
		pass
	
	def kill(self):
		'''
		IMDPacket(
				header=IMDHeader(None, packetType=IMDType.IMD_KILL), 
				data=None).send(self.sock)
		'''
		if self.sock != None:
			IMDKillPacket().send(self.sock)
	
	def __next__(self):
		if not self.connected:
			raise StopIteration
		else:
			p = self.recv()
			if isinstance(p,IMDDisconnectPacket):
				self.close()
			return p
		
	def recv(self):
	    if self.sock == None: return IMDDisconnectPacket()
	    #print "IMDConnection recv", self.sock
	    p = IMDPacket.recv(self.sock)
	    return p
	
	def send(self, packet):
		packet.send(self.sock)

#===================================================================================
class IMDClientConnection(IMDConnection):
	def __init__(self, host, port):
		IMDConnection.__init__(self, host, port)

	def connect(self):
		start     = time.clock()
		self.connected = False
		count     = 0
		while time.clock() - start < IMDConnection._TIMEOUT and count < IMDConnection._TIMEOUT and self.connected == False:
		    try:
				#print "IMDClientConnection __init__", time.clock()
				self.sock.connect(self.server_address)
				self.packet         = IMDHandshakePacket.recv(self.sock)  # Handshake
				#print "IMDClientConnection __init__:  first packet received ", self.packet
				self.connected = True
		    except Exception as e:
		    			        time.sleep(1)  
		    count += 1
		    
		if not self.connected:
			print("IMDClientConnection __init__ "+ str(self.server_address) + " did not connect: ", e)
			raise socket.timeout
		
		self.sock.settimeout(5.)

		#print "IMDClientConnection __init__ sending go  packet"
		IMDGoPacket().send(self.sock)
	
	
#===================================================================================
class IMDServerConnection(IMDConnection):
	def __init__(self, port):
		IMDConnection.__init__(self, '', port)
		#self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind( ('', port) )
		self.sock.listen(1)
		
	def connect(self):
		#print "IMDServerConnection connect", self.sock
		self.connected = False
		self.sock,self.server_address = self.sock.accept()
		#print "IMDServerConnection connect accept ", self.server_address
		#print "IMDServerConnection connect sending IMDHandshakePacket", self.sock
		IMDHandshakePacket().send(self.sock)
		#print "IMDServerConnection connect waiting for IMDGoPacket"
		assert isinstance(IMDPacket.recv(self.sock),IMDGoPacket)
		#print "IMDServerConnection connect received IMDGoPacket"
		self.connected = True



#===================================================================================
import threading, sys, os, time, random
from queue import Queue, Empty

class IMDThread(threading.Thread):
	def __init__(self, remoteHost=None, port=3000):
		'''
		Constructor
		'''
		threading.Thread.__init__(self)
		
		if remoteHost == None:
		    self.remoteHost = 'localhost'
		else:
		    self.remoteHost = remoteHost
		self.port         = port
		
		self.callback     = dict()
		self.coordArray   = None
		self.coordinatesQ = Queue()
		self.imd          = None
		self.energies     = None
		self.energiesQ    = Queue()
		self.modified     = False
		self.modTime      = time.time()
		#print "IMDThread __init__", self.remoteHost, port
	    
	def cancel(self):
		#print "IMDThread cancel"
		self.imd.kill()
		self.imd.close()
	
	def coordinates(self):
	    '''
	    Returns coordinates as a linear array of float.
	    '''
	    return self.imd.packet.data.rawCoords

	def coordinatesAreNew(self):
	    return self.modified
	
	def getCoordinatesArray(self):
	    self.modified = False
	    return self.coordArray
	
	def getEnergies(self): return self.energies
	
	def getEnergiesQ(self): return self.energiesQ
	
	def getCoordinatesQ(self): return self.coordinatesQ

	def setCallback(self, f, imdType):
		'''
		When a packet of imdType type is received the function f will be called with
		the packet as argument.
		'''
		self.callback[imdType] = f
		
	def run(self):
		"""
		Runs the thread. Called by self.start.
		"""
		
		print("IMDThread run")
		self.imd = IMDClientConnection(self.remoteHost, self.port)
		self.imd.connect()
		
		#en = self.imd.recv()
		while True:
			#print "IMDThread.run receiving"
			p = self.imd.recv()
			if   p.packetType() == IMDType.IMD_DISCONNECT: 
				#print "IMDThread run: IMDType.IMD_DISCONNECT: remaining coordinates", self.coordinatesQ.qsize()
				
				# busy wait until data is used
				while not self.coordinatesQ.empty(): time.sleep(1)
				while not self.energiesQ.empty()   : time.sleep(1)

				self.imd.close()
				break
			elif p.header.packetType() == IMDType.IMD_FCOORDS:
				if IMDType.IMD_FCOORDS in self.callback:
					self.callback[IMDType.IMD_FCOORDS](p.getCoordinates().coordinates())
				else:
					self.coordArray = p.data.rawCoords
					self.coordinatesQ.put(p.data)
					#print "IMDThread run coordinatesQ = ",self ,self.coordinatesQ ,self.coordinatesQ.qsize()
					self.modified   = True
			elif p.header.packetType() == IMDType.IMD_ENERGIES:
				#print "IMDThread run: IMDType.IMD_ENERGIES: ", self.callback
				if IMDType.IMD_ENERGIES in self.callback:
					self.callback[IMDType.IMD_ENERGIES](p.getEnergies())
				else:
				    self.energies   = p.data
				    self.energiesQ.put(p.data)
			
			#if en.header.packetType() == IMDType.IMD_ENERGIES:
			#	print en.data.tstep, en.data.T, en.data.Etot, en.data.Epot, en.data.Evdw, en.data.Eelec, en.data.Ebond, en.data.Eangle, en.data.Edihe, en.data.Eimpr
			#if en.header.packetType() == IMDType.IMD_FCOORDS:
			#	print en.data.rawCoords
			#print "IMDThread run: packet received: ", p.__class__.__name__
			#time.sleep(1)  
		print("IMDThread.run finished")
		
	

#================================================================================================
# ================== TEST 1 ======================================================================

port = 35528
host = 'localhost'

def fakeServer1():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind( ('', port) )
	s.listen(1)
	s.settimeout(10)
	print("fakeServer1: Waiting")
	c,a = s.accept()
	print("fakeServer1: connected")
	IMDHandshakePacket().send(c)
	p = IMDPacket.recv(c)
	assert isinstance(p,IMDGoPacket)
	print("fakeServer1: Go")
	e = IMDEnergies()
	e.T = 298
	print("fakeServer1: sending T")
	IMDEnergiesPacket(e).send(c)
	p = IMDPacket.recv(c)
	assert isinstance(p,IMDKillPacket)
	IMDDisconnectPacket().send(c)
	print("fakeServer1: Killed! ... closing")
	c.close()
	s.close()
	
def client1():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect( (host, port) )
	p = IMDPacket.recv(s)
	assert isinstance(p,IMDHandshakePacket)
	print("client: handshake")
	IMDGoPacket().send(s)
	p = IMDPacket.recv(s)
	print("client: T received")
	assert isinstance(p,IMDEnergiesPacket)
	print("client: T=", p.getEnergies().T)
	IMDKillPacket().send(s)
	p = IMDPacket.recv(s)
	assert isinstance(p,IMDDisconnectPacket)
	print("client: IMDDisconnectPacket received, closing")
	s.close()
	
def fakeServer2():
	c = IMDServerConnection(port)
	print("fakeServer2: IMDServerConnection")
	c.connect()
	print("fakeServer2: connected")
	e = IMDEnergies()
	e.T = 298 
	print("fakeServer2: sending T")
	c.send(IMDEnergiesPacket(e))
	p = c.recv()
	assert isinstance(p,IMDKillPacket)
	c.send(IMDDisconnectPacket())
	print("fakeServer2: Killed! ... closing")
	c.close()
	
def client2():
	c = IMDClientConnection(host, port)
	c.connect()
	print("client2: connected")
	p = c.recv()
	assert isinstance(p,IMDEnergiesPacket)
	print("client2: T=", p.getEnergies().T)
	c.send(IMDKillPacket())
	p = c.recv()
	assert isinstance(p,IMDDisconnectPacket)
	print("client2: IMDDisconnectPacket received, closing")
	c.close()
	
def fakeServer3():
	c = IMDServerConnection(port)
	c.connect()
	print("fakeServer3: connected")
	e = IMDEnergies()
	for t in range(298,303):
		e.T = t
		print("fakeServer3: sending T=", t)
		c.send(IMDEnergiesPacket(e))
	c.send(IMDDisconnectPacket())
	print("fakeServer3: closing")
	c.close()
	
def client3():
	c = IMDClientConnection(host, port)
	c.connect()
	print("client3: connected")
	for p in c:
		if isinstance(p,IMDEnergiesPacket):
			print("client3: T=", p.getEnergies().T)
	print("client3: closing")
	c.close()
	
from random import random
def fakeServer4():
	c = IMDServerConnection(port)
	c.connect()
	a = IMDCoords()
	for i in range(5):
		# time spent on other computations
		time.sleep(int(random()*5))
		# ###############################
		a.setFromIterable([random(),random(),random()])
		print("fakeServer4: ", a.coordinates()[0])
		c.send(IMDCoordPacket(a))
	c.send(IMDDisconnectPacket())
	print("fakeServer4: closing")
	c.close()
	
def client4():
	t = IMDThread(host, port)
	t.start()
	while t.isAlive():
		# time spent on other computations
		time.sleep(int(random()*5))
		# ###############################
		print("client4: polling")
		while True:
			try: c = t.getCoordinatesQ().get_nowait()
			except Empty: break
			#try: e = t.getEnergiesQ().get_nowait()
			#except Empty: break
			print("client4: ", c.coordinates()[0])
	t.cancel()
	print("client4: closing")


def coordsF(c):
	print("coordsF5: ", c[0])
	
def client5():
	t = IMDThread(host, port)
	t.setCallback(coordsF, IMDType.IMD_FCOORDS)
	t.start()
	while t.isAlive():
		# time spent on other computations
		time.sleep(int(random()*5))
		# ###############################
	t.cancel()
	print("client5: closing")

	
def test(server, client):
	ts = threading.Thread(target=server, args = ())
	tc = threading.Thread(target=client, args = ())
	ts.start()
	tc.start()
	ts.join()
	tc.join()
	
	
if __name__ == '__main__':
	test(fakeServer4, client5)
	exit(0)

	#imd = IMDConnection('molecula.uprh.edu', 3545)
	imd = IMDConnection('localhost', 3546)
	
	print('starting up on %s port %s' % imd.server_address)
	#time.sleep(5)  
	imd.go()
	
	i=0
	while True:
		en = imd.recv()
		print("recibi tipo ",en.packetType())
		if en.packetType() == IMDType.IMD_DISCONNECT: break
		#(en, cocr) = imd.recv()
		
		if en.packetType() == IMDType.IMD_ENERGIES:
			print("IMD_ENERGIES ", en.data.tstep, en.data.T, en.data.Etot, en.data.Epot, en.data.Evdw, en.data.Eelec, en.data.Ebond, en.data.Eangle, en.data.Edihe, en.data.Eimpr)
		if en.packetType() == IMDType.IMD_FCOORDS:
			print("IMD_FCOORDS ", en.data.rawCoords[:6])
		i+=1
		print("IMD_FCOORDS ", i)
		if i % 1000 == 0:
			break
		#c = imd.recv()
	
	imd.close()
	
