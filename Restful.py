import http.server
import json
from PinRobot import PinRobot

class HandleRestRequest(http.server.BaseHTTPRequestHandler):
    Robot = None
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()


    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header(
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
        
        Robot.SendCommand(j["command"])  
        s.send_response(0, j["command"])
        s.send_header("Content-type", "application/text")
        s.end_headers()

class RESTfulServer:
    def __init__(self):
        return

    def start_server2(self, robot_class=PinRobot, server_class=http.server.HTTPServer, handler_class=HandleRestRequest,):
        server_address = ('', 8000)
        handler_class.Robot = robot_class
        httpd = server_class(server_address, handler_class )
        httpd.serve_forever()
    


    


