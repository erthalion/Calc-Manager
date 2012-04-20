"""
.. module:: GnuPlot
:platform: Unix,Windows
:synopsis: Service for plotting with gnuplot

.. moduleauthor:: Erthalion

"""
import sys
import os
import logging
import IPlotService

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                   )

class GnuPlotService():
    def __init__(self):
        pass


    '''filename without extension
    '''
    def plotAnimation(self,filename,countIterations):
        gnuplotScript = open(filename+".gpi","w")
        gnuplotScript.writelines({"clear\n",
                                  "reset\n",
                                  "set terminal gif animate delay 10\n",
                                  "set output"+filename+".gif\n",
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
            gnuplotScript.write("splot \""+filename+".dat\" index "+str(i)+" using 1:2:3 with pm3d t \"waves\"")

        os.popen4("gnuplot "+filename+".gpi")

    def convertToVideo(self,filename):
        os.popen4("mencoder "+filename+".gif -mf fps=25 -o "+filename+".avi -ovc lavc -lavcopts vcodec=mpeg4")
