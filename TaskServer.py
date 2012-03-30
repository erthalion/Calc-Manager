#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
import threading
import logging

class TaskRequestHandler( SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        print data
        data = data.replace('\n','')
        if data == 'shutdown':
            print 'server shutdown!'
            response = 'server shutdown!'
            self.request.sendall(response)
            self.server.shutdown()

        if data == 'load':
            while 1:
                print 'load'

        if data == 'echo':
            response = 'echo'
            self.request.sendall(response)


class TaskServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = 1


def main():
    HOST='localhost'
    PORT=9997
    server = TaskServer((HOST,PORT),TaskRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.daemon = True
    server_thread.start()
    logging.debug("server started!")


if __name__ == "__main__":
    main()
