#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import logging


dirname = os.path.dirname(os.path.realpath( __file__ ))

sys.path.append( os.path.join(dirname,'..','..') )
import apppath


class AudioNotify:
    def __init__(self,params):
        self.temporaryDirectory = apppath.pathTemporary('audionotify')

        self.pathSoundClipBackupStarted = None

        if params['audionotify_url_backupstarted']:
            url = params['audionotify_url_backupstarted']
            self.pathSoundClipBackupStarted = os.path.join(self.temporaryDirectory,'audionotify_url_backupstarted')

            if not os.path.isfile(self.pathSoundClipBackupStarted):
                AudioNotify._loadSoundUrlToFile(url,self.pathSoundClipBackupStarted)

        self.pathSoundClipBackupFinished = None

        if params['audionotify_url_backupfinished']:
            url = params['audionotify_url_backupfinished']
            self.pathSoundClipBackupFinished = os.path.join(self.temporaryDirectory,'audionotify_url_backupfinished')

            if not os.path.isfile(self.pathSoundClipBackupFinished):
                AudioNotify._loadSoundUrlToFile(url,self.pathSoundClipBackupFinished)

        self.pathSoundClipRipStarted = None

        if params['audionotify_url_ripstarted']:
            url = params['audionotify_url_ripstarted']
            self.pathSoundClipRipStarted = os.path.join(self.temporaryDirectory,'audionotify_url_ripstarted')

            if not os.path.isfile(self.pathSoundClipRipStarted):
                AudioNotify._loadSoundUrlToFile(url,self.pathSoundClipRipStarted)

        self.pathSoundClipRipFinished = None

        if params['audionotify_url_ripfinished']:
            url = params['audionotify_url_ripfinished']
            self.pathSoundClipRipFinished = os.path.join(self.temporaryDirectory,'audionotify_url_ripfinished')

            if not os.path.isfile(self.pathSoundClipRipFinished):
                AudioNotify._loadSoundUrlToFile(url,self.pathSoundClipRipFinished)
                
        if params['audionotify_url_error']:
            url = params['audionotify_url_error']
            self.pathSoundClipError = os.path.join(self.temporaryDirectory,'audionotify_url_error')
            
            if not os.path.isfile(self.pathSoundClipError):
                AudioNotify._loadSoundUrlToFile(url,self.pathSoundClipError)

        logging.debug('AudioNotify initialized with config: ' + str(params))
        
    def __repr__(self):
        return "<AudioNotify>"

    def startedBackingUpDisc(self,discName):
        if self.pathSoundClipBackupStarted is not None:
            AudioNotify._playSound( self.pathSoundClipBackupStarted )

    def finishedBackingUpDisc(self,discName):
        if self.pathSoundClipBackupFinished is not None:
            AudioNotify._playSound( self.pathSoundClipBackupFinished )

    def startedRippingTracks(self,tracks,discName):
        if self.pathSoundClipRipStarted is not None:
            AudioNotify._playSound( self.pathSoundClipRipStarted )

    def finishedRippingTracks(self,tracks,discName,ripTracksDict={}):
        if self.pathSoundClipRipFinished is not None:
            AudioNotify._playSound( self.pathSoundClipRipFinished )

    def failure(self,discName,errorMessage):
        if self.pathSoundClipError is not None:
            AudioNotify._playSound( self.pathSoundClipError )

    @staticmethod
    def _loadSoundUrlToFile(urlLoad,fileToSave):
        import urllib2
        
        response = urllib2.urlopen(urlLoad).read()
        
        f = open(fileToSave,'w')
        f.write(response)
        f.close()

    @staticmethod
    def _playSound(soundFile):
        import platform

        platformName = platform.system().lower().strip()
        
        import subprocess

        #Can only run on Macs
        if platformName == 'darwin':
            subprocess.check_output(['afplay',soundFile])

        elif platformName == 'linux':
            subprocess.check_output(['aplay',soundFile])


def test():
     params = {}
     params['audionotify_url_backupstarted'] = 'http://soundbible.com/grab.php?id=1997&type=wav'
     params['audionotify_url_backupfinished'] = None
     params['audionotify_url_ripstarted'] = 'http://soundbible.com/grab.php?id=1997&type=wav'
     params['audionotify_url_ripfinished'] = None
     params['audionotify_url_error'] = 'http://soundbible.com/grab.php?id=1997&type=wav'

     m = AudioNotify(params)
     m.startedBackingUpDisc('MOVIENAME')
     m.finishedBackingUpDisc('MOVIENAME')
     m.startedRippingTracks([],'MOVIENAME')
     m.finishedRippingTracks([],'MOVIENAME')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test()

