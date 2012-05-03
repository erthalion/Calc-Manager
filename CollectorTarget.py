import logging

class CollectorTarget:
    calculations=[]
    parameters=[]
    area=[]
    descriptions=[]
    is_descr=False

    def __init__(self):
        is_descr=False
        self.logger = logging.getLogger('CollectorTarget')
        self.logger.debug("__init__")


    def start(self, tag, attrib):
        if tag == 'Calculation':
            self.calculations.append(attrib)
        if tag == 'Parameters':
            self.parameters.append(attrib)
        if tag == 'Area':
            self.area.append(attrib)
        if tag == 'Description':
            self.is_descr=True

    def data(self, data):
        if(self.is_descr):
            self.descriptions.append("%s" % (data))

    def end(self,tag):
        if tag == 'Description':
            self.is_descr = False
