# -*- coding: utf-8 -*-
'''
Created on Feb 26, 2012

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
from PyQt5 import Qt, QtGui
#import PyQt5.Qwt5 as Qwt
import qwt as Qwt
from numpy import array,ones,linalg,mean,std
import datetime

class Plot(Qwt.QwtPlot):
    """
    This is a generalized plotting class that avoids having to duplicate the
    same class for two plots that are mostly alike but display different information.
    
    Think for it as some sort of EnergyPlot and KineticsPlot merged together.
    """
    xpos        = 0
    ypos        = 1
    colorpos    = 2
    xrange      = 100.0
    tolerance   = 0.0001
    
    def __init__(self, name, charts, plotType="Total", parent=None):
        Qwt.QwtPlot.__init__(self, parent)
        self.name = name
        self.setCanvasBackground(Qt.Qt.white)
        self.setAxisTitle(Qwt.QwtPlot.xBottom, "Step")
        self.setAutoReplot(True)
        
        self.charts = charts
        
        self.curve  = None

        self.prevEnergyStep = -1
        
        self.average    = Qwt.QwtPlotCurve("average")
        self.average.attach(self)
        self.average.setPen(Qt.QPen(Qt.Qt.green))
        
        self.setType(plotType)
        
    def addValuePair(self, etype, x, y):
        #print "addValuePair ",etype, x, y
        if len(self.charts[etype][self.xpos]) >= 0 and len(self.charts[etype][self.ypos]) >= 0:
            if (len(self.charts[etype][self.xpos]) == 0 and len(self.charts[etype][self.ypos]) == 0) or (self.charts[etype][self.xpos][-1] != x and self.charts[etype][self.ypos][-1] != y):
                self.charts[etype][self.xpos].append(x)
                self.charts[etype][self.ypos].append(y)

    def addValues(self, types, t, es):
        for i in range(len(types)):
            if es[i] != None and types[i] in self.charts:
                self.addValuePair(types[i], t, es[i])

        self.updateCurve()

    def addValuesFromNamd(self, namdOutput):
        chartLine = None
        #print "addValuesFromNamd received ",namdOutput
        for linea in namdOutput:
            if linea[0:6] == "ENERGY":
                chartLine = linea

                time = bond = angle = dih = impr = elec = vdw = bound = misc = kine = tot = temp = pot = tot3 = tempa = pres = gpres = vol = presa = gprea = None
                try:
                    #print "on_timer(", len(chartLine),")", chartLine
                    time  = int  (chartLine[8:16])
                    bond  = float(chartLine[16:31])
                    angle = float(chartLine[31:46])
                    dih   = float(chartLine[46:61])
                    impr  = float(chartLine[61:76])
                    elec  = float(chartLine[81:96])
                    vdw   = float(chartLine[96:111])
                    bound = float(chartLine[111:126])
                    misc  = float(chartLine[126:141])
                    kine  = float(chartLine[141:156])
                    tot   = float(chartLine[161:176])
                    temp  = float(chartLine[176:191])
                    pot   = float(chartLine[191:206])
                    tot3  = float(chartLine[206:221])
                    tempa = float(chartLine[221:236])
                    pres  = float(chartLine[241:256])
                    gpres = float(chartLine[256:271])
                    vol   = float(chartLine[271:286])
                    presa = float(chartLine[286:301])
                    gprea = float(chartLine[301:])
                except:
                    print("Plot.on_timer: energy line missed.")
                    pass

                #try:
                #print "addValuesFromNamd",time,self.prevEnergyStep,self.plotType
                if time != None and time > self.prevEnergyStep:
                    self.addValues(
                        ["Bond", "Angle", "Dihedral", "Improper", "Electric", "Van der Waals", "Boundary", "Miscelaneous", "Kinetic", "tot", "Temperature", "Potential", "tot3", "Temperature Average", "Pressure", "G-Pressure", "Volume", "Pressure Average", "G-Pressure Average"],
                        time,
                        [bond, angle, dih, impr, elec, vdw, bound, misc, kine, tot, temp, pot, tot3, tempa, pres, gpres, vol, presa, gprea]
                    )
                self.prevEnergyStep = time

                #except:
                #    print "simTab.on_timer: problems updating plots."

            #elif linea[0:4] == "Info" or linea[0:3] == "LDB" or linea[0:7] == "Warning":
                #print linea
            else:
                pass
    
    def addValuesFromIMD(self, imdEnergies):
        #if imdEnergies != None:
        #	print "addValuesFromIMD ",imdEnergies.tstep,self.prevEnergyStep 
        #else: print "addValuesFromIMD None"

        if imdEnergies != None and imdEnergies.tstep != None and imdEnergies.tstep > self.prevEnergyStep:
            #print "addValuesFromIMD ", imdEnergies.tstep, imdEnergies.Epot
            vdw     = imdEnergies.Evdw
            bond    = imdEnergies.Ebond
            angle   = imdEnergies.Eangle
            dih     = imdEnergies.Edihe
            impr    = imdEnergies.Eimpr
            elec    = imdEnergies.Eelec
            #bound  = 0.0
            #misc   = 0.0
            pot     = imdEnergies.Epot
            tot     = imdEnergies.Etot
            kine    = tot - elec - dih - impr - bond - angle - vdw
            
            self.addValues(
                ["Van der Waals","Bond","Angle","Dihedral","Improper","Electric","Kinetic","Potential","Total"],
                imdEnergies.tstep,
                [vdw,bond,angle,dih,impr,elec,kine,pot,tot]
            )

            self.prevEnergyStep = imdEnergies.tstep

    
    def reset(self):
        for t in list(self.charts.keys()):
            self.charts[t][self.xpos] = []
            self.charts[t][self.ypos] = []
        self.setType(self.plotType)
        self.prevEnergyStep = -1
        
    def setType(self, newType):
        self.plotType = newType
        self.x        = self.charts[newType][self.xpos]
        self.y        = self.charts[newType][self.ypos]
        
        if self.curve != None:
            self.curve.detach()
        
        self.curve  = Qwt.QwtPlotCurve(newType)
        self.curve.attach(self)
        self.curve.setPen(Qt.QPen(self.charts[newType][self.colorpos]))
        
        self.setTitle(newType)
        self.updateCurve()

    def types(self):
        return list(self.charts.keys())
    
    def updateCurve(self):
        if len(self.x) > self.xrange:
            self.setAxisScale(Qwt.QwtPlot.xBottom, self.x[int(-self.xrange)], self.x[-1], 0)
            self.curve.setData(self.x[int(-self.xrange):], self.y[int(-self.xrange):])
        elif len(self.x) > 0:
            self.setAxisScale(Qwt.QwtPlot.xBottom, self.x[0], self.x[-1], 0)
            self.curve.setData(self.x, self.y)
        
        if len(self.y) > 0:
            if max(self.y) - min(self.y) < self.tolerance:
                av = float(sum(self.y)) / len(self.y)
                self.average.setData([], [])
            else:
                xrange = max(0,int(len(self.x)-self.xrange))
                xx = self.x[xrange:]
                yy = self.y[xrange:]
                A = array([xx, ones(len(xx))])
                slope, intercept = linalg.lstsq(A.T, yy)[0]
                y0 = slope*xx[0] + intercept
                y1 = slope*xx[-1] + intercept
                self.average.setData([xx[0], xx[-1]], [y0, y1])
                p = mean(yy)
                s = 2. * std(yy)
                #print "updateCurve ", yy, p, s
                self.setAxisScale(Qwt.QwtPlot.yLeft, max(p-s,min(yy)), min(p+s,max(yy)), 0)

    def mousePressEvent(self, event):
        if event.button() == 1: # left-button click
            keys = list(self.charts.keys())
            keys.sort()
            self.setType(keys[(keys.index(self.plotType)+1)%len(keys)])
        elif event.button() == 2: # right-button click
            self.saveData()
    
    def saveData(self):
        msg     = 'Save ' + self.plotType + ' Chart Data'
        date    = datetime.datetime.now().strftime("%Y-%m-%d at %I.%M.%S %p")
        name    = self.plotType + " Wolffia data " + date + ".csv"
        
        file    = str(QtGui.QFileDialog.getSaveFileName(self, msg, name, '*.csv'))
        
        if len(file) > 0:
            output = open(file, 'w')
            output.write("Step, " + self.plotType + "\n")
            for i in range(len(self.charts[self.plotType][0])):
                output.write("{0}, {1}\n".format(self.charts[self.plotType][0][i], self.charts[self.plotType][1][i]))
            output.close()




class EnergyPlot(Plot):
    
    def __init__(self, plotType="Total", parent=None):
        self.energy = {
            "Van der Waals":	[[], [], Qt.Qt.red			   ],
            "Bond":			 [[], [], Qt.Qt.green			 ],
            "Angle":			[[], [], Qt.Qt.blue			  ],
            "Dihedral":		 [[], [], Qt.Qt.cyan			  ],
            "Improper":		 [[], [], Qt.Qt.magenta		   ],
            "Electric":		 [[], [], Qt.Qt.yellow			],
            #"Boundary":		[[], [], QtGui.QColor(128,  0,   0, 255)],
            #"Miscelaneous":	[[], [], QtGui.QColor(0,  128,   0, 255)],
            "Kinetic":		  [[], [], QtGui.QColor(0,	0, 128, 255)],
            "Potential":		[[], [], QtGui.QColor(128,128,   0, 255)],
            "Total":			[[], [], QtGui.QColor(128,  0, 128, 255)]
        }
        self = Plot.__init__(self, "EnergyPlot", self.energy, plotType, parent)


class KineticsPlot(Plot):
        
        def __init__(self, plotType="Total", parent=None):
            self.kinetics = {
                "Temperature":		  [[], [], Qt.Qt.red			   ],
                "Temperature Average":  [[], [], Qt.Qt.green			 ],
                "Pressure":			 [[], [], Qt.Qt.blue			  ],
                "Pressure Average":	 [[], [], Qt.Qt.cyan			  ],
                "G-Pressure":		   [[], [], Qt.Qt.magenta		   ],
                "G-Pressure Average":   [[], [], Qt.Qt.yellow			],
                "Volume":			   [[], [], QtGui.QColor(128,  0, 128, 255)]
            }
            self = Plot.__init__(self, "KineticsPlot", self.kinetics, plotType, parent)
