import http.server
import json
from PinRobot import PinRobot

class HandleRestRequest(http.server.BaseHTTPRequestHandler):

    def sendResponse(s, code, message=None):
            s.send_response(code, message)
            s.send_header('Content-Type', 'application/json')
            s.end_headers()

    def doPOST(s):
        length = int(s.headers["Content-Length"])
        ctype = s.headers["Content-Type"]

        try:
            if(ctype != "application/json"):
                raise

            j = json.loads(str(s.rfile.read(length), 'utf-8'))
            for command in j["commands"]:
                if(True is s.Robot.SendCommand(command)):
                    print("execution of " + command + " was succesful")
                else:
                    raise     

            sendResponse(200)
        except:
            sendResponse(405)


    def __init__(s, robot, * args):
        s.Robot = robot
        http.server.BaseHTTPRequestHandler.__init__(s, *args)
        
    def do_HEAD(s):
        sendResponse(200)


    def do_GET(s):
        """Respond to a GET request."""
        sendResponse(501, "Not implemented")

    def do_POST(s):
        """Receive a POST request."""
        doPost()

class RESTfulServer:
    def __init__(s, robot, port=8000):
        def handler(*args):
            HandleRestRequest(robot, *args)

        
        server_address = ('', port)
        httpd = http.server.HTTPServer(server_address, handler)
        print("Listening at port " + str(port))
        httpd.serve_forever()
        
    


    


