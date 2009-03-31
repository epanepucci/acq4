# -*- coding: utf-8 -*-
import threading, os, fcntl, time, re, types
from functions import strncmp
from MetaArray import MetaArray

class Locker:
    def __init__(self, lock):
        self.lock = lock
        self.lock.acquire()
    def __del__(self):
        self.lock.release()

class DataManager:
    """Class for creating and caching DataHandler objects to make sure there is only one manager object per directory. 
    This class is thread-safe.
    
    ONE OBJECT IS GENERATED BY THE LIBRARY, DO NOT CREATE YOUR OWN! Use createDataHandler as your starting point."""
    
    def __init__(self, password=None, baseDir=None):
        if password != "do not copy this password":
            raise Exception("Applications should not create their own Factories, use createDataHandler as a starting point.")
        self.dm = {}
        self.lock = threading.RLock()
        self.baseDir = baseDir
        
    def getDM(self, dirName, create=False):
        l = Locker(self.lock)
        if not self.dm.has_key(dirName):
            self.dm['dirName'] = DataHandler(self, dirName, create=create)
        dm = self.dm['dirName']
        return dm
        
    def getBaseDir(self):
        l = Locker(self.lock)
        return self.getDM(self.baseDir)
        
    def setBaseDir(self, d):
        l = Locker(self.lock)
        self.baseDir = d

GLOBAL_DMFACTORY = DataManager("do not copy this password")

def createDataHandler(baseDir, create=False):
    global GLOBAL_DMFACTORY
    return GLOBAL_DMFACTORY.getDM(baseDir, create=create)




