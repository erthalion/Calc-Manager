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
import Task
import uuid
import GnuPlot
from CollectorTarget import CollectorTarget
from time import strftime
from lxml import etree

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                   )

class TaskManager:
    """It's presentation of calculation task

    .. note:: architecture!!!
    """

    def __init__(self,schema):
        """
        Args:
        schema (CollectorTarget): data, wich describing calculation task
        """

        self.schema=schema
        self.taskList=[]
        self.logger = logging.getLogger('TaskManager')

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

        uid = uuid.uuid1()
        dateCalc = strftime("%Y-%m-%d:%H-%M-"+str(uid))
        print dateCalc

        try:
            os.mkdir(dateCalc)
            description=open("./"+dateCalc+"/Description.txt","w")
            description.write(descrText)
            description.close()
        except:
            sys.exit("could't write descr file\n")

        return dateCalc,uid

    def start(self):
        """Start calculation with prebuild/postbuild
        """

        loop=True

        for i in range(0,len(self.schema.calculations)):
            dateCalc,uid=self.__createDescription__(i)
            #process
            self.taskList.append(Task.Task(self.schema,i,dateCalc,uid))
            self.taskList[i].setPlotService(GnuPlot.GnuPlotService())
            self.taskList[i].start()


        return self.taskList
