from http.server import BaseHTTPRequestHandler

class HandleRestRequest(BaseHTTPRequestHandler):
    def __sendResponse(s, code, message=None):
        s.send_response(code, message)
        s.send_header('Content-Type', 'application/json')
        s.end_headers()

    def __doPOSTWork(s):
        length = int(s.headers["Content-Length"])
        ctype = s.headers["Content-Type"]

        try:
            if(ctype != "application/json"):
                raise

            jsonText = str(s.rfile.read(length), 'utf-8')
            if(False is s.postProcess(jsonText, s.processArg)):
                raise

            s.__sendResponse(200)
        except:
            s.__sendResponse(405)

    def __init__(s, function, argument, * args):
        s.postProcess = function
        s.processArg = argument
        BaseHTTPRequestHandler.__init__(s, *args)
        
    def do_HEAD(s):
        s.__sendResponse(200)

    def do_POST(s):
        """Receive a POST request."""
        s.__doPOSTWork()