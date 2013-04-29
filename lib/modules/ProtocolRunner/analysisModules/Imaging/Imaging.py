# -*- coding: utf-8 -*-
from lib.modules.ProtocolRunner.analysisModules import AnalysisModule
from lib.Manager import getManager
from PyQt4 import QtCore, QtGui
from imagingTemplate import Ui_Form
import numpy as np
import pyqtgraph as pg
import functions as fn
import metaarray




class ImagingModule(AnalysisModule):
    def __init__(self, *args):
        AnalysisModule.__init__(self, *args)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.postGuiInit()
        self.man = getManager()
        self.image=pg.ImageItem()
        self.ui.histogram.setImageItem(self.image)
        self.ui.histogram.autoHistogramRange()
        self.ui.plotWidget.addItem(self.image)
        self.ui.plotWidget.setLabel('bottom', 'Time', 's')
        self.ui.plotWidget.setLabel('left', 'Distance', 'm')
        self.ui.plotWidget.register('ImagingPlot')
        self.ui.alphaSlider.valueChanged.connect(self.imageAlphaAdjust)        
        self.img = None  ## image shown in camera module

        self.ui.scannerComboBox.setTypes('scanner')
        self.ui.detectorComboBox.setTypes('daqChannelGroup')
                
    def quit(self):
        AnalysisModule.quit(self)
        
    def protocolStarted(self, *args):
        pass
    
    def protocolFinished(self):
        pass
        
    def newFrame(self, frame):
        """
        Called when protocol is finished (truly completes, no errors/abort)
        frame contains all of the data returned from all devices
        """
        imageDownSample = self.ui.downSampling.value() # this is the "image" downsample,
        # get the downsample for the daq. This is far more complicated than it should be...
        finfo = frame['result'][self.detectorDevice()]["Channel":'Input']
        info = finfo.infoCopy()
        #if 'downsampling' in info[1]['DAQ']['Input'].keys():
            #daqDownSample = info[1]['DAQ']['Input']['downsampling']
        #else:
            #daqDownSample = 1
        daqDownSample = info[1]['DAQ']['Input'].get('downsampling', 1)
        if daqDownSample != 1:
            raise HelpfulException("Set downsampling in DAQ to 1!")
        # get the data and the command used on the scanner
        pmtdata = frame['result'][self.detectorDevice()]["Channel":'Input'].asarray()
        t = frame['result'][self.detectorDevice()].xvals('Time')
        dt = t[1]-t[0]
        progs = frame['cmd'][self.scannerDevice()]['program']
        if len(progs) == 0:
            self.image.setImage(np.zeros((1,1)))
            return
        prog = progs[0]
        nscans = prog['nScans']
        limits = prog['points']
        dist = (pg.Point(limits[0])-pg.Point(limits[1])).length()
        startT = prog['startTime']
        endT = prog['endTime']
        
        if prog['type'] == 'lineScan':
            totSamps = prog['samplesPerScan']+prog['samplesPerPause']
            imageData = pmtdata[prog['startStopIndices'][0]:prog['startStopIndices'][0]+nscans*totSamps]
            imageData=imageData.reshape(nscans, totSamps)
            imageData = imageData[:,0:prog['samplesPerScan']] # trim off the pause data
            imageData = fn.downsample(imageData, imageDownSample, axis=1)
            self.image.setImage(imageData)
            self.image.setRect(QtCore.QRectF(startT, 0.0, endT-startT, dist ))
            self.ui.plotWidget.autoRange()
            self.ui.histogram.imageChanged(autoLevel=True)
            storeFlag = frame['cmd']['protocol']['storeData'] # get flag 
            print "before StoreFlag and storeflag is:", storeFlag
            if storeFlag:
                dirhandle = frame['cmd']['protocol']['storageDir'] # grab directory
                self.info={'detector': self.detectorDevice(), 'scanner': self.scannerDevice(), 'indices': prog['startStopIndices'], 
                           'samplesPerScan': prog['samplesPerScan'], 'nscans': prog['nScans'], 'positions': [[prog['points'][0].x(), prog['points'][0].y()], [prog['points'][1].x(), prog['points'][1].y()]],
                           'downSample': downSample, 'daqDownSample': daqDownSample}

                info = [dict(name='Time', units='s', values=t[prog['startStopIndices'][0]:prog['startStopIndices'][1]:prog['samplesPerScan']]), dict(name='Distance'), self.info]
                ma = metaarray.MetaArray(imageData, info=info)
                print 'I am writing imaging.ma'
                dirhandle.writeFile(ma, 'Imaging.ma')

        if prog['type'] == 'multipleLineScan':
            totSamps = int(np.sum(prog['scanPointList'])) # samples per scan, before downsampling
            imageData = pmtdata[prog['startStopIndices'][0]:prog['startStopIndices'][0]+int((nscans*totSamps))].copy()           
            imageData = imageData.reshape(nscans, totSamps)
            csum = np.cumsum(prog['scanPointList'])
            for i in xrange(0, len(csum), 2):
                    imageData[:,csum[i]:csum[i+1]] = 0

            #imageData = imageData[:,0:prog['samplesPerScan']] # trim off the pause data
            imageData = fn.downsample(imageData, imageDownSample, axis=1)
            self.image.setImage(imageData)
            self.image.setRect(QtCore.QRectF(startT, 0.0, totSamps*dt*nscans, dist ))
            self.ui.plotWidget.autoRange()
            self.ui.histogram.imageChanged(autoLevel=True)
            storeFlag = frame['cmd']['protocol']['storeData'] # get flag 
            print "before StoreFlag and storeflag is:", storeFlag
            print frame['cmd']
            if storeFlag:
                dirhandle = frame['cmd']['protocol']['storageDir'] # grab directory
                self.info={'detector': self.detectorDevice(), 'scanner': self.scannerDevice(), 'indices': prog['startStopIndices'], 
                           'scanPointList': prog['scanPointList'], 'nscans': prog['nScans'], 
                           'positions': prog['points'],
                           'downSample': imageDownSample, 'daqDownSample': daqDownSample}
                print 'totSamps: ', totSamps
                print 'prog[startstop..]: ', prog['startStopIndices']
                info = [dict(name='Time', units='s', values=t[prog['startStopIndices'][0]:prog['startStopIndices'][1]-int(totSamps):int(totSamps)]), dict(name='Distance'), self.info]
                ma = metaarray.MetaArray(imageData, info=info)
                print 'I am writing imaging.ma'
                dirhandle.writeFile(ma, 'Imaging.ma')
                raise Exception()

        if prog['type'] == 'rectScan':
            samplesPerScan = int((prog['startStopIndices'][1]-prog['startStopIndices'][0])/prog['nScans'])
            print samplesPerScan
            imageData = pmtdata[prog['startStopIndices'][0]:prog['startStopIndices'][0] +nscans*samplesPerScan]
            imageData=imageData.reshape(nscans, samplesPerScan)
            imageData = fn.downsample(imageData, imageDownSample, axis=1)
            self.image.setImage(imageData)
            limits = prog['points']
            #self.image.setRect(QtCore.QRectF(startT, 0.0, totSamps*dt*nscans,  ))
            self.ui.plotWidget.autoRange()
            self.ui.histogram.imageChanged(autoLevel=True)

            sd = self.pr.getDevice(self.scannerDevice())
            camMod = sd.cameraModule().window()
            if self.img is not None:
                camMod.removeItem(self.img)
                self.img = None
            self.img = pg.ImageItem(imageData)
            camMod.addItem(self.img)
            w = imageData.shape[0]
            h = imageData.shape[1]
            localPts = map(pg.Vector, [[0,0], [w,0], [0,h], [0,0,1]]) # w and h of data of image in pixels.
            globalPts = prog['points'] # sort of. - 
            m = pg.solve3DTransform(localPts, map(pg.Vector, globalPts+[[0,0,1]]))
            m[:,2] = m[:,3]
            m[2] = m[3]
            m[2,2] = 1
            tr = QtGui.QTransform(*m[:3,:3].transpose().reshape(9))
            self.img.setTransform(tr)
            #if storeFlag:
                #dirhandle = frame['cmd']['protocol']['storageDir'] # grab directory
                #self.info={'detector': self.detectorDevice(), 'scanner': self.scannerDevice(), 'indices': prog['startStopIndices'], 
                           #'samplesPerScan': prog['samplesPerScan'], 'nscans': prog['nScans'], 'positions': [[prog['points'][0].x(), prog['points'][0].y()], [prog['points'][1].x(), prog['points'][1].y()]],
                           #'downSample': downSample}
                #print dict
                # to line below, add x, y for the camera (look at camera video output)
                #info = [dict(name='Time', units='s', values=t[prog['startStopIndices'][0]:prog['startStopIndices'][1]:prog['samplesPerScan']]), dict(name='Distance'), self.info]
                #ma = metaarray.MetaArray(imageData, info=info)
                #dirhandle.writeFile(ma, 'Imaging.ma')
        
        
    def imageAlphaAdjust(self):
        if self.img is None:
            return
        alpha = self.ui.alphaSlider.value()
        self.img.setImage(opacity=float(alpha/100.))
        
        
    def detectorDevice(self):
        return str(self.ui.detectorComboBox.currentText())
        
    def scannerDevice(self):
        return str(self.ui.scannerComboBox.currentText())
        
        

        