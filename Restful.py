import http.server
import cgi


class HandlePost(http.server.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()


    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.send_response(404, "blablabla")

    def do_POST(s):
        length=int(s.headers["Content-Length"])
        ctype=s.headers["Content-Type"]

        if(ctype != "application/json"):
            return

         
        postvars = cgi.parse_qsl(s.rfile.read(length), keep_blank_values=1)
        print(postvars)
   

#        ctype, pdict = cgi.parse_header(s.headers.getall('content-type'))
#        if ctype == 'application/json':
#            length = int(self.headers.getheader('content-length'))
#            data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
#            recordID = self.path.split('/')[-1]
#            LocalData.records[recordID] = data
#            print ("record %s is added successfully" % recordID)
#        else:
#            data = {}
#            self.send_response(200)
#            self.end_headers()
   

def start_server(port=8000, bind="", cgi=True):
    if True == cgi:
        http.server.test(HandlerClass=http.server.CGIHTTPRequestHandler, port=port, bind=bind)
    else:
        http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler, port=port, bind=bind)


def start_server2(server_class=http.server.HTTPServer, handler_class=HandlePost):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class )
    httpd.serve_forever()
    


start_server2()
    


