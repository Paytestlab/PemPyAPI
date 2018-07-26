#!/usr/bin/python3

from http.server import HTTPServer
from Rest.RestHandler import HandleRestRequest
from socketserver import ThreadingMixIn
import threading

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True;
 
    def shutdown(self):
        self.socket.close();
        HTTPServer.shutdown(self);

class RESTfulThreadedServer():
    allow_reuse_address = True;

    def __init__(s, functionPost, functionGet, argument, port=8000):
        def handler(*args):
            HandleRestRequest(functionPost, functionGet, argument, *args);
        server_address = ('', port);
        s.server =  ThreadedHTTPServer(server_address, handler);
        s.port = port;

    def start(s):
        s.server_thread = threading.Thread(target=s.server.serve_forever);
        s.server_thread.daemon = True;
        s.server_thread.start();
        
        print("Listening at port " + str(s.port));

    def waitForThread(s):
        s.server_thread.join();

    def shutdown(self):
        self.socket.close();
        HTTPServer.shutdown(self);
