#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
import threading
import logging
import StringIO
import TaskManager

from CollectorTarget import CollectorTarget
from lxml import etree

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                   )

def setValue(dictionary,key,parameter,index):
    dictionary[index][key]=parameter.text

class TaskRequestHandler( SocketServer.BaseRequestHandler):

    def __init__(self,request,client_address,server):
        self.logger = logging.getLogger('TaskRequestHandler')
        self.logger.debug('__init__')
        SocketServer.BaseRequestHandler.__init__(self,request,client_address,server)
        return

    def setup(self):
        self.logger.debug('setup')
        return SocketServer.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')

        data = self.request.recv(1024)
        self.logger.debug(data)

        clearData = data.replace('\n','')
        if clearData == 'shutdown':
            self.logger.debug('server shutdown!')
            response = 'server shutdown!'
            self.request.sendall(response)
            self.server.shutdown()
            return

        if clearData == 'echo':
            response = 'echo'
            self.request.sendall(response)
            return

        #schema=CollectorTarget()
        #parser = etree.XMLParser(target = schema)
        #doc = etree.XML(data,parser)

        tree = etree.XML(data)
        schema = CollectorTarget()
        calculations = tree.xpath('/experiment/calculation')

        Calculation=[]
        Parameters=[]
        Area=[]
        Preprocess=[]
        Postprocess=[]
        Description=[]

        for index,calc in enumerate(calculations):
            '''
            add empty element for dict
            '''
            Calculation.append(calc.attrib)
            Parameters.append({})
            Area.append({})
            Preprocess.append({})
            Postprocess.append({})

            for param in list(calc):
                if param.tag == 'description':
                    Description.append(param.text)

                if param.tag == 'parameters':
                    for parameter in list(param):
                        if parameter.tag == 'precision':
                            setValue(Parameters,'precision',parameter,index)

                        if parameter.tag == 'timestep':
                            setValue(Parameters,'timestep',parameter,index)

                        if parameter.tag == 'time':
                            setValue(Parameters,'time',parameter,index)

                        if parameter.tag == 'outputfile':
                            setValue(Parameters,'outputfile',parameter,index)

                        if parameter.tag == 'frequency':
                            setValue(Parameters,'frequency',parameter,index)

                if param.tag == 'area':
                    for area in list(param):
                        if area.tag == 'length':
                            setValue(Area,'length',area,index)

                        if area.tag == 'height':
                            setValue(Area,'height',area,index)

                        if area.tag == 'nodex':
                            setValue(Area,'nodex',area,index)

                        if area.tag == 'nodey':
                            setValue(Area,'nodey',area,index)

                if param.tag == 'preprocess':
                    for preprocess in list(param):
                        if preprocess.tag == 'compilationtype':
                            setValue(Preprocess,'compilationtype',preprocess,index)

                        if preprocess.tag == 'sourcepath':
                            setValue(Preprocess,'sourcepath',preprocess,index)

                if param.tag == 'postprocess':
                    for postprocess in list(param):
                        if postprocess.tag == 'outputtype':
                            setValue(Postprocess,'outputtype',postprocess,index)


        schema.descriptions=Description
        schema.calculations=Calculation
        schema.parameters=Parameters
        schema.area=Area

        print 'task manager starting'
        taskManager = TaskManager.TaskManager(schema)
        taskList=taskManager.start()

        for task in taskList:
            response="task "+str(task.getUid())+" acepted!"
            self.request.send(response)

        self.request.close()


    def finish(self):
        self.logger.debug('finish')
        return SocketServer.BaseRequestHandler.finish(self)


class TaskServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = 1

    def  __init__(self, server_address, handler_class):
        self.logger = logging.getLogger('TaskServer')
        self.logger.debug('__init__')
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        SocketServer.TCPServer.server_activate(self)
        return

    #def serve_forever(self):
    #    self.logger.debug('waiting for request')
    #    self.logger.info('Handling requests, press <Ctrl-C> to quit')
    #    while True:
    #        self.handle_request()
    #        return

    def handle_request(self):
        self.logger.debug('handle_request')
        return SocketServer.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.verify_request(self, request, client_address)

    #def process_request(self, request, client_address):
    #    self.logger.debug('process_request(%s, %s)', request, client_address)
    #    return SocketServer.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        self.logger.debug('server_close')
        return SocketServer.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return SocketServer.TCPServer.close_request(self, request_address)

def main():
    HOST='localhost'
    PORT=9998
    server = TaskServer((HOST,PORT),TaskRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.daemon = True
    server_thread.start()


if __name__ == "__main__":
    main()
