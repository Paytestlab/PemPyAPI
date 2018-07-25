#!/usr/bin/python3

from http.server import HTTPServer
from RestHandler import HandleRestRequest

class RESTfulServer:
    def __init__(s, functionPost, functionGet, argument, port=8000):
        def handler(*args):
            HandleRestRequest(functionPost, functionGet, argument, *args)

        server_address = ('', port)
        httpd = HTTPServer(server_address, handler)
        print("Listening at port " + str(port))
        httpd.serve_forever()
        
    


    


