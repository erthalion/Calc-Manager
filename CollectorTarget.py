import logging
from lxml import etree

def setValue(dictionary,key,parameter,index):
    dictionary[index][key]=parameter.text

class CollectorTarget:
    calculations=[]
    parameters=[]
    area=[]
    descriptions=[]
    preprocesses=[]
    postprocesses=[]

    def __init__(self,data):
        tree = etree.XML(data)
        calcus = tree.xpath('/experiment/calculation')

        for index,calc in enumerate(calcus):
            '''
            add empty element for dict
            '''
            self.calculations.append(calc.attrib)
            self.parameters.append({})
            self.area.append({})
            self.preprocesses.append({})
            self.postprocesses.append({})

            for param in list(calc):
                if param.tag == 'description':
                    self.descriptions.append(param.text)

                if param.tag == 'parameters':
                    for parameter in list(param):
                        setValue(self.parameters,parameter.tag,parameter,index)

                if param.tag == 'area':
                    for area in list(param):
                        setValue(self.area,area.tag,area,index)

                if param.tag == 'preprocess':
                    for preprocess in list(param):
                        setValue(self.preprocesses,preprocess.tag,preprocess,index)

                if param.tag == 'postprocess':
                    for postprocess in list(param):
                            setValue(self.postprocesses,postprocess.tag,postprocess,index)

