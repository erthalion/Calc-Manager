import sys
import os
import subprocess
from CollectorTarget import CollectorTarget
from time import strftime
from lxml import etree

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: calc.py schema_file.xml\n")
    schema=CollectorTarget()
    parser = etree.XMLParser(target = schema)
    doc = etree.parse ( sys.argv[1],parser)

    for i in range(0,len(schema.calculations)):
        #create description file
        descrText = str.format("Area parameters:\nHeight {0}\nLenght {1}\nNx {2}\nNy{3}\n",
        schema.area[i]['Height'],
        schema.area[i]['Length'],
        schema.area[i]['NodeX'],
        schema.area[i]['NodeY'])

        descrText+=str.format("Task parameters:\nPrecision {0}\nTime {1}\nTimeStep {2}\n",
        schema.parameters[i]['Precision'],
        schema.parameters[i]['Time'],
        schema.parameters[i]['TimeStep'])

        descrText+=schema.descriptions[i]
        dateCalc = strftime("%Y-%m-%d:%H-%M-"+str(i))

        try:
            os.mkdir(dateCalc)
            description=open("./"+dateCalc+"/Description.txt","w")
            description.write(descrText)
            description.close()
        except:
            sys.exit("could't write descr file\n")

        #process
        subprocess.call(["./"+schema.calculations[i]['Filename'],
            schema.area[i]['Height'],
            schema.area[i]['Length'],
            schema.area[i]['NodeX'],
            schema.area[i]['NodeY'],
            schema.parameters[i]['Precision'],
            dateCalc+"/"+schema.parameters[i]['OutputFile']+".dat",
            schema.parameters[i]['Time'],
            schema.parameters[i]['TimeStep'],
            schema.parameters[i]['Frequency']
            ])
        
        #postprocess
        time = int(schema.parameters[i]['Time'])/int(schema.parameters[i]['Frequency'])
        subprocess.call(["./"+schema.calculations[i]['PostBuild'],
            dateCalc+"/"+schema.parameters[i]['OutputFile'],str(time)])
