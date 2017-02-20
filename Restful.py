import http.server
import json
from PinRobot import PinRobot

class HandleRestRequest(http.server.BaseHTTPRequestHandler):

    def __init__(self, robot, * args):
        self.Robot = robot
        self.Robot.SendCommand("Home")
        http.server.BaseHTTPRequestHandler.__init__(self, *args)

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()


    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.send_response(501, "Not implemented")

    def do_POST(s):
        """Receive a POST request."""
        length=int(s.headers["Content-Length"])
        ctype=s.headers["Content-Type"]

        if(ctype != "application/json"):
            return

        field_data = s.rfile.read(length)
        a = str(field_data, 'utf-8')
        
        j = json.loads(a)
        try:
            if(s.Robot.SendCommand(j["command"]) is True):
                s.send_response(200)
                s.send_header("Content-type", "application/json")
                s.end_headers()
            else:
                s.send_response(405)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        except:
            s.send_response(405)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        
        #s.send_response(0, j["command"])


class RESTfulServer:
    def __init__(self, robot, port=8000):
        def handler(*args):
            HandleRestRequest(robot, *args)

        
        server_address = ('', port)
        httpd = http.server.HTTPServer(server_address, handler)
        httpd.serve_forever()
        
    


    


