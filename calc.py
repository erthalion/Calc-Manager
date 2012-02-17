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
        dateCalc = strftime("%Y-%m-%d:%H-%M-"+str(i))
        os.mkdir(dateCalc)
        
        description=open("./"+dateCalc+"/Description.txt","w")
        description.write(schema.descriptions[i])
        description.close()

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
