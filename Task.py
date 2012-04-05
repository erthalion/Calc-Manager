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
from CollectorTarget import CollectorTarget
from time import strftime
from lxml import etree

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                   )

class Task:
    """It's presentation of calculation task

    .. note:: architecture!!!
    """

    def __init__(self,schema):
        """
        Args:
        schema (CollectorTarget): data, wich describing calculation task
        """
        
        self.schema=schema
        self.logger = logging.getLogger('Task')

    def __createDescription__(self,i):
        """Create metadata with descrition of calculations
        Args:
        i (int): number of calculation
        """

        descrText = str.format("Area parameters:\nHeight {0}\nLenght {1}\nNx {2}\nNy{3}\n",
                               self.schema.area[i]['Height'],
                               self.schema.area[i]['Length'],
                               self.schema.area[i]['NodeX'],
                               self.schema.area[i]['NodeY'])
        descrText+=str.format("Task parameters:\nPrecision {0}\nTime {1}\nTimeStep {2}\n",
                              self.schema.parameters[i]['Precision'],
                              self.schema.parameters[i]['Time'],
                              self.schema.parameters[i]['TimeStep'])
        descrText+=self.schema.descriptions[i]
        dateCalc = strftime("%Y-%m-%d:%H-%M-"+str(i))
        print dateCalc

        try:
            os.mkdir(dateCalc)
            description=open("./"+dateCalc+"/Description.txt","w")
            description.write(descrText)
            description.close()
        except:
            sys.exit("could't write descr file\n")

        return dateCalc

    def start(self):
        """Start calculation with prebuild/postbuild
        """

        loop=True

        for i in range(0,len(self.schema.calculations)):
            dateCalc=self.__createDescription__(i)
            #process
            runCmd = str.format("./{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}",
                                self.schema.calculations[i]['Filename'],
                                self.schema.area[i]['Height'],
                                self.schema.area[i]['Length'],
                                self.schema.area[i]['NodeX'],
                                self.schema.area[i]['NodeY'],
                                self.schema.parameters[i]['Precision'],
                                dateCalc+"/"+self.schema.parameters[i]['OutputFile']+".dat",
                                self.schema.parameters[i]['Time'],
                                self.schema.parameters[i]['TimeStep'],
                                self.schema.parameters[i]['Frequency'])
            w,rr=os.popen4(runCmd)
            input=[rr]
            while loop:
                r,w,e=select.select(input,[],[])
                for op in r:
                    s=op.readline()
                    s=s.rstrip()
                    if s=='stop':
                        self.logger.debug("stopping")
                        loop=False
                    if not s:
                        input.remove(op)
                    else:
                        print '>',s.rstrip()

            #postprocess
            time = int(self.schema.parameters[i]['Time'])/int(self.schema.parameters[i]['Frequency'])
            subprocess.call(["./"+self.schema.calculations[i]['PostBuild'],
                             dateCalc+"/"+self.schema.parameters[i]['OutputFile'],str(time)])
