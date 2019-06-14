#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
#  MixtureViewer.py
#  Version 0.1, October, 2011
#
#  Wolffia Molecule viewer widget.
#
"""
    Copyright 2011, 2012: José O.  Sotero Esteva, Mirgery  Medina Cuadrado, 

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

import sys,  time, random, numpy
from PyQt4 import QtCore, QtGui, QtOpenGL,Qt
from OpenGL import GL, GLU, GLUT
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from GeometricObjects import SolidSphere

if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../')
from conf.Wolffia_conf import WOLFFIA_GRAPHICS
from lib.chemicalGraph.Mixture import Mixture

import openbabel
_ELEMENT_TABLE_ = openbabel.OBElementTable()
from History import History, ShownMoleculesSet
from lib.chemicalGraph.Mixture import Mixture

import math

#_GlLIST = GL.glGenLists(1)


_MIXTURE_GENLIST_ = 1
_ATOM_GENLIST_ = 12
_BOND_GENLIST_ = 13



class DCDLoader(QtCore.QThread):
	def __init__(self, parent, mixture, box, fileName):
		from lib.io.dcd import DCDTrajectoryReader
		super(DCDLoader, self).__init__()
		self.coordinatesGenerator = DCDTrajectoryReader(None,fileName)
		self.parent = parent
		self.mixture = mixture
		self.box =  box
	def run(self):
		for X,Y,Z,pbc in self.coordinatesGenerator:
			print "DCDLoader updating frame"
			self.mixture.updateCoordinatesFromArray([item for tuples in zip(X,Y,Z) for item in tuples])
			if pbc != None:
				self.box.setCellBasisVectors([[pbc[0], 0.0, 0.0],
									[0.0, pbc[2], 0.0],
									[0.0, 0.0, pbc[5]]])
				#self.box.setCellOrigin([pbc[1], pbc[3],pbc[4]])

			self.emit(QtCore.SIGNAL('update'))
			#self.update() 


class MixtureViewer(QtOpenGL.QGLWidget):
    ''' 
    Widget that renders Mixture graphical representations.
    '''
    updateRequest = QtCore.pyqtSignal(QtOpenGL.QGLWidget)
	#xRotationChanged = QtCore.pyqtSignal(int)
    #yRotationChanged = QtCore.pyqtSignal(int)
    #zRotationChanged = QtCore.pyqtSignal(int)
    #translationChanged = QtCore.pyqtSignal(int)
    
    _PIXELS_PER_ANGSTROM_THRESHOLD_ = 1
    
    lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
    atomRadius = 0.6

    
    def __init__(self, history=None, parent=None, mixture=Mixture(), sharedGL=None):
        """
        MixtureViewer constructor.
        
        @type  parent: QtOpenGL.QWidget
        @param parent: Parent widget.
        
        @type  mixture: Mixture
        @param mixture: Mixture to be displayed.
        """
        
        OpenGL.ERROR_CHECKING = False
        
        # "MixtureViewer__init__"
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        
        if history == None:
            self.history = History()
            self.history.currentState().reset()
            #print "MixtureViewer",self.history 
        else:
            self.history = history

        #self.mixture = self.history.currentState().getMixture()
        #self.mixture = mixture

        self.parent = parent
        self.reset()
        
        #MixtureViewer.genList = GL.glGenLists(1)
        #global _GlLIST
        self.genList = sharedGL
        #self.setMixture(self.history.currentState().getMixture())
        #self.makeGenList()
        self.highResolution = False
        self.solventHighResolution  = False
        self.labeling       = False
        self.axes           = True
        self.help           = False
        self.jointAtoms     = None
        self.previewerMode  = "rotate"
        
        self.setAutoFillBackground(False)
        self.moleculeEditor = None
        
        self.setMixture(mixture)
		
        self.setAcceptDrops(True)
        
        self.updateRequest.connect(QtOpenGL.QGLWidget.updateGL)
        
        '''
        '''
    def setBuildTab(self, table):
        self.moleculeEditor = table
        

    def reset(self):
    	#print "MixtureViewer reset"
        self.lastPos = QtCore.QPoint()
        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.translation = [0,0,0]
        self.zoom = 1.0
        self.margin = 3
        self.drawer = None
        self.sphere = None
        #self.moleculeEditor = None
        
		#self.setBoundingSphere([[0.,0.,0.], 2.])
        self.buildTables(Mixture())
        self.setBoundingSphere()
        
        self.lastPos = QtCore.QPoint()
        #self.genList = None
        self.changeTracker = 0
        
        self.quadric = gluNewQuadric()
        if self.quadric != None:
            gluQuadricNormals(self.quadric, GLU_SMOOTH)
            gluQuadricTexture(self.quadric, GL_TRUE)
        
        #window properties
        self.setMinimumWidth(250)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding))
        
        self.setBox(None)
        
        self.jointAtoms = None

	def setMixtureBAK(self, mixture, adjustViewingVolume=False):
		"""
		Sets mixture to be displayed.
		
		@type  mixture: Mixture
		@param mixture: Mixture to be displayed.
		"""
		#print "actualizando MixtureViewer con ", mixture, adjustViewingVolume
		#self.history.currentState().updateMixture(mixture)
		self.mixture = mixture
		self.changeTracker = 0
		#self.makeGenList()
		if mixture != None:
			if adjustViewingVolume:
				self.setBoundingSphere(self.mixture.boundingSphere())
				#print "enclosingBox", mixture.enclosingBox()
				#print "boundingSphere", mixture.boundingSphere()
				#print "viewBox", self.viewBox
				self.resizeGL(self.size().width(), self.size().height())
			#if mixture.changed(self.changeTracker): self.makeGenList()
			self.makeGenList()
			self.updateRequest.emit(self)	 #self.updateGL() 
		else:
			self.setBoundingSphere([[0.,0.,0.], 2.])
		#print "MixtureViewer setMixture fin ", mixture, adjustViewingVolume

    def setMixture(self, mixture, selectedMolecules=None, shownMolecules=None, adjustViewingVolume=False):
		"""
		Sets mixture to be displayed.
		
		@type  mixture: Mixture
		@param mixture: Mixture to be displayed.
		"""
		#print "actualizando MixtureViewer con ", mixture, adjustViewingVolume
		#self.history.currentState().updateMixture(mixture)
		#self.mixture = None         # para forzar errores en los lugares que los usen
		self.changeTracker = None   # para forzar errores en los lugares que los usen

		
		if mixture != None:
			self.buildTables(mixture)
			if adjustViewingVolume:
				self.setBoundingSphere()
				#print "enclosingBox", mixture.enclosingBox()
				#print "boundingSphere", mixture.boundingSphere()
				#print "viewBox", self.viewBox
				self.resizeGL(self.size().width(), self.size().height())
			#if mixture.changed(self.changeTracker): self.makeGenList()
			self.makeGenList()
			self.updateRequest.emit(self)	 #self.updateGL() 
		else:
			selectedMolecules = mixture.moleculeNames()  if selectedMolecules != None else selectedMolecules
			shownMolecules    = set(mixture.molecules()) if shownMolecules    != None else shownMolecules
			
			self.buildTables(Mixture())
			self.setBoundingSphere()
		#print "MixtureViewer setMixture fin ", mixture, adjustViewingVolume

    def buildTables(self, mixture):
		self.atomCoordinates = []
		self.atomElements	 = []
		self.bondsTable	     = []
		for mol in mixture:
			for a in mixture.getMolecule(mol).atomsGenerator():
				self.atomCoordinates.append(a.getCoord())
				self.atomElements.append(a.getInfo().getElement())
			for b in mixture.getMolecule(mol).bondsGenerator():
				self.bondsTable.append((b[0].getCoord(),b[1].getCoord()))

    def setBox(self, box):
        #print "setBox"
        self.drawer = box
        if box != None:
            self.resizeGL(self.size().width(), self.size().height())
            self.updateRequest.emit(self)     #self.updateGL() 

    def update(self, adjustViewingVolume=True):
        #start = time.clock()
        #print "MitueViewer.update"
        import inspect
        print "MitueViewer.update, caller=",inspect.stack()[1][3]

        if self.isVisible():
            #print "MitueViewer.update", self.size().width(), self.size().height()
            if adjustViewingVolume: self.setBoundingSphere()
            #print "MitueViewer.update", self.size().width(), self.size().height()
            #print "MitueViewer.update self.setBoundingSphere", self.boundingSphere
            self.resizeGL(self.size().width(), self.size().height())
    
            if self.moleculeEditor == None: self.makeGenList()
            else: 
                #print "MixtureViewer update", self.parent,self.moleculeEditor.editor.selectedMolecules()
                self.makeGenList(self.moleculeEditor.editor.selectedMolecules())
            
            self.updateRequest.emit(self)     #self.updateGL() 
            
            #self.paintGL() #20140713
            #QtOpenGL.QGLWidget.update(self) #20140713
        else:
            self.genList = None # forces call to makeGenList() at the next paint
            
        #print "MitueViewer.update time=", time.clock() - start


    def setMode(self, mode):
        '''
        Sets the mode for the previewer, the modes are:
        Move
        Rotate
        Remove a sphere
        Remove a square
        Make bonds between 2 atoms
        '''

        self.previewerMode = mode

        if mode == "move": self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        elif mode == "select": self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        elif mode == "makeBonds": self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif mode == "pore": self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        elif mode == "square": self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        else:
            self.setCursor(QtGui.QCursor(QtGui.QPixmap(str(WOLFFIA_GRAPHICS) + mode + ".png")))
        #print "setMode ", mode, self.cursor().shape()
    #-------------------------------------------------------------------
    
    def dragEnterEvent (self, event):
		dropUrl = event.mimeData().urls()[0]
		if not dropUrl.isLocalFile():
			#print "dragEnterEvent no es local"
			return 
		
		#print "dragEnterEvent",event.mimeData().hasFormat('text/plain')
		if event.mimeData().hasFormat('text/plain'):
		    #print self.parent , "<<<<<<<<<<<-----------Self.parent"
		    #try:
		    	fileName = str(dropUrl.toLocalFile ())
		        #pdbDir = str(text.mimeData().text()).rstrip().split("file://")
		        basename, extension = os.path.splitext(str(dropUrl.toLocalFile ()))
		        #extension = os.path.splitext(pdbDir[1])[1]
		        #print "dragEnterEvent ", extension
		        #dir = pdbDir[1].split(".")
		   
		        if extension.lower() in ['.pdb', '.wfy', '.wfm', '.cc1', '.dcd']:
					event.accept()
          
    #-------------------------------------------------------------------
    def drawAs3DCriterion(self):
        return self.highResolution
        
        #minDim = min([self.viewBox[1]-self.viewBox[0],self.viewBox[3]-self.viewBox[2]])
        #minSize = min([self.size().width(), self.size().height()])
        #print "drawAs3DCriterion", minSize, minDim, self.zoom, minSize / minDim * self.zoom
        #return minSize / minDim * self.zoom > self._PIXELS_PER_ANGSTROM_THRESHOLD_

    #-------------------------------------------------------------------
    def dropEvent(self, event):
		dropUrl = event.mimeData().urls()[0]
		fileName = str(dropUrl.toLocalFile ())
		basename, extension = os.path.splitext(str(dropUrl.toLocalFile ()))
		extension = extension.lower()
		
		if extension == '.pdb' or extension == '.cc1':
		    from interface.classifier.Load import Load
		    self.history.push()

		    loader = Load(self,fileName)

		    loader.show()
		    print "MixtureViewer dropEvent exec"
		    loader.exec_()
		    print" EXEC"
		    
		    #Adding mixture
		    print "MixtureViewer dropEvent adding mixture"
		    self.parent.buildTab.addMixture(loader.getMixture())
		    self.parent.update()       
		     
		elif extension == '.wfy':
			self.history.push()
			
			folder = self.history.currentState().getBuildDirectory()  # remember current folder
			mName = self.history.currentState().getMixture().getMixtureName()
			self.history.currentState().load(fileName)
			#print "dropEvent ",self.history.currentState().getMixture().getMixtureName(),self.history.currentState().getBuildDirectory(), " to ", mName , folder
			self.history.currentState().setBuildDirectory(folder)
			self.history.currentState().getMixture().setMixtureName(mName)
			self.history.currentState().save()
			
			self.update()
			self.parent.update()   
			QtGui.QMessageBox.information(self, "Wolffia's message", folder + " loaded.", QtGui.QMessageBox.Ok)
		    
		elif extension == '.wfm':
		    #print "LoadWFM filename",fileName
		    #origMols = set(self.history.currentState().getMixture().moleculeNames())
		    self.history.currentState().getMixture().loadWFM(fileName)
		    #newMols = set(self.history.currentState().getMixture().moleculeNames()).difference(origMols)
		    #print "dropEvent ", origMols, newMols,set(self.history.currentState().getMixture().moleculeNames())0
		    self.history.currentState().shownMolecules.showAll()
		    #Adding mixture
		    self.update()
		    self.parent.update() 
            
 		elif extension == '.dcd':
			#from lib.io.dcd import DCDTrajectoryReader
			self.history.push()
			#tReader = DCDTrajectoryReader(None,fileName)
			self.dcdLoader = DCDLoader(self,self.history.currentState().getMixture(),self.history.currentState().getDrawer(),fileName)
			self.connect(self.dcdLoader, QtCore.SIGNAL('update'), self.parent.update)
			self.dcdLoader.start()
			#for X,Y,Z in tReader:
				#print "DCDLoader loading frame"
				#self.history.currentState().getMixture().updateCoordinatesFromArray([item for tuples in zip(X,Y,Z) for item in tuples])
            

    def makeBallGenList(self):
		if not hasattr(self, 'ballGenList'):
			self.ballGenList = GL.glGenLists(1)
			#print "__init3__ initializeGL", self.ballGenList
			GL.glNewList(self.ballGenList, GL.GL_COMPILE)
			GLU.gluSphere(self.quadric,MixtureViewer.atomRadius,7,7)
			GL.glEndList()
            
    #-------------------------------------------------------------------
    def makeGenList(self, selectedMolecules=[]):
        import time
        #start = time.clock()
        self.mixture = self.history.currentState().getMixture()
        
        import inspect
        print "MitueViewer.makeGenList, caller=",inspect.stack()[1][3]
        
        #print "makeGenList mixture",self, self.mixture
        self.makeBallGenList()
        
        if self.genList == None or self.genList == 0:
            self.genList = GL.glGenLists(_MIXTURE_GENLIST_)
            #print "makeGenList genList created ", self.genList 
            
        if self.mixture != None and self.genList != 0 and self.genList !=None:
			GL.glNewList(self.genList, GL.GL_COMPILE)
			self.paintAll(selectedMolecules)
			GL.glEndList()
        else: 
        	#print "genList didn't make a list, mixture=",self.mixture
        	pass
        #stop = time.clock()
        #print "genList",self.parent, self.genList, " time",stop-start

    def paintAll(self, selectedMolecules=[]):
		import inspect
		print "paintAll, caller=",inspect.stack()[1][3]
		#if not self.isVisible(): 
		#	print "paintAll: not visible .... skipping"
		#	return

		#self.mixture = self.history.currentState().getMixture()
		if self.history != None:
			shownMolecules = self.history.currentState().shownMolecules
			#shownMolecules = ShownMoleculesSet(self.mixture)
		else:
			shownMolecules = set(self.mixture.molecules())
			
		shownSolute = shownMolecules.difference(self.mixture.getSolvent())
		shownSolvent = shownMolecules.intersection(self.mixture.getSolvent())
		if self.drawAs3DCriterion():
		    self.paintBonds(selectedMolecules, shownSolute)
		    self.paintAtoms(selectedMolecules, shownSolute)
		else:
		    self.paintBondsAsLines(selectedMolecules, shownSolute)
		    
		if self.solventHighResolution:
		    self.paintBonds(selectedMolecules, shownSolvent)
		    self.paintAtoms(selectedMolecules, shownSolvent)
		else:
		    self.paintAtomsAsPoints(selectedMolecules, shownSolvent)
        
        
    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)
    
#-----------------------------------------------------------------------------
    def mouseMoveEvent (self,text):
         mimeData = QtCore.QMimeData()

         drag = QtGui.QDrag(self)
         drag.setMimeData(mimeData)
         drag.setHotSpot(e.pos() - self.rect().topLeft())

         dropAction = drag.start(QtCore.Qt.MoveAction)       
#-----------------------------------------------------------------------------

    def setZoom(self, z):
        self.zoom = z
        self.resizeGL(self.size().width(), self.size().height())
        self.updateRequest.emit(self)     #self.updateGL() 

    def setTranslation(self, movement):
        self.translation[0] += movement[0]
        self.translation[1] += movement[1]
        self.translation[2] += movement[2]
        self.updateRequest.emit(self)     #self.updateGL() 
        
    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            #self.xRotationChanged.emit(angle)
            self.updateRequest.emit(self)     #self.updateGL() 

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            #self.yRotationChanged.emit(angle)
            self.updateRequest.emit(self)     #self.updateGL() 

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            #self.zRotationChanged.emit(angle)
            self.updateRequest.emit(self)     #self.updateGL()        

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle


    def keyPressEvent(self, event):
        #print "keyPressEvent"
        
        text = event.text()
        prevDrawMode = self.drawAs3DCriterion()
        if len(text) > 0:
            ch = event.text().at(0).toAscii()
            key = event.key()
            if 't' == ch:
                # Increase the detail threshold (make the terrain less detailed - worse looking but faster)
                self.mThreshold += 0.5
                #print "SAMPLE: Threshold = ", self.mThreshold
            elif 'T' == ch:
                # Decrease the detail threshold (make the terrain more detailed - better looking but slower)
                self.mThreshold -= 0.5
                #print "SAMPLE: Threshold = ", self.mThreshold
            elif 'x' == ch:
                self.setXRotation(self.xRot + 20)
            elif 'y' == ch:
                self.setYRotation(self.yRot + 20)
            elif 'z' == ch:
                self.setZRotation(self.zRot + 20)
            elif 'X' == ch:
                self.setXRotation(self.xRot - 20)
            elif 'Y' == ch:
                self.setYRotation(self.yRot - 20)
            elif 'Z' == ch:
                self.setZRotation(self.zRot - 20)
            elif '-' == ch:
                #print "-"
                self.zoom *= .9
                self.update()
            elif '+' == ch:
                self.zoom *= 1.1
                self.update()
            elif 'h' == ch:
                self.highResolution = not self.highResolution
            elif 'H' == ch:
                self.help = not self.help
            elif 'l' == ch:
                self.labeling = not self.labeling
            elif 'a' == ch:
                self.axes = not self.axes
        
        if prevDrawMode != self.drawAs3DCriterion():
            self.makeGenList()
        
        self.updateRequest.emit(self)     #self.updateGL() 



    def initializeGL2(self):
        #print "initializeGL"
        MAX_VIEW_DISTANCE = 8000.0
        try:
    
            GL.glShadeModel(GL.GL_SMOOTH)
            #GL.glEnable(GL.GL_CULL_FACE)
            
            GL.glClearColor(0.,0.,0.,1.)
            self.lightZeroPosition = [0., 0., 2.*self.boundingSphere[1]]
            self.lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
            self.setLigth()
            
            
            #GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, self.lightZeroColor)
            #GL.glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_FALSE)
    
            #GL.glLightf(GL.GL_LIGHT0, GL.GL_CONSTANT_ATTENUATION, 0.1)
            #GL.glLightf(GL.GL_LIGHT0, GL.GL_LINEAR_ATTENUATION, 0.05)
            
            GL.glEnable(GL.GL_LIGHTING)
            GL.glEnable(GL.GL_LIGHT0)
            GL.glEnable(GL.GL_DEPTH_TEST)
            
            GL.glLineWidth(1.)
            

        #GL.glPushMatrix()
        except Exception, ex:
            print "ERROR: ", ex

    def initializeGL(self):
        #print "initializeGL"
  
        glEnable(GL_CULL_FACE)
  
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
  
        glEnable(GL_NORMALIZE)
        glEnable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
  
        #set ambient and diffuse light colors by glColor
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
  
        #set intensity of light factors before using glColor
        specularLight = [1.0, 1.0, 1.0, 1.0]
        ambientLight = [0.2, 0.2, 0.2, 1.0]
        diffuseLight = [0.6, 0.6, 0.6, 1.0]
        position0 = [0., 0., 2.*self.boundingSphere[1]]
        position1 = [0., 0., -2.*self.boundingSphere[1]]
  
		#set light parameters
        glLightfv(GL_LIGHT0, GL_SPECULAR, specularLight)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
        glLightfv(GL_LIGHT0, GL_POSITION, position0)
        glEnable(GL_LIGHT0)
  
        #set light parameters
        glLightfv(GL_LIGHT1, GL_SPECULAR, specularLight)
        glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLight)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLight)
        glLightfv(GL_LIGHT1, GL_POSITION, position1)
        glEnable(GL_LIGHT1)
  
        #set relfective properties
        specReflect = [ 0.8, 0.8, 0.8, 1.0]
        glMaterialfv(GL_FRONT, GL_SPECULAR, specReflect)
        glMateriali(GL_FRONT, GL_SHININESS, 15)
  
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)

        '''
        self.ballGenList = GL.glGenLists(1)
        print "__init3__ initializeGL", self.ballGenList
        GL.glNewList(self.ballGenList, GL.GL_COMPILE)
        GLU.gluSphere(self.quadric,MixtureViewer.atomRadius,7,7)
        GL.glEndList()
        '''

        self.atomList = GL.glGenLists(_ATOM_GENLIST_)
        if self.atomList == None: self.atomList = _ATOM_GENLIST_

        self.makeBallGenList()
    	
        '''
        self.bondGenList = GL.glGenLists(1)
        GL.glNewList(self.bondGenList, GL.GL_COMPILE)
        GLU.gluCylinder(self.quadric,.2,.2,1., 7,1)
        GL.glEndList()
		'''


    def getClickedAtomCoordinates(self, pos):
        self.modelMatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.projMatrix = glGetDoublev(GL_PROJECTION_MATRIX)
        self.viewport = glGetIntegerv(GL_VIEWPORT)
        #print "getClickedAtomCoordinates2 glGetIntegerv", self.projMatrix
        x = pos.x()
        y = int(self.size().height() - pos.y())
        
        z = glReadPixels( x, y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        #print "getClickedAtomCoordinates", x, y,z, glGetError() == GL_NO_ERROR
        result = glReadPixels(x, y, 1, 1,  GL_RGBA,GL_FLOAT) 
        #print "getClickedAtomCoordinates glReadPixels ", result

        p0 = gluUnProject(x,y,z, self.modelMatrix, self.projMatrix, self.viewport)
        #print "getClickedAtomCoordinates  gluUnProject0", p0

        # search for the closest atom
        minDist = float("inf")
        shownMolecules = self.history.currentState().shownMolecules.shownList(self.mixture)
        for molecule in shownMolecules:
            #molecule = self.mixture.getMolecule(molName)
            for atoms in molecule.atoms():
                attr = molecule.getAtomAttributes(atoms)
                x2,y2,z2 = gluProject(attr.getCoord()[0], attr.getCoord()[1], attr.getCoord()[2], self.modelMatrix, self.projMatrix, self.viewport)
                #print "getClickedAtomCoordinates  gluProject1",attr.getType(), x2,y2,z2
                #d = attr.distanceToPoint(p0)
                d = (x-x2)**2 + (y-y2)**2 + (z-z2)**2
                if d < minDist:
                    minDist = d
                    closestAtom = atoms
                    closestCoords = attr.getCoord()
                    closestMolecule = self.mixture.getMoleculeID(molecule)
        return closestMolecule, closestAtom, closestCoords

    def getClickedAtomCoordinates2(self, pos):
        self.modelMatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.projMatrix = glGetDoublev(GL_PROJECTION_MATRIX)
        self.viewport = glGetIntegerv(GL_VIEWPORT)
        #print "getClickedAtomCoordinates2 glGetIntegerv", viewport
        #print "getClickedAtomCoordinates2 GL_DEPTH_BITS", glGetIntegerv (GL_DEPTH_BITS)
                       
        x = pos.x()
        y = int(self.viewport[3] - pos.y())
        
        # glReadPixels is not working, always returns 1
        # atom selected is the closest to the line defined by all points
        # that map to screen coordinates (x,y)
        z = glReadPixels( x, y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        #print "getClickedAtomCoordinates2", x, y,z, glGetError() == GL_NO_ERROR
        result = glReadPixels(x, y, 1, 1,  GL_RGBA,GL_FLOAT) 
        #print "getClickedAtomCoordinates2 glReadPixels ", result

        p0 = gluUnProject(x,y,0.0, self.modelMatrix, self.projMatrix, self.viewport)
        #print "getClickedAtomCoordinates2  gluUnProject0", p0
        p1 = gluUnProject(x,y,1., self.modelMatrix, self.projMatrix, self.viewport)
        #print "getClickedAtomCoordinates2  gluUnProject1", p1
        # search for the closest atom
        minDist = float("inf")
        shownMolecules = self.history.currentState().shownMolecules.shownList(self.mixture)
        for molName in shownMolecules:
            molecule = self.mixture.getMolecule(molName)
            for atoms in molecule.atoms():
                attr = molecule.getAtomAttributes(atoms)
                d = attr.distanceToLine([p0,p1])
                if d < minDist:
                    minDist = d
                    closestAtom = atoms
                    closestCoords = attr.getCoord()
                    closestMolecule = molName
        return closestMolecule, closestAtom, closestCoords

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            if self.previewerMode == "rotate":
                self.lastPos = event.pos()   
                        
            if self.previewerMode == "move":
                self.lastPos = event.pos()
                
            elif self.previewerMode == "makeBonds":
                #print "mousePressEvent ", self.format().depth()
                closest = self.getClickedAtomCoordinates(event.pos())
                #print "Mixture Viewer closestAtom", closest
                #print "Mixture Viewer closestAtom", self.mixture.getMolecule(closest[0]).getAtomAttributes(closest[1])
                self.jointAtoms = [closest,closest]
            elif self.previewerMode == "pore":
                #print "mousePressEvent ", self.format().depth()
                closest = self.getClickedAtomCoordinates(event.pos())
                #print "Mixture Viewer closestAtom", closest
                #print "Mixture Viewer closestAtom", self.mixture.getMolecule(closest[0]).getAtomAttributes(closest[1])
                self.jointAtoms = [closest,closest]
            elif self.previewerMode == "select":
                if self.moleculeEditor != None:
                    self.selected = self.getClickedAtomCoordinates(event.pos())
                    self.moleculeEditor.editor.setMolecule(self.mixture.getMolecule(self.selected[0]), self.selected[0],removeIfPresent=True)
                    self.moleculeEditor.insertAllToManager()
                    #print "Mixture Viewer select", self.selected[0], self.mixture.getMolecule(self.selected[0]).getAtomAttributes(self.selected[1])
                self.update()
            
            elif self.previewerMode  == "zoom":
                self.lastPos = event.pos()
                
    def mouseMoveEvent(self, event):
        #print "mouseMoveEvent",event.x(),event.y()
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        if event.buttons() & QtCore.Qt.LeftButton:
            if self.previewerMode == "rotate":
                self.setXRotation(self.xRot + 8 * dy)
                self.setYRotation(self.yRot + 8 * dx)
                self.updateRequest.emit(self)     #self.updateGL() 
                #self.setZRotation(self.zRot + 8 * dx)
            
            elif self.previewerMode == "move":
                p0 = gluUnProject(0.,0.,0.5, self.modelMatrix, self.projMatrix, self.viewport)
                p1 = gluUnProject(dx,dy,0.5, self.modelMatrix, self.projMatrix, self.viewport)
                d = [p1[0]-p0[0],p0[1]-p1[1],p0[2]-p1[2]]
                #print "mouseMoveEvent",dx,dy,d
                self.setTranslation(d)
                #self.setTranslation([math.cos(math.radians(self.xRot)) * dx, math.sin(math.radians(self.yRot)) * dy, 0])
            
            elif self.previewerMode == "makeBonds":
                self.jointAtoms[1] = self.getClickedAtomCoordinates(event.pos())
                #print "mouseMoveEvent line", self.jointAtoms
                #print "mouseMoveEvent line", self.mixture.getMolecule(self.jointAtoms[0][0]).getAtomAttributes(self.jointAtoms[0][1]), self.mixture.getMolecule(self.jointAtoms[1][0]).getAtomAttributes(self.jointAtoms[1][1])
                self.updateRequest.emit(self)     #self.updateGL() 
            
            elif self.previewerMode == "pore":
                self.jointAtoms[1] = self.getClickedAtomCoordinates(event.pos())
                #print "mouseMoveEvent line", self.jointAtoms
                #print "mouseMoveEvent line", self.mixture.getMolecule(self.jointAtoms[0][0]).getAtomAttributes(self.jointAtoms[0][1]), self.mixture.getMolecule(self.jointAtoms[1][0]).getAtomAttributes(self.jointAtoms[1][1])
                self.updateRequest.emit(self)     #self.updateGL() 

            elif self.previewerMode == "zoom":
                if dy < 0:
                    self.setZoom(self.zoom*1.1)
                else:
                    self.setZoom(self.zoom*.9)
            elif self.previewerMode == "select":
                if self.moleculeEditor != None:
                    try:
                        self.moleculeEditor.editor.setMolecule(self.mixture.getMolecule(self.selected[0]), self.selected[0],removeIfPresent=True)
                        self.selected = self.getClickedAtomCoordinates(event.pos())
                        self.moleculeEditor.editor.setMolecule(self.mixture.getMolecule(self.selected[0]), self.selected[0],removeIfPresent=True)
                        self.moleculeEditor.insertAllToManager()
                    except UnboundLocalError:
                        pass
                    #print "Mixture Viewer select", self.selected[0], self.mixture.getMolecule(self.selected[0]).getAtomAttributes(self.selected[1])
                self.update()
                    
        self.lastPos = event.pos()

    def mouseReleaseEvent(self, event):
        #print "mouseReleaseEvent", int(event.buttons())
        if self.previewerMode == "rotate":
        	#self.update()
            pass
        elif self.previewerMode == "move":
        	#self.update()
            pass
        elif self.previewerMode == "pore":
            if self.jointAtoms != None:
                self.history.push()
                self.jointAtoms[1] = self.getClickedAtomCoordinates(event.pos())
                #print "mouseReleaseEvent pore", self.jointAtoms
                print "mouseReleaseEvent pore", self.mixture.getMolecule(self.jointAtoms[0][0]).getAtomAttributes(self.jointAtoms[0][1]), self.mixture.getMolecule(self.jointAtoms[1][0]).getAtomAttributes(self.jointAtoms[1][1])
                self.history.currentState().getMixture().removeAtomsFromSphere(self.jointAtoms, self.history.currentState().shownMolecules)            
                print "mouseReleaseEvent pore ... regrese"
                self.jointAtoms = None
                self.history.getCurrentState().shownMolecules.addMolecules(self.history.currentState().getMixture())
                self.parent.update()
                self.updateRequest.emit(self)     #self.updateGL()         
        elif self.previewerMode == "makeBonds":
            if self.jointAtoms != None:
                self.history.push()
                self.jointAtoms[1] = self.getClickedAtomCoordinates(event.pos())
                #print "mouseReleaseEvent makeBonds", self.jointAtoms
                #print "mouseReleaseEvent line", self.mixture.getMolecule(self.jointAtoms[0][0]).getAtomAttributes(self.jointAtoms[0][1]), self.mixture.getMolecule(self.jointAtoms[1][0]).getAtomAttributes(self.jointAtoms[1][1])
                try:
                    (newMol, delMol) = self.history.getCurrentState().getMixture().addBond([self.jointAtoms[0][0], self.jointAtoms[0][1]], [self.jointAtoms[1][0], self.jointAtoms[1][1]])
                    if delMol != None: self.history.currentState().shownMolecules.remove(delMol)
                    self.history.currentState().shownMolecules.addMolecules(self.history.getCurrentState().getMixture())
                    self.jointAtoms = None
                    self.parent.update()
                    self.updateRequest.emit(self)     #self.updateGL() 
                except:
                    message = QtGui.QMessageBox(1, "Warning", "Attempted to make a double or self bond.")
                    message.exec_()
        elif self.previewerMode == "zoom":
            pass

    def paintGL(self):
        import inspect
        #print "paintGL, caller=",inspect.stack()[1][3]
        #self.setBoundingSphere(self.mixture.boundingSphere())
        #self.resizeGL(self.size().width(), self.size().height())
        
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        
        GL.glTranslated(self.translation[0], self.translation[1], self.translation[2])
        
        # rotate w/r to origin
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)

        # translate center of the mixture at the origin
        GL.glTranslated(-self.boundingSphere[0][0], -self.boundingSphere[0][1], -self.boundingSphere[0][2])
        #print "paintGLglTranslated ", self.mixture.boundingSphere(), self.drawer.getBoundingSphere(), self.boundingSphere

        # set colors and material reflections
        RED = [1.0,0.,0.,1.]
        GREEN = [0.0,1.,0.,1.]
        BLUE = [0.0,0.0,1.0,1.]
        GL.glMaterialfv(GL.GL_FRONT,GL.GL_DIFFUSE,RED)
        GL.glMaterialfv(GL.GL_FRONT,GL.GL_DIFFUSE,GREEN)
        GL.glMaterialfv(GL.GL_BACK,GL.GL_DIFFUSE,BLUE)
        #self.setLigth()
        
        # draw
        self.paintBox()
        if self.axes: self.paintAxes()
        self.paintJointAtoms()
 
        if self.genList == None or self.genList == 0:
            self.update()
        if self.genList != None:
            GL.glCallList(self.genList)

        if self.labeling: self.paintLabels()
        
        if self.help: self.paintHelp()
                
        #---------------------------
        self.modelMatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.projMatrix  = glGetDoublev(GL_PROJECTION_MATRIX)
        self.viewport    = glGetIntegerv(GL_VIEWPORT)


    def setLigth(self):
        pass
        #print "setLigth"
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix(GL_MODELVIEW)
        if self.drawAs3DCriterion():
            glLoadIdentity()
        
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, self.lightZeroPosition)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, self.lightZeroColor)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, self.lightZeroColor)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, self.lightZeroColor)
            
        glPopMatrix(GL_MODELVIEW)

    def paintBonds(self, selectedMolecules=[], shownMolecules=set()):
        #print "paintBonds",self.history.currentState().getShownMolecules()
        #print "paintBonds"
        #selectedMoleculesNames = [m.name() for m in selectedMolecules]
        start = time.clock()
        if self.mixture != None:
            
            #print "paintBonds selectedMolecules", selectedMolecules
            for molecule in shownMolecules:
                if molecule in selectedMolecules: GL.glColor3fv([1.,0.,0.])
                else: GL.glColor3fv([0.,1.,0.])
                
                GL.glPushMatrix()
                #GL.glMultMatrixd(molecule.matrix[0] + molecule.matrix[1] + molecule.matrix[2] + molecule.matrix[3])
                for bond in molecule.bondsGenerator():
                    #print "paintBonds bond", bond
                    GL.glPushMatrix()
                    atom1 =  bond[0].getCoord()
                    atom2 =  bond[1].getCoord()
                    GL.glTranslatef(atom1[0],atom1[1],atom1[2])
                    d = atom2-atom1
                    r = numpy.linalg.norm(d)
                    if math.fabs(d[2]) < 0.0001:
					   ax = math.copysign( math.degrees(math.acos(d[0]/r)), d[1] )
					   #print "paintBonds d, ax", d, ax
					   GL.glRotate(ax,  0.,  0.,  1.)
					   GL.glRotate(90.,  0.,  1.,  0.)
                    else:
                       ax = math.copysign( math.degrees(math.acos(d[2]/r)), d[2] )
                       #if d[2] < 0: ax = -ax
                       #print "paintBonds d, ax, -d[1]*d[2],  d[0]*d[2]", d, ax, -d[1]*d[2],  d[0]*d[2]
                       GL.glRotate(ax,  -d[1]*d[2],  d[0]*d[2],  0.)
                    GLU.gluCylinder(self.quadric,.2,.2,r, 7,1)
                    #GL.glCallList(self.bondGenList)
                    GL.glPopMatrix()
                GL.glPopMatrix()
        #print "paintBonds time",time.clock()-start
       
    def paintBondsAsLines(self, selectedMolecules=[], shownMolecules=set()):
        if self.mixture != None:

            #GL.glMaterialfv(GL_FRONT, GL_EMISSION, self.lightZeroColor)
            #GL.glMaterialfv(GL.GL_BACK,GL.GL_DIFFUSE,[0.,0.,0.,1.])
            glBegin(GL_LINES)
            #print "paintBondsAsLines ",shownMolecules
        
            for molecule in shownMolecules:
            #for molName in shownMolecules:
                #molecule = self.mixture.getMolecule(molName)
                #print "paintBondsAsLines", molecule
                
                if molecule in selectedMolecules: GL.glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [1.0,0.0,0.0,1.])
                else: GL.glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0,1.0,0.0,1.])
                
                for (a0,a1) in molecule.bondsGenerator():
					glVertex3dv(a0.getCoord())
					glVertex3dv(a1.getCoord())
            glEnd()
        GL.glMaterialfv(GL_FRONT, GL_EMISSION, [0.,0.,0.,1.])


    def paintAtomsBAK(self, selectedMolecules=[], shownMolecules=set()):
		#print "paintAtoms"
		#pass
		import time
		start = time.clock()
		if self.mixture != None:
				
			#print "paintAtoms shownMolecules",shownMolecules
			#for molecule in shownMolecules:
			for a in range(len(self.atomCoordinates)):
				selectedMolecule = False
				atom =  self.atomCoordinates[a]
				if selectedMolecule: GL.glColor3fv([1.,0.,0.])
				else: 
					rgb = _ELEMENT_TABLE_.GetRGB(_ELEMENT_TABLE_.GetAtomicNum(self.atomElements[a]))
					GL.glColor3fv(rgb)
				GL.glPushMatrix()
				GL.glTranslatef(atom[0], atom[1], atom[2])
				#print "paintAtoms ",self.ballGenList
				GL.glCallList(self.ballGenList)
				#GLU.gluSphere(self.quadric,MixtureViewer.atomRadius,7,7)
				GL.glPopMatrix()

		print "paintAtoms time",time.clock()-start


    def paintAtoms(self, selectedMolecules, shownMolecules):
		#import inspect
		#print "paintAtoms, caller=",inspect.stack()[1][3]
		#print "paintAtoms"
		#pass
		#import time
		#start = time.clock()

		#print "paintAtoms ",selectedMolecules,shownMolecules
		for molecule in shownMolecules:
			selectedMolecule = molecule in selectedMolecules
			for attr in molecule.atomsGenerator():
				atom =  attr.getCoord()
				if selectedMolecule: GL.glColor3fv([1.,0.,0.])
				else: 
					rgb = _ELEMENT_TABLE_.GetRGB(_ELEMENT_TABLE_.GetAtomicNum(attr.getInfo().getElement()))
					GL.glColor3fv(rgb)
				GL.glPushMatrix()
				GL.glTranslatef(atom[0], atom[1], atom[2])
				#print "paintAtoms ",self.ballGenList
				#GL.glCallList(self.ballGenList)
				GLU.gluSphere(self.quadric,MixtureViewer.atomRadius,7,7)
				GL.glPopMatrix()

		#print "paintAtoms time",time.clock()-start


    def paintAtomsAsPoints(self, selectedMolecules=[], shownMolecules=set()):
		#print "paintAtomsAsPoints"
		#pass
		#import time
		start = time.clock()
		if self.mixture != None:
				
			#print "paintAtomsAsPoints shownMolecules",shownMolecules
			for molecule in shownMolecules:
				selectedMolecule = molecule in selectedMolecules
				glBegin(GL_POINTS)
				for attr in molecule.atomsGenerator():
					if selectedMolecule: GL.glColor3fv([1.,0.,0.])
					else: 
						GL.glColor3fv(_ELEMENT_TABLE_.GetRGB(_ELEMENT_TABLE_.GetAtomicNum(attr.getInfo().getElement())))
					glVertex3dv(attr.getCoord())
				glEnd()
				   
		#print "paintAtomsAsPoints time",time.clock()-start


    def paintLabels(self):
        #print "paintLabels"
        #pass
        if self.mixture != None:
            font = QtGui.QFont()
            font.setPointSizeF(200./self.boundingSphere[1]*self.zoom)
            
            #GL.glMaterialfv(GL_FRONT, GL_EMISSION, [0.,0.,0.,1.])
            #GL.glMaterialfv(GL.GL_BACK,GL.GL_DIFFUSE, [1.0,0.8,0.8,1.])
            self.qglColor (QtGui.QColor("mintcream"))
                           
            if self.history != None:
                shownMolecules = self.history.currentState().shownMolecules.shownList(self.mixture)
            else:
                shownMolecules = self.mixture.molecules()
            for molecule in shownMolecules:
            #for molName in shownMolecules:
                #molecule = self.mixture.getMolecule(molName)
                GL.glPushMatrix()

                for atoms in molecule.atoms():
                    attr = molecule.getAtomAttributes(atoms)
                    atom =  attr.getCoord()
                    GL.glPushMatrix()
                    GL.glTranslated(atom[0], atom[1], atom[2])
                    #GLU.gluSphere(self.quadric,.3,7,7)
                    if self.drawAs3DCriterion():
						#self.renderText(MixtureViewer.atomRadius+ 0.1,MixtureViewer.atomRadius+0.1,MixtureViewer.atomRadius+0.1, str(atoms) + ":" + attr.getInfo().getType(), font=font)
						self.renderText(0,0,MixtureViewer.atomRadius, attr.getInfo().getType(), font=font)
                    else:
                        self.renderText(0.15,0.15,0.15, str(atoms) + ":" + attr.getInfo().getType(), font=font)
                    GL.glPopMatrix()
                GL.glPopMatrix()

    def paintHelp(self):
        glDisable(GL_DEPTH_TEST)
        
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QColor("mintcream"))
        #print "paintHelp ",self.size().width()+10, self.size().height()-150
        painter.drawText(10, self.size().height()-100, "Hot keys:")
        painter.drawText(10, self.size().height()-80, "    H  : toggle help")
        painter.drawText(10, self.size().height()-60, "    h  : toggle high resolution")
        painter.drawText(10, self.size().height()-40,  "   +/- : zoom in / out,")
        painter.drawText(10, self.size().height()-20,  "    l  : toggle labels")
        #painter.drawText(10, self.size().height()-150, "")
        painter.end()
        glEnable(GL_DEPTH_TEST)


    def paintAxes(self):
        #print "paintAxes"
        GL.glMaterialfv(GL_FRONT, GL_EMISSION, [1.0,0.5,0.5,1.])
        glLineWidth(1)
        glBegin(GL_LINES)
        glVertex3d(0.,0.,0.)
        glVertex3d(self.boundingSphere[1]/3.,0.,0.)
        glEnd()
        self.renderText(0.9*self.boundingSphere[1]/3.,0.2,0.2, "X")
        GL.glMaterialfv(GL_FRONT, GL_EMISSION, [0.5,1.,0.5,1.])
        glBegin(GL_LINES)
        glVertex3d(0.,0.,0.)
        glVertex3d(0.,self.boundingSphere[1]/3.,0.)
        glEnd()
        self.renderText(0.2,0.9*self.boundingSphere[1]/3.,0.2, "Y")
        GL.glMaterialfv(GL_FRONT, GL_EMISSION, [0.5,0.5,1.,1.])
        glBegin(GL_LINES)
        glVertex3d(0.,0.,0.)
        glVertex3d(0.,0.,self.boundingSphere[1]/3.)
        glEnd()
        self.renderText(0.2,0.2,0.9*self.boundingSphere[1]/3., "Z")
        GL.glMaterialfv(GL_FRONT, GL_EMISSION, [0.,0.,0.,1.])

    def paintJointAtoms(self):
        #print "paintJointAtoms",self.jointAtoms
        if self.jointAtoms != None and list(self.jointAtoms[0][2]) != list(self.jointAtoms[1][2]):
            #print "paintJointAtoms",self.jointAtoms
            
            #print "paintJointAtoms ", self.jointAtoms
            GL.glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [1.0,0.0,0.0,1.])
            glLineWidth(4)
            glBegin(GL_LINES)
            glVertex3dv(self.jointAtoms[0][2])
            glVertex3dv(self.jointAtoms[1][2])
            glEnd()
            GL.glMaterialfv(GL_FRONT, GL_EMISSION, [0.,0.,0.,1.])
            #print "paintJointAtoms out"
    
    
    def paintBox(self):
        #print "paintBox"
        if self.hasBox():
                GL.glMaterialfv(GL_FRONT, GL_EMISSION, [0.,0.,1.,1.])
                B = self.drawer.getCellBasisVectors()
                O = self.drawer.getCellOrigin()
                
                """
                         v7______v6
                        / |     / |
                       /  |    /  |
                      /  v4___/__v5
                     /   /   /   /
                    v3_____v2   /
                     | /    |  /
                     |/     | /
                    vO______v1
                """
                v0 = O
                v1 = [B[0][0]+O[0], B[0][1]+O[1], B[0][2]+O[2]] 
                v3 = [B[1][0]+O[0], B[1][1]+O[1], B[1][2]+O[2]] 
                v4 = [B[2][0]+O[0], B[2][1]+O[1], B[2][2]+O[2]] 
                
                v2 = [v3[0]+v1[0]-O[0], v3[1]+v1[1]-O[1], v3[2]+v1[2]-O[2]] 
                v5 = [v4[0]+v1[0]-O[0], v4[1]+v1[1]-O[1], v4[2]+v1[2]-O[2]] 
                v6 = [v5[0]+v3[0]-O[0], v5[1]+v3[1]-O[1], v5[2]+v3[2]-O[2]] 
                v7 = [v4[0]+v3[0]-O[0], v4[1]+v3[1]-O[1], v4[2]+v3[2]-O[2]] 
                
                #top
                glBegin(GL_LINE_LOOP)
                #glColor3f(0.0,1.,0.);
                glVertex3d(v3[0], v3[1], v3[2])
                glVertex3d(v2[0], v2[1], v2[2])
                glVertex3d(v6[0], v6[1], v6[2])        #boxmax
                glVertex3d(v7[0], v7[1], v7[2])
                glEnd()
                
                #bottom
                glBegin(GL_LINE_LOOP)
                #glColor3f(0.0,1.,0.);
                glVertex3d(v0[0], v0[1], v0[2])        #boxmin
                glVertex3d(v1[0], v1[1], v1[2])
                glVertex3d(v5[0], v5[1], v5[2])
                glVertex3d(v4[0], v4[1], v4[2])
                glEnd()
                
                #front
                glBegin(GL_LINE_LOOP)
                #glColor3f(0.0,1.,0.);
                glVertex3d(v0[0], v0[1], v0[2])
                glVertex3d(v1[0], v1[1], v1[2])
                glVertex3d(v2[0], v2[1], v2[2])
                glVertex3d(v3[0], v3[1], v3[2])
                glEnd()
                
                #back
                glBegin(GL_LINE_LOOP)
                #glColor3f(0.0,1.,0.);
                glVertex3d(v4[0], v4[1], v4[2])
                glVertex3d(v5[0], v5[1], v5[2])
                glVertex3d(v6[0], v6[1], v6[2])    
                glVertex3d(v7[0], v7[1], v7[2])
                glEnd()
                
                #left
                glBegin(GL_LINE_LOOP)
                #glColor3f(0.0,1.,0.);
                glVertex3d(v0[0], v0[1], v0[2])
                glVertex3d(v4[0], v4[1], v4[2])
                glVertex3d(v7[0], v7[1], v7[2])
                glVertex3d(v3[0], v3[1], v3[2])
                glEnd()
                
                #right
                glBegin(GL_LINE_LOOP)
                #glColor3f(0.0,1.,0.);
                glVertex3d(v1[0], v1[1], v1[2])
                glVertex3d(v5[0], v5[1], v5[2])
                glVertex3d(v6[0], v6[1], v6[2])
                glVertex3d(v2[0], v2[1], v2[2])
                glEnd()
        GL.glMaterialfv(GL_FRONT, GL_EMISSION, [0.,0.,0.,1.])

    def setSphere(self, sphere):
        self.drawer = sphere
 
    def paintSphere(self):
        if self.drawer != None and self.drawer.hasSphere():
            center = self.drawer.getSphericalBCcenter()
            radius = self.drawer.getSphericalBCr1()
            
            #ideas from http://opengl20.blogspot.com/2008/05/glulookat-by-keyboard.html
            mySphere = gluNewQuadric()
            gluQuadricDrawStyle(mySphere, GLU_POINT) #or GLU_SILHOUETTE
            
            glTranslatef(center[0], center[1], center[2])
            gluSphere(mySphere, radius, 12, 12)
        
#-------------------------------------------------------------------
    def resizeGL(self, width, height):
        #import inspect
        #print "resizeGL, caller=",inspect.stack()[1][3]

        side = int(min(width, height)*2*self.zoom)
        #print "resizeGL", width, height, side,self.zoom
        #print "resizeGL glViewport", (width - side) / 2, (height - side) / 2, side, side
        
        if side < 0:
            return
        
        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)
        
        self.setProjection()

    #-------------------------------------------------------------------
    def setBoundingSphere2(self, sphere):
        #print "setBoundingSphere",sphere
        self.boundingSphere = sphere
        if self.hasBox():
            boxSphere = self.drawer.getBoundingSphere()
            dist = math.sqrt((sphere[0][0]-boxSphere[0][0])**2 \
                           + (sphere[0][1]-boxSphere[0][1])**2 \
                           + (sphere[0][2]-boxSphere[0][2])**2) 
            if sphere[1] < dist + boxSphere[1]:
                self.boundingSphere[1] = dist + boxSphere[1]
                self.boundingSphere[0][0] = (sphere[0][0]+boxSphere[0][0])/2
                self.boundingSphere[0][1] = (sphere[0][1]+boxSphere[0][1])/2
                self.boundingSphere[0][2] = (sphere[0][2]+boxSphere[0][2])/2
        self.computeViewBox()

	#-------------------------------------------------------------------
    def setBoundingSphere(self):
		self.buildTables(self.history.currentState().getMixture())
		#print "setBoundingSphere for ", len(self.atomCoordinates), " atoms."
		self.boundingSphere = [[0.,0.,0.], 1.]
		if self.atomCoordinates != []:
			Xs = [x for x,y,z in self.atomCoordinates]
			Ys = [y for x,y,z in self.atomCoordinates]
			Zs = [z for x,y,z in self.atomCoordinates]
			maxXs = max(Xs)
			minXs = min(Xs)
			maxYs = max(Ys)
			minYs = min(Ys)
			maxZs = max(Zs)
			minZs = min(Zs)
			self.boundingSphere[0][0] = (maxXs+minXs)/2
			self.boundingSphere[0][1] = (maxYs+minYs)/2
			self.boundingSphere[0][2] = (maxZs+minZs)/2
			self.boundingSphere[1]    = math.sqrt((maxXs-minXs)**2 + (maxYs-minYs)**2 + (maxZs-minZs)**2) 
		if self.hasBox():
			boxSphere = self.drawer.getBoundingSphere()
			dist = math.sqrt((self.boundingSphere[0][0]-boxSphere[0][0])**2 \
						   + (self.boundingSphere[0][1]-boxSphere[0][1])**2 \
						   + (self.boundingSphere[0][2]-boxSphere[0][2])**2) 
			if self.boundingSphere[1] < dist + self.boundingSphere[1]:
				self.boundingSphere[1] = dist + boxSphere[1]
				self.boundingSphere[0][0] = (self.boundingSphere[0][0]+boxSphere[0][0])/2
				self.boundingSphere[0][1] = (self.boundingSphere[0][1]+boxSphere[0][1])/2
				self.boundingSphere[0][2] = (self.boundingSphere[0][2]+boxSphere[0][2])/2
			
		self.computeViewBox()

    def hasBox(self): return self.drawer != None and self.drawer.hasCell()
   
    def computeViewBox(self):
        # compute bounding box consistent with bounding sphere
        sphere = self.boundingSphere
        zNear  = sphere[1]
        zFar   = zNear + sphere[1]
        left   = sphere[0][0] - sphere[1]
        right  = sphere[0][0] + sphere[1]
        bottom = sphere[0][1] - sphere[1]
        top    = sphere[0][1] + sphere[1]
        
        self.viewBox = [left, right, bottom, top, zNear, zFar]
        #print "computeViewBox ", self.viewBox
        # if self.drawer != None:
        #     box = self.drawer.getFaces()
        #     print "  faces = ",box
        #     for i in range(0,len(self.viewBox),2):
        #         self.viewBox[i] = min(self.viewBox[i], box[i])
        #     for i in range(1,len(self.viewBox),2):
        #         self.viewBox[i] = max(self.viewBox[i], box[i])
        #     print "  final viewbox", self.viewBox
        
    #-------------------------------------------------------------------
    def setProjection(self):
        #print "setProjection"
        #print "setProjection",self.viewBox 
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        
        # set box centered at the origin
        if self.boundingSphere == None or self.boundingSphere[1] <= 0:
            GL.glOrtho(-2, 2, -2, 2, -2, 2)
        else:
            self.setBoundingSphere()
            width = self.boundingSphere[1]
            #print "setProjection glOrtho", -width, width, -width, width, -width, width 
            GL.glOrtho(-width, width,
                    -width, width,
                    -width, width)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        
        
    def setHighResolution(self, high=True, doUpdate=True):
        if  self.highResolution != high:
            self.highResolution = high
            if doUpdate:
                self.makeGenList()
                self.updateRequest.emit(self)     #self.updateGL() 
            
    def setSolventHighResolution  (self, high=True, doUpdate=True):
        if  self.solventHighResolution != high:
            self.solventHighResolution = high
            if doUpdate:
                self.makeGenList()
                self.updateRequest.emit(self)     #self.updateGL()      
        
    def setLabeling(self, label=True, doUpdate=True):
        if  self.labeling != label:
            self.labeling = label
            if doUpdate:
                self.makeGenList()
                self.updateRequest.emit(self)     #self.updateGL() 

    def showAxes(self, val=True, doUpdate=True):
        if  self.axes != val:
            self.axes = val
            if doUpdate:
                self.makeGenList()
                self.updateRequest.emit(self)     #self.updateGL() 

    def showHelp(self, val=True, doUpdate=True):
        if  self.help != val:
            self.help = val
            if doUpdate:
                self.makeGenList()
                self.updateRequest.emit(self)     #self.updateGL() 

    def paintEvent (self,  event):
        #print "MixtureViewer paintEvent"
        #self.update()
        return QtOpenGL.QGLWidget.paintEvent(self, event)


#========================================================================
class MixtureViewerTest(QtGui.QWidget):
    #print "MixtureViewerTest"
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
  
        self.moleculeWidget = MoleculeWidget()
  
  
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.moleculeWidget)
        self.setLayout(mainLayout)
  
        self.setWindowTitle(self.tr("Molecule GL"))



class PreviewCheckbox(QtGui.QCheckBox):
    def __init__(self, mol, history, parent=None):
        QtGui.QCheckBox.__init__(self,parent)
        self.parent = parent
        self.mol = mol
        self.history = history
        QtCore.QObject.connect(self, QtCore.SIGNAL("clicked(bool)"), self.clicked)
        
        self.setChecked( self.history.currentState().shownMolecules.isShown(self.mol) )
        
        #print "PreviewCheckbox created ", mol
        
    def clicked(self):
        #print "PreviewCheckbox", self.isChecked()

        if self.mol[:8] == "SOLVENT(":
            for solv in self.history.currentState().mixture.molecules():
                if solv[:8] == "SOLVENT(":
                    if self.isChecked():
                        self.history.currentState().shownMolecules.show(solv)
                    else:
                        self.history.currentState().shownMolecules.hide(solv)
        elif self.isChecked():
            self.history.currentState().shownMolecules.show(self.mol)
        else:
            self.history.currentState().shownMolecules.hide(self.mol)
        #self.history.currentState().mixture.setChanged()
        #self.parent.emit(QtCore.SIGNAL("paintEvent"), QtCore.QEvent(QtCore.QEvent.None)  )
        self.parent.update()

import math
def normalize(v):
	d = math.sqrt(sum([x*x for x in v]))
	return [c / d for c in v]



class Sphere:
	def __init__(self, radius, resolution=0):
		#if resolution > 0:
		self.vertexList = list(Icosahedron().vertexList)
		self.normalsList = self.vertexList
		for subdivision in range(resolution):
			newList = []
			for i in range(0,len(self.vertexList),3):
				newList += Triangle(self.vertexList[i:i+3]).subdivide()
			self.vertexList = newList
		'''
		else:
			self.vertexList = list(Icosahedron.vertexList)
			self.normalsList = self.vertexList
		'''

		for v in self.vertexList: v *= radius
		
	def generateTriangles(self):
		#glPushMatrix()
		#glLoadIdentity()
		glBegin(GL_TRIANGLES)
		for v in self.vertexList:
			glNormal3dv(v)
			glVertex3dv(v)
		glEnd()
		#glPopMatrix()
	
	        
        
#========================================================================
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    molecule = MixtureViewerTest()
    molecule.show()
    
    sys.exit(app.exec_())
  
