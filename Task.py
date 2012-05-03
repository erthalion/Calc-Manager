"""
.. module:: Task
:platform: Unix,Windows
:synopsis: Task for calculation

.. moduleauthor:: Erthalion

"""
import sys
import os
import select
import subprocess
import logging
import uuid

from CollectorTarget import CollectorTarget
from time import strftime
from lxml import etree
from threading import Thread

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                   )

class Task(Thread):
    """It's presentation of calculation task

    .. note:: architecture!!!
    """

    def __init__(self,schema,number,dateCalc,uid):
        """
        Args:

        schema (CollectorTarget): data, wich describing calculation task
        """
        Thread.__init__(self)
        self.schema=schema
        self.uid=uid
        self.number=number
        self.dateCalc=dateCalc
        self.logger = logging.getLogger('Task')
        self.logger.debug("__init__")

    def getUid(self):
        return self.uid

    def setPlotService(self,plotService):
        self.plotService = plotService

    def setProcessService(self,processService):
        self.processService = processService
        self.plotService.setProcessService(processService)

    def run(self):
        """Start calculation with prebuild/postbuild
        """

        loop=True

        #preprocess
        self.processService.start("make -C Kurs")

        #process
        runCmd = str.format("./{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}",
                            self.schema.calculations[self.number]['Filename'],
                            self.schema.area[self.number]['Height'],
                            self.schema.area[self.number]['Length'],
                            self.schema.area[self.number]['NodeX'],
                            self.schema.area[self.number]['NodeY'],
                            self.schema.parameters[self.number]['Precision'],
                            self.dateCalc+"/"+self.schema.parameters[self.number]['OutputFile']+".dat",
                            self.schema.parameters[self.number]['Time'],
                            self.schema.parameters[self.number]['TimeStep'],
                            self.schema.parameters[self.number]['Frequency'])
        w, rr = self.processService.startWithStdIO(runCmd)
        input=[rr]
        while loop:
            r,w,e=select.select(input,[],[])
            for op in r:
                s=op.readline()
                s=s.rstrip()

                if s=='stop':
                    self.logger.debug("stopping")
                    loop=False
                    break

                if not s:
                    input.remove(op)
                #else:
                #    print '>',s.rstrip()


        #postprocess
        time = int(self.schema.parameters[self.number]['Time'])/int(self.schema.parameters[self.number]['Frequency'])
        self.plotService.plotAnimation(self.dateCalc+"/"+self.schema.parameters[self.number]['OutputFile'],time)
        self.plotService.convertToVideo(self.dateCalc+"/"+self.schema.parameters[self.number]['OutputFile'])
