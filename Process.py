"""
.. module:: Process
:platform: Unix,Windows
:synopsis: Service for starting subprocess task

.. moduleauthor:: Erthalion

"""
import sys
import os
import logging
import subprocess

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                   )

class ProcessService():
    def __init__(self):
        pass

    def startWithStdIO(self,cmd):
        '''
        start for collect std output (for get runtime info)
        '''
        print cmd
        proc = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,close_fds=True)
        return (proc.stdin,proc.stdout)

    def start(self,cmd):
        '''
        simple start (for gnuplot animation and mencoder)
        '''
        print cmd
        subprocess.call(cmd,shell=True)

    def startAsync(self,cmd):
        pass
