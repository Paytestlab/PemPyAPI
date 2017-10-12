from http.server import HTTPServer
from RestHandler import HandleRestRequest

class RESTfulServer:
    def __init__(s, function, argument, port=8000):
        def handler(*args):
            HandleRestRequest(function, argument, *args)

        server_address = ('', port)
        httpd = HTTPServer(server_address, handler)
        print("Listening at port " + str(port))
        httpd.serve_forever()
        
    


    