class DataHandler:
    def __init__(self, manager, baseDir, create=False):
        self.manager = manager
        self.baseDir = baseDir
        if self.baseDir[-1] != '/':
            self.baseDir += '/'
        self.indexFile = self.baseDir+'.index'
        self.logFile = self.baseDir+'.log'
        
        self.lock = threading.RLock()
        
        if not os.path.isdir(baseDir):
            if create:
                os.mkdir(baseDir)
            else:
                raise Exception("Directory %s does not exist." % baseDir)
        
        if os.path.isfile(self.indexFile):
            self._readIndex()
        else:
            self.index = {}
            self._writeIndex()
        
    def __del__(self):
        pass
    
    def __getitem__(self, item):
        if type(item) is types.StringType:
            return self.getDir(item)
        elif type(item) is types.TupleType:
            dm = self
            for d in item:
                dm = dm.getDir(d)
            return dm
    
    def _readIndex(self, lock=True):
        l = Locker(self.lock)
        fd = open(self.indexFile)
        if lock:
            fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            self.index = eval(fd.read())
        except:
            print "***************Error while reading index file %s!*******************" % self.indexFile
            raise
        fd.close()
        
    def _writeIndex(self, lock=True):
        l = Locker(self.lock)
        fd = open(self.indexFile, 'w')
        if lock:
            fcntl.flock(fd, fcntl.LOCK_EX)
        fd.write(str(self.index))
        fd.close()
    
    def logMsg(self, msg):
        """Write a message into the log for this directory."""
        l = Locker(self.lock)
        t = time.strftime('[20%y.%m.%d %H:%m:%S]')
        fd = open(self.logFile, 'a')
        fcntl.flock(fd, fcntl.LOCK_EX)
        fd.write('%s %s\n' % (t, msg))
        fd.close()
    
    def mkdir(self, name, autoIndex=False, info={}):
        """Create a new subdirectory, return a new DataHandler object. If autoIndex is true, add a number to the end of the dir name if it already exists."""
        l = Locker(self.lock)
        
        if autoIndex:
            fullName = name+"_000"
        else:
            fullName = name
            
        if os.path.isdir(self.baseDir+fullName):
            if autoIndex:
                files = os.listdir(self.baseDir)
                files = filter(lambda f: re.match(name + r'_\d+$', f), files)
                files.sort()
                maxVal = int(files[-1][-3:])
                fullName = name + "_%03d" % (maxVal+1)
            else:
                raise Exception("Directory %s already exists." % (self.baseDir+fullName))
            
        ndm = self.manager.getDM(self.baseDir+fullName, create=True)
        self.addFile(fullName, info)
        return ndm
    
    def getDir(self, subdir, create=False):
        """Return a DataHandler for the specified subdirectory. If the subdir does not exist, it will be created only if create==True"""
        l = Locker(self.lock)
        ndir = self.baseDir+subdir
        if os.path.isdir(ndir):
            return self.manager.getDM(ndir)
        else:
            if create:
                return self.mkdir(subdir)
            else:
                raise Exception('Directory %s does not exist.' % ndir)
        
    def dirExists(self, dirName):
        return os.path.isdir(self.baseDir+dirName)
            
    def getToday(self):
        #yr = self.getDir(time.strftime("20%y"), create=True)
        #mo = yr.getDir(time.strftime("%m"), create=True)
        #return mo.getDir(time.strftime("%d"), create=True)
        return self.getDir(time.strftime("20%y.%m.%d"), create=True)
    
    
    def ls(self):
        """Return a list of all managed files in the directory"""
        l = Locker(self.lock)
        self._readIndex()
        ls = self.index.keys()
        ls.sort(strncmp)
        return ls
    
    def fileInfo(self, file):
        """Return a dict of the meta info stored for file"""
        l = Locker(self.lock)
        self._readIndex()
        if self.index.has_key(file):
            return self.index[file]
        else:
            raise Exception("File %s is not indexed" % file)
    
    def writeFile(self, obj, fileName, info={}, autoIncrement=False):
        """Write a file to this directory using obj.write(fileName), store info in the index."""
        t = time.time()
        l = Locker(self.lock)
        fn = self.baseDir+fileName
        if autoIncrement:
            d = 0
            while True:
                fn1 = "%s_%04d" % (fn, d)
                if not os.path.exists(fn1):
                    fn = fn1
                    break
                d += 1
        fd = open(fn, 'w')
        fcntl.flock(fd, fcntl.LOCK_EX)
        obj.write(fn)
        fd.close()
        if not info.has_key('__object_type__'):
            info['__object_type__'] = str(type(obj))
        if not info.has_key('__timestamp__'):
            info['__timestamp__'] = t
        self.setFileInfo(fileName, info)
    
    def addFile(self, file, info={}, protect=False):
        """Add a pre-existing file into the index. Overwrites any pre-existing info for the file unless protect is True"""
        l = Locker(self.lock)
        fn = self.baseDir+file
        if not (os.path.isfile(fn) or os.path.isdir(fn)):
            raise Exception("File %s does not exist." % fn)
        if protect and self.index.has_key(file):
            raise Exception("File %s is already indexed." % file)
        self.setFileInfo(file, info)
    
    def setFileInfo(self, file, info):
        l = Locker(self.lock)
        fd = open(self.indexFile, 'r')
        fcntl.flock(fd, fcntl.LOCK_EX)
        self._readIndex(lock=False)
        self.index[file] = info
        self._writeIndex(lock=False)
        fd.close()
        
    def setFileAttr(file, attr, value):
        l = Locker(self.lock)
        if not self.index.has_key('file'):
            self.setFileInfo(file, {attr: value})
        else:
            fd = open(self.indexFile, 'r')
            fcntl.flock(fd, fcntl.LOCK_EX)
            self._readIndex(lock=False)
            self.index[file][attr] = value
            self._writeIndex(lock=False)
            fd.close()
        
    def parent(self):
        pdir = re.sub(r'/[^/]+/$', '', self.baseDir)
        return self.manager.getDM(pdir)

    def getFile(self, fileName):
        ## Todo: Make this function check __object_type__ and dynamically determine what kind of object to create
        return MetaArray(file=self.baseDir + fileName)





class FakeDataHandler:
    def __init__(self, *args):
        pass    
    def __del__(self):
        pass
    
    def logMsg(self, *args):
        pass
    
    def mkdir(self, *args):
        return self
    
    def getDir(self, *args):
        return self
        
    def dirExists(self, *args):
        return False
            
    def getToday(self):
        return self
    
    def ls(self):
        return []
    
    def fileInfo(self, *args):
        return {}
    
    def writeFile(self, *args):
        pass
    
    def addFile(self, *args):
        pass
    
    def setFileInfo(self, *args):
        pass
        
    def setFileAttr(file, *args):
        pass
        
    def parent(self):
        return self
