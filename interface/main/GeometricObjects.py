# GeometricObjects.py
# -*- coding: utf-8 -*-

import math
from OpenGL import GL

# solid sphere adapted from http://www.opentk.com/node/1283 (several errors fixed)
# self._stacks is ignored (self._stacks = self._slices)

class SolidSphere(object):

    def __init__(self):
        self.setResolution(1,3,3)


    def setResolution(self, r, sl, st):
        self._radius = r
        self._slices = sl
        self._stacks = st
        self._changed = True
        self.genList()

    def draw(self):
      if self._changed:
        self.genList()
        self._changed = False



    def genList(self):
        self.genList = GL.glGenLists(1)
        GL.glNewList(self.genList, GL.GL_COMPILE)


        if (self._slices % 2) > 0:
            self._slices = self._slices + 1
        if self._radius < 0.0:
            self._radius = -self._radius

        if self._radius == 0.0:
            self._radius = 1.0

        if self._slices < 8:
            self._slices = 8

        OneThroughslices = 1.0 / self._slices
        TwoPIThroughslices = 2.0 * math.pi * OneThroughslices

        for j in range(self._slices):
            theta1 = (j * TwoPIThroughslices)
            theta2 = ((j+1) * TwoPIThroughslices)
            GL.glBegin(GL.GL_TRIANGLE_STRIP)

            for i in range(self._slices+1):
                theta3 = i * TwoPIThroughslices

                Normal = [math.cos(theta2) * math.cos(theta3),
                      math.sin(theta2),
                      math.cos(theta2) * math.sin(theta3)]

                Position = [	self._radius * Normal[0],
                        self._radius * Normal[1],
                        self._radius * Normal[2]]

                GL.glNormal3dv(Normal)
                GL.glTexCoord2d(i * OneThroughslices, 2.0 * (j+1) * OneThroughslices)
                GL.glVertex3dv(Position)

                Normal = [math.cos(theta1) * math.cos(theta3),
                      math.sin(theta1),
                      math.cos(theta1) * math.sin(theta3)]

                Position = [	self._radius * Normal[0],
                        self._radius * Normal[1],
                        self._radius * Normal[2]]

                GL.glNormal3dv(Normal)
                GL.glTexCoord2d(i * OneThroughslices, 2.0 * j * OneThroughslices)
                GL.glVertex3dv(Position)
            GL.glEnd()
        GL.glEndList()

