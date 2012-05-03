"""
.. module:: GnuPlot
:platform: Unix,Windows
:synopsis: Service for plotting with gnuplot

.. moduleauthor:: Erthalion

"""
import sys
import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                   )

class GnuPlotService():
    def __init__(self):
        self.logger = logging.getLogger('GnuPlotService')
        self.logger.debug("__init__")


    '''filename without extension
    '''
    def plotAnimation(self,filename,countIterations):
        gnuplotScript = open(filename+".gpi","w")
        gnuplotScript.writelines({"clear\n",
                                  "reset\n",
                                  "set terminal gif animate delay 10\n",
                                  "set output \""+filename+".gif\"\n",
                                  "set isosample 40,40\n",
                                  "set hidden3d\n",
                                  "set xrange [0:1]\n",
                                  "set xlabel \"X\"\n",
                                  "set yrange [0:1]\n",
                                  "set ylabel \"Y\"\n",
                                  "set xrange [-0.003:0.007]\n",
                                  "set zlabel \"Z\"\n",
                                  "set cbrange [-0.003:0.007]\n"})
        for i in range(0,countIterations):
            gnuplotScript.write("splot \""+filename+".dat\" index "+str(i)+" using 1:2:3 with pm3d t \"waves\"\n")

        cmd = "gnuplot "+filename+".gpi"
        self.processService.start(cmd)

    def convertToVideo(self,filename):
        cmd="mencoder "+filename+".gif -mf fps=25 -o "+filename+".avi -ovc lavc -lavcopts vcodec=mpeg4"
        self.processService.start(cmd)

    def setProcessService(self,processService):
        self.processService = processService
